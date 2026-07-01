"""
CDN 回源 302 代理端点

CDN 回源时调用本端点，解码自包含 token 获取原始直链，返回 302 重定向到源站。
CDN 跟随 302 后直接从源站拉取视频并缓存。
零存储依赖，token 自带签名和过期时间。
"""
import logging
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, Response
from fastapi import HTTPException
from service.video_parse_service import _decode_token

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
async def origin_health():
    """七牛源站测试专用，返回 200 证明源站可用"""
    return Response(content="OK", media_type="text/plain")


@router.get("/{token}")
async def video_redirect(token: str):
    """
    CDN 回源 → 302 到原始直链

    七牛 CDN 回源时会将请求路径原样转发到后端。
    解码 token 获取原始直链，返回 302 让 CDN 去源站拉取。
    """
    raw_url = _decode_token(token)
    if not raw_url:
        logger.warning("download token 无效或已过期: %s", token)
        raise HTTPException(status_code=410, detail="下载链接已过期，请重新获取")

    logger.info("302 redirect token → %s...", raw_url[:80])
    return RedirectResponse(url=raw_url, status_code=302)
