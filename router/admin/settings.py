from typing import Optional

from fastapi import APIRouter
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query
from fastapi.exceptions import HTTPException

from common import Dao
from model.schema import TSetting, TCity
from model.m_schema import SSetting, SCity, CreateCity, SNotice, CreateNotice, FilterResNotice
from dao import d_settings, d_db
import re
from datetime import datetime

Base = declarative_base()
metadata = Base.metadata

router = APIRouter()

#
# @router.post(f'/update')
# async def update_settings(item: SSetting):
#     '''id序号，代表修改对应的字段：
#     1,recommend_num
#     2,flash_order_income
#     3,tuan_order_income
#     4,flash_order_max
#     5,flash_order_money_max
#     6,flash_order_active_user
#     7,consume_money_active_user
#     8,many_high_user
#     9,many_top_user
#     10,flash_order_income_retio
#     11,flash_order_income_layer
#     12,flash_order_income_toper
#     13,flash_order_income_groupsir
#     14,flash_order_owner_times
#     15,parent_user_limit
#     16,flash_order_income_subsidy
#     17,random_proportion
#     18,random_max success
#     19,random_low success
#     20,ws1_proportion
#     21,ws2_proportion
#     22,ws3_proportion
#     '''
#     res = {"status": 200, "message": "success"}
#     if item.id == 1:
#         d_settings.update_settings({"recommend_num": item.recommend_num})
#         res["message"] = "recommend_num success"
#     elif item.id == 2:
#         d_settings.update_settings({"flash_order_income": item.flash_order_income})
#         res["message"] = "flash_order_income success"
#     elif item.id == 3:
#         d_settings.update_settings({"tuan_order_income": item.tuan_order_income})
#         res["message"] = "tuan_order_income success"
#     elif item.id == 4:
#         d_settings.update_settings({"flash_order_max": item.flash_order_max})
#         res["message"] = "flash_order_max success"
#     elif item.id == 5:
#         d_settings.update_settings({"flash_order_money_max": item.flash_order_money_max})
#         res["message"] = "flash_order_money_max success"
#     elif item.id == 6:
#         d_settings.update_settings({"flash_order_active_user": item.flash_order_active_user})
#         res["message"] = "flash_order_active_user success"
#     elif item.id == 7:
#         d_settings.update_settings({"consume_money_active_user": item.consume_money_active_user})
#         res["message"] = "consume_money_active_user success"
#     elif item.id == 8:
#         d_settings.update_settings({"many_high_user": item.many_high_user})
#         res["message"] = "many_high_user success"
#     elif item.id == 9:
#         d_settings.update_settings({"many_top_user": item.many_top_user})
#         res["message"] = "many_top_user success"
#     elif item.id == 10:
#         d_settings.update_settings({"flash_order_income_retio": item.flash_order_income_retio})
#         res["message"] = "flash_order_income_retio success"
#     elif item.id == 11:
#         d_settings.update_settings({"flash_order_income_layer": item.flash_order_income_layer})
#         res["message"] = "flash_order_income_layer success"
#     elif item.id == 12:
#         d_settings.update_settings({"flash_order_income_toper": item.flash_order_income_toper})
#         res["message"] = "flash_order_income_toper success"
#     elif item.id == 13:
#         d_settings.update_settings({"flash_order_income_groupsir": item.flash_order_income_groupsir})
#         res["message"] = "flash_order_income_groupsir success"
#     elif item.id == 14:
#         d_settings.update_settings({"flash_order_owner_times": item.flash_order_owner_times})
#         res["message"] = "flash_order_owner_times success"
#     elif item.id == 15:
#         d_settings.update_settings({"parent_user_limit": item.parent_user_limit})
#         res["message"] = "parent_user_limit success"
#     elif item.id == 16:
#         d_settings.update_settings({"flash_order_income_subsidy": item.flash_order_income_subsidy})
#         res["message"] = "flash_order_income_subsidy success"
#     elif item.id == 17:
#         d_settings.update_settings({"random_proportion": item.random_proportion})
#         res["message"] = "random_proportion success"
#     elif item.id == 18:
#         d_settings.update_settings({"random_max": item.random_max})
#         res["message"] = "random_max success"
#     elif item.id == 19:
#         d_settings.update_settings({"random_low": item.random_low})
#         res["message"] = "random_low success"
#     elif item.id == 20:
#         d_settings.update_settings({"ws1_proportion": item.ws1_proportion})
#         res["message"] = "ws1_proportion success"
#     elif item.id == 21:
#         d_settings.update_settings({"ws2_proportion": item.ws2_proportion})
#         res["message"] = "ws2_proportion success"
#     elif item.id == 22:
#         d_settings.update_settings({"ws3_proportion": item.ws3_proportion})
#         res["message"] = "ws3_proportion success"
#     return res
#
# @router.get(f'/get', response_model=SSetting)
# async def get_settings():
#     return d_settings.get_settings()
#
# @router.post(f'/add_city', summary='添加系统地理配置')
# async def add_city(data: CreateCity):
#     search_city = d_settings.get_city_by_name(data.cname)
#     if not search_city:
#         if data.parid is None:
#             data.parid = 0
#         if data.status is None:
#             data.status = 0
#         d_settings.insert_city(data)
#         return {"status": 200, "data": f"{data.cname}, 创建成功"}
#     else:
#         return {"status": 200, "data": f"{data.cname}, 已经存在"}
#
# @router.post(f'/update_city', summary='修改系统地理配置')
# async def update_city(data: SCity):
#     search_city = d_settings.get_city_by_id(data.id)
#     re_data = {"status": 200, "data": f"{data.id},{data.cname}, 修改成功"}
#     if search_city:
#         if search_city.cname != data.cname:
#             d_settings.update_city_cname(data)
#         else:
#             re_data = {"status": 200, "data": f"{data.id},{data.cname}, 无需修改"}
#     else:
#         re_data = {"status": 200, "data": f"{data.cname}, 不存在"}
#     return re_data
#
# @router.post(f'/del_city', summary='删除系统地理配置')
# async def del_city():
#     pass
#
# @router.post(f'/get_city', summary='获取系统地理配置')
# async def get_city(parid:int = 0):
#     if parid is None:
#         parid = 0
#     if parid <=0:
#         return d_settings.get_city_tops()
#     else:
#         return d_settings.get_city_subs(parid)
#

@router.post(f'/notice/create', response_model=SNotice)
async def create_notice(item: CreateNotice) -> SNotice:
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

    return d_db.insert_notice(item)


@router.post(f'/notice/update', response_model=str)
async def update_notice(item: SNotice) -> str:
    d_db.update_notice(item)
    return "success"


@router.get(f'/notice/get', response_model=SNotice)
async def get_notice(notice_id: int) -> SNotice:
    return d_db.get_notice(notice_id)


@router.get(f'/notice/filter', response_model=FilterResNotice)
async def filter_notice(
        id: Optional[str] = None,
        user_ids: Optional[str] = None,
        type: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        register_time: Optional[str] = None,
        status: Optional[str] = None,
        l_id: Optional[str] = None,
        l_user_ids: Optional[str] = None,
        l_type: Optional[str] = None,
        l_title: Optional[str] = None,
        l_description: Optional[str] = None,
        l_register_time: Optional[str] = None,
        l_status: Optional[str] = None,
        s_user_ids: Optional[str] = None,
        s_type: Optional[str] = None,
        s_title: Optional[str] = None,
        s_description: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResNotice:
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

    if user_ids is not None:
        values = user_ids.split(',')
        if len(values) == 1:
            val = values[0]
            items['user_ids'] = val
        else:
            val = values[0]
            if val != '':
                items['user_ids_start'] = val

            val = values[1]
            if val != '':
                items['user_ids_end'] = val

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

    if status is not None:
        values = status.split(',')
        if len(values) == 1:
            val = values[0]
            items['status'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['status_start'] = int(val)

            val = values[1]
            if val != '':
                items['status_end'] = int(val)

    if s_user_ids is not None:
        search_items['user_ids'] = '%' + s_user_ids + '%'

    if s_type is not None:
        search_items['type'] = '%' + s_type + '%'

    if s_title is not None:
        search_items['title'] = '%' + s_title + '%'

    if s_description is not None:
        search_items['description'] = '%' + s_description + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_user_ids is not None:
        values = l_user_ids.split(',')
        values = [val for val in values]
        set_items['user_ids'] = values

    if l_type is not None:
        values = l_type.split(',')
        values = [val for val in values]
        set_items['type'] = values

    if l_title is not None:
        values = l_title.split(',')
        values = [val for val in values]
        set_items['title'] = values

    if l_description is not None:
        values = l_description.split(',')
        values = [val for val in values]
        set_items['description'] = values

    if l_register_time is not None:
        values = l_register_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['register_time'] = values

    if l_status is not None:
        values = l_status.split(',')
        values = [int(val) for val in values]
        set_items['status'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_notice(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_notice(items, search_items, set_items)

    return FilterResNotice(data=data, total=c)
