from typing import Optional

from fastapi import APIRouter
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query

from common import Dao
from model.schema import TSetting, TGroupsir, TUser
from dao import d_groupsir
from model.m_schema import CreateGroupsir

Base = declarative_base()
metadata = Base.metadata

router = APIRouter()


@router.post(f'/create_groupsir')
async def create_groupsir(item: CreateGroupsir):
    """
    提交字段：user_id（用户id，T_user表id）、parent_id(值为0表示团长，大于0表示团长下成员)、notes（对团成员的备注信息）
    """
    re = {'status': 200, 'detail': 'add access'}
    insert_tgroupsir = TGroupsir(
        user_id=item.user_id,
        parent_id=item.parent_id,
        notes=item.notes
    )
    re['detail'] = d_groupsir.insert_gorupsir(insert_tgroupsir)
    return re

@router.post(f'/get_groupsir')
async def get_groupsir(items: d_groupsir.SearchGroupsir):
    if items.group_id:
        return d_groupsir.get_groupsir(items.group_id)
    else:
        return d_groupsir.search_groupsir(items)

@router.post(f'/is_groupsir')
async def get_groupsir_for_user(user_id:int = 0):
    """
    status的值：'0: 启用,   1: 暂停,  -1：出团或解散', -2: 不不存在。
    is_groupsir的值：0表示团长，大于0表示当前会员的团长id，-2表示不存在
    """
    re = {"is_groupsir": -2, "status": -2}
    if user_id > 0:
        groupsir = d_groupsir.get_member_for_user(user_id)
        if groupsir:
            re['status'] = groupsir.status
            re['is_groupsir'] = groupsir.parent_id
    return re

@router.post(f'/update_groupsir_status')
async def update_groupsir_status(user_id:int = 0, status:int = 0):
    """
    user_id,是会员id不是团长id；status，'0: 启用,   1: 暂停,  -1：出团或解散'
    """
    re = {'status': 200, 'detail': 'update access'}
    if user_id > 0:
        d_groupsir.update_groupsir_status(user_id, status)
    return re

@router.post(f'/update_empower')
async def update_empower(user_id:int = 0, status:int = 0):
    """
    user_id,是会员id不是团长id； status:'0: 未授权   1:已授权（可以使用所有商品秒杀包）'
    """
    re = {'status': 200, 'detail': 'update access'}
    if user_id > 0:
        re['detail'] = d_groupsir.update_groupsir_empower(user_id, status)
    return re


