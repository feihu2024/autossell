import requests
import logging
import uuid
from pathlib import Path
from qiniu import Auth, BucketManager
from config import QINIU

logger = logging.getLogger(__name__)

# ALAPI 视频解析接口地址
ALAPI_VIDEO_URL = "https://v3.alapi.cn/api/video/url"

# 七牛云对外访问域名（硬编码）
QINIU_BASE_URL = 'https://mlcfjihuaqn.yxiaozhu.com'


def _fetch_to_qiniu(resource_url: str, prefix: str = "video") -> str:
    """
    通过七牛 fetch 接口抓取远程资源并存储到七牛云

    :param resource_url: 远程资源链接
    :param prefix: 存储路径前缀（video / cover / pics / livephoto）
    :return: 七牛公开访问链接，失败返回空字符串
    """
    if not resource_url:
        return ""

    if not QINIU_BASE_URL:
        logger.error("七牛云域名未配置")
        return ""

    # 提取文件扩展名
    try:
        suffix = Path(resource_url.split('?')[0]).suffix
    except Exception:
        suffix = ""
    if not suffix:
        # 根据资源类型指定默认后缀：视频类 → .mp4，图片类 → .jpg
        _is_video = prefix in ("video", "livephoto") or "video" in prefix
        suffix = ".mp4" if _is_video else ".jpg"

    key = f"{prefix}/{uuid.uuid4()}{suffix}"

    try:
        qiniu_auth = Auth(QINIU.accessKey, QINIU.secretKey)
        bucket = BucketManager(qiniu_auth)
        ret, info = bucket.fetch(resource_url, QINIU.bucketName, key)
        if info.status_code == 200 and ret is not None:
            qiniu_key = ret.get("key", key)
            raw_url = f"{QINIU_BASE_URL}/{qiniu_key}"
            # 生成私有空间签名链接（公开空间同样兼容），有效期 24 小时
            signed_url = qiniu_auth.private_download_url(raw_url, expires=86400)
            return signed_url
        else:
            logger.warning(f"七牛 fetch 失败 {resource_url}: status={info.status_code}")
            return ""
    except Exception as e:
        logger.error(f"七牛上传异常 {resource_url}: {e}")
        return ""


def _upload_resources(data: dict) -> None:
    """
    将 ALAPI 返回数据中的视频、封面、图集、动态图转存到七牛云，原地替换链接

    :param data: ALAPI 返回的 data 字段（会被原地修改）
    """
    # 视频链接
    video_url = data.get("video_url")
    if video_url:
        qiniu_url = _fetch_to_qiniu(video_url, "video")
        if qiniu_url:
            data["video_url"] = qiniu_url

    # 封面图片
    cover_url = data.get("cover_url")
    if cover_url:
        qiniu_url = _fetch_to_qiniu(cover_url, "cover")
        if qiniu_url:
            data["cover_url"] = qiniu_url

    # 图集列表
    pics = data.get("pics")
    if isinstance(pics, list):
        for i, pic_url in enumerate(pics):
            if pic_url:
                qiniu_url = _fetch_to_qiniu(pic_url, "pics")
                if qiniu_url:
                    pics[i] = qiniu_url

    # 动态图 livephoto
    livephotos = data.get("livephoto")
    if isinstance(livephotos, list):
        for item in livephotos:
            if isinstance(item, dict):
                lp_cover = item.get("cover")
                if lp_cover:
                    qiniu_url = _fetch_to_qiniu(lp_cover, "livephoto_cover")
                    if qiniu_url:
                        item["cover"] = qiniu_url
                lp_video = item.get("video")
                if lp_video:
                    qiniu_url = _fetch_to_qiniu(lp_video, "livephoto_video")
                    if qiniu_url:
                        item["video"] = qiniu_url


def parse_video_url(token: str, url: str) -> dict:
    """
    通过 ALAPI 解析视频链接，提取视频/封面/图集并转存至七牛云

    :param token: ALAPI 接口令牌，由管理端配置传入
    :param url: 用户输入的视频链接（支持抖音、快手、小红书、B站等平台）
    :return: 解析结果字典，video_url / cover_url / pics / livephoto 已替换为七牛云链接
    """
    if not token:
        return {"code": -1, "msg": "token 不能为空，请联系管理员配置"}

    if not url:
        return {"code": -1, "msg": "视频链接不能为空"}

    # 校验七牛配置
    if not all([QINIU.accessKey, QINIU.secretKey, QINIU.bucketName, QINIU_BASE_URL]):
        return {"code": -1, "msg": "七牛云配置不完整，请联系管理员"}

    payload = {
        "token": token,
        "url": url.strip()
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(ALAPI_VIDEO_URL, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.Timeout:
        logger.error(f"视频解析超时: {url}")
        return {"code": -1, "msg": "解析超时，请稍后重试"}
    except requests.exceptions.RequestException as e:
        logger.error(f"视频解析请求异常: {e}")
        return {"code": -1, "msg": f"请求失败: {str(e)}"}
    except Exception as e:
        logger.error(f"视频解析未知异常: {e}")
        return {"code": -1, "msg": f"系统异常: {str(e)}"}

    if result.get("code") != 200:
        logger.warning(f"视频解析失败: {result.get('msg', '未知错误')}")
        return {"code": -1, "msg": result.get("msg", "解析失败，请检查链接是否正确")}

    # 提取资源并转存到七牛云
    data = result.get("data", {})
    if data:
        _upload_resources(data)

    logger.info(f"视频解析并转存成功: {data.get('title', '')}")
    return result
