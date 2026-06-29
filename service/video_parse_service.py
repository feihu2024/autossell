import requests
import logging
import uuid
from pathlib import Path
from qiniu import Auth, BucketManager
from config import VIDEOQINIU
from dao.d_video_config import get_config_value
from service.video_parser import parse, ParseError, NetworkError

logger = logging.getLogger(__name__)

ALAPI_VIDEO_URL = "https://v3.alapi.cn/api/video/url"
ZHUCEKA_API = "https://api.zhuceka.cn/home/api"
QINIU_BASE_URL = 'https://vipvideo.yxiaozhu.com'


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
        qiniu_auth = Auth(VIDEOQINIU.accessKey, VIDEOQINIU.secretKey)
        bucket = BucketManager(qiniu_auth)
        ret, info = bucket.fetch(resource_url, VIDEOQINIU.bucketName, key)
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


def _check_qiniu_config() -> bool:
    if not all([VIDEOQINIU.accessKey, VIDEOQINIU.secretKey, VIDEOQINIU.bucketName, QINIU_BASE_URL]):
        return False
    return True


# ============================================================
#  第一层：ALAPI
# ============================================================

def _parse_via_alapi(url: str) -> dict:
    token = get_config_value("video_parse", "token")
    if not token:
        logger.warning("ALAPI token 未配置，跳过第一层")
        return {"code": -1, "msg": "token 未配置"}

    if not _check_qiniu_config():
        logger.warning("七牛云配置不完整，跳过第一层")
        return {"code": -1, "msg": "七牛云配置不完整"}

    payload = {"token": token, "url": url}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(ALAPI_VIDEO_URL, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.Timeout:
        logger.error("ALAPI 解析超时: %s", url)
        return {"code": -1, "msg": "解析超时"}
    except requests.exceptions.RequestException as e:
        logger.error("ALAPI 请求异常: %s", e)
        return {"code": -1, "msg": f"请求失败: {e}"}
    except Exception as e:
        logger.error("ALAPI 未知异常: %s", e)
        return {"code": -1, "msg": f"系统异常: {e}"}

    if result.get("code") != 200:
        logger.warning("ALAPI 解析失败: %s", result.get('msg', '未知错误'))
        return {"code": -1, "msg": result.get("msg", "解析失败")}

    data = result.get("data", {})
    if data:
        _upload_resources(data)

    logger.info("ALAPI 解析并转存成功: %s", data.get('title', '') if isinstance(data, dict) else '')
    return result


# ============================================================
#  第二层：zhuceka API
# ============================================================

def _parse_via_zhuceka(url: str) -> dict:
    dsuid = get_config_value("video_parse", "dsuid")
    dskey = get_config_value("video_parse", "dskey")
    if not dsuid or not dskey:
        logger.warning("zhuceka dsuid/dskey 未配置，跳过第二层")
        return {"code": -1, "msg": "zhuceka 配置未设置"}

    if not _check_qiniu_config():
        return {"code": -1, "msg": "七牛云配置不完整"}

    params = {
        "type": "dsp",
        "uid": dsuid,
        "key": dskey,
        "url": url,
    }

    try:
        response = requests.get(ZHUCEKA_API, params=params, timeout=15)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.Timeout:
        logger.error("zhuceka 解析超时: %s", url)
        return {"code": -1, "msg": "解析超时"}
    except requests.exceptions.RequestException as e:
        logger.error("zhuceka 请求异常: %s", e)
        return {"code": -1, "msg": f"请求失败: {e}"}
    except Exception as e:
        logger.error("zhuceka 未知异常: %s", e)
        return {"code": -1, "msg": f"系统异常: {e}"}

    if result.get("code") != 200:
        logger.warning("zhuceka 解析失败: %s", result.get('msg', '未知错误'))
        return {"code": -1, "msg": result.get("msg", "解析失败")}

    raw_data = result.get("data", {}) or {}

    # zhuceka images 归一化为字符串列表
    raw_images = raw_data.get("images", []) or []
    pics = []
    for img in raw_images:
        if isinstance(img, str):
            pics.append(img)
        elif isinstance(img, dict):
            u = img.get("url", "")
            if u:
                pics.append(u)

    # zhuceka live_photo 归一化为 [{"cover": "", "video": ""}] 结构
    raw_livephotos = raw_data.get("live_photo", []) or []
    livephotos = []
    for item in raw_livephotos:
        if isinstance(item, dict):
            livephotos.append({
                "cover": item.get("cover", item.get("cover_url", "")),
                "video": item.get("video", item.get("video_url", "")),
            })
        elif isinstance(item, str):
            livephotos.append({"cover": "", "video": item})

    data = {
        "video_url": raw_data.get("video", ""),
        "cover_url": raw_data.get("cover", ""),
        "title": raw_data.get("title", ""),
        "desc": "",
        "pics": pics,
        "livephoto": livephotos,
    }

    _upload_resources(data)

    logger.info("zhuceka 解析并转存成功: %s", data.get('title', ''))
    return {"code": 200, "data": data}


# ============================================================
#  第三层：自有逻辑（video_parser 直抓）
# ============================================================

def _try_direct_parse(url: str):
    try:
        info = parse(url)
    except (ParseError, NetworkError, Exception) as e:
        logger.warning("video_parser 直抓失败: %s", e)
        return False, None

    data = _parse_url_to_data(info)

    if not _check_qiniu_config():
        logger.warning("七牛云配置不完整，无法转存资源，返回原始链接")
    else:
        _upload_resources(data)

    logger.info("video_parser 直抓并转存成功: %s", data.get('title', ''))
    return True, data


# ============================================================
#  统一入口：四层递进
# ============================================================

def parse_video_url(url: str) -> dict:
    """
    视频链接解析入口（四层递进）：
    1. ALAPI
    2. zhuceka API
    3. 自有逻辑（video_parser 直抓 doubao/小云雀）
    4. 友好提示：提取异常请联系客服
    """
    if not url:
        return {"code": -1, "msg": "视频链接不能为空"}

    url_stripped = url.strip()

    # 第一层：ALAPI
    result = _parse_via_alapi(url_stripped)
    if result.get("code") == 200:
        return result
    logger.warning("第一层 ALAPI 失败，尝试第二层 zhuceka: %s", result.get("msg"))

    # 第二层：zhuceka API
    result = _parse_via_zhuceka(url_stripped)
    if result.get("code") == 200:
        return result
    logger.warning("第二层 zhuceka 失败，尝试第三层自有逻辑: %s", result.get("msg"))

    # 第三层：自有逻辑（video_parser 直抓）
    ok, data = _try_direct_parse(url_stripped)
    if ok:
        return {"code": 200, "data": data}

    # 第四层：友好提示
    return {"code": -1, "msg": "提取异常请联系客服"}
