import requests
import logging
from dao.d_video_config import get_config_value

logger = logging.getLogger(__name__)

# ALAPI 图片生成接口地址
ALAPI_IMAGE_GEN_URL = "https://v3.alapi.cn/api/ai/images/generations_sync"
# ALAPI 图片生成任务查询接口地址
ALAPI_IMAGE_TASK_URL = "https://v3.alapi.cn/api/ai/images/generations/task"


def generate_image(
    prompt: str,
    size: str = "",
    resolution: str = "1k",
    image_urls: str = "",
) -> dict:
    """
    通过 ALAPI 调用 AI 图片生成接口
    token、model、n 从数据库 video_config 表读取

    :param prompt: 图片生成提示词，用户端传入
    :param size: 图片尺寸，用户端选择（为空时使用模型默认）
    :param resolution: 图片分辨率，用户端选择，默认 "1k"
    :param image_urls: 参考图片地址（可选，可空置）
    :return: ALAPI 原始返回结果（透传给前端）
    """
    # 从数据库读取管理端配置
    token = get_config_value("ai_image", "token")
    if not token:
        return {"code": -1, "msg": "token 未配置，请联系管理员"}

    model = get_config_value("ai_image", "model") or "gpt-image-2"
    n_str = get_config_value("ai_image", "n") or "1"
    try:
        n = int(n_str)
    except (ValueError, TypeError):
        n = 1

    if not prompt:
        return {"code": -1, "msg": "提示词(prompt)不能为空"}

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

        if result.get("code") == 200:
            logger.info(f"图片生成成功: prompt={prompt[:50]}...")
            return result
        else:
            logger.warning(f"图片生成失败: {result.get('msg', '未知错误')}")
            return result  # 透传 ALAPI 的错误信息

    except requests.exceptions.Timeout:
        logger.error(f"图片生成超时: prompt={prompt[:50]}...")
        return {"code": -1, "msg": "请求超时，请稍后重试"}
    except requests.exceptions.RequestException as e:
        logger.error(f"图片生成请求异常: {e}")
        return {"code": -1, "msg": f"请求失败: {str(e)}"}
    except Exception as e:
        logger.error(f"图片生成未知异常: {e}")
        return {"code": -1, "msg": f"系统异常: {str(e)}"}


def query_image_task(task_id: str) -> dict:
    """
    查询文生图异步任务结果
    token 从数据库 video_config 表读取

    :param task_id: 文生图任务ID，前端传入
    :return: ALAPI 原始返回结果（透传给前端）
    """
    token = get_config_value("ai_image", "token")
    if not token:
        return {"code": -1, "msg": "token 未配置，请联系管理员"}

    if not task_id:
        return {"code": -1, "msg": "task_id 不能为空"}

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
            logger.info(f"查询图片任务成功: task_id={task_id}")
        else:
            logger.warning(f"查询图片任务失败: {result.get('msg', '未知错误')}")
        return result  # 透传 ALAPI 返回结果

    except requests.exceptions.Timeout:
        logger.error(f"查询图片任务超时: task_id={task_id}")
        return {"code": -1, "msg": "请求超时，请稍后重试"}
    except requests.exceptions.RequestException as e:
        logger.error(f"查询图片任务请求异常: {e}")
        return {"code": -1, "msg": f"请求失败: {str(e)}"}
    except Exception as e:
        logger.error(f"查询图片任务未知异常: {e}")
        return {"code": -1, "msg": f"系统异常: {str(e)}"}
