import logging
import uuid
import os
from urllib.parse import urlparse
from qiniu import Auth, put_data, BucketManager
from config import QINIU

logger = logging.getLogger(__name__)

# 上传文件存储前缀
UPLOAD_PREFIX = "temp_video/"

# 允许的视频扩展名
ALLOWED_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv", ".wmv", ".m4v", ".3gp"}


def upload_video(file_bytes: bytes, original_filename: str) -> dict:
    """
    将视频文件上传至七牛云，返回公网访问 URL

    :param file_bytes: 视频文件的二进制内容
    :param original_filename: 原始文件名（用于提取扩展名）
    :return: {"code": 200, "data": {"video_url": "https://xxx/temp_video/uuid.mp4"}} 或错误信息
    """
    if not file_bytes:
        return {"code": -1, "msg": "文件不能为空"}

    # 提取扩展名并校验
    ext = os.path.splitext(original_filename)[1].lower() if original_filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        return {"code": -1, "msg": f"不支持的视频格式: {ext}，支持: {', '.join(ALLOWED_EXTENSIONS)}"}

    # 文件大小限制（500MB）
    max_size = 500 * 1024 * 1024
    if len(file_bytes) > max_size:
        return {"code": -1, "msg": "文件大小超过500MB限制"}

    # 生成唯一文件名
    key = f"{UPLOAD_PREFIX}{uuid.uuid4().hex}{ext}"

    try:
        # 七牛鉴权
        qiniu_auth = Auth(QINIU.accessKey, QINIU.secretKey)
        token = qiniu_auth.upload_token(QINIU.bucketName, key, expires=3600)

        # 上传二进制数据
        ret, info = put_data(token, key, file_bytes)

        if info.status_code != 200:
            logger.error(f"七牛上传失败: status_code={info.status_code}, body={info.text_body}")
            return {"code": -1, "msg": "上传失败，请稍后重试"}

        # 拼接公网访问 URL
        domain = QINIU.DOMAIN
        if not domain:
            logger.error("七牛 DOMAIN 未配置")
            return {"code": -1, "msg": "七牛域名未配置，请联系管理员"}

        # 确保 domain 以 https:// 开头且不以 / 结尾
        if not domain.startswith("http"):
            domain = f"https://{domain}"
        domain = domain.rstrip("/")

        video_url = f"{domain}/{key}"

        # 私有空间：生成带签名的访问链接，有效期 4 小时
        qiniu_auth = Auth(QINIU.accessKey, QINIU.secretKey)
        signed_url = qiniu_auth.private_download_url(video_url, expires=14400)

        logger.info(f"视频上传成功: {signed_url}")
        return {"code": 200, "data": {"video_url": signed_url}}

    except Exception as e:
        logger.error(f"视频上传异常: {e}")
        return {"code": -1, "msg": f"上传异常: {str(e)}"}


def delete_file_by_url(url: str) -> dict:
    """
    根据七牛 URL 删除七牛空间内对应的文件

    :param url: 七牛访问链接（签名或非签名均可，只取路径部分作为 key）
    :return: {"code": 200, "msg": "删除成功"} 或错误信息
    """
    if not url:
        return {"code": -1, "msg": "url 不能为空"}

    try:
        # 从 URL 中提取 key（去掉域名前缀和查询参数）
        parsed = urlparse(url)
        key = parsed.path.lstrip("/")
        if not key:
            return {"code": -1, "msg": "无法从 url 中解析文件路径"}

        bucket_mgr = BucketManager(Auth(QINIU.accessKey, QINIU.secretKey))
        ret, info = bucket_mgr.delete(QINIU.bucketName, key)

        if info.status_code == 200:
            logger.info(f"文件删除成功: key={key}")
            return {"code": 200, "msg": "删除成功"}
        elif info.status_code == 612:
            logger.warning(f"文件不存在: key={key}")
            return {"code": -1, "msg": "文件不存在或已删除"}
        else:
            logger.error(f"文件删除失败: status_code={info.status_code}, body={info.text_body}")
            return {"code": -1, "msg": "删除失败，请稍后重试"}

    except Exception as e:
        logger.error(f"文件删除异常: {e}")
        return {"code": -1, "msg": f"删除异常: {str(e)}"}
