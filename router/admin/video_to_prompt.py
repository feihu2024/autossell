from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from service.video_to_prompt_service import video_to_prompt, parse_sse_line
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class VideoToPromptRequest(BaseModel):
    api_key: str                          # DashScope API Key，管理端传入
    model: str                            # 模型名称，管理端传入
    video_url: str                         # 视频公网URL，用户上传后传入
    prompt: str                            # 提示词，管理端传入
    fps: Optional[float] = 2.0           # 抽帧频率，管理端传入，默认2.0
    max_frames: Optional[int] = 2000      # 最大帧数，管理端传入，默认2000
    min_pixels: Optional[int] = 65536    # 最小像素，管理端传入，默认65536
    max_pixels: Optional[int] = 655360   # 最大像素，管理端传入，默认655360
    total_pixels: Optional[int] = 134217728  # 总像素限制，管理端传入，默认134217728
    stream: Optional[bool] = False       # 是否流式输出，管理端传入，默认False


@router.post("/video_to_prompt")
async def video_to_prompt_api(req: VideoToPromptRequest):
    """
    视频反推提示词接口（基于阿里云 DashScope 多模态 API）

    请求参数:
        api_key:      DashScope API Key（管理端传入）
        model:        模型名称，如 "qwen-vl-max-latest"（管理端传入）
        video_url:    视频公网URL（用户上传后传入）
        prompt:       提示词，指导模型如何分析视频（管理端传入）
        fps:          抽帧频率（管理端传入，默认2.0）
        max_frames:   最大帧数（管理端传入，默认2000）
        min_pixels:   最小像素（管理端传入，默认65536）
        max_pixels:   最大像素（管理端传入，默认655360）
        total_pixels: 总像素限制（管理端传入，默认134217728）
        stream:       是否流式输出（管理端传入，默认False）
    """
    result = video_to_prompt(
        api_key=req.api_key,
        model=req.model,
        video_url=req.video_url,
        prompt=req.prompt,
        fps=req.fps,
        max_frames=req.max_frames,
        min_pixels=req.min_pixels,
        max_pixels=req.max_pixels,
        total_pixels=req.total_pixels,
        stream=req.stream,
    )

    # 流式输出：SSE 转发给前端
    if req.stream and result.get("code") == 200 and "stream_response" in result:
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
