from fastapi import APIRouter, HTTPException, Body
from sqlalchemy.engine import Row
from sqlalchemy import or_, func
from common import global_define as gg
from service import qiniu_service
from dao.task import d_task
from model.task import m_task

router = APIRouter()

@router.get('/link_stat', summary="链接处理状态")
async def link_stat():
    return gg.link_stat

@router.get('/qiniu_token', summary="获取七牛上传Token")
async def qiniu_token(filename: str, type: str = 'sucai', task_id:int = 0):
    """
    参数：
    filename，上传文件名，如果abcdef.jpg
    type，上传类型，默认值“sucai”表示素材文件上传，“fengmian”表示封面图，"tuyang“表示图样上传，“daka”表示打卡图上传,“qita”表示其他类型上传
    task_id, 所属任务id
    返回值：
    code：  200表示正常，304表示filename上传重复,305任务不存在,404表示发生错误
    """
    re_val = {"code": 200, "id": 1, "fname": filename, "token": "123456"}
    if type == "sucai":
        get_sucai = d_task.get_taskuser_for_filename(filename, 0, task_id)
        if get_sucai:
            re_val['code'] = 304
            re_val['id'] = 0
            re_val['token'] = ''
        else:
            if d_task.get_task_for_id(task_id):
                save_data = d_task.insert_taskuser_for_filename(filename, task_id)
                token = qiniu_service.get_upload_token(filename)
                re_val["token"] = token
                re_val['id'] = save_data.id
            else:
                re_val['code'] = 305
                re_val['id'] = 0
                re_val['token'] = ''
    else:
        token = qiniu_service.get_upload_token(filename)
        re_val["token"] = token
        re_val['id'] = 0

    return re_val


@router.get('/qiniu_httpurl', summary="获取七牛访问url")
async def qiniu_httpurl(httpurl: str):
    """
    七牛资源下载
    :httpurl: 如：http://task.yxiaozhu.com/5f59dace081de.jpg
    :return: http://task.yxiaozhu.com/5f59dace081de.jpg?e=1719126477&token=Mply7-4INH5tRfYBrYc8MTT-l2_0xhwUhXI4R7_i:BgAmqkA7x8MxR9mUULxq0-_RDzQ=
    """
    return qiniu_service.get_download_url(httpurl)

@router.post('/topic_name_sv')
async def topic_name_sv(data: m_task.SaveTopic):
    """
    更新任务主题
    """
    res = d_task.get_topic_for_id_taskid(data.tp_id, data.task_id)
    if not res:
        raise HTTPException(status_code=400, detail="非法数据")
    d_task.update_topic_name(data.tp_id, data.topic_name)
    return {"code":200}

@router.post('/topic_comment_sv')
async def topic_comment_sv(data: m_task.SaveTopic):
    """
    更新任务主题评论
    """
    res = d_task.get_topic_for_id_taskid(data.tp_id, data.task_id)
    if not res:
        raise HTTPException(status_code=400, detail="非法数据")
    d_task.update_topic_comment(data.tp_id, data.topic_comment)
    return {"code":200}

@router.get('/get_task_for_user')
async def get_task_for_user(user_id: int):
    """
    获取某个用户的任务列表
    """
    re_val = {"code":200, "data":""}
    task_list = d_task.get_taskid_foruser(user_id)
    if task_list:
        res = d_task.get_task_forid(task_list)
        re_val['data'] = res
    return re_val
    #return {"code":200}

@router.get('/get_task_not_user')
async def get_task_not_user(user_id: int):
    """
    获取不是某个用户的任务列表
    """
    re_val = {"code":200, "data":""}
    task_list = d_task.get_taskid_foruser(user_id)
    if task_list:
        res = d_task.get_task_forid(task_list, 0)
        re_val['data'] = res
    return re_val
    #return {"code":200}

@router.get('/get_task_stat')
async def get_task_stat(task_id: int):
    """
    任务打卡信息统计
    总数、链接上传数、链接审核数、打卡条数、打卡审核数、合格数、未审核数
    """
    re_val = d_task.get_task_stat(task_id)
    return re_val
    #return {"code":200}

@router.get('/get_pub_plat')
async def get_pub_plat():
    """
    打卡平台列表
    """
    re_val = gg.pub_platform
    return re_val
    #return {"code":200}

@router.get('/get_task_statcount')
async def get_task_statcount(task_id: int, taskuser_id:int, user_id:int):
    """
    任务打卡信息统计,各平台流量统计
    task_id,任务id
    taskuser_id,素材id
    user_id,用户id
    """
    re_val = d_task.get_task_statcount(task_id, taskuser_id, user_id)
    return re_val

@router.get('/taskuser_dwonload')
async def taskuser_dwonload(ts_id:int):
    """
    素材下载次数累计
    """
    re_val = {"code":200, "data":0}
    re_val['data'] = d_task.taskuser_download_count_add(ts_id)
    return re_val