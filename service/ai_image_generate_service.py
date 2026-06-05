import requests
import logging
import json
import uuid
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from qiniu import Auth, BucketManager
from config import QINIU
from dao.d_video_config import get_config_value
from dao.d_ai_image_task import (
    create_image_task,
    get_pending_tasks_by_userid,
    update_task_qiniu_url,
    get_all_tasks_by_userid,
    delete_expired_tasks,
)

logger = logging.getLogger(__name__)

# ALAPI 图片生成异步接口地址
ALAPI_IMAGE_GEN_URL = "https://v3.alapi.cn/api/ai/images/generations_sync"
# ALAPI 图片生成任务查询接口地址
ALAPI_IMAGE_TASK_URL = "https://v3.alapi.cn/api/ai/images/generations/task"

# 七牛云对外访问域名（与视频解析保持一致）
QINIU_BASE_URL = 'https://mlcfjihuaqn.yxiaozhu.com'


def _fetch_image_to_qiniu(image_url: str) -> str:
    """
    通过七牛 fetch 接口抓取远程图片并存储到七牛云，返回签名访问链接
    参照视频解析 service 的实现方式

    :param image_url: 远程图片链接
    :return: 七牛签名访问链接，失败返回空字符串
    """
    if not image_url:
        return ""

    if not QINIU_BASE_URL:
        logger.error("七牛云域名未配置")
        return ""

    # 提取文件扩展名，默认 .png
    try:
        suffix = Path(image_url.split('?')[0]).suffix
    except Exception:
        suffix = ""
    if not suffix:
        suffix = ".png"

    key = f"ai_image/{uuid.uuid4()}{suffix}"

    try:
        qiniu_auth = Auth(QINIU.accessKey, QINIU.secretKey)
        bucket = BucketManager(qiniu_auth)
        ret, info = bucket.fetch(image_url, QINIU.bucketName, key)
        if info.status_code == 200 and ret is not None:
            qiniu_key = ret.get("key", key)
            raw_url = f"{QINIU_BASE_URL}/{qiniu_key}"
            # 生成私有空间签名链接（公开空间同样兼容），有效期 72 小时
            signed_url = qiniu_auth.private_download_url(raw_url, expires=259200)
            return signed_url
        else:
            logger.warning(f"七牛 fetch 图片失败 {image_url}: status={info.status_code}")
            return ""
    except Exception as e:
        logger.error(f"七牛上传图片异常 {image_url}: {e}")
        return ""


def _fetch_all_images_to_qiniu(images: list) -> str:
    """
    将 ALAPI 返回的多张图片 URL 全部抓取到七牛云，返回 JSON 数组字符串

    :param images: ALAPI 返回的图片列表 [{"url": "..."}, {"url": "..."}, ...]
    :return: JSON 数组字符串，如 '["七牛链接1", "七牛链接2"]'；无图时返回空 JSON 数组 '[]'
    """
    qiniu_urls = []
    for img in images:
        if isinstance(img, dict) and img.get("url"):
            qiniu_url = _fetch_image_to_qiniu(img["url"])
            if qiniu_url:
                qiniu_urls.append(qiniu_url)
            else:
                # 七牛抓取失败时使用原始链接
                qiniu_urls.append(img["url"])
    return json.dumps(qiniu_urls, ensure_ascii=False)


def generate_image(
    prompt: str,
    userid: str,
    size: str = "",
    resolution: str = "1k",
    image_urls: str = "",
) -> dict:
    """
    调用 ALAPI 异步接口生成 AI 图片，存储 task_id 和 userid 到数据库
    token、model、n 从数据库 video_config 表读取

    :param prompt: 图片生成提示词，用户端传入
    :param userid: 前端用户ID
    :param size: 图片尺寸，用户端选择（为空时使用模型默认）
    :param resolution: 图片分辨率，用户端选择，默认 "1k"
    :param image_urls: 参考图片地址（可选，可空置）
    :return: {"code": 200, "task_id": "xxx"} 或错误信息
    """
    # 从数据库读取管理端配置
    token = get_config_value("ai_image", "token")
    if not token:
        return {"code": -1, "msg": "token 未配置，请联系管理员"}

    model = get_config_value("ai_image", "model") or "gpt-image-2"
    n = get_config_value("ai_image", "n") or "1"

    if not prompt:
        return {"code": -1, "msg": "提示词(prompt)不能为空"}
    if not userid:
        return {"code": -1, "msg": "userid 不能为空"}

    payload = {
        "token": token,
        "model": model,
        "prompt": prompt,
        "n": n,
        "size": size,
        "image_urls": image_urls,
        "resolution": resolution,
    }

    # 过滤空字符串参数（可选字段空置时不传），保留数字类型
    payload = {k: v for k, v in payload.items() if v is not None and v != ""}

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(ALAPI_IMAGE_GEN_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()

        if result.get("code") == 200 and result.get("data", {}).get("task_id"):
            task_id = result["data"]["task_id"]
            logger.info(f"图片生成任务创建成功: prompt={prompt[:50]}..., task_id={task_id}, userid={userid}")
            # 存储到数据库，qiniu_url 默认 '生成中'
            # 根据是否携带 image_urls 判断类型: 有图片→图生图(wst)，无图片→文生图(tst)
            task_type = 'wst' if image_urls else 'tst'
            create_image_task(userid=userid, task_id=task_id, task_type=task_type)
            return {"code": 200, "task_id": task_id}
        else:
            logger.warning(f"图片生成任务创建失败: {result.get('msg', '未知错误')}")
            return result  # 透传 ALAPI 的错误信息

    except requests.exceptions.Timeout:
        logger.error(f"图片生成请求超时: prompt={prompt[:50]}...")
        return {"code": -1, "msg": "请求超时，请稍后重试"}
    except requests.exceptions.RequestException as e:
        logger.error(f"图片生成请求异常: {e}")
        return {"code": -1, "msg": f"请求失败: {str(e)}"}
    except Exception as e:
        logger.error(f"图片生成未知异常: {e}")
        return {"code": -1, "msg": f"系统异常: {str(e)}"}


def _background_fetch_and_update(task_id: str, images: list):
    """
    后台线程函数：将图片逐张抓取到七牛云，完成后更新数据库 qiniu_url
    失败时将状态更新为 '生成失败'
    """
    try:
        qiniu_urls_json = _fetch_all_images_to_qiniu(images)
        update_task_qiniu_url(task_id, qiniu_urls_json)
        logger.info(f"后台线程七牛抓取完成: task_id={task_id}, 图片数={len(images)}")
    except Exception as e:
        logger.error(f"后台线程七牛抓取异常: task_id={task_id}, err={e}")
        update_task_qiniu_url(task_id, "生成失败")


def query_user_image_tasks(userid: str) -> dict:
    """
    查询某用户的所有图片生成任务结果
    流程：
      1. 查询数据库中该用户 qiniu_url='生成中' 的记录
      2. 逐个调用 ALAPI 查询接口：
         - 若已完成且有图片 → 先将 qiniu_url 改为 '渲染中'，再启动后台线程执行七牛 fetch
         - 若 ALAPI 返回错误 → 将 qiniu_url 改为 '生成失败'
      3. 立即查询该用户所有任务并返回（不等后台线程）
    """
    if not userid:
        return {"code": -1, "msg": "userid 不能为空"}

    token = get_config_value("ai_image", "token")
    if not token:
        return {"code": -1, "msg": "token 未配置，请联系管理员"}

    # 1. 查询待处理的任务（qiniu_url='生成中'）
    pending_tasks = get_pending_tasks_by_userid(userid)
    logger.info(f"查询用户图片任务: userid={userid}, 待处理任务数={len(pending_tasks)}")

    # 2. 逐个调用 ALAPI 查询接口
    for task in pending_tasks:
        task_id = task["task_id"]
        payload = {
            "token": token,
            "task_id": task_id,
        }
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(ALAPI_IMAGE_TASK_URL, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 200:
                data = result.get("data", {})
                status = data.get("status", "")
                images = data.get("result", {}).get("images", [])
                if status == "completed" and images and isinstance(images, list) and len(images) > 0:
                    # ALAPI 已出图，先将状态改为 '渲染中'，再后台线程抓取到七牛
                    update_task_qiniu_url(task_id, "渲染中")
                    t = threading.Thread(
                        target=_background_fetch_and_update,
                        args=(task_id, images),
                        daemon=True,
                    )
                    t.start()
                    logger.info(f"任务已完成，启动后台七牛抓取: task_id={task_id}, 图片数={len(images)}")
                elif status == "failed":
                    # ALAPI 任务失败
                    update_task_qiniu_url(task_id, "生成失败")
                    logger.warning(f"ALAPI 任务失败: task_id={task_id}")
                else:
                    # 任务还在处理中（processing），保持 qiniu_url='生成中'
                    logger.info(f"任务处理中: task_id={task_id}, status={status}")
            else:
                # ALAPI 查询接口返回错误码，标记失败
                update_task_qiniu_url(task_id, "生成失败")
                logger.warning(f"查询任务失败: task_id={task_id}, msg={result.get('msg', '')}")
        except requests.exceptions.Timeout:
            logger.warning(f"查询任务超时: task_id={task_id}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"查询任务请求异常: task_id={task_id}, err={e}")
        except Exception as e:
            logger.warning(f"查询任务未知异常: task_id={task_id}, err={e}")

    # 3. 查询该用户所有任务的 qiniu_url 并立即返回
    all_tasks = get_all_tasks_by_userid(userid)
    return {"code": 200, "data": all_tasks}


# 数据库记录保留时长（秒），48 小时
RECORD_EXPIRE_SECONDS = 48 * 3600
# 每天凌晨3点执行清理
CLEANUP_HOUR = 3


def _cleanup_expired_records():
    """
    后台定时循环：每天凌晨3点扫描并删除超期的数据库记录
    """
    while True:
        now = datetime.now()
        target = now.replace(hour=CLEANUP_HOUR, minute=0, second=0, microsecond=0)
        if now >= target:
            target += timedelta(days=1)
        wait_seconds = (target - now).total_seconds()
        time.sleep(wait_seconds)
        try:
            deleted_count = delete_expired_tasks(RECORD_EXPIRE_SECONDS)
            if deleted_count > 0:
                logger.info(f"定时清理: 删除了 {deleted_count} 条过期记录")
            else:
                logger.info("定时清理: 无过期记录")
        except Exception as e:
            logger.error(f"定时清理异常: {e}")


def start_cleanup_daemon():
    """
    启动后台定时清理线程（daemon），在 FastAPI 启动时调用一次即可
    """
    t = threading.Thread(target=_cleanup_expired_records, daemon=True)
    t.start()
    logger.info("数据库过期记录定时清理线程已启动")
