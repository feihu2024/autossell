import requests
import logging
from dao.d_video_config import get_config_value
from service.video_parser import parse, ParseError, NetworkError

logger = logging.getLogger(__name__)

ALAPI_VIDEO_URL = "https://v3.alapi.cn/api/video/url"
ZHUCEKA_API = "https://api.zhuceka.cn/home/api"


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


# ============================================================
#  第一层：zhuceka API（大圣）
# ============================================================

def _parse_via_alapi(url: str) -> dict:
    token = get_config_value("video_parse", "token")
    if not token:
        logger.warning("ALAPI token 未配置，跳过第一层")
        return {"code": -1, "msg": "token 未配置"}

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
    logger.info("ALAPI 解析成功: %s", data.get('title', '') if isinstance(data, dict) else '')
    return result


# ============================================================
#  第二层：ALAPI
# ============================================================

def _parse_via_zhuceka(url: str) -> dict:
    dsuid = get_config_value("video_parse", "dsuid")
    dskey = get_config_value("video_parse", "dskey")
    if not dsuid or not dskey:
        logger.warning("zhuceka dsuid/dskey 未配置，跳过第二层")
        return {"code": -1, "msg": "zhuceka 配置未设置"}

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

    logger.info("zhuceka 解析成功: %s", data.get('title', ''))
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
    logger.info("video_parser 直抓成功: %s", data.get('title', ''))
    return True, data


# ============================================================
#  统一入口：四层递进
# ============================================================

def parse_video_url(url: str) -> dict:
    """
    视频链接解析入口（四层递进）：
    1. zhuceka API（大圣）
    2. ALAPI
    3. 自有逻辑（video_parser 直抓）
    4. 友好提示：提取异常请联系客服

    只返回原始公网 URL，不涉及 CDN/七牛/Redis 任何缓存逻辑。
    下载走独立接口 /web/video/download。
    """
    if not url:
        return {"code": -1, "msg": "视频链接不能为空"}

    url_stripped = url.strip()

    # 第一层：zhuceka（大圣）
    result = _parse_via_zhuceka(url_stripped)
    if result.get("code") == 200:
        return result
    logger.warning("第一层 zhuceka 失败，尝试第二层 ALAPI: %s", result.get("msg"))

    # 第二层：ALAPI
    result = _parse_via_alapi(url_stripped)
    if result.get("code") == 200:
        return result
    logger.warning("第二层 ALAPI 失败，尝试第三层自有逻辑: %s", result.get("msg"))

    # 第三层：自有逻辑（video_parser 直抓）
    ok, data = _try_direct_parse(url_stripped)
    if ok:
        return {"code": 200, "data": data}

    # 第四层：友好提示
    return {"code": -1, "msg": "提取异常请联系客服"}
