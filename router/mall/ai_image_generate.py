from fastapi import APIRouter
from service.ai_image_generate_service import generate_image
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class ImageGenerateRequest(BaseModel):
    token: str              # 管理端传入的 ALAPI 令牌
    prompt: str             # 用户端输入的提示词
    size: Optional[str] = ""   # 用户端选择的尺寸（可选，空则使用模型默认）
    resolution: Optional[str] = "1k"  # 用户端选择的分辨率，默认 "1k"
    image_urls: Optional[str] = ""    # 前端传入的参考图片地址（可选，可空置）
    model: Optional[str] = "gpt-image-2"  # 模型名称，默认 gpt-image-2
    n: Optional[int] = 1   # 生成数量，默认 1


@router.post("/")
def generate_image_api(req: ImageGenerateRequest):
    """
    AI 图片生成接口

    请求参数:
        token:      ALAPI 接口令牌（管理端传入）
        prompt:     图片生成提示词（用户端输入）
        size:       图片尺寸，如 "1024x1024"（可选，空则使用模型默认）
        resolution:  图片分辨率，如 "1k"、"2k"（可选，默认 "1k"）
        image_urls: 参考图片地址，用于图生图（可选，可空置）
        model:      模型名称，默认 "gpt-image-2"（可选）
        n:          生成图片数量，默认 1（可选）
    """
    result = generate_image(
        token=req.token,
        prompt=req.prompt,
        size=req.size,
        resolution=req.resolution,
        image_urls=req.image_urls,
        model=req.model,
        n=req.n,
    )
    return result
