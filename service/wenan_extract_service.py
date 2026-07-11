"""
zhuceka 文案提取服务
调用 https://api.zhuceka.cn/home/api?type=wenan 提取视频/图文的文案文本。
"""

import logging
import requests
from dao.d_video_config import get_config_value

logger = logging.getLogger(__name__)

ZHUCEKA_API = "https://api.zhuceka.cn/home/api"


def _resolve_clean_url(url: str, timeout: int = 10) -> str:
    """
    跟随短链接重定向，返回最终落地页 URL（纯净 URL）。
    例如 v.douyin.com/xxx → https://www.douyin.com/video/xxx
    """
    try:
        resp = requests.get(
            url,
            allow_redirects=True,
            stream=True,
            timeout=timeout,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    "Version/16.0 Mobile/15E148 Safari/604.1"
                )
            },
        )
        final_url = resp.url
        resp.close()
        if final_url != url:
            logger.info("URL 重定向: %s → %s", url, final_url)
        return final_url
    except requests.exceptions.Timeout:
        logger.warning("URL 重定向解析超时，使用原始 URL: %s", url)
        return url
    except requests.exceptions.RequestException as e:
        logger.warning("URL 重定向解析失败: %s，使用原始 URL", e)
        return url


def extract_wenan(url: str) -> dict:
    """
    文案提取入口：
    1. 清洗 URL（跟随短链接重定向）
    2. 从数据库读取 dsuid / dskey（复用 video_parse 模块配置）
    3. 调用 zhuceka wenan API
    4. 清洗返回值（去除 api 字段）

    :param url: 前端传入的 URL（分享链接或纯净链接）
    :return: {"code": 200, "msg": "提取成功", "data": {"text": "..."}}
    """
    if not url or not url.strip():
        return {"code": -1, "msg": "链接不能为空"}

    url = url.strip()

    # 1. 清洗 URL
    clean_url = _resolve_clean_url(url)

    # 2. 读取数据库凭证
    dsuid = get_config_value("video_parse", "dsuid")
    dskey = get_config_value("video_parse", "dskey")
    if not dsuid or not dskey:
        logger.warning("zhuceka dsuid/dskey 未配置")
        return {"code": -1, "msg": "服务配置异常，请联系管理员"}

    # 3. 调用 zhuceka API
    params = {
        "type": "wenan",
        "uid": dsuid,
        "key": dskey,
        "url": clean_url,
    }

    try:
        response = requests.get(ZHUCEKA_API, params=params, timeout=20)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.Timeout:
        logger.error("zhuceka 文案提取超时: %s", clean_url)
        return {"code": -1, "msg": "文案提取超时，请重试"}
    except requests.exceptions.RequestException as e:
        logger.error("zhuceka 文案提取请求异常: %s", e)
        return {"code": -1, "msg": f"请求失败: {e}"}
    except Exception as e:
        logger.error("zhuceka 文案提取未知异常: %s", e)
        return {"code": -1, "msg": f"系统异常: {e}"}

    # 4. 清洗返回值
    code = result.get("code", -1)
    msg = result.get("msg", "")
    data = result.get("data", {})

    if code != 200:
        logger.warning("zhuceka 文案提取失败: %s", msg)
        return {"code": -1, "msg": msg or "提取失败"}

    text = data.get("text", "") if isinstance(data, dict) else ""
    logger.info("zhuceka 文案提取成功，字数: %d", len(text))

    return {
        "code": 200,
        "msg": msg or "提取成功",
        "data": {"text": text},
    }
