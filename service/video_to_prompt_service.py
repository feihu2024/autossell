import requests
import logging
import json

logger = logging.getLogger(__name__)

# DashScope 视频理解接口地址
DASHSCOPE_VIDEO_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"


def video_to_prompt(
    api_key: str,
    model: str,
    video_url: str,
    prompt: str,
    fps: float = 2.0,
    max_frames: int = 2000,
    min_pixels: int = 65536,
    max_pixels: int = 655360,
    total_pixels: int = 134217728,
    stream: bool = False,
) -> dict:
    """
    通过 DashScope 多模态 API 理解视频内容，反推生成文字描述（提示词）

    :param api_key:      DashScope API Key，管理端传入
    :param model:        模型名称，如 "qwen-vl-max-latest"，管理端传入
    :param video_url:    视频公网URL，用户上传后传入
    :param prompt:       提示词，管理端传入
    :param fps:          抽帧频率，默认2.0，管理端传入
    :param max_frames:   最大帧数，默认2000，管理端传入
    :param min_pixels:   最小像素，默认65536，管理端传入
    :param max_pixels:   最大像素，默认655360，管理端传入
    :param total_pixels: 总像素限制，默认134217728，管理端传入
    :param stream:       是否流式输出，管理端传入
    :return: DashScope 原始返回结果（透传给前端）
    """
    if not api_key:
        return {"code": -1, "msg": "api_key 不能为空"}

    if not model:
        return {"code": -1, "msg": "模型名称不能为空"}

    if not video_url:
        return {"code": -1, "msg": "视频地址不能为空"}

    if not prompt:
        return {"code": -1, "msg": "提示词不能为空"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    if stream:
        headers["X-DashScope-SSE"] = "enable"

    # 构建 video 对象，只添加非默认值的参数（避免不支持的字段导致 400）
    video_obj = {"video": video_url, "fps": fps}
    if max_frames and max_frames != 2000:
        video_obj["max_frames"] = max_frames
    if min_pixels and min_pixels != 65536:
        video_obj["min_pixels"] = min_pixels
    if max_pixels and max_pixels != 655360:
        video_obj["max_pixels"] = max_pixels
    if total_pixels and total_pixels != 134217728:
        video_obj["total_pixels"] = total_pixels

    payload = {
        "model": model,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        video_obj,
                        {
                            "text": prompt,
                        },
                    ],
                }
            ],
        },
        "parameters": {
            "incremental_output": stream,
        },
    }

    try:
        response = requests.post(DASHSCOPE_VIDEO_URL, json=payload, headers=headers, timeout=120, stream=stream)
        response.raise_for_status()

        # 流式输出：返回原始响应对象，由 router 层处理 SSE 转发
        if stream:
            return {"code": 200, "stream_response": response}

        # 非流式输出：直接返回 JSON
        result = response.json()
        if result.get("output") or result.get("request_id"):
            logger.info(f"视频理解成功: model={model}, video={video_url[:80]}...")
            return result
        else:
            logger.warning(f"视频理解失败: {result.get('message', '未知错误')}")
            return result  # 透传 DashScope 的错误信息

    except requests.exceptions.Timeout:
        logger.error(f"视频理解超时: video={video_url[:80]}...")
        return {"code": -1, "msg": "请求超时，视频可能过长，请稍后重试"}
    except requests.exceptions.RequestException as e:
        logger.error(f"视频理解请求异常: {e}")
        return {"code": -1, "msg": f"请求失败: {str(e)}"}
    except Exception as e:
        logger.error(f"视频理解未知异常: {e}")
        return {"code": -1, "msg": f"系统异常: {str(e)}"}


def parse_sse_line(line: str):
    """
    解析单条 SSE 数据行，提取 content 文本
    """
    if line.startswith("data:"):
        data_str = line[5:].strip()
        if data_str == "[DONE]":
            return None
        try:
            data = json.loads(data_str)
            choices = data.get("output", {}).get("choices", [])
            if choices:
                content = choices[0].get("message", {}).get("content", [])
                if content:
                    for item in content:
                        if "text" in item:
                            return item["text"]
        except json.JSONDecodeError:
            pass
    return None
