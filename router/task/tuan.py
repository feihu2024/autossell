from fastapi import APIRouter, HTTPException, Body, Depends, Request
from sqlalchemy.engine import Row
from sqlalchemy import or_, func
from common import global_define as gg
from service import qiniu_service
from dao.task import d_task
from dao import d_user, d_groupsir
from model.task import m_task
from router.admin.user import verify_token

router = APIRouter(dependencies=[Depends(verify_token)])
# router = APIRouter()

@router.post('/add_sir')
async def add_sir(data: m_task.GroupSir):
    """
    添加和创建团长
    """
    user_info = d_user.get_user_by_id(data.user_id)
    if not user_info:
        raise HTTPException(status_code=400, detail="未找到用户")
    #设置团长身份
    if data.is_group > 0:
        d_task.update_is_groupsir(data.user_id, data.is_group, data.username, data.phone, data.email)
        # 更新入团日志
        d_task.add_groupuser_log(data.user_id, user_info.tuan_id, 0, gg.groupsir_type[3])
        #将被推荐的人，归属到新团长之下
        d_groupsir.update_groupsir_create_addmembers(data.user_id)

    if data.group_id > 0:
        tuan_info = d_user.get_user_by_id(data.group_id)
        if not tuan_info:
            raise HTTPException(status_code=400, detail="未找到团长信息")
        d_task.update_is_groupuser(data.user_id, data.group_id)
        # 更新入团日志
        d_task.add_groupuser_log(data.user_id, data.group_id, 0, gg.groupsir_type[1])

    return {"code": 200, "msg":"创建成功"}

@router.get('/testsir')
async def testsir(userid:int):
    # return d_user.get_invited_user_for_list(userid)
    return d_groupsir.update_groupsir_create_addmembers_test(userid)

@router.post('/del_sir')
async def del_sir(data: m_task.GroupSir):
    """
       取消团长身份
    """
    user_info = d_user.get_user_by_id(data.user_id)
    if not user_info:
        raise HTTPException(status_code=400, detail="未找到用户")
    if user_info.is_tuan <= 0:
        raise HTTPException(status_code=400, detail="非团长")
    d_task.update_is_groupuser(data.user_id, 0)
    member_ids = d_user.get_tuan_ids(data.user_id)
    #return member_ids
    update_id = user_info.tuan_id if user_info.tuan_id is not None else 0
    d_groupsir.update_groupsir_create_addmembers_run(member_ids, update_id)
    # 更新入团日志
    d_task.add_groupuser_log(data.user_id, 0, 0, gg.groupsir_type[4])
    return {"code": 200, "msg": "已取消"}

@router.post('/add_user_tosir')
async def add_user_tosir(data: m_task.GroupSir):
    """
       添加、转移团成员
    """
    user_info = d_user.get_user_by_id(data.user_id)
    sir_info = d_user.get_user_by_id(data.group_id)
    if not user_info or not sir_info:
        raise HTTPException(status_code=400, detail="未找到用户或团长")
    if user_info.tuan_id == data.group_id:
        raise HTTPException(status_code=400, detail=f"{data.user_id}已经是团员")
    if sir_info.is_tuan <= 0:
        raise HTTPException(status_code=400, detail=f"非团长{data.group_id}")
    #如果目标团长是自己的团员，则取消自己成员身份
    if sir_info.tuan_id == data.user_id:
        d_task.add_change_groupuser(data.group_id)
    d_task.add_change_groupuser(data.user_id, data.group_id)
    # 更新入团日志
    d_task.add_groupuser_log(data.user_id, data.group_id, 0, gg.groupsir_type[5])
    return {"code": 200, "msg": f"{data.user_id}已转移至{data.group_id}"}

@router.get('/get_groupsir_level')
async def get_groupsir_level():
    """
       获取团长级别列表
    """
    return gg.groupsir_level

@router.get('/get_blacklist')
async def get_blacklist():
    """
       获取黑名单列表
    """
    return gg.ts_blacklist

@router.get('/get_groupsir_stat')
async def get_blacklist(userid:int):
    """
       获取团长成员统计
    """
    re_stat = {'members': 0, 'gsirs': 0}
    re_stat['members'] = d_groupsir.get_members_count(userid)
    re_stat['gsirs'] = d_groupsir.get_gsir_count(userid)
    return re_stat

@router.post('/add_shengdai')
async def add_sir(data: m_task.ShengDai):
    """
    创建、取消省代
    """
    user_info = d_user.get_user_by_id(data.user_id)
    if not user_info:
        raise HTTPException(status_code=400, detail="未找到用户")
    #设置省代身份
    d_task.update_shengdai(data.user_id, data.level_shengdai)
    return {"code": 200, "msg":"设置成功"}