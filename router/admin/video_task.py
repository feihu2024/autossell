from dao import d_db, d_user, d_account, d_found, d_video_task, d_balance, d_good
from fastapi import APIRouter, Depends, Header, Request
from model.m_schema import *
from typing import Optional, List
from router import r_schema
from router.admin.user import verify_token
from common import global_define, global_function
from fastapi import HTTPException
from pydantic import BaseModel, Field
import re, math, time
from model.mall import m_account

router = APIRouter(dependencies=[Depends(verify_token)])
#
# class CreateBagPas_w(BaseModel):
#     # pass_num: Optional[str] = Field(title='加密编号(十六进制)')
#     # pc_name: Optional[str] = Field(title='批次名称')
#     pc_num: Optional[int] = Field(title='批次数量')
#     pc_id: Optional[int] = Field(title='批次id(不可重复)')
#     # stat: Optional[int] = Field(title='是否激活,默认0未激活1已激活2过期未用')
#     # register_time: Optional[datetime] = Field(title='创建时间')
#     # startime: Optional[datetime] = Field(title='激活时间')
#     # user_id: Optional[int] = Field(title='激活会员id')
#     endtime: Optional[datetime] = Field(title='结束时间')
#     # cate_id: Optional[int] = Field(title='批次分类id')
#
# class CreateBagCagegory_w(BaseModel):
#     pc_name: Optional[str] = Field(title='批次名称')
#     pc_num: Optional[int] = Field(title='批次数量')
#     endtime: Optional[datetime] = Field(title='结束时间')
#     bag_id: Optional[int] = Field(title='礼包id')
#
class VideoActiveLabel(BaseModel):
    add_label: Optional[str] = Field(title='标签文本，以逗号分割')
    video_id: Optional[int] = Field(title='视频文章id')

@router.get(f'/vtask/pub_platform', summary="获取发布平台列表")
async def get_pub_platform():
    return global_define.pub_platform

@router.get(f'/vtask/video_level', summary="获取视频分发身份列表")
async def get_video_level():
    return global_define.video_level

@router.post(f'/vtask_type/create', response_model=SVideoTaskType, summary="创建视频任务分类")
async def create_video_task_type(item: CreateVideoTaskType) -> SVideoTaskType:
    dict_item = dict(item)
    for k,v in dict_item.items():
        if v is not None:
            v = str(v)
            v = v.replace(" ", "")
            get_search = re.search(r"'", v, flags=0)
            get_search2 = re.search(r'%27', v, flags=0)
            get_search3 = re.search(r'unionselect', v, flags=0)
            if get_search or get_search2 or get_search3:
               raise HTTPException(status_code=404, detail='bad way~~~~~~')

    return d_db.insert_video_task_type(item)

@router.post(f'/vtask_type/update', response_model=str, summary="修改视频任务分类")
async def update_video_task_type(item: SVideoTaskType) -> str:
    d_db.update_video_task_type(item)
    return "success"

@router.get(f'/vtask_type/get', response_model=SVideoTaskType, summary="获取任务分类详情")
async def get_video_task_type(video_task_type_id: int) -> SVideoTaskType:
    return d_db.get_video_task_type(video_task_type_id)


@router.post(f'/vtask/create', response_model=SVideoTask, summary="创建视频任务")
async def create_video_task(item: CreateVideoTask) -> SVideoTask:
    dict_item = dict(item)
    for k,v in dict_item.items():
        if v is not None:
            v = str(v)
            v = v.replace(" ", "")
            get_search = re.search(r"'", v, flags=0)
            get_search2 = re.search(r'%27', v, flags=0)
            get_search3 = re.search(r'unionselect', v, flags=0)
            if get_search or get_search2 or get_search3:
               raise HTTPException(status_code=404, detail='bad way~~~~~~')
    if hasattr(item, 'audit'):
        del item.audit
    if hasattr(item, 'stat'):
        del item.stat
    if hasattr(item, 'audit_time'):
        del item.audit_time
    return d_db.insert_video_task(item)

@router.post(f'/vtask/update', response_model=str, summary="修改视频任务")
async def update_video_task(item: SVideoTask) -> str:
    if hasattr(item, 'audit'):
        del item.audit
    if hasattr(item, 'stat'):
        del item.stat
    if hasattr(item, 'audit_time'):
        del item.audit_time
    d_db.update_video_task(item)
    return "success"

@router.get(f'/vtask/get', response_model=SVideoTask, summary="获取视频任务详情")
async def get_video_task(video_task_id: int) -> SVideoTask:
    return d_db.get_video_task(video_task_id)

@router.get(f'/vtask_receive/get', response_model=SVideoTaskReceive, summary="获取用户领取视频任务详情")
async def get_video_task_receive(video_task_receive_id: int) -> SVideoTaskReceive:
    return d_db.get_video_task_receive(video_task_receive_id)

class this_createVideoRecharge(BaseModel):
    good_id: Optional[int] = Field(title='礼包商品id')
    good_name: Optional[str] = Field(title='礼包名称')
    admin_name: Optional[str] = Field(title='操作员名字')
    user_id: Optional[int] = Field(title='码主id')
    user_phone: Optional[str] = Field(title='码主电话')
    user_name: Optional[str] = Field(title='码主用户昵称')
    video_level: Optional[int] = Field(title='视频分发身份0达人,1店长,2服务商,3分公司')
    # level_id: Optional[int] = Field(title='用户等级 默认是0粉丝,1会员,2核心会员')
    create_nmu: Optional[int] = Field(title='本次生成总数')
    # act_user_id: Optional[int] = Field(title='激活用户id')
    # act_user_phone: Optional[str] = Field(title='激活用户电话')
    # act_user_name: Optional[str] = Field(title='激活指定用户昵称')
    # act_time: Optional[datetime] = Field(title='激活时间')
    # is_act: Optional[int] = Field(title='是否被激活,0未激活,1已激活')
    act_code: Optional[str] = Field(title='激活码')
    batch_code: Optional[str] = Field(title='创建批次码')

@router.post(f'/vrecharge/create', summary="生成视频分发条数充值码，支持多项")
async def create_video_recharge(item: this_createVideoRecharge) -> SVideoRecharge:
    dict_item = dict(item)
    for k,v in dict_item.items():
        if v is not None:
            v = str(v)
            v = v.replace(" ", "")
            get_search = re.search(r"'", v, flags=0)
            get_search2 = re.search(r'%27', v, flags=0)
            get_search3 = re.search(r'unionselect', v, flags=0)
            if get_search or get_search2 or get_search3:
               raise HTTPException(status_code=404, detail='bad way~~~~~~')
    batch_code = global_function.get_num32_randoms()
    good_info = d_good.get_good_data(item.good_id)
    if good_info:
        item.video_level = good_info.video_level
        for i in range(0, item.create_nmu):
            item.act_code = global_function.get_randoms(21)
            item.batch_code = batch_code
            d_db.insert_video_recharge(item)
            time.sleep(0.4)
    else:
        return "未知商品礼包"

    return "success"

@router.get(f'/vrecharge/get', response_model=SVideoRecharge, summary="获取视频分发条数充值码详情")
async def get_video_recharge(video_recharge_id: int) -> SVideoRecharge:
    return d_db.get_video_recharge(video_recharge_id)



@router.get(f'/vtask_type/get_filter', response_model=FilterResVideoTaskType, summary="获取任务分类检索列表")
async def filter_video_task_type(
        id: Optional[str] = None,
        title: Optional[str] = None,
        describe: Optional[str] = None,
        cover: Optional[str] = None,
        l_id: Optional[str] = None,
        s_title: Optional[str] = None,
        s_describe: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResVideoTaskType:
    """
    1. 按照字段查询`?field1=value1&field2=value2`
    2. 按照范围查询，大于某个值`?field=value,`, 表示filed大于value
    3. 按照范围查询，小于某个值`?field=,value`， 表示field小于value
    4. 按照范围查询，范围值`?field=value1,value2`，表示搜索field大于等于value1，小于等于value2
    5. page是页数，第一页为1
    6. page_size为每一页大小， 默认20
    7. 如果是日期，请使用时间戳，十位的时间戳，单位：秒
    8. 所有字符串字段均可搜索，需要在字段前加个前缀`s_`,例如搜索`username`包含`zhang`， 则可以这样`s_username=zhang`写,这里只是一个假设
    9. 字段的多选择（in关系），需要在字段前加前缀`l_`,并且以逗号`,`隔开,例如要找出`id=2`或者`id=3`的样本，可以这样写`?l_id=2,3`
    """

    items = dict()
    search_items = dict()
    set_items = dict()

    if id is not None:
        values = id.split(',')
        if len(values) == 1:
            val = values[0]
            items['id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['id_start'] = int(val)

            val = values[1]
            if val != '':
                items['id_end'] = int(val)

    if title is not None:
        values = title.split(',')
        if len(values) == 1:
            val = values[0]
            items['title'] = val
        else:
            val = values[0]
            if val != '':
                items['title_start'] = val

            val = values[1]
            if val != '':
                items['title_end'] = val

    if describe is not None:
        values = describe.split(',')
        if len(values) == 1:
            val = values[0]
            items['describe'] = val
        else:
            val = values[0]
            if val != '':
                items['describe_start'] = val

            val = values[1]
            if val != '':
                items['describe_end'] = val

    if cover is not None:
        values = cover.split(',')
        if len(values) == 1:
            val = values[0]
            items['cover'] = val
        else:
            val = values[0]
            if val != '':
                items['cover_start'] = val

            val = values[1]
            if val != '':
                items['cover_end'] = val

    if s_title is not None:
        search_items['title'] = '%' + s_title + '%'

    if s_describe is not None:
        search_items['describe'] = '%' + s_describe + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_video_task_type(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_video_task_type(items, search_items, set_items)

    return FilterResVideoTaskType(data=data, total=c)

@router.get(f'/vtask/get_filter', response_model=FilterResVideoTask, summary="检索视频任务列表")
async def filter_video_task(
        id: Optional[str] = None,
        title: Optional[str] = None,
        describe: Optional[str] = None,
        shoper_id: Optional[str] = None,
        shoper_name: Optional[str] = None,
        shoper_phone: Optional[str] = None,
        stat: Optional[str] = None,
        is_auto: Optional[str] = None,
        cover: Optional[str] = None,
        type_id: Optional[str] = None,
        l_id: Optional[str] = None,
        s_title: Optional[str] = None,
        s_describe: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResVideoTask:
    """
    1. 按照字段查询`?field1=value1&field2=value2`
    2. 按照范围查询，大于某个值`?field=value,`, 表示filed大于value
    3. 按照范围查询，小于某个值`?field=,value`， 表示field小于value
    4. 按照范围查询，范围值`?field=value1,value2`，表示搜索field大于等于value1，小于等于value2
    5. page是页数，第一页为1
    6. page_size为每一页大小， 默认20
    7. 如果是日期，请使用时间戳，十位的时间戳，单位：秒
    8. 所有字符串字段均可搜索，需要在字段前加个前缀`s_`,例如搜索`username`包含`zhang`， 则可以这样`s_username=zhang`写,这里只是一个假设
    9. 字段的多选择（in关系），需要在字段前加前缀`l_`,并且以逗号`,`隔开,例如要找出`id=2`或者`id=3`的样本，可以这样写`?l_id=2,3`
    """

    items = dict()
    search_items = dict()
    set_items = dict()

    if id is not None:
        values = id.split(',')
        if len(values) == 1:
            val = values[0]
            items['id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['id_start'] = int(val)

            val = values[1]
            if val != '':
                items['id_end'] = int(val)

    if title is not None:
        values = title.split(',')
        if len(values) == 1:
            val = values[0]
            items['title'] = val
        else:
            val = values[0]
            if val != '':
                items['title_start'] = val

            val = values[1]
            if val != '':
                items['title_end'] = val

    if describe is not None:
        values = describe.split(',')
        if len(values) == 1:
            val = values[0]
            items['describe'] = val
        else:
            val = values[0]
            if val != '':
                items['describe_start'] = val

            val = values[1]
            if val != '':
                items['describe_end'] = val

    if shoper_id is not None:
        values = shoper_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['shoper_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['shoper_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['shoper_id_end'] = int(val)

    if shoper_name is not None:
        values = shoper_name.split(',')
        if len(values) == 1:
            val = values[0]
            items['shoper_name'] = val
        else:
            val = values[0]
            if val != '':
                items['shoper_name_start'] = val

            val = values[1]
            if val != '':
                items['shoper_name_end'] = val

    if shoper_phone is not None:
        values = shoper_phone.split(',')
        if len(values) == 1:
            val = values[0]
            items['shoper_phone'] = val
        else:
            val = values[0]
            if val != '':
                items['shoper_phone_start'] = val

            val = values[1]
            if val != '':
                items['shoper_phone_end'] = val

    if stat is not None:
        values = stat.split(',')
        if len(values) == 1:
            val = values[0]
            items['stat'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['stat_start'] = int(val)

            val = values[1]
            if val != '':
                items['stat_end'] = int(val)

    if is_auto is not None:
        values = is_auto.split(',')
        if len(values) == 1:
            val = values[0]
            items['is_auto'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['is_auto_start'] = int(val)

            val = values[1]
            if val != '':
                items['is_auto_end'] = int(val)

    if cover is not None:
        values = cover.split(',')
        if len(values) == 1:
            val = values[0]
            items['cover'] = val
        else:
            val = values[0]
            if val != '':
                items['cover_start'] = val

            val = values[1]
            if val != '':
                items['cover_end'] = val

    if type_id is not None:
        values = type_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['type_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['type_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['type_id_end'] = int(val)

    if s_title is not None:
        search_items['title'] = '%' + s_title + '%'

    if s_describe is not None:
        search_items['describe'] = '%' + s_describe + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_video_task(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_video_task(items, search_items, set_items)

    return FilterResVideoTask(data=data, total=c)

@router.get(f'/vrecharge/filter', response_model=FilterResVideoRecharge, summary="获取视频码生成列表")
async def filter_video_recharge(
        id: Optional[str] = None,
        good_id: Optional[str] = None,
        good_name: Optional[str] = None,
        user_id: Optional[str] = None,
        user_phone: Optional[str] = None,
        user_name: Optional[str] = None,
        video_level: Optional[str] = None,
        level_id: Optional[str] = None,
        create_nmu: Optional[str] = None,
        act_user_id: Optional[str] = None,
        act_user_phone: Optional[str] = None,
        act_user_name: Optional[str] = None,
        act_time: Optional[str] = None,
        is_act: Optional[str] = None,
        act_code: Optional[str] = None,
        batch_code: Optional[str] = None,
        l_id: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResVideoRecharge:
    """
    1. 按照字段查询`?field1=value1&field2=value2`
    2. 按照范围查询，大于某个值`?field=value,`, 表示filed大于value
    3. 按照范围查询，小于某个值`?field=,value`， 表示field小于value
    4. 按照范围查询，范围值`?field=value1,value2`，表示搜索field大于等于value1，小于等于value2
    5. page是页数，第一页为1
    6. page_size为每一页大小， 默认20
    7. 如果是日期，请使用时间戳，十位的时间戳，单位：秒
    8. 所有字符串字段均可搜索，需要在字段前加个前缀`s_`,例如搜索`username`包含`zhang`， 则可以这样`s_username=zhang`写,这里只是一个假设
    9. 字段的多选择（in关系），需要在字段前加前缀`l_`,并且以逗号`,`隔开,例如要找出`id=2`或者`id=3`的样本，可以这样写`?l_id=2,3`
    """

    items = dict()
    search_items = dict()
    set_items = dict()

    if id is not None:
        values = id.split(',')
        if len(values) == 1:
            val = values[0]
            items['id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['id_start'] = int(val)

            val = values[1]
            if val != '':
                items['id_end'] = int(val)

    if good_id is not None:
        values = good_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['good_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['good_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['good_id_end'] = int(val)

    if good_name is not None:
        values = good_name.split(',')
        if len(values) == 1:
            val = values[0]
            items['good_name'] = val
        else:
            val = values[0]
            if val != '':
                items['good_name_start'] = val

            val = values[1]
            if val != '':
                items['good_name_end'] = val

    if user_id is not None:
        values = user_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['user_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['user_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['user_id_end'] = int(val)

    if user_phone is not None:
        values = user_phone.split(',')
        if len(values) == 1:
            val = values[0]
            items['user_phone'] = val
        else:
            val = values[0]
            if val != '':
                items['user_phone_start'] = val

            val = values[1]
            if val != '':
                items['user_phone_end'] = val

    if user_name is not None:
        values = user_name.split(',')
        if len(values) == 1:
            val = values[0]
            items['user_name'] = val
        else:
            val = values[0]
            if val != '':
                items['user_name_start'] = val

            val = values[1]
            if val != '':
                items['user_name_end'] = val

    if video_level is not None:
        values = video_level.split(',')
        if len(values) == 1:
            val = values[0]
            items['video_level'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['video_level_start'] = int(val)

            val = values[1]
            if val != '':
                items['video_level_end'] = int(val)

    if level_id is not None:
        values = level_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['level_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['level_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['level_id_end'] = int(val)

    if create_nmu is not None:
        values = create_nmu.split(',')
        if len(values) == 1:
            val = values[0]
            items['create_nmu'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['create_nmu_start'] = int(val)

            val = values[1]
            if val != '':
                items['create_nmu_end'] = int(val)

    if act_user_id is not None:
        values = act_user_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['act_user_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['act_user_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['act_user_id_end'] = int(val)

    if act_user_phone is not None:
        values = act_user_phone.split(',')
        if len(values) == 1:
            val = values[0]
            items['act_user_phone'] = val
        else:
            val = values[0]
            if val != '':
                items['act_user_phone_start'] = val

            val = values[1]
            if val != '':
                items['act_user_phone_end'] = val

    if act_user_name is not None:
        values = act_user_name.split(',')
        if len(values) == 1:
            val = values[0]
            items['act_user_name'] = val
        else:
            val = values[0]
            if val != '':
                items['act_user_name_start'] = val

            val = values[1]
            if val != '':
                items['act_user_name_end'] = val

    if act_time is not None:
        values = act_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['act_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['act_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['act_time_end'] = datetime.fromtimestamp(int(val))

    if is_act is not None:
        values = is_act.split(',')
        if len(values) == 1:
            val = values[0]
            items['is_act'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['is_act_start'] = int(val)

            val = values[1]
            if val != '':
                items['is_act_end'] = int(val)

    if act_code is not None:
        values = act_code.split(',')
        if len(values) == 1:
            val = values[0]
            items['act_code'] = val
        else:
            val = values[0]
            if val != '':
                items['act_code_start'] = val

            val = values[1]
            if val != '':
                items['act_code_end'] = val

    if batch_code is not None:
        values = batch_code.split(',')
        if len(values) == 1:
            val = values[0]
            items['batch_code'] = val
        else:
            val = values[0]
            if val != '':
                items['batch_code_start'] = val

            val = values[1]
            if val != '':
                items['batch_code_end'] = val

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_video_recharge(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_video_recharge(items, search_items, set_items)

    return FilterResVideoRecharge(data=data, total=c)

@router.get(f'/vrecharge/batch/filter', summary="获取视频码创建批次列表")
async def filter_video_batch_recharge(page:int=1):
    return d_video_task.get_vrecharge_brach_list(page)

@router.get(f'/vtask_receive/filter', response_model=FilterResVideoTaskReceive, summary="获取用户视频任务领取列表")
async def filter_video_task_receive(
        id: Optional[str] = None,
        task_id: Optional[str] = None,
        shoper_id: Optional[str] = None,
        user_id: Optional[str] = None,
        user_name: Optional[str] = None,
        user_phone: Optional[str] = None,
        audit_comment: Optional[str] = None,
        audit_status: Optional[str] = None,
        l_id: Optional[str] = None,
        l_user_id: Optional[str] = None,
        s_title: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResVideoTaskReceive:
    """
    1. 按照字段查询`?field1=value1&field2=value2`
    2. 按照范围查询，大于某个值`?field=value,`, 表示filed大于value
    3. 按照范围查询，小于某个值`?field=,value`， 表示field小于value
    4. 按照范围查询，范围值`?field=value1,value2`，表示搜索field大于等于value1，小于等于value2
    5. page是页数，第一页为1
    6. page_size为每一页大小， 默认20
    7. 如果是日期，请使用时间戳，十位的时间戳，单位：秒
    8. 所有字符串字段均可搜索，需要在字段前加个前缀`s_`,例如搜索`username`包含`zhang`， 则可以这样`s_username=zhang`写,这里只是一个假设
    9. 字段的多选择（in关系），需要在字段前加前缀`l_`,并且以逗号`,`隔开,例如要找出`id=2`或者`id=3`的样本，可以这样写`?l_id=2,3`
    """

    items = dict()
    search_items = dict()
    set_items = dict()

    if id is not None:
        values = id.split(',')
        if len(values) == 1:
            val = values[0]
            items['id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['id_start'] = int(val)

            val = values[1]
            if val != '':
                items['id_end'] = int(val)

    if task_id is not None:
        values = task_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['task_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['task_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['task_id_end'] = int(val)

    if shoper_id is not None:
        values = shoper_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['shoper_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['shoper_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['shoper_id_end'] = int(val)

    if user_id is not None:
        values = user_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['user_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['user_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['user_id_end'] = int(val)

    if user_name is not None:
        values = user_name.split(',')
        if len(values) == 1:
            val = values[0]
            items['user_name'] = val
        else:
            val = values[0]
            if val != '':
                items['user_name_start'] = val

            val = values[1]
            if val != '':
                items['user_name_end'] = val

    if user_phone is not None:
        values = user_phone.split(',')
        if len(values) == 1:
            val = values[0]
            items['user_phone'] = val
        else:
            val = values[0]
            if val != '':
                items['user_phone_start'] = val

            val = values[1]
            if val != '':
                items['user_phone_end'] = val

    if audit_comment is not None:
        values = audit_comment.split(',')
        if len(values) == 1:
            val = values[0]
            items['audit_comment'] = val
        else:
            val = values[0]
            if val != '':
                items['audit_comment_start'] = val

            val = values[1]
            if val != '':
                items['audit_comment_end'] = val

    if audit_status is not None:
        values = audit_status.split(',')
        if len(values) == 1:
            val = values[0]
            items['audit_status'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['audit_status_start'] = int(val)

            val = values[1]
            if val != '':
                items['audit_status_end'] = int(val)

    if s_title is not None:
        search_items['title'] = '%' + s_title + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_user_id is not None:
        values = l_user_id.split(',')
        values = [int(val) for val in values]
        set_items['user_id'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_video_task_receive(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_video_task_receive(items, search_items, set_items)

    return FilterResVideoTaskReceive(data=data, total=c)


@router.get(f'/vrecharge_log/filter', response_model=FilterResVideoRechargeLog, summary="获取用户视频条数购买/消费日志列表")
async def filter_video_recharge_log(
        id: Optional[str] = None,
        user_id: Optional[str] = None,
        phone: Optional[str] = None,
        type: Optional[str] = None,
        description: Optional[str] = None,
        out_trade_no: Optional[str] = None,
        owner_id: Optional[str] = None,
        owner_nick: Optional[str] = None,
        l_id: Optional[str] = None,
        l_good_id: Optional[str] = None,
        l_owner_id: Optional[str] = None,
        s_description: Optional[str] = None,
        s_out_trade_no: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResVideoRechargeLog:
    """
    1. 按照字段查询`?field1=value1&field2=value2`
    2. 按照范围查询，大于某个值`?field=value,`, 表示filed大于value
    3. 按照范围查询，小于某个值`?field=,value`， 表示field小于value
    4. 按照范围查询，范围值`?field=value1,value2`，表示搜索field大于等于value1，小于等于value2
    5. page是页数，第一页为1
    6. page_size为每一页大小， 默认20
    7. 如果是日期，请使用时间戳，十位的时间戳，单位：秒
    8. 所有字符串字段均可搜索，需要在字段前加个前缀`s_`,例如搜索`username`包含`zhang`， 则可以这样`s_username=zhang`写,这里只是一个假设
    9. 字段的多选择（in关系），需要在字段前加前缀`l_`,并且以逗号`,`隔开,例如要找出`id=2`或者`id=3`的样本，可以这样写`?l_id=2,3`
    """

    items = dict()
    search_items = dict()
    set_items = dict()

    if id is not None:
        values = id.split(',')
        if len(values) == 1:
            val = values[0]
            items['id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['id_start'] = int(val)

            val = values[1]
            if val != '':
                items['id_end'] = int(val)

    if user_id is not None:
        values = user_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['user_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['user_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['user_id_end'] = int(val)

    if phone is not None:
        values = phone.split(',')
        if len(values) == 1:
            val = values[0]
            items['phone'] = val
        else:
            val = values[0]
            if val != '':
                items['phone_start'] = val

            val = values[1]
            if val != '':
                items['phone_end'] = val

    if type is not None:
        values = type.split(',')
        if len(values) == 1:
            val = values[0]
            items['type'] = val
        else:
            val = values[0]
            if val != '':
                items['type_start'] = val

            val = values[1]
            if val != '':
                items['type_end'] = val

    if description is not None:
        values = description.split(',')
        if len(values) == 1:
            val = values[0]
            items['description'] = val
        else:
            val = values[0]
            if val != '':
                items['description_start'] = val

            val = values[1]
            if val != '':
                items['description_end'] = val

    if out_trade_no is not None:
        values = out_trade_no.split(',')
        if len(values) == 1:
            val = values[0]
            items['out_trade_no'] = val
        else:
            val = values[0]
            if val != '':
                items['out_trade_no_start'] = val

            val = values[1]
            if val != '':
                items['out_trade_no_end'] = val

    if owner_id is not None:
        values = owner_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['owner_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['owner_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['owner_id_end'] = int(val)

    if owner_nick is not None:
        values = owner_nick.split(',')
        if len(values) == 1:
            val = values[0]
            items['owner_nick'] = val
        else:
            val = values[0]
            if val != '':
                items['owner_nick_start'] = val

            val = values[1]
            if val != '':
                items['owner_nick_end'] = val

    if s_description is not None:
        search_items['description'] = '%' + s_description + '%'

    if s_out_trade_no is not None:
        search_items['out_trade_no'] = '%' + s_out_trade_no + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_good_id is not None:
        values = l_good_id.split(',')
        values = [val for val in values]
        set_items['good_id'] = values

    if l_owner_id is not None:
        values = l_owner_id.split(',')
        values = [int(val) for val in values]
        set_items['owner_id'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_video_recharge_log(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_video_recharge_log(items, search_items, set_items)

    return FilterResVideoRechargeLog(data=data, total=c)

@router.post(f'/vtask/audit', response_model=str, summary="审核视频任务")
async def audit_video_task(item: d_video_task.AuditModel) -> str:
    if not item.audit or not item.receive_id or not item.audit_adm:
        return "数据错误"
    # d_video_task.update_audit(item)
    receive_info = d_video_task.get_receive_by_id(item.receive_id)
    if receive_info:
        task_info = d_video_task.get_video_task(receive_info.task_id)
        if task_info:
            if item.audit == 2 and receive_info.money_status == 0:
                if task_info.money > 0:
                    d_account.video_balance_change(receive_info.user_id, task_info.money, '视频任务奖励金', f"task_id:{item.video_id},receive_id:{item.receive_id},审核{item.audit_adm},audit_info:{item.audit_info}")
                if task_info.coin > 0:
                    d_account.video_coin_change(receive_info.user_id, task_info.coin, '视频任务奖励券', f"task_id:{item.video_id},receive_id:{item.receive_id},审核{item.audit_adm},audit_info:{item.audit_info}")
                receive_user_info = d_user.get_user_by_id(receive_info.user_id)
                receive_invit_info = None
                if receive_user_info.invited_user_id is None:
                    receive_user_info.invited_user_id = 0
                if receive_user_info.invited_user_id > 0:
                    receive_invit_info = d_user.get_user_by_id(receive_user_info.invited_user_id)
                #推荐奖
                if task_info.rem_money > 0 and receive_invit_info:
                    d_balance.invited_user_money(receive_invit_info.id, task_info.rem_money, global_define.balance_type[40], receive_info.id, f"{task_info.id}|{task_info.title}")
                    #间推奖
                    if receive_invit_info.invited_user_id is None:
                        receive_invit_info.invited_user_id = 0
                    if task_info.rem_mid_money > 0 and receive_invit_info.invited_user_id > 0:
                        receive_invit2_info = d_user.get_user_by_id(receive_invit_info.invited_user_id)
                        d_balance.invited_user_money(receive_invit2_info.id, task_info.rem_mid_money, global_define.balance_type[41], receive_info.id, f"{task_info.id}|{task_info.title}")

                #推荐团长奖
                tuan_info = None
                if receive_user_info.is_tuan > 0:
                    tuan_info = receive_user_info
                else:
                    if receive_user_info.tuan_id > 0:
                        tuan_info = d_user.get_user_by_id(receive_user_info.tuan_id)
                if task_info.rem_team > 0 and tuan_info:
                    d_balance.invited_user_money(tuan_info.id, task_info.rem_team, global_define.balance_type[42], receive_info.id, f"{task_info.id}|{task_info.title}")

                    #间推团长奖
                    if tuan_info.tuan_id > 0 and task_info.rem_mid_team > 0:
                        d_balance.invited_user_money(tuan_info.tuan_id, task_info.rem_mid_team, global_define.balance_type[43],\
                                                     receive_info.id, f"{task_info.id}|{task_info.title}")

                #居间收益
                if task_info.live_mid_uid > 0 and task_info.live_mid_money > 0:
                    live_mid_uinfo = d_user.get_user_by_id(task_info.live_mid_uid)
                    d_balance.invited_user_money(live_mid_uinfo.id, task_info.live_mid_money, global_define.balance_type[48], receive_info.id, f"{task_info.id}|{task_info.title}")

                d_video_task.update_receive_audit_and_money(item)
            else:
                d_video_task.update_receive_audit(item)
            return "success"
        else:
            return "未知任务"
    else:
        return "未知领取任务"


@router.post(f'/vtask/material/create', response_model=SVideoTaskMaterial, summary="创建视频任务素材")
async def create_video_task_material(item: CreateVideoTaskMaterial) -> SVideoTaskMaterial:
    if not item.bag_id:
        return "数据错误1"
    if item.bag_id < 1:
        return "数据错误2"
    dict_item = dict(item)
    for k, v in dict_item.items():
        if v is not None:
            v = str(v)
            v = v.replace(" ", "")
            get_search = re.search(r"'", v, flags=0)
            get_search2 = re.search(r'%27', v, flags=0)
            get_search3 = re.search(r'unionselect', v, flags=0)
            if get_search or get_search2 or get_search3:
                raise HTTPException(status_code=404, detail='bad way~~~~~~')

    return d_db.insert_video_task_material(item)

@router.get(f"/vtask/material/del", summary="删除视频任务素材")
async def vtask_material_del(matid:int = -1):
    if matid > 0:
        d_video_task.del_material(matid)
        return "success"
    else:
        return "数据错误"


@router.get(f'/vtask/material/filter', response_model=FilterResVideoTaskMaterial, summary="获取视频任务素材列表")
async def filter_video_task_material(
        id: Optional[str] = None,
        task_id: Optional[str] = None,
        path: Optional[str] = None,
        m_type: Optional[str] = None,
        bag_id: Optional[str] = None,
        order_by: Optional[str] = None) -> FilterResVideoTaskMaterial:
        # page: int = 1,
        # page_size: int = 20
    """
    1. 按照字段查询`?field1=value1&field2=value2`
    2. 按照范围查询，大于某个值`?field=value,`, 表示filed大于value
    3. 按照范围查询，小于某个值`?field=,value`， 表示field小于value
    4. 按照范围查询，范围值`?field=value1,value2`，表示搜索field大于等于value1，小于等于value2
    5. page是页数，第一页为1
    6. page_size为每一页大小， 默认20
    7. 如果是日期，请使用时间戳，十位的时间戳，单位：秒
    8. 所有字符串字段均可搜索，需要在字段前加个前缀`s_`,例如搜索`username`包含`zhang`， 则可以这样`s_username=zhang`写,这里只是一个假设
    9. 字段的多选择（in关系），需要在字段前加前缀`l_`,并且以逗号`,`隔开,例如要找出`id=2`或者`id=3`的样本，可以这样写`?l_id=2,3`
    """

    items = dict()
    search_items = dict()
    set_items = dict()

    is_del = '0'
    page: int = 1
    page_size: int = 20

    if id is not None:
        values = id.split(',')
        if len(values) == 1:
            val = values[0]
            items['id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['id_start'] = int(val)

            val = values[1]
            if val != '':
                items['id_end'] = int(val)

    if task_id is not None:
        values = task_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['task_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['task_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['task_id_end'] = int(val)

    if path is not None:
        values = path.split(',')
        if len(values) == 1:
            val = values[0]
            items['path'] = val
        else:
            val = values[0]
            if val != '':
                items['path_start'] = val

            val = values[1]
            if val != '':
                items['path_end'] = val

    if m_type is not None:
        values = m_type.split(',')
        if len(values) == 1:
            val = values[0]
            items['m_type'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['m_type_start'] = int(val)

            val = values[1]
            if val != '':
                items['m_type_end'] = int(val)

    if bag_id is not None:
        values = bag_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['bag_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['bag_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['bag_id_end'] = int(val)

    if is_del is not None:
        values = is_del.split(',')
        if len(values) == 1:
            val = values[0]
            items['is_del'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['is_del_start'] = int(val)

            val = values[1]
            if val != '':
                items['is_del_end'] = int(val)

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_video_task_material(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_video_task_material(items, search_items, set_items)

    return FilterResVideoTaskMaterial(data=data, total=c)

@router.get(f"/receive/audit/get", summary="获取下一条待审核已领取的任务")
async def receive_audit_get(receive_id:int = -1):
    if receive_id > 0:
        res = d_video_task.get_receive_next(receive_id)
        if res:
            return res
        else:
            return "end"
    else:
        return "数据错误"

@router.post(f'/vtask/material/bag/create', response_model=SVideoTaskMaterialBag, summary="创建视频素材包")
async def create_video_task_material_bag(item: CreateVideoTaskMaterialBag) -> SVideoTaskMaterialBag:
    dict_item = dict(item)
    for k, v in dict_item.items():
        if v is not None:
            v = str(v)
            v = v.replace(" ", "")
            get_search = re.search(r"'", v, flags=0)
            get_search2 = re.search(r'%27', v, flags=0)
            get_search3 = re.search(r'unionselect', v, flags=0)
            if get_search or get_search2 or get_search3:
                raise HTTPException(status_code=404, detail='bad way~~~~~~')

    return d_db.insert_video_task_material_bag(item)


@router.post(f'/vtask/material/bag/update', response_model=str, summary="修改视频素材包")
async def update_video_task_material_bag(item: SVideoTaskMaterialBag) -> str:
    if item.is_del:
        return '数据错误'
    d_db.update_video_task_material_bag(item)
    return "success"

@router.post(f'/vtask/material/bag/del', response_model=str, summary="删除视频素材包")
async def update_video_task_material_bag(item: SVideoTaskMaterialBag) -> str:
    if not item.id:
        return '数据错误'
    item.is_del = 1
    d_db.update_video_task_material_bag(item)
    return "success"

@router.get(f'/vtask/material/bag/filter', response_model=FilterResVideoTaskMaterialBag, summary="视频素材包分页列表")
async def filter_video_task_material_bag(
        id: Optional[str] = None,
        task_id: Optional[str] = None,
        bag_name: Optional[str] = None,
        l_bag_name: Optional[str] = None,
        s_bag_name: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1) -> FilterResVideoTaskMaterialBag:
    """
    1. 按照字段查询`?field1=value1&field2=value2`
    2. 按照范围查询，大于某个值`?field=value,`, 表示filed大于value
    3. 按照范围查询，小于某个值`?field=,value`， 表示field小于value
    4. 按照范围查询，范围值`?field=value1,value2`，表示搜索field大于等于value1，小于等于value2
    5. page是页数，第一页为1
    6. page_size为每一页大小， 默认20
    7. 如果是日期，请使用时间戳，十位的时间戳，单位：秒
    8. 所有字符串字段均可搜索，需要在字段前加个前缀`s_`,例如搜索`username`包含`zhang`， 则可以这样`s_username=zhang`写,这里只是一个假设
    9. 字段的多选择（in关系），需要在字段前加前缀`l_`,并且以逗号`,`隔开,例如要找出`id=2`或者`id=3`的样本，可以这样写`?l_id=2,3`
    """

    items = dict()
    search_items = dict()
    set_items = dict()

    page_size = 20
    items['is_del'] = 0

    if id is not None:
        values = id.split(',')
        if len(values) == 1:
            val = values[0]
            items['id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['id_start'] = int(val)

            val = values[1]
            if val != '':
                items['id_end'] = int(val)

    if task_id is not None:
        values = task_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['task_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['task_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['task_id_end'] = int(val)

    if bag_name is not None:
        values = bag_name.split(',')
        if len(values) == 1:
            val = values[0]
            items['bag_name'] = val
        else:
            val = values[0]
            if val != '':
                items['bag_name_start'] = val

            val = values[1]
            if val != '':
                items['bag_name_end'] = val

    if s_bag_name is not None:
        search_items['bag_name'] = '%' + s_bag_name + '%'

    if l_bag_name is not None:
        values = l_bag_name.split(',')
        values = [val for val in values]
        set_items['bag_name'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_video_task_material_bag(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_video_task_material_bag(items, search_items, set_items)

    return FilterResVideoTaskMaterialBag(data=data, total=c)


@router.post(f'/video_article_type/create', response_model=SVideoArticleType, summary="创建文章分类")
async def create_video_article_type(item: CreateVideoArticleType) -> SVideoArticleType:
    dict_item = dict(item)
    for k,v in dict_item.items():
        if v is not None:
            v = str(v)
            v = v.replace(" ", "")
            get_search = re.search(r"'", v, flags=0)
            get_search2 = re.search(r'%27', v, flags=0)
            get_search3 = re.search(r'unionselect', v, flags=0)
            if get_search or get_search2 or get_search3:
               raise HTTPException(status_code=404, detail='bad way~~~~~~')

    return d_db.insert_video_article_type(item)

@router.post(f'/video_article_type/update', response_model=str, summary="更新文章分类")
async def update_video_article_type(item: SVideoArticleType) -> str:
    d_db.update_video_article_type(item)
    return "success"


@router.get(f'/video_article_type/filter', response_model=FilterResVideoArticleType, summary="文章分类列表")
async def filter_video_article_type(
        id: Optional[str] = None,
        title: Optional[str] = None,
        describe: Optional[str] = None,
        s_title: Optional[str] = None,
        s_describe: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResVideoArticleType:
    """
    1. 按照字段查询`?field1=value1&field2=value2`
    2. 按照范围查询，大于某个值`?field=value,`, 表示filed大于value
    3. 按照范围查询，小于某个值`?field=,value`， 表示field小于value
    4. 按照范围查询，范围值`?field=value1,value2`，表示搜索field大于等于value1，小于等于value2
    5. page是页数，第一页为1
    6. page_size为每一页大小， 默认20
    7. 如果是日期，请使用时间戳，十位的时间戳，单位：秒
    8. 所有字符串字段均可搜索，需要在字段前加个前缀`s_`,例如搜索`username`包含`zhang`， 则可以这样`s_username=zhang`写,这里只是一个假设
    9. 字段的多选择（in关系），需要在字段前加前缀`l_`,并且以逗号`,`隔开,例如要找出`id=2`或者`id=3`的样本，可以这样写`?l_id=2,3`
    """

    items = dict()
    search_items = dict()
    set_items = dict()

    if id is not None:
        values = id.split(',')
        if len(values) == 1:
            val = values[0]
            items['id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['id_start'] = int(val)

            val = values[1]
            if val != '':
                items['id_end'] = int(val)

    if title is not None:
        values = title.split(',')
        if len(values) == 1:
            val = values[0]
            items['title'] = val
        else:
            val = values[0]
            if val != '':
                items['title_start'] = val

            val = values[1]
            if val != '':
                items['title_end'] = val

    if describe is not None:
        values = describe.split(',')
        if len(values) == 1:
            val = values[0]
            items['describe'] = val
        else:
            val = values[0]
            if val != '':
                items['describe_start'] = val

            val = values[1]
            if val != '':
                items['describe_end'] = val

    if s_title is not None:
        search_items['title'] = '%' + s_title + '%'

    if s_describe is not None:
        search_items['describe'] = '%' + s_describe + '%'

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_video_article_type(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_video_article_type(items, search_items, set_items)

    return FilterResVideoArticleType(data=data, total=c)

class CreateVideoArticleListList(BaseModel):
    video_article: Optional[CreateVideoArticle] = Field(None, title='创建视频文章结构')
    video_article_list: List[CreateVideoArticleList] = Field(None, title='创建视频文章内容列表结构')

class UpdateVideoArticleListList(BaseModel):
    video_article: Optional[SVideoArticle] = Field(None, title='修改视频文章结构')
    video_article_list: List[SVideoArticleList] = Field(None, title='修改视频文章内容列表结构')

@router.post(f'/video/article/create', summary="创建视频文章和文章内容列表")
async def create_video_article(item: CreateVideoArticleListList):
    re_val = {}
    dict_item = dict(item.video_article)
    for k,v in dict_item.items():
        if v is not None:
            v = str(v)
            v = v.replace(" ", "")
            get_search = re.search(r"'", v, flags=0)
            get_search2 = re.search(r'%27', v, flags=0)
            get_search3 = re.search(r'unionselect', v, flags=0)
            if get_search or get_search2 or get_search3:
               raise HTTPException(status_code=404, detail='bad way~~~~~~')
    item.video_article.is_draft = 0
    re_val['video_article'] = d_db.insert_video_article(item.video_article)
    menu_num = 1
    for item_menu in item.video_article_list:
        menu_key = f"video_article_list{menu_num}"
        item_menu.article_id = re_val['video_article'].id
        re_val[menu_key] = d_db.insert_video_article_list(item_menu)
        menu_num += 1
    # logging.info(re_val)
    return re_val

@router.post(f'/video/article/draft/create', summary="创建草稿视频文章")
async def create_video_draft_article(item: CreateVideoArticleListList):
    re_val = {}
    dict_item = dict(item.video_article)
    for k, v in dict_item.items():
        if v is not None:
            v = str(v)
            v = v.replace(" ", "")
            get_search = re.search(r"'", v, flags=0)
            get_search2 = re.search(r'%27', v, flags=0)
            get_search3 = re.search(r'unionselect', v, flags=0)
            if get_search or get_search2 or get_search3:
                raise HTTPException(status_code=404, detail='bad way~~~~~~')
    item.video_article.is_draft = 1
    re_val['video_article'] = d_db.insert_video_article(item.video_article)
    menu_num = 1
    for item_menu in item.video_article_list:
        menu_key = f"video_article_list{menu_num}"
        item_menu.article_id = re_val['video_article'].id
        re_val[menu_key] = d_db.insert_video_article_list(item_menu)
        menu_num += 1
    # logging.info(re_val)
    return re_val

@router.post(f'/video/article/draft/update', response_model=str, summary="修改草稿视频文章")
async def update_video_article(item: UpdateVideoArticleListList) -> str:
    item.video_article.is_draft = 1
    d_db.update_video_article(item.video_article)
    for item_menu in item.video_article_list:
        if item_menu.id == 0:
            add_instance = CreateVideoArticleList(
                type_id=item_menu.type_id,
                article_id=item.video_article.id,
                operator_id=item_menu.operator_id,
                content=item_menu.content
            )
            d_db.insert_video_article_list(add_instance)
        else:
            d_db.update_video_article_list(item_menu)
    return "success"

@router.post(f'/video/article/update', response_model=str, summary="修改视频文章")
async def update_video_article(item: UpdateVideoArticleListList) -> str:
    item.video_article.is_draft = 0
    d_db.update_video_article(item.video_article)
    for item_menu in item.video_article_list:
        if item_menu.id == 0:
            add_instance = CreateVideoArticleList(
                type_id=item_menu.type_id,
                article_id=item.video_article.id,
                operator_id=item_menu.operator_id,
                content=item_menu.content
            )
            d_db.insert_video_article_list(add_instance)
        else:
            d_db.update_video_article_list(item_menu)
    return "success"

@router.post(f'/video/article/del', response_model=str, summary="删除视频文章")
async def update_video_article_del(item: SVideoArticle) -> str:
    d_video_task.del_video_article(item.id)
    return "success"

@router.post(f'/video/article/list/del', response_model=str, summary="删除视频文章内容模块")
async def update_video_article_list_del(item: SVideoArticleList) -> str:
    d_video_task.del_video_article_list(item.id)
    return "success"

@router.get(f'/video/article/list/filter', response_model=FilterResVideoArticleList, summary="视频文章内容模块列表")
async def filter_video_article_list(
        type_id: Optional[str] = None,
        article_id: Optional[str] = None,
        is_del: Optional[str] = '0',
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResVideoArticleList:
    """
    1. 按照字段查询`?field1=value1&field2=value2`
    2. 按照范围查询，大于某个值`?field=value,`, 表示filed大于value
    3. 按照范围查询，小于某个值`?field=,value`， 表示field小于value
    4. 按照范围查询，范围值`?field=value1,value2`，表示搜索field大于等于value1，小于等于value2
    5. page是页数，第一页为1
    6. page_size为每一页大小， 默认20
    7. 如果是日期，请使用时间戳，十位的时间戳，单位：秒
    8. 所有字符串字段均可搜索，需要在字段前加个前缀`s_`,例如搜索`username`包含`zhang`， 则可以这样`s_username=zhang`写,这里只是一个假设
    9. 字段的多选择（in关系），需要在字段前加前缀`l_`,并且以逗号`,`隔开,例如要找出`id=2`或者`id=3`的样本，可以这样写`?l_id=2,3`
    """

    items = dict()
    search_items = dict()
    set_items = dict()

    if type_id is not None:
        values = type_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['type_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['type_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['type_id_end'] = int(val)

    if article_id is not None:
        values = article_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['article_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['article_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['article_id_end'] = int(val)

    if is_del is not None:
        values = is_del.split(',')
        if len(values) == 1:
            val = values[0]
            items['is_del'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['is_del_start'] = int(val)

            val = values[1]
            if val != '':
                items['is_del_end'] = int(val)

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_video_article_list(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_video_article_list(items, search_items, set_items)

    return FilterResVideoArticleList(data=data, total=c)

@router.get(f'/video/article/filter', response_model=FilterResVideoArticle, summary="检索视频文章")
async def filter_video_article(
        id: Optional[str] = None,
        type_id: Optional[str] = None,
        title: Optional[str] = None,
        s_description: Optional[str] = None,
        s_title: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResVideoArticle:
    """
    1. 按照字段查询`?field1=value1&field2=value2`
    2. 按照范围查询，大于某个值`?field=value,`, 表示filed大于value
    3. 按照范围查询，小于某个值`?field=,value`， 表示field小于value
    4. 按照范围查询，范围值`?field=value1,value2`，表示搜索field大于等于value1，小于等于value2
    5. page是页数，第一页为1
    6. page_size为每一页大小， 默认20
    7. 如果是日期，请使用时间戳，十位的时间戳，单位：秒
    8. 所有字符串字段均可搜索，需要在字段前加个前缀`s_`,例如搜索`username`包含`zhang`， 则可以这样`s_username=zhang`写,这里只是一个假设
    9. 字段的多选择（in关系），需要在字段前加前缀`l_`,并且以逗号`,`隔开,例如要找出`id=2`或者`id=3`的样本，可以这样写`?l_id=2,3`
    """

    items = dict()
    search_items = dict()
    set_items = dict()
    is_del = '0'

    if id is not None:
        values = id.split(',')
        if len(values) == 1:
            val = values[0]
            items['id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['id_start'] = int(val)

            val = values[1]
            if val != '':
                items['id_end'] = int(val)

    if type_id is not None:
        values = type_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['type_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['type_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['type_id_end'] = int(val)

    if is_del is not None:
        values = is_del.split(',')
        if len(values) == 1:
            val = values[0]
            items['is_del'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['is_del_start'] = int(val)

            val = values[1]
            if val != '':
                items['is_del_end'] = int(val)

    if title is not None:
        values = title.split(',')
        if len(values) == 1:
            val = values[0]
            items['title'] = val
        else:
            val = values[0]
            if val != '':
                items['title_start'] = val

            val = values[1]
            if val != '':
                items['title_end'] = val

    if s_description is not None:
        search_items['description'] = '%' + s_description + '%'

    if s_title is not None:
        search_items['title'] = '%' + s_title + '%'

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_video_article(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_video_article(items, search_items, set_items)

    return FilterResVideoArticle(data=data, total=c)

@router.post(f'/video/article/label', response_model=str, summary="添加文章标签")
async def update_video_article_label(item: VideoActiveLabel) -> str:
    d_video_task.add_video_label(item.video_id, item.add_label)
    return "success"