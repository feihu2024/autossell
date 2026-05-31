import os
import uuid
from fastapi import APIRouter, UploadFile, File, Form
from service.video_upload_service import upload_video_to_public

router = APIRouter()

# 视频临时保存目录
UPLOAD_DIR = "./upload_temp"


@router.post("/upload_video")
async def upload_video(
    video: UploadFile = File(..., description="用户上传的视频文件"),
    max_duration: float = Form(..., description="最大允许时长（分钟），管理端传入"),
):
    """
    视频上传接口

    功能：
        1. 接收前端上传的视频文件
        2. 校验视频时长是否 <= max_duration（分钟）
        3. 时长合法则上传至七牛云，返回公网可访问的URL
        4. 前端拿到URL后可传给视频理解接口

    请求参数（multipart/form-data）：
        video:        视频文件（用户端上传）
        max_duration: 最大允许时长，单位分钟（管理端传入）
    """
    # 确保临时目录存在
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # 保存到临时目录
    ext = os.path.splitext(video.filename)[1] or ".mp4"
    temp_filename = f"{uuid.uuid4().hex}{ext}"
    temp_path = os.path.join(UPLOAD_DIR, temp_filename)

    try:
        # 写入临时文件
        with open(temp_path, "wb") as f:
            content = await video.read()
            f.write(content)

        # 校验时长并上传
        result = upload_video_to_public(
            file_path=temp_path,
            max_duration_minutes=max_duration,
        )

        return result

    finally:
        # 无论成功失败，清理临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)
