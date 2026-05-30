from fastapi import APIRouter, HTTPException, Body
from sqlalchemy.engine import Row
from sqlalchemy import or_, func
from model.task import m_task
from dao.task import d_task
from common import global_define
from dao import d_order, d_db, d_user


router = APIRouter()

@router.get('/get_taskclockup')
async def get_taskclockup(task_id:int = -1, taskuser_id:int = -1, user_id:int = -1):
    """
    获取某用户、某任务的打卡和链接列表,
    task_id, 任务id
    taskuser_id, 素材ID
    user_id, 用户id
    """
    re_val = {"code": 0, "data": "", "total":0}
    if task_id < 1 or taskuser_id < 0:
        raise HTTPException(status_code=400, detail="非法数据")
    res = d_task.find_taskclockup(taskuser_id, user_id)
    return res

@router.get('/taskclockup_audit')
async def taskclockup_audit(lp_id:int = -1, audit:int = 0, stat_count:int = 0):
    """
    打卡审核,
    lp_id, 打开id
    audit, 0未审核,1合格,2不合格
    stat_count,播放量
    """
    if lp_id < 1:
        raise HTTPException(status_code=400, detail="非法数据")
    d_task.taskclockup_audit(lp_id, audit, stat_count)
    return {"code":200}

@router.get('/audit_reason')
async def audit_reason(lp_id:int = -1, audit:int = 0):
    """
    不合格原因
    """
    return global_define.nopass

@router.get('/audit_reason')
async def audit_reason(lp_id:int = -1, audit:int = 0):
    """
    不合格原因
    """
    return global_define.nopass

@router.post('/upload_clockup')
async def upload_clockup(data: m_task.UserTaskclockup):
    """
    用户打卡,添加和修改
    """
    re_val = {"code": 200, "msg": "保存成功"}
    res = d_task.get_taskuser_for_id_taskid(data.sucai_id, data.task_id)
    if res:
        if data.id > 0:
            d_task.update_clockup(data)
        else:
            d_task.insert_clockup(data)
            d_task.update_taskuser_upload(data.sucai_id)
    else:
        re_val["code"] = 304
        re_val["msg"] = "未找到素材或任务。"
    return re_val

@router.get('/get_taskclock_count')
async def get_taskclock_count(user_id:int, task_id:int = 0,topic_id:int = 0,taskuser_id:int = 0, status:int = -1):
    """
    获取打卡统计数据。
    user_id: 用户id，必填;
    task_id：任务id，可不设置;
    topic_id：话题id，可不设置;
    taskuser_id：素材id，可不设置;
    status：打卡审核状态，默认0
    """
    user_info = d_user.get_user_by_id(user_id)
    if not user_info:
        raise HTTPException(status_code=400, detail="非法用户")
    re_val = {"code":200, "data":0}
    re_val['data'] = d_task.get_taskclock_count_touser(user_id, task_id, topic_id, taskuser_id, status)
    return re_val