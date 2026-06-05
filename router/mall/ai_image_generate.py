from fastapi import APIRouter
from service.ai_image_generate_service import generate_image, query_user_image_tasks
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()


class ImageGenerateRequest(BaseModel):
    prompt: str             # 用户端输入的提示词
    userid: str             # 前端用户ID
    size: Optional[str] = ""   # 用户端选择的尺寸（可选，空则使用模型默认）
    resolution: Optional[str] = "1k"  # 用户端选择的分辨率，默认 "1k"
    image_urls: Optional[List[str]] = None    # 前端传入的参考图片地址列表（可选，支持多张）


class ImageTaskQueryRequest(BaseModel):
    userid: str             # 前端用户ID


@router.post("/")
def generate_image_api(req: ImageGenerateRequest):
    """
    AI 图片生成接口（异步，token、model、n 从数据库读取）

    请求参数:
        prompt:     图片生成提示词（用户端输入）
        userid:     前端用户ID
        size:       图片尺寸，如 "1024x1024"（可选，空则使用模型默认）
        resolution:  图片分辨率，如 "1k"、"2k"（可选，默认 "1k"）
        image_urls: 参考图片地址列表，用于图生图（可选，支持多张，如 ["url1","url2"]）
    返回:
        {"code": 200, "task_id": "ALAPI返回的任务ID"}
    """
    result = generate_image(
        prompt=req.prompt,
        userid=req.userid,
        size=req.size,
        resolution=req.resolution,
        image_urls=req.image_urls,
    )
    return result


@router.post("/query")
def query_user_image_tasks_api(req: ImageTaskQueryRequest):
    """
    查询用户图片生成任务列表（自动轮询待处理任务并抓取图片）

    请求参数:
        userid: 前端用户ID
    返回:
        {"code": 200, "data": [{"task_id": "xxx", "qiniu_url": "xxx 或 生成中"}, ...]}
    """
    result = query_user_image_tasks(userid=req.userid)
    return result
