from dao import d_db, d_user, d_account, d_found, d_video_task, d_good, d_adbrand
from fastapi import APIRouter, Depends, Header, Request
import logging
from model.m_schema import *
from typing import Optional, List
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
class CreateUserAdbrandAndMenu(BaseModel):
    user_adbrand: Optional[CreateUserAdbrand] = Field(None, title='创建广告模板结构')
    user_adbrand_menu: List[CreateUserAdbrandMenu] = Field(None, title='创建项目模板菜单结构')

class UpdateUserAdbrandAndMenu(BaseModel):
    user_adbrand: Optional[SUserAdbrand] = Field(None, title='修改广告模板结构')
    user_adbrand_menu: List[SUserAdbrandMenu] = Field(None, title='修改项目模板菜单结构')

@router.post(f'/adbrand/create', summary="创建品牌广告模板")
async def create_user_adbrand(item: CreateUserAdbrandAndMenu):
    logging.info('创建品牌广告模板，adbrand/create')
    # logging.info(item)
    re_val = {}
    dict_item = dict(item.user_adbrand)
    for k, v in dict_item.items():
        if v is not None:
            v = str(v)
            v = v.replace(" ", "")
            get_search = re.search(r"'", v, flags=0)
            get_search2 = re.search(r'%27', v, flags=0)
            get_search3 = re.search(r'unionselect', v, flags=0)
            if get_search or get_search2 or get_search3:
                raise HTTPException(status_code=404, detail='bad way~~~~~~')
    item.user_adbrand.is_default = 0
    re_val['user_adbrand'] = d_db.insert_user_adbrand(item.user_adbrand)
    # logging.info(re_val['user_adbrand'])
    menu_num = 1
    for item_menu in item.user_adbrand_menu:
        menu_key = f"user_adbrand_menu{menu_num}"
        item_menu.adbrand_id = re_val['user_adbrand'].id
        re_val[menu_key] = d_db.insert_user_adbrand_menu(item_menu)
        menu_num += 1
    # logging.info(re_val)
    return re_val


@router.post(f'/adbrand/update', response_model=str, summary="更新品牌广告模板")
async def update_user_adbrand(item: UpdateUserAdbrandAndMenu) -> str:
    logging.info('更新品牌广告模板，adbrand/update')
    d_db.update_user_adbrand(item.user_adbrand)
    for item_menu in item.user_adbrand_menu:
        if item_menu.id == 0:
            add_instance = CreateUserAdbrandMenu(
                adbrand_id=item.user_adbrand.id,
                m_name=item_menu.m_name,
                pic_url=item_menu.pic_url,
                m_title=item_menu.m_title,
                m_type=item_menu.m_type,
                text_one=item_menu.text_one,
                text_two=item_menu.text_two,
                is_del=item_menu.is_del,
                is_hide=item_menu.is_hide
            )
            d_db.insert_user_adbrand_menu(add_instance)
        else:
            d_db.update_user_adbrand_menu(item_menu)
    return "success"


@router.get(f'/adbrand/get', response_model=SUserAdbrand, summary="获取品牌广告模板详情")
async def get_user_adbrand(user_adbrand_id: int) -> SUserAdbrand:
    return d_db.get_user_adbrand(user_adbrand_id)

@router.get(f'/adbrand/del', summary="删除品牌模板")
async def get_user_adbrand_del(adbrand_id: int):
    d_adbrand.update_adbrand_ad_del(adbrand_id)
    return d_adbrand.del_brand(adbrand_id)

@router.get(f'/adbrand/set/default', summary="设置/取消默认品牌模板")
async def get_user_adbrand_default(adbrand_id: int, default:int=1):
    """
    default=1 设置默认，0取消
    """
    return d_adbrand.set_brand_default(adbrand_id, default)

@router.get(f'/adbrand/filter', response_model=FilterResUserAdbrand, summary="获取品牌广告列表")
async def filter_user_adbrand(
        id: Optional[str] = None,
        ad_id: Optional[str] = None,
        good_id: Optional[str] = None,
        is_del: Optional[str] = None,
        l_id: Optional[str] = None,
        l_is_del: Optional[str] = None,
        s_title: Optional[str] = None,
        s_describe: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResUserAdbrand:
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

    if ad_id is not None:
        values = ad_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['ad_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['ad_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['ad_id_end'] = int(val)

    if good_id is not None:
        values = good_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['good_id'] = val
        else:
            val = values[0]
            if val != '':
                items['good_id_start'] = val

            val = values[1]
            if val != '':
                items['good_id_end'] = val

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

    if s_title is not None:
        search_items['title'] = '%' + s_title + '%'

    if s_describe is not None:
        search_items['describe'] = '%' + s_describe + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_is_del is not None:
        values = l_is_del.split(',')
        values = [int(val) for val in values]
        set_items['is_del'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_user_adbrand(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_user_adbrand(items, search_items, set_items)

    return FilterResUserAdbrand(data=data, total=c)


@router.get(f'/user_adbrand/filter', response_model=FilterResUserAd, summary="获取用户配置的品牌广告分享页列表")
async def filter_user_ad(
        id: Optional[str] = None,
        user_id: Optional[str] = None,
        adbrand_id: Optional[str] = None,
        is_del: Optional[str] = None,
        l_id: Optional[str] = None,
        s_user_name: Optional[str] = None,
        s_user_phone: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResUserAd:
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

    if adbrand_id is not None:
        values = adbrand_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['adbrand_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['adbrand_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['adbrand_id_end'] = int(val)

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

    if s_user_name is not None:
        search_items['user_name'] = '%' + s_user_name + '%'

    if s_user_phone is not None:
        search_items['user_phone'] = '%' + s_user_phone + '%'

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
    data = d_db.filter_user_ad(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_user_ad(items, search_items, set_items)

    return FilterResUserAd(data=data, total=c)


@router.post(f'/user/ad/uinfo/update', response_model=str, summary="修改广告用户信息")
async def update_user_ad_uinfo(item: SUserAdUinfo) -> str:
    d_db.update_user_ad_uinfo(item)
    return "success"


@router.get(f'/user/ad/uinfo/get', response_model=SUserAdUinfo, summary="获取广告用户信息")
async def get_user_ad_uinfo(user_ad_uinfo_id: int) -> SUserAdUinfo:
    return d_db.get_user_ad_uinfo(user_ad_uinfo_id)

@router.get(f'/user/ad/uinfo/filter', response_model=FilterResUserAdUinfo, summary="获取广告用户信息列表")
async def filter_user_ad_uinfo(
        id: Optional[str] = None,
        user_id: Optional[str] = None,
        user_name: Optional[str] = None,
        user_phone: Optional[str] = None,
        is_del: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResUserAdUinfo:
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
    data = d_db.filter_user_ad_uinfo(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_user_ad_uinfo(items, search_items, set_items)

    return FilterResUserAdUinfo(data=data, total=c)

@router.get('/get/goods/list', summary='获取广告页商品列表')
async def get_goods_list(good_id:str = ''):
    """
    good_id，商品id，如：112,113,114,115
    """
    goods = []
    for t in good_id.split(','):
        try:
            nn = int(t)
            if nn > 0:
                goods.append(nn)
        except:
            pass
    if len(goods) > 0:
        return d_good.get_good_for_ids(goods)
    else:
        return '未找到商品！'


@router.post(f'/user/adbrand/file/create', response_model=SUserAdbrandFile, summary='创建品牌模板菜单的文件数据')
async def create_user_adbrand_file(item: CreateUserAdbrandFile) -> SUserAdbrandFile:
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

    return d_db.insert_user_adbrand_file(item)

@router.post(f'/user/adbrand/file/update', response_model=str, summary='修改品牌模板菜单的文件数据')
async def update_user_adbrand_file(item: SUserAdbrandFile) -> str:
    d_db.update_user_adbrand_file(item)
    return "success"

@router.get(f'/user/adbrand/file/filter', response_model=FilterResUserAdbrandFile, summary='获取品牌模板菜单的文件数据列表')
async def filter_user_adbrand_file(
        adbrand_id: Optional[str] = None,
        menu_id: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResUserAdbrandFile:
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

    if adbrand_id is not None:
        values = adbrand_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['adbrand_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['adbrand_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['adbrand_id_end'] = int(val)

    if menu_id is not None:
        values = menu_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['menu_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['menu_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['menu_id_end'] = int(val)
    items['is_del'] = 0
    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_user_adbrand_file(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_user_adbrand_file(items, search_items, set_items)

    return FilterResUserAdbrandFile(data=data, total=c)

@router.get(f'/user/adbrand/menu/filter', response_model=FilterResUserAdbrandMenu, summary='获取品牌模板菜单数据列表')
async def filter_user_adbrand_menu(
        adbrand_id: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResUserAdbrandMenu:
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

    if adbrand_id is not None:
        values = adbrand_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['adbrand_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['adbrand_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['adbrand_id_end'] = int(val)
    items['is_del'] = 0
    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_user_adbrand_menu(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_user_adbrand_menu(items, search_items, set_items)

    return FilterResUserAdbrandMenu(data=data, total=c)

@router.get(f'/user/adbrand/menu/del', response_model=str, summary='删除品牌模板菜单数据')
async def update_user_adbrand_menu_del(menu_id: int) -> str:
    d_adbrand.delete_menu_by_id(menu_id)
    return "success"
