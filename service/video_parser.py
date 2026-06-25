"""
视频/图片无水印解析模块

支持的平台:
    - 豆包 (doubao.com)          — 视频
    - 小云雀/剪映 (xiaoyunque.jianying.com) — 视频 + 图片

核心函数:
    parse(url)            -> MediaInfo   自动识别平台/媒体类型，统一入口
    parse_doubao(url)     -> MediaInfo   仅解析豆包视频
    parse_xiaoyunque(url) -> MediaInfo   仅解析小云雀（自动识别视频/图片）
    extract_url(text)     -> str | None  从混合文本中提取视频链接
"""

import re
import json
import logging

from dataclasses import dataclass, field
from typing import Optional, List
from urllib.parse import urlparse, parse_qs

import requests

logger = logging.getLogger(__name__)


# ============================================================
#  自定义异常
# ============================================================

class ParseError(Exception):
    """解析失败（链接格式不对、API返回异常等）"""
    pass


class NetworkError(Exception):
    """网络请求失败"""
    pass


# ============================================================
#  数据结构
# ============================================================

@dataclass
class ImageItem:
    """单张图片信息"""
    url: str = ""
    width: int = 0
    height: int = 0
    format: str = ""

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "width": self.width,
            "height": self.height,
            "format": self.format,
        }


@dataclass
class MediaInfo:
    """解析后的媒体信息，兼容视频和图片"""

    # --- 通用字段 ---
    success: bool = True
    platform: str = ""
    media_type: str = "video"
    title: str = ""
    desc: str = ""

    # --- 视频字段 ---
    url: str = ""
    poster: str = ""
    width: int = 0
    height: int = 0

    # --- 豆包视频专属 ---
    definition: str = ""
    duration: int = 0
    codec: str = ""
    size: int = 0

    # --- 小云雀视频专属 ---
    url_with_params: str = ""

    # --- 图片字段 ---
    images: List[ImageItem] = field(default_factory=list)

    # --- 内部缓存 ---
    _download_headers: dict = field(default_factory=dict, repr=False)

    def to_dict(self) -> dict:
        d = {
            "success": self.success,
            "platform": self.platform,
            "media_type": self.media_type,
            "title": self.title,
            "desc": self.desc,
        }

        if self.media_type == "image":
            d["images"] = [img.to_dict() for img in self.images]
            if self.images:
                d["width"] = self.images[0].width
                d["height"] = self.images[0].height
        else:
            d["url"] = self.url
            d["poster"] = self.poster
            d["width"] = self.width
            d["height"] = self.height
            if self.platform == "doubao":
                d.update({
                    "definition": self.definition,
                    "duration": self.duration,
                    "codec": self.codec,
                    "size": self.size,
                })
            elif self.platform == "xiaoyunque":
                d["url_with_params"] = self.url_with_params

        return d


# 向后兼容别名
VideoInfo = MediaInfo


# ============================================================
#  工具函数
# ============================================================

def extract_url(text: str) -> Optional[str]:
    matches = re.findall(
        r'https?://[^\s"\'`<>，。！？、；：（）【】《》\n\r]+',
        text
    )
    for url in matches:
        if 'doubao.com' in url or 'xiaoyunque.jianying.com' in url:
            return url.rstrip('.,;:!?')
    return None


def _clean_url(text: str) -> str:
    url = extract_url(text)
    if url:
        return url
    return text.strip()


# ============================================================
#  豆包视频解析
# ============================================================

DOUBAO_API = (
    "https://www.doubao.com/samantha/media/get_play_info"
    "?version_code=20800&language=zh-CN&device_platform=web"
    "&aid=497858&real_aid=497858&pkg_type=release_version"
    "&device_id=&pc_version=2.51.7&region=&sys_region="
    "&samantha_web=1&use-olympus-account=1&web_tab_id="
)

DOUBAO_HEADERS = {
    "Content-Type": "application/json",
    "Origin": "https://www.doubao.com",
    "Referer": "https://www.doubao.com/",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
}

DOUBAO_DOWNLOAD_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
}


def _extract_doubao_video_id(url_or_text: str) -> str:
    text = _clean_url(url_or_text)

    if re.match(r'^[a-zA-Z0-9_]+$', text):
        return text

    m = re.search(r'video_id=([a-zA-Z0-9_]+)', text)
    if not m:
        raise ParseError(f"无法从链接中提取 video_id: {text}")
    return m.group(1)


def parse_doubao(url_or_text: str) -> MediaInfo:
    video_id = _extract_doubao_video_id(url_or_text)

    try:
        resp = requests.post(
            DOUBAO_API,
            headers=DOUBAO_HEADERS,
            json={"key": video_id},
            timeout=15,
        )
        resp.raise_for_status()
    except requests.Timeout:
        raise NetworkError("豆包API请求超时")
    except requests.RequestException as e:
        raise NetworkError(f"豆包API网络请求失败: {e}")

    data = resp.json()

    if data.get("code") != 0 or not data.get("data"):
        raise ParseError(f"豆包API返回异常: {json.dumps(data, ensure_ascii=False)}")

    info = data["data"]["original_media_info"]

    return MediaInfo(
        success=True,
        platform="doubao",
        media_type="video",
        url=info["main_url"],
        poster=data["data"].get("poster_url", ""),
        definition=info["meta"]["definition"],
        width=info["meta"]["width"],
        height=info["meta"]["height"],
        duration=info["meta"]["duration"],
        codec=info["meta"].get("codec_type", ""),
        size=info["meta"].get("size", 0),
        _download_headers=DOUBAO_DOWNLOAD_HEADERS,
    )


# ============================================================
#  小云雀解析
# ============================================================

XIAOYUNQUE_API = (
    "https://xiaoyunque.jianying.com/luckycat/cn/jianying/campaign/"
    "v1/pippit/share/landing_page?aid=8700"
)

MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
)

DESKTOP_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36"
)


def _resolve_short_link(short_url: str) -> dict:
    try:
        resp = requests.get(
            short_url,
            allow_redirects=True,
            headers={"User-Agent": MOBILE_UA},
            timeout=15,
        )
        resp.raise_for_status()
    except requests.Timeout:
        raise NetworkError("小云雀短链跳转超时")
    except requests.RequestException as e:
        raise NetworkError(f"小云雀短链网络请求失败: {e}")

    final_url = resp.url
    parsed = urlparse(final_url)
    raw_params = dict(parse_qs(parsed.query))
    params = {k: v[0] if isinstance(v, list) else v for k, v in raw_params.items()}

    if "inspiration_id" not in params:
        raise ParseError(
            f"短链跳转后无法提取 inspiration_id，最终 URL: {final_url}"
        )

    return params


def _extract_raw_url(signed_url: str) -> str:
    parsed = urlparse(signed_url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def _guess_image_format(url: str) -> str:
    if ".webp" in url.lower():
        return "webp"
    if ".png" in url.lower():
        return "png"
    if ".gif" in url.lower():
        return "gif"
    return "jpeg"


def _parse_xiaoyunque_video(item: dict) -> MediaInfo:
    video_list = item.get("video_info", [])
    if not video_list:
        raise ParseError("小云雀API未返回视频信息")

    video = video_list[0]
    signed_url = video["video_url"]
    raw_url = _extract_raw_url(signed_url)

    return MediaInfo(
        success=True,
        platform="xiaoyunque",
        media_type="video",
        title=item.get("title", ""),
        desc=item.get("desc", ""),
        url=raw_url,
        url_with_params=signed_url,
        poster=video.get("cover_url", ""),
        width=video.get("width", 0),
        height=video.get("height", 0),
        _download_headers={
            "User-Agent": DESKTOP_UA,
        },
    )


def _parse_xiaoyunque_image(item: dict) -> MediaInfo:
    image_list = item.get("image_info", [])
    if not image_list:
        raise ParseError("小云雀API未返回图片信息")

    images = []
    for img in image_list:
        img_url = img.get("image_url", "")
        images.append(ImageItem(
            url=img_url,
            width=img.get("width", 0),
            height=img.get("height", 0),
            format=_guess_image_format(img_url),
        ))

    return MediaInfo(
        success=True,
        platform="xiaoyunque",
        media_type="image",
        title=item.get("title", ""),
        desc=item.get("desc", ""),
        images=images,
        _download_headers={
            "User-Agent": DESKTOP_UA,
        },
    )


def parse_xiaoyunque(url_or_text: str) -> MediaInfo:
    clean = _clean_url(url_or_text)

    if "xiaoyunque.jianying.com" not in clean:
        raise ParseError(f"不是小云雀链接: {clean}")

    query_params = _resolve_short_link(clean)

    try:
        api_resp = requests.post(
            XIAOYUNQUE_API,
            json={"query_params": query_params},
            headers={
                "User-Agent": MOBILE_UA,
                "Referer": clean,
                "Content-Type": "application/json",
            },
            timeout=15,
        )
        api_resp.raise_for_status()
    except requests.Timeout:
        raise NetworkError("小云雀API请求超时")
    except requests.RequestException as e:
        raise NetworkError(f"小云雀API网络请求失败: {e}")

    data = api_resp.json()

    if data.get("err_no") != 0 or not data.get("data"):
        raise ParseError(
            f"小云雀API返回异常: {json.dumps(data, ensure_ascii=False)}"
        )

    try:
        page = data["data"]["page_info"]["inspiration_page"]
        item = page["item_info"]
    except KeyError as e:
        raise ParseError(f"小云雀响应结构异常，缺少字段: {e}")

    if "image_info" in item:
        return _parse_xiaoyunque_image(item)
    elif "video_info" in item:
        return _parse_xiaoyunque_video(item)
    else:
        raise ParseError(
            f"小云雀返回未知媒体类型，item_info keys: {list(item.keys())}"
        )


# ============================================================
#  统一入口
# ============================================================

def parse(url_or_text: str) -> MediaInfo:
    text = url_or_text.lower()

    if "xiaoyunque.jianying.com" in text:
        return parse_xiaoyunque(url_or_text)

    if "doubao.com" in text:
        return parse_doubao(url_or_text)

    if re.match(r'^[a-zA-Z0-9_]+$', url_or_text.strip()):
        return parse_doubao(url_or_text)

    raise ParseError(
        f"不支持的链接格式。目前支持：豆包（视频）、小云雀（视频+图片）。\n"
        f"输入: {url_or_text[:100]}"
    )
