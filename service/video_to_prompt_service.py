import requests
import logging
import json
from dao.d_video_config import get_config_value

logger = logging.getLogger(__name__)

# DashScope 视频理解接口地址
DASHSCOPE_VIDEO_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"

# 各参数的默认值，用于判断是否需要发送给 API
DEFAULT_MAX_FRAMES = 2000
DEFAULT_MIN_PIXELS = 65536
DEFAULT_MAX_PIXELS = 655360
DEFAULT_TOTAL_PIXELS = 134217728


def _safe_float(val, default=2.0):
    """安全转换为 float"""
    if val is None:
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def _safe_int(val, default):
    """安全转换为 int"""
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def _safe_bool(val, default=False):
    """安全转换为 bool"""
    if val is None:
        return default
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.lower() in ("true", "1", "yes")
    return default


def video_to_prompt(video_url: str) -> dict:
    """
    通过 DashScope 多模态 API 理解视频内容，反推生成文字描述（提示词）
    所有管理端参数从数据库 video_config 表读取

    :param video_url: 视频公网URL，前端传入
    :return: DashScope 原始返回结果（透传给前端）
    """
    # 从数据库读取管理端配置
    api_key = get_config_value("video_to_prompt", "api_key")
    if not api_key:
        return {"code": -1, "msg": "api_key 未配置，请联系管理员"}

    model = get_config_value("video_to_prompt", "model") or "qwen3.6-plus"
    prompt = get_config_value("video_to_prompt", "prompt")
    if not prompt:
        return {"code": -1, "msg": "提示词未配置，请联系管理员"}

    fps = _safe_float(get_config_value("video_to_prompt", "fps"), 2.0)
    max_frames = _safe_int(get_config_value("video_to_prompt", "max_frames"), DEFAULT_MAX_FRAMES)
    min_pixels = _safe_int(get_config_value("video_to_prompt", "min_pixels"), DEFAULT_MIN_PIXELS)
    max_pixels = _safe_int(get_config_value("video_to_prompt", "max_pixels"), DEFAULT_MAX_PIXELS)
    total_pixels = _safe_int(get_config_value("video_to_prompt", "total_pixels"), DEFAULT_TOTAL_PIXELS)
    stream = _safe_bool(get_config_value("video_to_prompt", "stream"), False)

    if not video_url:
        return {"code": -1, "msg": "视频地址不能为空"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    if stream:
        headers["X-DashScope-SSE"] = "enable"

    # 构建 video 对象，只添加非默认值的参数（避免不支持的字段导致 400）
    video_obj = {"video": video_url, "fps": fps}
    if max_frames and max_frames != DEFAULT_MAX_FRAMES:
        video_obj["max_frames"] = max_frames
    if min_pixels and min_pixels != DEFAULT_MIN_PIXELS:
        video_obj["min_pixels"] = min_pixels
    if max_pixels and max_pixels != DEFAULT_MAX_PIXELS:
        video_obj["max_pixels"] = max_pixels
    if total_pixels and total_pixels != DEFAULT_TOTAL_PIXELS:
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
