import hashlib
import hmac
import base64
import time
import zlib
import logging
import requests
from config import SECRET
from dao.d_video_config import get_config_value
from service.video_parser import parse, ParseError, NetworkError

logger = logging.getLogger(__name__)

ALAPI_VIDEO_URL = "https://v3.alapi.cn/api/video/url"
ZHUCEKA_API = "https://api.zhuceka.cn/home/api"
CDN_DOWNLOAD_BASE = 'https://vipvideo.yxiaozhu.com/web/video/download'

# ============================================================
#  自包含 Token：raw_url + 过期时间 + HMAC 签名 → base64
#  零存储，无状态，多 Worker / 高并发均无影响
# ============================================================
_TOKEN_TTL = 3600
_TOKEN_SECRET = SECRET.SECRET_KEY.encode()


_SEP = "\x00"  # 字段分隔符，URL 中不可能出现，确保 split 安全


def _encode_token(raw_url: str) -> str:
    """将 raw_url 编码为带签名和过期时间的 token（zlib 压缩 URL 以缩短 token）"""
    expire = str(int(time.time()) + _TOKEN_TTL)
    compressed = base64.urlsafe_b64encode(zlib.compress(raw_url.encode())).rstrip(b"=").decode()
    payload = f"{expire}{_SEP}{compressed}"
    sig = hmac.new(_TOKEN_SECRET, payload.encode(), hashlib.sha256).hexdigest()[:16]
    data = f"{expire}{_SEP}{compressed}{_SEP}{sig}"
    token = base64.urlsafe_b64encode(data.encode()).rstrip(b"=").decode()
    return token


def _decode_token(token: str) -> str:
    """解码 token → raw_url，过期或伪造返回 None"""
    try:
        padding = 4 - len(token) % 4
        if padding != 4:
            token += "=" * padding
        decoded = base64.urlsafe_b64decode(token.encode()).decode()
        expire_str, compressed, sig = decoded.split(_SEP, 2)
        if int(expire_str) < time.time():
            return None
        expected = hmac.new(
            _TOKEN_SECRET,
            f"{expire_str}{_SEP}{compressed}".encode(),
            hashlib.sha256,
        ).hexdigest()[:16]
        if not hmac.compare_digest(sig, expected):
            return None
        c_bytes = compressed.encode()
        c_padding = 4 - len(c_bytes) % 4
        if c_padding != 4:
            c_bytes += b"=" * c_padding
        raw_url = zlib.decompress(base64.urlsafe_b64decode(c_bytes)).decode()
        return raw_url
    except Exception:
        return None


def _gen_download_url(raw_url: str) -> str:
    """生成 CDN 下载链接，token 自包含 raw_url（无需存储）"""
    if not raw_url:
        return ""
    token = _encode_token(raw_url)
    return f"{CDN_DOWNLOAD_BASE}/{token}"


def _add_download_urls_to_data(data: dict) -> None:
    """为 data 中所有媒体资源（视频/封面/图片组/livephoto）生成 CDN 下载链接"""
    if not isinstance(data, dict):
        return

    # 视频
    video_url = data.get("video_url", "")
    if video_url:
        data["download_url"] = _gen_download_url(video_url)

    # 封面（兼容 cover_url / cover）
    cover_url = data.get("cover_url", "") or data.get("cover", "")
    if cover_url:
        data["cover_download_url"] = _gen_download_url(cover_url)

    # 图片组（兼容 pics / images）
    pics = data.get("pics") or data.get("images")
    if isinstance(pics, list):
        data["pics_download"] = [_gen_download_url(p) for p in pics if p]

    # livephoto
    livephotos = data.get("livephoto") or data.get("live_photo")
    if isinstance(livephotos, list):
        lp_download = []
        for item in livephotos:
            if isinstance(item, dict):
                lp_download.append({
                    "cover": _gen_download_url(item.get("cover", "")),
                    "video": _gen_download_url(item.get("video", "")),
                })
            elif isinstance(item, str):
                lp_download.append({
                    "cover": "",
                    "video": _gen_download_url(item),
                })
        data["livephoto_download"] = lp_download


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
#  第一层：ALAPI
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
    _add_download_urls_to_data(data)

    logger.info("ALAPI 解析成功: %s", data.get('title', '') if isinstance(data, dict) else '')
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

    _add_download_urls_to_data(data)

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
    _add_download_urls_to_data(data)

    logger.info("video_parser 直抓成功: %s", data.get('title', ''))
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
