from dao import d_order, d_db
from fastapi import APIRouter, Depends, Header, Request
from model.mall import m_order
from router import r_schema
from typing import List
from router.admin.user import verify_token
from common import global_define
from fastapi import HTTPException
from model.m_schema import *
import re

router = APIRouter(dependencies=[Depends(verify_token)])


# @router.get(f'/check_record', response_model=None, summary='核销记录')
# async def get_check_record(item):
#     pass
#
# @router.post(f'/bigorder_set/create', response_model=SBigorderSet)
# async def create_bigorder_set(item: CreateBigorderSet) -> SBigorderSet:
#     dict_item = dict(item)
#     for k, v in dict_item.items():
#         if v is not None:
#             v = str(v)
#             v = v.replace(" ", "")
#             get_search = re.search(r"'", v, flags=0)
#             get_search2 = re.search(r'%27', v, flags=0)
#             get_search3 = re.search(r'unionselect', v, flags=0)
#             if get_search or get_search2 or get_search3:
#                 raise HTTPException(status_code=404, detail='bad way~~~~~~')
#
#     return d_db.insert_bigorder_set(item)


@router.post(f'/bigorder_set/update', response_model=str, summary='更新复投配置参数')
async def update_bigorder_set(item: SBigorderSet) -> str:
    d_db.update_bigorder_set(item)
    return "success"


@router.get(f'/bigorder_set/get', response_model=SBigorderSet, summary='获取单一配置项')
async def get_bigorder_set(bigorder_set_id: int) -> SBigorderSet:
    return d_db.get_bigorder_set(bigorder_set_id)


@router.get(f'/bigorder_set/filter', response_model=FilterResBigorderSet, summary='复投配置列表')
async def filter_bigorder_set(
        id: Optional[str] = None,
        set_name: Optional[str] = None,
        val_int: Optional[str] = None,
        val_str: Optional[str] = None,
        set_cont: Optional[str] = None,
        l_id: Optional[str] = None,
        l_set_name: Optional[str] = None,
        l_val_int: Optional[str] = None,
        l_val_str: Optional[str] = None,
        l_set_cont: Optional[str] = None,
        s_set_name: Optional[str] = None,
        s_val_str: Optional[str] = None,
        s_set_cont: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResBigorderSet:
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

    if set_name is not None:
        values = set_name.split(',')
        if len(values) == 1:
            val = values[0]
            items['set_name'] = val
        else:
            val = values[0]
            if val != '':
                items['set_name_start'] = val

            val = values[1]
            if val != '':
                items['set_name_end'] = val

    if val_int is not None:
        values = val_int.split(',')
        if len(values) == 1:
            val = values[0]
            items['val_int'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['val_int_start'] = int(val)

            val = values[1]
            if val != '':
                items['val_int_end'] = int(val)

    if val_str is not None:
        values = val_str.split(',')
        if len(values) == 1:
            val = values[0]
            items['val_str'] = val
        else:
            val = values[0]
            if val != '':
                items['val_str_start'] = val

            val = values[1]
            if val != '':
                items['val_str_end'] = val

    if set_cont is not None:
        values = set_cont.split(',')
        if len(values) == 1:
            val = values[0]
            items['set_cont'] = val
        else:
            val = values[0]
            if val != '':
                items['set_cont_start'] = val

            val = values[1]
            if val != '':
                items['set_cont_end'] = val

    if s_set_name is not None:
        search_items['set_name'] = '%' + s_set_name + '%'

    if s_val_str is not None:
        search_items['val_str'] = '%' + s_val_str + '%'

    if s_set_cont is not None:
        search_items['set_cont'] = '%' + s_set_cont + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_set_name is not None:
        values = l_set_name.split(',')
        values = [val for val in values]
        set_items['set_name'] = values

    if l_val_int is not None:
        values = l_val_int.split(',')
        values = [int(val) for val in values]
        set_items['val_int'] = values

    if l_val_str is not None:
        values = l_val_str.split(',')
        values = [val for val in values]
        set_items['val_str'] = values

    if l_set_cont is not None:
        values = l_set_cont.split(',')
        values = [val for val in values]
        set_items['set_cont'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_bigorder_set(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_bigorder_set(items, search_items, set_items)

    return FilterResBigorderSet(data=data, total=c)


@router.post(f'/bigorder_initbag/create', response_model=SBigorderInitbag, summary='创建初始礼包')
async def create_bigorder_initbag(item: CreateBigorderInitbag) -> SBigorderInitbag:
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

    return d_db.insert_bigorder_initbag(item)


@router.post(f'/bigorder_initbag/update', response_model=str, summary='修改礼包')
async def update_bigorder_initbag(item: SBigorderInitbag) -> str:
    d_db.update_bigorder_initbag(item)
    return "success"


@router.get(f'/bigorder_initbag/get', response_model=SBigorderInitbag, summary='获取单一礼包详情')
async def get_bigorder_initbag(bigorder_initbag_id: int) -> SBigorderInitbag:
    return d_db.get_bigorder_initbag(bigorder_initbag_id)


@router.get(f'/bigorder_initbag/filter', response_model=FilterResBigorderInitbag, summary='获取所有礼包详情')
async def filter_bigorder_initbag(
        id: Optional[str] = None,
        bag_name: Optional[str] = None,
        register_time: Optional[str] = None,
        tuan_id: Optional[str] = None,
        price_total: Optional[str] = None,
        invited_money: Optional[str] = None,
        layer_every: Optional[str] = None,
        layer_num: Optional[str] = None,
        grant_num: Optional[str] = None,
        bag_cont: Optional[str] = None,
        bag_type: Optional[str] = None,
        l_id: Optional[str] = None,
        l_bag_name: Optional[str] = None,
        l_register_time: Optional[str] = None,
        l_tuan_id: Optional[str] = None,
        l_price_total: Optional[str] = None,
        l_invited_money: Optional[str] = None,
        l_layer_every: Optional[str] = None,
        l_layer_num: Optional[str] = None,
        l_grant_num: Optional[str] = None,
        l_bag_cont: Optional[str] = None,
        l_bag_type: Optional[str] = None,
        s_bag_name: Optional[str] = None,
        s_bag_cont: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResBigorderInitbag:
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

    if register_time is not None:
        values = register_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['register_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['register_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['register_time_end'] = datetime.fromtimestamp(int(val))

    if tuan_id is not None:
        values = tuan_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['tuan_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['tuan_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['tuan_id_end'] = int(val)

    if price_total is not None:
        values = price_total.split(',')
        if len(values) == 1:
            val = values[0]
            items['price_total'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['price_total_start'] = int(val)

            val = values[1]
            if val != '':
                items['price_total_end'] = int(val)

    if invited_money is not None:
        values = invited_money.split(',')
        if len(values) == 1:
            val = values[0]
            items['invited_money'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['invited_money_start'] = int(val)

            val = values[1]
            if val != '':
                items['invited_money_end'] = int(val)

    if layer_every is not None:
        values = layer_every.split(',')
        if len(values) == 1:
            val = values[0]
            items['layer_every'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['layer_every_start'] = int(val)

            val = values[1]
            if val != '':
                items['layer_every_end'] = int(val)

    if layer_num is not None:
        values = layer_num.split(',')
        if len(values) == 1:
            val = values[0]
            items['layer_num'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['layer_num_start'] = int(val)

            val = values[1]
            if val != '':
                items['layer_num_end'] = int(val)

    if grant_num is not None:
        values = grant_num.split(',')
        if len(values) == 1:
            val = values[0]
            items['grant_num'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['grant_num_start'] = int(val)

            val = values[1]
            if val != '':
                items['grant_num_end'] = int(val)

    if bag_cont is not None:
        values = bag_cont.split(',')
        if len(values) == 1:
            val = values[0]
            items['bag_cont'] = val
        else:
            val = values[0]
            if val != '':
                items['bag_cont_start'] = val

            val = values[1]
            if val != '':
                items['bag_cont_end'] = val

    if bag_type is not None:
        values = bag_type.split(',')
        if len(values) == 1:
            val = values[0]
            items['bag_type'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['bag_type_start'] = int(val)

            val = values[1]
            if val != '':
                items['bag_type_end'] = int(val)

    if s_bag_name is not None:
        search_items['bag_name'] = '%' + s_bag_name + '%'

    if s_bag_cont is not None:
        search_items['bag_cont'] = '%' + s_bag_cont + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_bag_name is not None:
        values = l_bag_name.split(',')
        values = [val for val in values]
        set_items['bag_name'] = values

    if l_register_time is not None:
        values = l_register_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['register_time'] = values

    if l_tuan_id is not None:
        values = l_tuan_id.split(',')
        values = [int(val) for val in values]
        set_items['tuan_id'] = values

    if l_price_total is not None:
        values = l_price_total.split(',')
        values = [int(val) for val in values]
        set_items['price_total'] = values

    if l_invited_money is not None:
        values = l_invited_money.split(',')
        values = [int(val) for val in values]
        set_items['invited_money'] = values

    if l_layer_every is not None:
        values = l_layer_every.split(',')
        values = [int(val) for val in values]
        set_items['layer_every'] = values

    if l_layer_num is not None:
        values = l_layer_num.split(',')
        values = [int(val) for val in values]
        set_items['layer_num'] = values

    if l_grant_num is not None:
        values = l_grant_num.split(',')
        values = [int(val) for val in values]
        set_items['grant_num'] = values

    if l_bag_cont is not None:
        values = l_bag_cont.split(',')
        values = [val for val in values]
        set_items['bag_cont'] = values

    if l_bag_type is not None:
        values = l_bag_type.split(',')
        values = [int(val) for val in values]
        set_items['bag_type'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_bigorder_initbag(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_bigorder_initbag(items, search_items, set_items)

    return FilterResBigorderInitbag(data=data, total=c)


@router.get(f'/bigorder_log/filter', response_model=FilterResBigorderLog, summary='获取公排用户复购日志')
async def filter_bigorder_log(
        id: Optional[str] = None,
        register_time: Optional[str] = None,
        user_id: Optional[str] = None,
        price_total: Optional[str] = None,
        invited_money: Optional[str] = None,
        layer_every: Optional[str] = None,
        layer_num: Optional[str] = None,
        grant_num: Optional[str] = None,
        bag_cont: Optional[str] = None,
        l_id: Optional[str] = None,
        l_register_time: Optional[str] = None,
        l_user_id: Optional[str] = None,
        l_price_total: Optional[str] = None,
        l_invited_money: Optional[str] = None,
        l_layer_every: Optional[str] = None,
        l_layer_num: Optional[str] = None,
        l_grant_num: Optional[str] = None,
        l_bag_cont: Optional[str] = None,
        s_bag_cont: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResBigorderLog:
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

    if register_time is not None:
        values = register_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['register_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['register_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['register_time_end'] = datetime.fromtimestamp(int(val))

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

    if price_total is not None:
        values = price_total.split(',')
        if len(values) == 1:
            val = values[0]
            items['price_total'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['price_total_start'] = int(val)

            val = values[1]
            if val != '':
                items['price_total_end'] = int(val)

    if invited_money is not None:
        values = invited_money.split(',')
        if len(values) == 1:
            val = values[0]
            items['invited_money'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['invited_money_start'] = int(val)

            val = values[1]
            if val != '':
                items['invited_money_end'] = int(val)

    if layer_every is not None:
        values = layer_every.split(',')
        if len(values) == 1:
            val = values[0]
            items['layer_every'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['layer_every_start'] = int(val)

            val = values[1]
            if val != '':
                items['layer_every_end'] = int(val)

    if layer_num is not None:
        values = layer_num.split(',')
        if len(values) == 1:
            val = values[0]
            items['layer_num'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['layer_num_start'] = int(val)

            val = values[1]
            if val != '':
                items['layer_num_end'] = int(val)

    if grant_num is not None:
        values = grant_num.split(',')
        if len(values) == 1:
            val = values[0]
            items['grant_num'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['grant_num_start'] = int(val)

            val = values[1]
            if val != '':
                items['grant_num_end'] = int(val)

    if bag_cont is not None:
        values = bag_cont.split(',')
        if len(values) == 1:
            val = values[0]
            items['bag_cont'] = val
        else:
            val = values[0]
            if val != '':
                items['bag_cont_start'] = val

            val = values[1]
            if val != '':
                items['bag_cont_end'] = val

    if s_bag_cont is not None:
        search_items['bag_cont'] = '%' + s_bag_cont + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_register_time is not None:
        values = l_register_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['register_time'] = values

    if l_user_id is not None:
        values = l_user_id.split(',')
        values = [int(val) for val in values]
        set_items['user_id'] = values

    if l_price_total is not None:
        values = l_price_total.split(',')
        values = [int(val) for val in values]
        set_items['price_total'] = values

    if l_invited_money is not None:
        values = l_invited_money.split(',')
        values = [int(val) for val in values]
        set_items['invited_money'] = values

    if l_layer_every is not None:
        values = l_layer_every.split(',')
        values = [int(val) for val in values]
        set_items['layer_every'] = values

    if l_layer_num is not None:
        values = l_layer_num.split(',')
        values = [int(val) for val in values]
        set_items['layer_num'] = values

    if l_grant_num is not None:
        values = l_grant_num.split(',')
        values = [int(val) for val in values]
        set_items['grant_num'] = values

    if l_bag_cont is not None:
        values = l_bag_cont.split(',')
        values = [val for val in values]
        set_items['bag_cont'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_bigorder_log(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_bigorder_log(items, search_items, set_items)

    return FilterResBigorderLog(data=data, total=c)