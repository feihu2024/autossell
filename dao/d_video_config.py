from common import Dao
from model.schema import TVideoConfig


def get_config_by_module(module: str) -> dict:
    """
    查询指定模块的全部配置，返回 {config_key: config_value} 字典

    :param module: 模块名，如 video_parse / ai_image / video_to_prompt
    :return: 配置字典，查询不到返回空字典
    """
    with Dao() as db:
        rows = db.query(TVideoConfig).filter(TVideoConfig.module == module).all()
        return {row.config_key: row.config_value for row in rows}


def get_config_value(module: str, config_key: str):
    """
    查询指定模块下某个配置的值

    :param module: 模块名
    :param config_key: 配置键
    :return: 配置值字符串，不存在返回 None
    """
    with Dao() as db:
        row = db.query(TVideoConfig).filter(
            TVideoConfig.module == module,
            TVideoConfig.config_key == config_key
        ).first()
        return row.config_value if row else None


def update_config(module: str, config_key: str, config_value: str) -> bool:
    """
    更新指定模块下某个配置的值

    :param module: 模块名
    :param config_key: 配置键
    :param config_value: 新的配置值
    :return: 是否更新成功
    """
    with Dao() as db:
        row = db.query(TVideoConfig).filter(
            TVideoConfig.module == module,
            TVideoConfig.config_key == config_key
        ).first()
        if row:
            row.config_value = config_value
            db.commit()
            return True
        return False


def batch_update_config(module: str, configs: dict) -> bool:
    """
    批量更新指定模块的配置

    :param module: 模块名
    :param configs: {config_key: config_value} 字典
    :return: 是否全部更新成功
    """
    with Dao() as db:
        rows = db.query(TVideoConfig).filter(TVideoConfig.module == module).all()
        updated = 0
        for row in rows:
            if row.config_key in configs:
                row.config_value = configs[row.config_key]
                updated += 1
        if updated > 0:
            db.commit()
        return True
