from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from service.video_upload_service import upload_video, delete_file_by_url

router = APIRouter()


@router.post("/")
async def upload_video_api(file: UploadFile = File(...)):
    """
    视频上传接口：将前端传入的视频文件上传至七牛云，返回带签名的私有空间 URL

    请求格式: multipart/form-data
    参数:
        file: 视频文件（必填）

    返回:
        {"code": 200, "data": {"video_url": "带签名的七牛URL，有效期4小时"}}
    """
    file_bytes = await file.read()

    if not file_bytes or len(file_bytes) == 0:
        return {"code": -1, "msg": "上传文件为空"}

    return upload_video(file_bytes, file.filename or "")


class DeleteFileRequest(BaseModel):
    url: str


@router.post("/delete")
async def delete_file_api(req: DeleteFileRequest):
    """
    文件删除接口：根据七牛 URL 删除对应文件，前端退出页面时调用

    参数:
        url: 七牛访问链接（签名URL或原始URL均可）

    返回:
        {"code": 200, "msg": "删除成功"}
    """
    return delete_file_by_url(req.url)
