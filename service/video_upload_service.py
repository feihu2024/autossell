import logging
import uuid
import datetime
from pathlib import Path
from urllib.parse import urlparse
from qiniu import Auth, BucketManager
from config import QINIU, DIRS
from service import qiniu_service

# 七牛云对外访问域名（硬编码）
QINIU_BASE_URL = 'https://mlcfjihuaqn.yxiaozhu.com'

logger = logging.getLogger(__name__)


def upload_video(file_bytes: bytes, filename: str) -> dict:
    """
    将前端传入的视频文件上传至七牛云，返回带签名的私有空间 URL（有效期 4 小时）

    :param file_bytes: 文件二进制内容
    :param filename: 原始文件名（用于取后缀）
    :return: {"code": 200, "data": {"video_url": "带签名URL"}} 或错误信息
    """
    # 文件大小校验：150MB
    if len(file_bytes) > 150 * 1024 * 1024:
        return {"code": -1, "msg": "已超文件最大限制（150MB）"}

    try:
        file_type = "video"
        file_date = f"{datetime.date.today()}"
        file_name = f"{uuid.uuid1()}{Path(filename).suffix}"
        file_dir = Path(DIRS.assets_dir) / file_type / file_date
        file_dir.mkdir(parents=True, exist_ok=True)
        file_path = file_dir / file_name

        # 落盘本地（临时文件）
        with open(str(file_path), "wb") as f:
            f.write(file_bytes)

        # 上传到七牛
        qiniu_res = qiniu_service.qiniu_upload(str(file_path), file_name)
        if not qiniu_res:
            return {"code": -1, "msg": "七牛上传失败"}

        # 生成私有空间签名 URL，有效期 4 小时
        raw_url = f"{QINIU_BASE_URL}/{file_name}"
        qiniu_auth = Auth(QINIU.accessKey, QINIU.secretKey)
        signed_url = qiniu_auth.private_download_url(raw_url, expires=14400)

        logger.info(f"视频上传成功: {file_name}")
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
