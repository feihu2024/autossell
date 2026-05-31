import os
import uuid
import struct
import logging
from config import QINIU, DOMAIN
from service.qiniu_service import qiniu_upload

logger = logging.getLogger(__name__)


def get_video_duration(file_path: str) -> float:
    """
    纯 Python 解析 MP4 文件获取视频时长（秒），零外部依赖

    通过解析 MP4 的 moov -> mvhd box 获取时长，支持 MP4/M4V/MOV 格式

    :param file_path: 视频文件本地路径
    :return: 视频时长（秒），解析失败返回 -1
    """
    try:
        file_size = os.path.getsize(file_path)
        with open(file_path, "rb") as f:
            # 查找 moov box
            moov_data = _find_moov_box(f, file_size)
            if moov_data is None:
                return -1

            # 在 moov 中查找 mvhd box
            mvhd_data = _find_box(moov_data, b"mvhd")
            if mvhd_data is None:
                return -1

            # 解析 mvhd（跳过 1 字节 version + 3 字节 flags）
            version = mvhd_data[0]
            if version == 0:
                # 32 位时间：跳过 4 字节 version/flags + 4 字节 creation + 4 字节 modification + 4 字节 timescale + 4 字段 duration
                timescale = struct.unpack(">I", mvhd_data[12:16])[0]
                duration = struct.unpack(">I", mvhd_data[16:20])[0]
            elif version == 1:
                # 64 位时间：跳过 4 字节 version/flags + 8 字节 creation + 8 字节 modification + 4 字节 timescale + 8 字段 duration
                timescale = struct.unpack(">I", mvhd_data[20:24])[0]
                duration = struct.unpack(">Q", mvhd_data[24:32])[0]
            else:
                return -1

            if timescale <= 0:
                return -1

            return duration / timescale
    except Exception:
        return -1


def _find_moov_box(f, file_size):
    """
    在文件顶层 box 中查找 moov，返回 moov box 的数据
    """
    offset = 0
    while offset < file_size:
        f.seek(offset)
        header = f.read(8)
        if len(header) < 8:
            return None
        box_size, box_type = struct.unpack(">I4s", header)
        box_size = int(box_size)

        if box_type == b"moov":
            f.seek(offset + 8)
            moov_data = f.read(box_size - 8)
            return moov_data

        if box_size == 0:
            box_size = file_size - offset
        elif box_size == 1:
            f.seek(offset + 8)
            ext = f.read(8)
            box_size = struct.unpack(">Q", ext)[0]

        offset += box_size
    return None


def _find_box(data, target_type):
    """
    在 box 数据中查找指定类型的子 box，返回子 box 数据
    """
    offset = 0
    data_len = len(data)
    while offset < data_len:
        if offset + 8 > data_len:
            return None
        box_size, box_type = struct.unpack(">I4s", data[offset:offset + 8])
        box_size = int(box_size)

        if box_type == target_type:
            return data[offset + 8:offset + box_size]

        if box_size == 0:
            box_size = data_len - offset
        elif box_size == 1:
            box_size = struct.unpack(">Q", data[offset + 8:offset + 16])[0]

        offset += box_size
    return None


def upload_video_to_public(file_path: str, max_duration_minutes: float) -> dict:
    """
    校验视频时长并上传至七牛云，返回公网可访问的URL

    :param file_path: 视频文件本地路径
    :param max_duration_minutes: 最大允许时长（分钟），超过则拒绝
    :return:
        成功: {"code": 200, "msg": "success", "data": {"video_url": "https://...", "duration": 120.5, "filename": "xxx.mp4"}}
        失败: {"code": -1, "msg": "错误信息"}
    """
    if not file_path or not os.path.exists(file_path):
        return {"code": -1, "msg": "视频文件不存在"}

    # 获取视频时长
    duration_seconds = get_video_duration(file_path)
    if duration_seconds < 0:
        return {"code": -1, "msg": "无法读取视频信息，请检查视频文件格式是否正确（仅支持 MP4/MOV 格式）"}

    max_duration_seconds = max_duration_minutes * 60

    if duration_seconds > max_duration_seconds:
        duration_min = round(duration_seconds / 60, 2)
        return {
            "code": -1,
            "msg": f"视频时长 {duration_min} 分钟，超过最大限制 {max_duration_minutes} 分钟",
            "data": {"duration": round(duration_seconds, 2)},
        }

    # 生成唯一文件名，保留原始扩展名
    ext = os.path.splitext(file_path)[1] or ".mp4"
    upload_name = f"video_{uuid.uuid4().hex[:16]}{ext}"

    # 上传到七牛云
    upload_result = qiniu_upload(filepath=file_path, upload_name=upload_name)

    if not upload_result:
        return {"code": -1, "msg": "视频上传失败，请稍后重试"}

    # 拼接公网访问地址
    video_url = f"{DOMAIN}/{upload_name}" if DOMAIN else f"https://{QINIU.bucketName}.cn-east-2.qiniup.com/{upload_name}"

    logger.info(f"视频上传成功: {video_url}, 时长: {round(duration_seconds, 2)}秒")

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "video_url": video_url,
            "duration": round(duration_seconds, 2),
            "filename": upload_name,
        },
    }
