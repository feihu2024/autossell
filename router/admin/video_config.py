from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from dao.d_video_config import get_config_by_module, batch_update_config

router = APIRouter()


class ConfigItem(BaseModel):
    config_key: str
    config_value: Optional[str] = ""


class BatchUpdateRequest(BaseModel):
    module: str  # video_parse / ai_image / video_to_prompt
    configs: list  # [{"config_key": "token", "config_value": "xxx"}, ...]


@router.get("/{module}")
def get_module_config(module: str):
    """
    查询指定模块的全部配置

    路径参数:
        module: 模块名 video_parse / ai_image / video_to_prompt
    """
    config = get_config_by_module(module)
    if not config:
        return {"code": -1, "msg": f"未找到模块 {module} 的配置"}
    return {"code": 200, "data": config}


@router.put("/")
def update_module_config(req: BatchUpdateRequest):
    """
    批量修改指定模块的配置项

    请求体:
        module: 模块名
        configs: 要修改的配置列表，每项包含 config_key 和 config_value
    """
    if not req.module:
        return {"code": -1, "msg": "模块名不能为空"}

    if not req.configs:
        return {"code": -1, "msg": "配置列表不能为空"}

    # 将列表转为字典
    config_dict = {}
    for item in req.configs:
        if isinstance(item, dict):
            config_dict[item.get("config_key")] = item.get("config_value", "")
        else:
            config_dict[item.config_key] = item.config_value

    batch_update_config(req.module, config_dict)

    # 返回更新后的最新配置
    updated = get_config_by_module(req.module)
    return {"code": 200, "msg": "配置更新成功", "data": updated}
