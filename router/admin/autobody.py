from dao import d_db, d_user, d_account, d_found, d_video_task, d_balance, d_autobody
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
class AutoBodyStat(BaseModel):
    auto_id: Optional[int] = Field(title='智能体id')
    # stat: Optional[int] = Field(title='')

class AutoBodyOrder(BaseModel):
    auto_id: Optional[int] = Field(title='智能体id')
    order_id: Optional[int] = Field(title='排序id')

@router.post(f'/autobody/type/create', response_model=SAutobodyType, summary="创建智能体分类")
async def create_autobody_type(item: CreateAutobodyType) -> SAutobodyType:
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

    return d_db.insert_autobody_type(item)

@router.post(f'/autobody/type/update', response_model=str, summary="修改智能体分类")
async def update_autobody_type(item: SAutobodyType) -> str:
    d_db.update_autobody_type(item)
    return "success"


@router.get(f'/autobody_type/filter', response_model=FilterResAutobodyType, summary="智能体分类列表")
async def filter_autobody_type(
        id: Optional[str] = None,
        title: Optional[str] = None,
        describe: Optional[str] = None,
        s_title: Optional[str] = None,
        s_describe: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResAutobodyType:
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
    data = d_db.filter_autobody_type(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_autobody_type(items, search_items, set_items)

    return FilterResAutobodyType(data=data, total=c)

@router.post(f'/autobody/file/create', response_model=SAutobodyFile, summary="创建智能体文件")
async def create_autobody_file(item: CreateAutobodyFile) -> SAutobodyFile:
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

    return d_db.insert_autobody_file(item)


# @router.post(f'/autobody_file/update', response_model=str, summary="修改智能体文件")
# async def update_autobody_file(item: SAutobodyFile) -> str:
#     d_db.update_autobody_file(item)
#     return "success"


@router.get(f'/autobody_file/filter', response_model=FilterResAutobodyFile, summary="智能体文件列表")
async def filter_autobody_file(
        id: Optional[str] = None,
        autobody_id: Optional[str] = None,
        s_title: Optional[str] = None,
        s_describe: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResAutobodyFile:
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

    if autobody_id is not None:
        values = autobody_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['autobody_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['autobody_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['autobody_id_end'] = int(val)

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
    data = d_db.filter_autobody_file(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_autobody_file(items, search_items, set_items)

    return FilterResAutobodyFile(data=data, total=c)

@router.post(f'/autobody/create', response_model=SAutobody, summary="创建智能体")
async def create_autobody(item: CreateAutobody) -> SAutobody:
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

    return d_db.insert_autobody(item)


@router.post(f'/autobody/update', response_model=str, summary="修改智能体")
async def update_autobody(item: SAutobody) -> str:
    d_db.update_autobody(item)
    return "success"

@router.post(f'/autobody/update/close', response_model=str, summary="关闭智能体")
async def update_autobody_close(item: AutoBodyStat) -> str:
    d_autobody.close_autobody(item.auto_id)
    return "success"

@router.post(f'/autobody/update/open', response_model=str, summary="打开智能体")
async def update_autobody_open(item: AutoBodyStat) -> str:
    d_autobody.open_autobody(item.auto_id)
    return "success"

@router.post(f'/autobody/update/del', response_model=str, summary="删除智能体")
async def update_autobody_del(item: AutoBodyStat) -> str:
    d_autobody.del_autobody(item.auto_id)
    return "success"

@router.post(f'/autobody/update/order', response_model=str, summary="修改智能体优先级")
async def update_autobody_order(item: AutoBodyOrder) -> str:
    d_autobody.update_autobody_order(item.auto_id, item.order_id)
    return "success"


@router.get(f'/autobody/filter', response_model=FilterResAutobody, summary="获取智能体列表")
async def filter_autobody(
        id: Optional[str] = None,
        type_id: Optional[str] = None,
        order_id: Optional[str] = None,
        stat: Optional[str] = None,
        s_at_name: Optional[str] = None,
        s_describe: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResAutobody:
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

    if order_id is not None:
        values = order_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['order_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['order_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['order_id_end'] = int(val)

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

    items['del_stat'] = 0

    if s_at_name is not None:
        search_items['at_name'] = '%' + s_at_name + '%'

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
    data = d_db.filter_autobody(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_autobody(items, search_items, set_items)

    return FilterResAutobody(data=data, total=c)

