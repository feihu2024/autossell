import requests
import logging
import uuid
from pathlib import Path
from qiniu import Auth, BucketManager
from config import QINIU
from dao.d_video_config import get_config_value
from service.video_parser import parse, ParseError, NetworkError

logger = logging.getLogger(__name__)

ALAPI_VIDEO_URL = "https://v3.alapi.cn/api/video/url"
QINIU_BASE_URL = 'https://mlcfjihuaqn.yxiaozhu.com'


def _fetch_to_qiniu(resource_url: str, prefix: str = "video") -> str:
    if not resource_url:
        return ""
    if not QINIU_BASE_URL:
        logger.error("七牛云域名未配置")
        return ""
    try:
        suffix = Path(resource_url.split('?')[0]).suffix
    except Exception:
        suffix = ""
    if not suffix:
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
            signed_url = qiniu_auth.private_download_url(raw_url, expires=259200)
            return signed_url
        else:
            logger.warning("七牛 fetch 失败 %s: status=%s", resource_url, info.status_code)
            return ""
    except Exception as e:
        logger.error("七牛上传异常 %s: %s", resource_url, e)
        return ""


def _upload_resources(data: dict) -> None:
    video_url = data.get("video_url")
    if video_url:
        qiniu_url = _fetch_to_qiniu(video_url, "video")
        if qiniu_url:
            data["video_url"] = qiniu_url

    cover_url = data.get("cover_url")
    if cover_url:
        qiniu_url = _fetch_to_qiniu(cover_url, "cover")
        if qiniu_url:
            data["cover_url"] = qiniu_url

    pics = data.get("pics")
    if isinstance(pics, list):
        for i, pic_url in enumerate(pics):
            if pic_url:
                qiniu_url = _fetch_to_qiniu(pic_url, "pics")
                if qiniu_url:
                    pics[i] = qiniu_url

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


def _parse_url_to_data(info) -> dict:
    data = {
        "video_url": "",
        "cover_url": "",
        "title": info.title or "",
        "pics": [],
        "livephoto": [],
    }
    if info.media_type == "image":
        data["pics"] = [img.url for img in info.images if img.url]
    else:
        data["video_url"] = info.url or ""
        data["cover_url"] = info.poster or ""
    return data


def _try_direct_parse(url: str):
    """
    尝试用 video_parser 直抓，成功返回 (True, data_dict)，失败返回 (False, None)
    """
    try:
        info = parse(url)
    except (ParseError, NetworkError, Exception) as e:
        logger.warning("video_parser 直抓失败（将降级到 ALAPI）: %s", e)
        return False, None

    data = _parse_url_to_data(info)

    if not all([QINIU.accessKey, QINIU.secretKey, QINIU.bucketName, QINIU_BASE_URL]):
        logger.warning("七牛云配置不完整，无法转存资源，返回原始链接")
    else:
        _upload_resources(data)

    logger.info("video_parser 直抓并转存成功: %s", data.get('title', ''))
    return True, data


def _parse_via_alapi(url: str) -> dict:
    """
    原逻辑：从数据库读 token，调用 ALAPI 解析，转存七牛
    """
    token = get_config_value("video_parse", "token")
    if not token:
        return {"code": -1, "msg": "token 未配置，请联系管理员"}

    if not all([QINIU.accessKey, QINIU.secretKey, QINIU.bucketName, QINIU_BASE_URL]):
        return {"code": -1, "msg": "七牛云配置不完整，请联系管理员"}

    payload = {"token": token, "url": url}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(ALAPI_VIDEO_URL, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.Timeout:
        logger.error("视频解析超时: %s", url)
        return {"code": -1, "msg": "解析超时，请稍后重试"}
    except requests.exceptions.RequestException as e:
        logger.error("视频解析请求异常: %s", e)
        return {"code": -1, "msg": f"请求失败: {e}"}
    except Exception as e:
        logger.error("视频解析未知异常: %s", e)
        return {"code": -1, "msg": f"系统异常: {e}"}

    if result.get("code") != 200:
        logger.warning("视频解析失败: %s", result.get('msg', '未知错误'))
        return {"code": -1, "msg": result.get("msg", "解析失败，请检查链接是否正确")}

    data = result.get("data", {})
    if data:
        _upload_resources(data)

    logger.info("ALAPI 解析并转存成功: %s", data.get('title', '') if isinstance(data, dict) else '')
    return result


def parse_video_url(url: str) -> dict:
    """
    视频链接解析入口：
    1. 先尝试 video_parser 直抓（豆包视频、小云雀视频/图片）
    2. 直抓失败 → 降级到 ALAPI
    """
    if not url:
        return {"code": -1, "msg": "视频链接不能为空"}

    url_stripped = url.strip()
    lower_url = url_stripped.lower()

    # 只有含 doubao.com 或 xiaoyunque.jianying.com 才尝试直抓
    if "doubao.com" in lower_url or "xiaoyunque.jianying.com" in lower_url:
        ok, data = _try_direct_parse(url_stripped)
        if ok:
            return {"code": 200, "data": data}

    # 降级：走 ALAPI
    return _parse_via_alapi(url_stripped)
