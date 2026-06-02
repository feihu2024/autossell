from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from service.video_to_prompt_service import video_to_prompt, parse_sse_line
from pydantic import BaseModel

router = APIRouter()


class VideoToPromptRequest(BaseModel):
    video_url: str  # 视频公网URL，前端传入


@router.post("/")
async def video_to_prompt_api(req: VideoToPromptRequest):
    """
    视频反推提示词接口（所有管理端参数从数据库读取）

    请求参数:
        video_url: 视频公网URL（前端传入）
    """
    result = video_to_prompt(video_url=req.video_url)

    # 流式输出：SSE 转发给前端
    if req.video_url and result.get("code") == 200 and "stream_response" in result:
        resp = result["stream_response"]

        def event_generator():
            for line in resp.iter_lines(decode_unicode=True):
                if not line:
                    continue
                text = parse_sse_line(line)
                if text is not None:
                    yield text

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    return result
