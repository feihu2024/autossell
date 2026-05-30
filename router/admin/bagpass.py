from dao import d_db, d_supplier, d_user, d_account, d_bagpass
from fastapi import APIRouter, Depends, Header, Request
from model import m_schema, schema
from model.m_schema import *
from router.mall import user
from typing import Optional, List
from router import r_schema
from router.admin.user import verify_token
from common import global_define, global_function
from fastapi import HTTPException
from pydantic import BaseModel, Field
import re

router = APIRouter(dependencies=[Depends(verify_token)])

class CreateBagPas_w(BaseModel):
    # pass_num: Optional[str] = Field(title='加密编号(十六进制)')
    # pc_name: Optional[str] = Field(title='批次名称')
    pc_num: Optional[int] = Field(title='批次数量')
    pc_id: Optional[int] = Field(title='批次id(不可重复)')
    # stat: Optional[int] = Field(title='是否激活,默认0未激活1已激活2过期未用')
    # register_time: Optional[datetime] = Field(title='创建时间')
    # startime: Optional[datetime] = Field(title='激活时间')
    # user_id: Optional[int] = Field(title='激活会员id')
    endtime: Optional[datetime] = Field(title='结束时间')
    # cate_id: Optional[int] = Field(title='批次分类id')

class CreateBagCagegory_w(BaseModel):
    pc_name: Optional[str] = Field(title='批次名称')
    pc_num: Optional[int] = Field(title='批次数量')
    endtime: Optional[datetime] = Field(title='结束时间')
    bag_id: Optional[int] = Field(title='礼包id')

class BagPasActive(BaseModel):
    pc_code: Optional[str] = Field(title='卡密码，十六进制编码')
    user_id: Optional[int] = Field(title='激活会员id')

@router.post(f'/bag_cagegory/create', summary="创建卡密批次分类")
async def create_bag_cagegory(item: CreateBagCagegory_w):
    save_item = schema.TBagCagegory(
        pc_name=item.pc_name,
        pc_num=item.pc_num,
        endtime=item.endtime,
        bag_id=item.bag_id
    )
    return d_bagpass.insert_bagpass(save_item)

# @router.post(f'/bag_cagegory/update', response_model=str, summary="修改卡密批次分类")
# async def update_bag_cagegory(item: SBagCagegory) -> str:
#     d_db.update_bag_cagegory(item)
#     return "success"


@router.get(f'/bag_cagegory/filter', response_model=FilterResBagCagegory, summary="分页获取卡密批次分类列表")
async def filter_bag_cagegory(
        id: Optional[str] = None,
        pc_name: Optional[str] = None,
        pc_num: Optional[str] = None,
        register_time: Optional[str] = None,
        endtime: Optional[str] = None,
        bag_id: Optional[str] = None,
        l_id: Optional[str] = None,
        l_pc_name: Optional[str] = None,
        l_pc_num: Optional[str] = None,
        l_register_time: Optional[str] = None,
        l_endtime: Optional[str] = None,
        l_bag_id: Optional[str] = None,
        s_pc_name: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResBagCagegory:
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

    if pc_name is not None:
        values = pc_name.split(',')
        if len(values) == 1:
            val = values[0]
            items['pc_name'] = val
        else:
            val = values[0]
            if val != '':
                items['pc_name_start'] = val

            val = values[1]
            if val != '':
                items['pc_name_end'] = val

    if pc_num is not None:
        values = pc_num.split(',')
        if len(values) == 1:
            val = values[0]
            items['pc_num'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['pc_num_start'] = int(val)

            val = values[1]
            if val != '':
                items['pc_num_end'] = int(val)

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

    if endtime is not None:
        values = endtime.split(',')
        if len(values) == 1:
            val = values[0]
            items['endtime'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['endtime_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['endtime_end'] = datetime.fromtimestamp(int(val))

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

    if s_pc_name is not None:
        search_items['pc_name'] = '%' + s_pc_name + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_pc_name is not None:
        values = l_pc_name.split(',')
        values = [val for val in values]
        set_items['pc_name'] = values

    if l_pc_num is not None:
        values = l_pc_num.split(',')
        values = [int(val) for val in values]
        set_items['pc_num'] = values

    if l_register_time is not None:
        values = l_register_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['register_time'] = values

    if l_endtime is not None:
        values = l_endtime.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['endtime'] = values

    if l_bag_id is not None:
        values = l_bag_id.split(',')
        values = [int(val) for val in values]
        set_items['bag_id'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_bag_cagegory(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_bag_cagegory(items, search_items, set_items)

    return FilterResBagCagegory(data=data, total=c)

@router.get(f'/bag_pas/filter', response_model=FilterResBagPas, summary="分页获取卡密列表")
async def filter_bag_pas(
        id: Optional[str] = None,
        pass_num: Optional[str] = None,
        pc_name: Optional[str] = None,
        pc_num: Optional[str] = None,
        pc_id: Optional[str] = None,
        stat: Optional[str] = None,
        register_time: Optional[str] = None,
        startime: Optional[str] = None,
        user_id: Optional[str] = None,
        endtime: Optional[str] = None,
        cate_id: Optional[str] = None,
        l_id: Optional[str] = None,
        l_pass_num: Optional[str] = None,
        l_pc_name: Optional[str] = None,
        l_pc_num: Optional[str] = None,
        l_pc_id: Optional[str] = None,
        l_stat: Optional[str] = None,
        l_register_time: Optional[str] = None,
        l_startime: Optional[str] = None,
        l_user_id: Optional[str] = None,
        l_endtime: Optional[str] = None,
        l_cate_id: Optional[str] = None,
        s_pass_num: Optional[str] = None,
        s_pc_name: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResBagPas:
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

    if pass_num is not None:
        values = pass_num.split(',')
        if len(values) == 1:
            val = values[0]
            items['pass_num'] = val
        else:
            val = values[0]
            if val != '':
                items['pass_num_start'] = val

            val = values[1]
            if val != '':
                items['pass_num_end'] = val

    if pc_name is not None:
        values = pc_name.split(',')
        if len(values) == 1:
            val = values[0]
            items['pc_name'] = val
        else:
            val = values[0]
            if val != '':
                items['pc_name_start'] = val

            val = values[1]
            if val != '':
                items['pc_name_end'] = val

    if pc_num is not None:
        values = pc_num.split(',')
        if len(values) == 1:
            val = values[0]
            items['pc_num'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['pc_num_start'] = int(val)

            val = values[1]
            if val != '':
                items['pc_num_end'] = int(val)

    if pc_id is not None:
        values = pc_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['pc_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['pc_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['pc_id_end'] = int(val)

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

    if startime is not None:
        values = startime.split(',')
        if len(values) == 1:
            val = values[0]
            items['startime'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['startime_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['startime_end'] = datetime.fromtimestamp(int(val))

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

    if endtime is not None:
        values = endtime.split(',')
        if len(values) == 1:
            val = values[0]
            items['endtime'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['endtime_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['endtime_end'] = datetime.fromtimestamp(int(val))

    if cate_id is not None:
        values = cate_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['cate_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['cate_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['cate_id_end'] = int(val)

    if s_pass_num is not None:
        search_items['pass_num'] = '%' + s_pass_num + '%'

    if s_pc_name is not None:
        search_items['pc_name'] = '%' + s_pc_name + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_pass_num is not None:
        values = l_pass_num.split(',')
        values = [val for val in values]
        set_items['pass_num'] = values

    if l_pc_name is not None:
        values = l_pc_name.split(',')
        values = [val for val in values]
        set_items['pc_name'] = values

    if l_pc_num is not None:
        values = l_pc_num.split(',')
        values = [int(val) for val in values]
        set_items['pc_num'] = values

    if l_pc_id is not None:
        values = l_pc_id.split(',')
        values = [int(val) for val in values]
        set_items['pc_id'] = values

    if l_stat is not None:
        values = l_stat.split(',')
        values = [int(val) for val in values]
        set_items['stat'] = values

    if l_register_time is not None:
        values = l_register_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['register_time'] = values

    if l_startime is not None:
        values = l_startime.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['startime'] = values

    if l_user_id is not None:
        values = l_user_id.split(',')
        values = [int(val) for val in values]
        set_items['user_id'] = values

    if l_endtime is not None:
        values = l_endtime.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['endtime'] = values

    if l_cate_id is not None:
        values = l_cate_id.split(',')
        values = [int(val) for val in values]
        set_items['cate_id'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_bag_pas(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_bag_pas(items, search_items, set_items)

    return FilterResBagPas(data=data, total=c)


@router.post(f'/bag_pas/create', summary="创建卡密列，一个批次只能创建一次")
async def create_bag_pas(item: CreateBagPas_w):
    '''
        pc_num: Optional[int] = Field(title='批次数量')
        pc_id: Optional[int] = Field(title='批次id(不可重复)')
        endtime: Optional[datetime.datetime] = Field(title='结束时间')
    '''
    if not item.pc_id or not item.pc_num or not item.endtime:
        raise HTTPException(status_code=404, detail='参数错误')
    pc_ls = d_db.get_bag_cagegory(item.pc_id)
    if not pc_ls:
        raise HTTPException(status_code=404, detail=f"未找到批次分类:{item.pc_id}")
    if d_bagpass.find_pc(item.pc_id):
        raise HTTPException(status_code=404, detail=f"该批次分类已经创建:{item.pc_id}")
    total = item.pc_num + 1
    for i in range(1, total):
        pass_num = global_function.get_num32_randoms()

        save_item = schema.TBagPas(
            pass_num=pass_num,
            pc_name=pc_ls.pc_name,
            pc_num=item.pc_num,
            pc_id=pc_ls.id,
            endtime=item.endtime
        )
        d_bagpass.insert_bagpass_list(save_item)

        # insert_res = d_db.insert_roomgold(CreateRoomgold(
        #     level=1,
        #     start_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #     status_val=1,
        #     balance=room_config['room_balance'],
        #     partner_id=parent_room_id,
        #     position_one=user_id,
        #     position_one_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # ))
        # return insert_res

    return {'code': 200, 'message': 'success'}

@router.post(f'/bag_pas/active', summary="密列激活")
async def create_bag_active(item: BagPasActive):
    '''
    pc_code: Optional[str] = Field(title='卡密码，十六进制编码')
    user_id: Optional[int] = Field(title='激活会员id')
    '''
    pas_info = d_bagpass.find_pc_for_num(item.pc_code)
    if not  pas_info:
        raise HTTPException(status_code=404, detail='参数错误')
    if pas_info.stat != 0:
        raise HTTPException(status_code=404, detail='卡密码,有误！')
    u_info = d_user.get_user_by_id(item.user_id)
    if not u_info:
        raise HTTPException(status_code=404, detail='未知用户')
    #更新
    d_bagpass.bagpass_active(item.pc_code, item.user_id)
    return {'code': 200, 'message': 'success'}