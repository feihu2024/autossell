"""
文案提取接口
调用 zhuceka API 提取视频/图文的文案文本。
"""

from fastapi import APIRouter
from pydantic import BaseModel
from service.wenan_extract_service import extract_wenan

router = APIRouter()


class WenanRequest(BaseModel):
    url: str


@router.post("/")
async def wenan_extract(req: WenanRequest):
    """
    文案提取

    请求示例:
        POST /web/video/wenan
        {"url": "抖音分享链接 或 纯净链接"}

    返回示例:
        {"code": 200, "msg": "提取成功", "data": {"text": "文案内容..."}}
    """
    result = extract_wenan(req.url)
    return result
