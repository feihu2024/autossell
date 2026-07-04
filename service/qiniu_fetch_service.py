"""
七牛云同步资源抓取服务

使用 Qiniu Python SDK 的 BucketManager.fetch() 接口（同步抓取）。
"""

import hashlib
import logging
from typing import Optional

from qiniu import Auth, BucketManager
from config import VIDEOQINIU

logger = logging.getLogger(__name__)


# 资源类型 -> 七牛已有文件夹
_TYPE_FOLDER_MAP = {
    "video": "video",
    "cover": "cover",
    "livephoto_video": "livephoto_video",
    "livephoto_cover": "livephoto_cover",
    "pics": "pics",
}


def _make_key(original_url: str, folder: str, suffix: str = "") -> str:
    hex_hash = hashlib.md5(original_url.encode("utf-8")).hexdigest()
    if suffix:
        return f"{folder}/{hex_hash}.{suffix}"
    return f"{folder}/{hex_hash}"


def _folder_by_type(resource_type: str) -> str:
    return _TYPE_FOLDER_MAP.get(resource_type, "video")


def _guess_suffix(url: str, resource_type: str = "video") -> str:
    url_lower = url.lower().split("?")[0]
    for ext in (".mp4", ".webm", ".mov", ".jpg", ".jpeg", ".png", ".gif", ".webp", ".ts"):
        if url_lower.endswith(ext):
            return ext.lstrip(".")
    # 无扩展名 → 按资源类型给默认值
    if resource_type in ("cover", "pics", "livephoto_cover"):
        return "jpg"
    return "mp4"


def fetch_url(
    original_url: str,
    resource_type: str = "video",
    bucket: Optional[str] = None,
    key: Optional[str] = None,
) -> dict:
    """
    同步抓取：调用七牛 SDK BucketManager.fetch()，等待完成后返回七牛 URL。

    :param original_url: 要抓取的公网 URL
    :param resource_type: 资源类型（video/cover/livephoto_video/livephoto_cover/pics），决定存储到哪个已有文件夹
    :param bucket: 七牛空间名，不传则用 VIDEOQINIU.bucketName
    :param key: 七牛存储 key，不传则自动生成（基于 URL 的 MD5）
    :return: {"ok": True, "key": "...", "qiniu_url": "..."}
    """
    if not original_url:
        return {"ok": False, "error": "URL 不能为空"}

    bucket = bucket or VIDEOQINIU.bucketName
    if not bucket:
        return {"ok": False, "error": "七牛 bucketName 未配置"}

    if key is None:
        folder = _folder_by_type(resource_type)
        suffix = _guess_suffix(original_url, resource_type)
        key = _make_key(original_url, folder, suffix)

    auth = Auth(VIDEOQINIU.accessKey, VIDEOQINIU.secretKey)
    bucket_mgr = BucketManager(auth)

    # BucketManager.fetch(url, bucket, key)
    # 返回 (ret, info)
    # ret: dict e.g. {"key": "...", "hash": "..."} on success
    # info: ResponseInfo object, info.status_code == 200 on success
    try:
        ret, info = bucket_mgr.fetch(original_url, bucket, key)
        logger.info(
            "qiniu fetch: url=%s status=%d ret=%s",
            original_url[:80], info.status_code, ret,
        )
    except Exception as e:
        logger.error("qiniu fetch exception: %s", e)
        return {"ok": False, "error": f"请求七牛失败: {e}"}

    if info.status_code != 200:
        error_msg = "七牛抓取失败"
        try:
            if ret and isinstance(ret, dict):
                error_msg = ret.get("error", error_msg)
        except Exception:
            pass
        return {"ok": False, "error": f"七牛返回 {info.status_code}: {error_msg}"}

    returned_key = (ret and ret.get("key")) or key
    raw_url = f"{VIDEOQINIU.domain}/{returned_key}"
    # 空间是私有的，需要签名生成带 token 的临时下载链接
    qiniu_url = auth.private_download_url(raw_url, expires=86400)  # 24h 有效

    return {"ok": True, "key": returned_key, "qiniu_url": qiniu_url}
