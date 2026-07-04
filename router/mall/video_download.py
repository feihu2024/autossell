"""
视频下载路由：七牛同步 fetch 方案

POST /web/video/download
  接收单个公网 URL，提交七牛同步抓取，等待完成后返回七牛 URL。
  无需轮询，一次请求拿到结果。
"""
import logging
from fastapi import APIRouter
from pydantic import BaseModel

from service.qiniu_fetch_service import fetch_url

logger = logging.getLogger(__name__)

router = APIRouter()


class DownloadRequest(BaseModel):
    url: str
    type: str = "video"  # video/cover/livephoto_video/livephoto_cover/pics


class DownloadResponse(BaseModel):
    code: int
    msg: str = ""
    data: dict = None


@router.post("/", response_model=DownloadResponse)
async def download_media(req: DownloadRequest):
    """
    接收公网 URL，提交七牛同步抓取，返回七牛 URL。

    返回示例：
    {
      "code": 200,
      "data": {
        "qiniu_url": "https://vipvideo.yxiaozhu.com/video/xxx.mp4",
        "key": "video/xxx.mp4",
        "url": "原始URL"
      }
    }
    """
    if not req.url:
        return DownloadResponse(code=400, msg="url 不能为空")

    result = fetch_url(req.url, resource_type=req.type)

    if not result.get("ok"):
        logger.error("七牛 fetch 失败: %s", result.get("error"))
        return DownloadResponse(code=500, msg=result.get("error", "抓取失败"))

    logger.info("七牛 fetch 成功: key=%s, url=%s",
                result.get("key"), req.url[:80])

    return DownloadResponse(
        code=200,
        data={
            "qiniu_url": result.get("qiniu_url", ""),
            "key": result.get("key", ""),
            "url": req.url,
        },
    )
