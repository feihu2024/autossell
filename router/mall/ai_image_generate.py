from fastapi import APIRouter
from service.ai_image_generate_service import generate_image, query_image_task
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class ImageGenerateRequest(BaseModel):
    prompt: str             # 用户端输入的提示词
    size: Optional[str] = ""   # 用户端选择的尺寸（可选，空则使用模型默认）
    resolution: Optional[str] = "1k"  # 用户端选择的分辨率，默认 "1k"
    image_urls: Optional[str] = ""    # 前端传入的参考图片地址（可选，可空置）


class ImageTaskQueryRequest(BaseModel):
    task_id: str            # 文生图任务ID


@router.post("/")
def generate_image_api(req: ImageGenerateRequest):
    """
    AI 图片生成接口（token、model、n 从数据库读取）

    请求参数:
        prompt:     图片生成提示词（用户端输入）
        size:       图片尺寸，如 "1024x1024"（可选，空则使用模型默认）
        resolution:  图片分辨率，如 "1k"、"2k"（可选，默认 "1k"）
        image_urls: 参考图片地址，用于图生图（可选，可空置）
    """
    result = generate_image(
        prompt=req.prompt,
        size=req.size,
        resolution=req.resolution,
        image_urls=req.image_urls,
    )
    return result


@router.post("/task")
def query_image_task_api(req: ImageTaskQueryRequest):
    """
    查询文生图任务结果（token 从数据库读取）

    请求参数:
        task_id: 文生图任务ID（调用图片生成接口后返回）
    """
    result = query_image_task(task_id=req.task_id)
    return result
