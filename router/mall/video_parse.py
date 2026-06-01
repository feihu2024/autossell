from fastapi import APIRouter
from service.video_parse_service import parse_video_url
from pydantic import BaseModel

router = APIRouter()


class VideoParseRequest(BaseModel):
    token: str  # 管理端传入的 ALAPI 令牌
    url: str    # 用户输入的视频链接


@router.post("/")
def parse_video(req: VideoParseRequest):
    """
    视频链接解析接口

    请求参数:
        token: ALAPI 接口令牌（管理端传入）
        url: 视频链接（用户端传入，支持抖音、快手、小红书、B站等平台）
    """
    result = parse_video_url(token=req.token, url=req.url)
    return result
