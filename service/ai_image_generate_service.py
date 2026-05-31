import requests
import logging

logger = logging.getLogger(__name__)

# ALAPI 图片生成接口地址
ALAPI_IMAGE_GEN_URL = "https://v3.alapi.cn/api/ai/images/generations_sync"


def generate_image(
    token: str,
    prompt: str,
    size: str = "",
    resolution: str = "1k",
    image_urls: str = "",
    model: str = "gpt-image-2",
    n: int = 1,
) -> dict:
    """
    通过 ALAPI 调用 AI 图片生成接口

    :param token: ALAPI 令牌，管理端传入
    :param prompt: 图片生成提示词，用户端传入
    :param size: 图片尺寸，用户端选择（为空时使用模型默认）
    :param resolution: 图片分辨率，用户端选择，默认 "1k"
    :param image_urls: 参考图片地址（可选，可空置）
    :param model: 模型名称，默认 "gpt-image-2"
    :param n: 生成数量，默认 1
    :return: ALAPI 原始返回结果（透传给前端）
    """
    if not token:
        return {"code": -1, "msg": "token 不能为空，请联系管理员配置"}

    if not prompt:
        return {"code": -1, "msg": "提示词(prompt)不能为空"}

    payload = {
        "token": token,
        "model": model,
        "prompt": prompt,
        "n": n,
        "size": size,
        "image_urls": image_urls,
        "resolution": resolution,
    }

    # 过滤空字符串参数（可选字段空置时不传），保留数字类型
    payload = {k: v for k, v in payload.items() if v is not None and v != ""}

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(ALAPI_IMAGE_GEN_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()

        if result.get("code") == 200:
            logger.info(f"图片生成成功: prompt={prompt[:50]}...")
            return result
        else:
            logger.warning(f"图片生成失败: {result.get('msg', '未知错误')}")
            return result  # 透传 ALAPI 的错误信息

    except requests.exceptions.Timeout:
        logger.error(f"图片生成超时: prompt={prompt[:50]}...")
        return {"code": -1, "msg": "请求超时，请稍后重试"}
    except requests.exceptions.RequestException as e:
        logger.error(f"图片生成请求异常: {e}")
        return {"code": -1, "msg": f"请求失败: {str(e)}"}
    except Exception as e:
        logger.error(f"图片生成未知异常: {e}")
        return {"code": -1, "msg": f"系统异常: {str(e)}"}
