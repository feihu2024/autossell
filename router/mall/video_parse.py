from fastapi import APIRouter
from service.video_parse_service import parse_video_url
from pydantic import BaseModel

router = APIRouter()


class VideoParseRequest(BaseModel):
    url: str    # 用户输入的视频链接


@router.post("/")
def parse_video(req: VideoParseRequest):
    """
    视频链接解析接口（token 从数据库读取）

    请求参数:
        url: 视频链接（用户端传入，支持抖音、快手、小红书、B站等平台）
    """
    result = parse_video_url(url=req.url)
    return result
