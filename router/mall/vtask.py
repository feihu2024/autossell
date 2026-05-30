from dao import d_db, d_query, d_user, d_video_task
from model.m_schema import *
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Request
from .user import verify_token

# router = APIRouter()
router = APIRouter(dependencies=[Depends(verify_token)])


@router.get(f"/get/list/all", summary="获取所有视频任务列表")
async def get_list(request: Request, page:int=1):
    """
        t_coin
    """
    page = page
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "video_task",
        "selects": ["video_task"],
        "filters": [
            {
                "field": "video_task.stat",
                "op": "in",
                "value": [2, 1, 0]
            }
        ],
        "order_by": [{"field": "video_task.stat", "order": "asc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res

@router.get(f"/get/list/nostart", summary="获取未开启视频任务列表")
async def get_list_nostart(request: Request, page:int=1):
    """
        t_coin
    """
    page = page
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "video_task",
        "selects": ["video_task"],
        "filters": [
            {
                "field": "video_task.stat",
                "value": 0
            }
        ],
        "order_by": [{"field": "video_task.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res

@router.get(f"/get/list/start", summary="获取进行中视频任务列表")
async def get_list_start(request: Request, page:int=1):
    """
        t_coin
    """
    page = page
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "video_task",
        "selects": ["video_task"],
        "filters": [
            {
                "field": "video_task.stat",
                "value": 1
            }
        ],
        "order_by": [{"field": "video_task.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res

@router.get(f"/get/list/over", summary="获取已结束视频任务列表")
async def get_list_over(request: Request, page:int=1):
    """
        t_coin
    """
    page = page
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "video_task",
        "selects": ["video_task"],
        "filters": [
            {
                "field": "video_task.stat",
                "value": 1
            }
        ],
        "order_by": [{"field": "video_task.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res


@router.get(f"/get/list/receive", summary="获取用户全部领取的任务列表")
async def get_list_receive(request: Request, page:int=1):
    """
        t_coin
    """
    page = page
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "video_task_receive",
        "joins": [
            {
                "table": "video_task",
                "on_left": "task_id",
                "on_right": "id"
            }
        ],
        "selects": ["video_task_receive"],
        "filters": [
            {
                "field": "video_task_receive.user_id",
                "value": user_id
            }
        ],
        "order_by": [{"field": "video_task_receive.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res


@router.get(f"/get/list/receive/audit/one", summary="获取用户领取未审核的任务列表")
async def get_list_receive_audit_one(request: Request, page:int=1):
    """
        t_coin
    """
    page = page
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "video_task_receive",
        "joins": [
            {
                "table": "video_task",
                "on_left": "task_id",
                "on_right": "id"
            }
        ],
        "selects": ["video_task_receive"],
        "filters": [
            {
                "field": "video_task_receive.user_id",
                "value": user_id
            },
            {
                "field": "video_task_receive.audit_status",
                "value": 0
            }
        ],
        "order_by": [{"field": "video_task_receive.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res

@router.get(f"/get/data/stat", summary="获取达人/店主/服务商视频码的统计数据")
async def get_data_stat(request: Request, level:int = 0):
    """
        t_coin
    """
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    res = d_video_task.get_vrecharge_stat_data(level, user_id)
    return res

@router.get(f"/get/task/info", summary="获取视频任务详情")
async def get_task_info(request: Request, vtask_id:int = 0):
    """
        t_coin
    """
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if vtask_id <= 0:
        return '数据错误'
    res = d_video_task.get_vtask_by_id(vtask_id)
    return res

@router.get(f"/get/task/down/list", summary="获取任务素材下载列表,返回20条以内")
async def get_task_down_list(request: Request, task_id:int = -1, m_type:int = 0):
    """
        t_coin
        素材类型,0图片1视频2音频
    """
    page = 1
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)

    if task_id < 1:
        return '数据错误'

    task_info = d_video_task.get_vtask_by_id(task_id)
    if not task_info:
        return '未知任务'

    if task_info.received > task_info.top:
        return '此任务已达到上限，领取失败！'

    today_total = d_video_task.get_mater_count_to_today(user_id, task_id)
    if task_info.day_top <= today_total:
        return '今日任务已达到上限，领取失败！'

    m_type = task_info.type_id
    if m_type == 1:
        page_size = task_info.video_num
    if m_type == 0:
        page_size = task_info.pic_num

    # res = d_video_task.get_video_task_down_list(task_info.finish_id, task_info.type_id, page_size)

    query_data = d_query.FilterQueryData.parse_obj({
        "table": "video_task_material",
        "selects": ["video_task_material"],
        "filters": [
            {
                "field": "video_task_material.bag_id",
                "value": task_info.finish_id
            },
            {
                "field": "video_task_material.is_del",
                "value": 0
            },
            {
                "field": "video_task_material.m_type",
                "value": m_type
            },
            {
                "field": "video_task_material.is_download",
                "value": 0
            }
        ],
        "order_by": [{"field": "video_task_material.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    if res['data']:
        for row_data in res['data']:
            insert_data = d_video_task.MateDownLoadModel(
                mate_id=row_data.id,
                task_id=task_id,
                user_id=user_id
            )
            d_video_task.update_get_task_material(insert_data)
    return res

@router.get(f"/rece/task", summary="领取视频任务，需要下载素材完毕后调用该接口")
async def rece_task_info(request: Request, vtask_id:int = 0):
    """
        t_coin
    """
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if vtask_id <= 0:
        return '数据错误'
    res = d_video_task.get_vtask_by_id(vtask_id)
    if not res:
        return '未知任务'
    if res.received is None:
        res.received = 0
    if res.top is None:
        res.top = 0
    if res.received > res.top:
        return '此任务已达到上限，领取失败！'
    u_info = d_user.get_user_by_id(user_id)
    if not u_info:
        return '未知用户'
    #领取任务
    insert_datat = CreateVideoTaskReceive(task_id=res.id,\
                                          shoper_id=res.shoper_id,\
                                          shoper_name=res.shoper_name,\
                                          shoper_phone=res.shoper_phone, \
                                          user_id=user_id, \
                                          user_name=u_info.nickname, \
                                          user_phone=u_info.phone, \
                                          title=res.title, \
                                          bag_id=res.finish_id)
    base_info = d_db.insert_video_task_receive(insert_datat)
    #领取量加1
    add_num = res.received + 1
    d_video_task.task_recharge_add(vtask_id, add_num)
    return base_info


@router.get(f"/rece/check/task", summary="领取视频任务，合成视频验证")
async def rece_task_check_info(request: Request, vtask_id:int = 0):
    """
        t_coin
    """
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if vtask_id <= 0:
        return '数据错误'
    res = d_video_task.get_vtask_by_id(vtask_id)
    if not res:
        return '未知任务'
    if res.received is None:
        res.received = 0
    if res.top is None:
        res.top = 0
    if res.received > res.top:
        return '此任务已达到上限，领取失败！'
    u_info = d_user.get_user_by_id(user_id)
    if not u_info:
        return '未知用户'

    return 'success'

@router.post(f'/rece/pic', summary="用户回传任务图片")
async def rece_task_pic(request: Request, item: d_video_task.PicModel):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    task_info = d_video_task.get_receive_by_id(item.receive_id)
    if not task_info:
        return '未知用户'
    if task_info.user_id == user_id:
        d_video_task.update_uppic(item)
        return 'success'
    else:
        return '非法权限'


@router.get(f"/get/video/recharge/info/code", summary="通过激活码获取充值码详情")
async def get_video_recharge_info_code(request: Request, code:str = ""):
    """
        recharge_id
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if code == "":
        return '数据错误'
    res = d_video_task.get_recharge_by_code(code)
    return res

@router.get(f"/get/video/article", summary="获取视频文章列表")
async def get_video_article(request: Request, cid:int = 0, page:int = 1, searchtitle:str = None, searchlabel:str = None, searchany:str = None):
    """
        recharge_id
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    res = d_video_task.get_video_arc_list(cid, page, searchtitle, searchlabel, searchany)
    return res

@router.get(f"/get/video/article/content", summary="获取视频文章详情")
async def get_video_article_content(request: Request, aid:int):
    """
        recharge_id
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    res = d_video_task.get_video_article(aid)
    return res

@router.get(f"/get/video/article/type", summary="获取视频文章分类列表")
async def get_video_article_type(request: Request):
    """
        recharge_id
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    res = d_video_task.get_video_article_class()
    return res

@router.get(f"/get/video/article/list/filter", summary="获取视频文章模块列表")
async def get_video_article_list_filter(request: Request,art_id:int, page:int=1):
    """
        art_id, 视频文章id
    """
    page = page
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "video_article_list",
        "selects": ["video_article_list"],
        "filters": [
            {
                "field": "video_article_list.article_id",
                "value": art_id
            },
            {
                "field": "video_article_list.is_del",
                "value": 0
            }
        ],
        "order_by": [{"field": "video_article_list.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res
