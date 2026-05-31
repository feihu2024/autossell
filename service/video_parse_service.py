import requests
import logging

logger = logging.getLogger(__name__)

# ALAPI 视频解析接口地址
ALAPI_VIDEO_URL = "https://v3.alapi.cn/api/video/url"


def parse_video_url(token: str, url: str) -> dict:
    """
    通过 ALAPI 解析视频链接，提取无水印视频地址

    :param token: ALAPI 接口令牌，由管理端配置传入
    :param url: 用户输入的视频链接（支持抖音、快手、小红书、B站等平台）
    :return: 解析结果字典
        成功: {"code": 200, "msg": "success", "data": {...}}
        失败: {"code": -1, "msg": "错误信息"}
    """
    if not token:
        return {"code": -1, "msg": "token 不能为空，请联系管理员配置"}

    if not url:
        return {"code": -1, "msg": "视频链接不能为空"}

    payload = {
        "token": token,
        "url": url.strip()
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(ALAPI_VIDEO_URL, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        result = response.json()

        if result.get("code") == 200:
            logger.info(f"视频解析成功: {url}")
            return result
        else:
            logger.warning(f"视频解析失败: {result.get('msg', '未知错误')}")
            return {"code": -1, "msg": result.get("msg", "解析失败，请检查链接是否正确")}

    except requests.exceptions.Timeout:
        logger.error(f"视频解析超时: {url}")
        return {"code": -1, "msg": "解析超时，请稍后重试"}
    except requests.exceptions.RequestException as e:
        logger.error(f"视频解析请求异常: {e}")
        return {"code": -1, "msg": f"请求失败: {str(e)}"}
    except Exception as e:
        logger.error(f"视频解析未知异常: {e}")
        return {"code": -1, "msg": f"系统异常: {str(e)}"}
