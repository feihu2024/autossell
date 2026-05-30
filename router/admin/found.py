from dao import d_db, d_user, d_account, d_found
from fastapi import APIRouter, Depends, Header, Request
from model import m_schema, schema
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
# class BagPasActive(BaseModel):
#     pc_code: Optional[str] = Field(title='卡密码，十六进制编码')
#     user_id: Optional[int] = Field(title='激活会员id')


@router.get(f'/fund_pond/get', response_model=SFundPond, summary="获取周期资金池详情")
async def get_fund_pond(fund_pond_id: int) -> SFundPond:
    return d_db.get_fund_pond(fund_pond_id)

@router.get(f'/fund_pond/filter', response_model=FilterResFundPond, summary="获取周期资金池列表，可查询")
async def filter_fund_pond(
        id: Optional[str] = None,
        date_num: Optional[str] = None,
        stat: Optional[str] = None,
        balance: Optional[str] = None,
        run_balance: Optional[str] = None,
        register_time: Optional[str] = None,
        end_time: Optional[str] = None,
        run_time: Optional[str] = None,
        users: Optional[str] = None,
        detail: Optional[str] = None,
        l_id: Optional[str] = None,
        l_date_num: Optional[str] = None,
        l_stat: Optional[str] = None,
        l_balance: Optional[str] = None,
        l_run_balance: Optional[str] = None,
        l_register_time: Optional[str] = None,
        l_end_time: Optional[str] = None,
        l_run_time: Optional[str] = None,
        l_users: Optional[str] = None,
        l_detail: Optional[str] = None,
        s_date_num: Optional[str] = None,
        s_users: Optional[str] = None,
        s_detail: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResFundPond:
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

    if date_num is not None:
        values = date_num.split(',')
        if len(values) == 1:
            val = values[0]
            items['date_num'] = val
        else:
            val = values[0]
            if val != '':
                items['date_num_start'] = val

            val = values[1]
            if val != '':
                items['date_num_end'] = val

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

    if balance is not None:
        values = balance.split(',')
        if len(values) == 1:
            val = values[0]
            items['balance'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['balance_start'] = int(val)

            val = values[1]
            if val != '':
                items['balance_end'] = int(val)

    if run_balance is not None:
        values = run_balance.split(',')
        if len(values) == 1:
            val = values[0]
            items['run_balance'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['run_balance_start'] = int(val)

            val = values[1]
            if val != '':
                items['run_balance_end'] = int(val)

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

    if end_time is not None:
        values = end_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['end_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['end_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['end_time_end'] = datetime.fromtimestamp(int(val))

    if run_time is not None:
        values = run_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['run_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['run_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['run_time_end'] = datetime.fromtimestamp(int(val))

    if users is not None:
        values = users.split(',')
        if len(values) == 1:
            val = values[0]
            items['users'] = val
        else:
            val = values[0]
            if val != '':
                items['users_start'] = val

            val = values[1]
            if val != '':
                items['users_end'] = val

    if detail is not None:
        values = detail.split(',')
        if len(values) == 1:
            val = values[0]
            items['detail'] = val
        else:
            val = values[0]
            if val != '':
                items['detail_start'] = val

            val = values[1]
            if val != '':
                items['detail_end'] = val

    if s_date_num is not None:
        search_items['date_num'] = '%' + s_date_num + '%'

    if s_users is not None:
        search_items['users'] = '%' + s_users + '%'

    if s_detail is not None:
        search_items['detail'] = '%' + s_detail + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_date_num is not None:
        values = l_date_num.split(',')
        values = [val for val in values]
        set_items['date_num'] = values

    if l_stat is not None:
        values = l_stat.split(',')
        values = [int(val) for val in values]
        set_items['stat'] = values

    if l_balance is not None:
        values = l_balance.split(',')
        values = [int(val) for val in values]
        set_items['balance'] = values

    if l_run_balance is not None:
        values = l_run_balance.split(',')
        values = [int(val) for val in values]
        set_items['run_balance'] = values

    if l_register_time is not None:
        values = l_register_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['register_time'] = values

    if l_end_time is not None:
        values = l_end_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['end_time'] = values

    if l_run_time is not None:
        values = l_run_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['run_time'] = values

    if l_users is not None:
        values = l_users.split(',')
        values = [val for val in values]
        set_items['users'] = values

    if l_detail is not None:
        values = l_detail.split(',')
        values = [val for val in values]
        set_items['detail'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_fund_pond(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_fund_pond(items, search_items, set_items)

    return FilterResFundPond(data=data, total=c)

@router.get(f'/fund_pond_log/get', response_model=SFundPondLog, summary="某一单资金归集详情")
async def get_fund_pond_log(fund_pond_log_id: int) -> SFundPondLog:
    return d_db.get_fund_pond_log(fund_pond_log_id)

@router.get(f'/fund_pond_log/filter', response_model=FilterResFundPondLog, summary="获取资金归集日志列表，可查询")
async def filter_fund_pond_log(
        id: Optional[str] = None,
        add_balance: Optional[str] = None,
        all_balance: Optional[str] = None,
        register_time: Optional[str] = None,
        source_id: Optional[str] = None,
        source_cont: Optional[str] = None,
        l_id: Optional[str] = None,
        l_add_balance: Optional[str] = None,
        l_all_balance: Optional[str] = None,
        l_register_time: Optional[str] = None,
        l_source_id: Optional[str] = None,
        l_source_cont: Optional[str] = None,
        s_source_cont: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResFundPondLog:
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

    if add_balance is not None:
        values = add_balance.split(',')
        if len(values) == 1:
            val = values[0]
            items['add_balance'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['add_balance_start'] = int(val)

            val = values[1]
            if val != '':
                items['add_balance_end'] = int(val)

    if all_balance is not None:
        values = all_balance.split(',')
        if len(values) == 1:
            val = values[0]
            items['all_balance'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['all_balance_start'] = int(val)

            val = values[1]
            if val != '':
                items['all_balance_end'] = int(val)

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

    if source_id is not None:
        values = source_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['source_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['source_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['source_id_end'] = int(val)

    if source_cont is not None:
        values = source_cont.split(',')
        if len(values) == 1:
            val = values[0]
            items['source_cont'] = val
        else:
            val = values[0]
            if val != '':
                items['source_cont_start'] = val

            val = values[1]
            if val != '':
                items['source_cont_end'] = val

    if s_source_cont is not None:
        search_items['source_cont'] = '%' + s_source_cont + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_add_balance is not None:
        values = l_add_balance.split(',')
        values = [int(val) for val in values]
        set_items['add_balance'] = values

    if l_all_balance is not None:
        values = l_all_balance.split(',')
        values = [int(val) for val in values]
        set_items['all_balance'] = values

    if l_register_time is not None:
        values = l_register_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['register_time'] = values

    if l_source_id is not None:
        values = l_source_id.split(',')
        values = [int(val) for val in values]
        set_items['source_id'] = values

    if l_source_cont is not None:
        values = l_source_cont.split(',')
        values = [val for val in values]
        set_items['source_cont'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_fund_pond_log(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_fund_pond_log(items, search_items, set_items)

    return FilterResFundPondLog(data=data, total=c)


@router.get(f'/fund_weight_log/get', response_model=SFundWeightLog, summary="获取权重详情")
async def get_fund_weight_log(fund_weight_log_id: int) -> SFundWeightLog:
    return d_db.get_fund_weight_log(fund_weight_log_id)

@router.get(f'/fund_weight_log/filter', response_model=FilterResFundWeightLog, summary="获取权重增加列表，可查询")
async def filter_fund_weight_log(
        id: Optional[str] = None,
        register_time: Optional[str] = None,
        user_id: Optional[str] = None,
        user_phone: Optional[str] = None,
        weight: Optional[str] = None,
        all_balance: Optional[str] = None,
        add_rec: Optional[str] = None,
        all_rec: Optional[str] = None,
        source_id: Optional[str] = None,
        l_id: Optional[str] = None,
        l_register_time: Optional[str] = None,
        l_user_id: Optional[str] = None,
        l_user_phone: Optional[str] = None,
        l_weight: Optional[str] = None,
        l_all_balance: Optional[str] = None,
        l_add_rec: Optional[str] = None,
        l_all_rec: Optional[str] = None,
        l_source_id: Optional[str] = None,
        s_user_phone: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResFundWeightLog:
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

    if weight is not None:
        values = weight.split(',')
        if len(values) == 1:
            val = values[0]
            items['weight'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['weight_start'] = int(val)

            val = values[1]
            if val != '':
                items['weight_end'] = int(val)

    if all_balance is not None:
        values = all_balance.split(',')
        if len(values) == 1:
            val = values[0]
            items['all_balance'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['all_balance_start'] = int(val)

            val = values[1]
            if val != '':
                items['all_balance_end'] = int(val)

    if add_rec is not None:
        values = add_rec.split(',')
        if len(values) == 1:
            val = values[0]
            items['add_rec'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['add_rec_start'] = int(val)

            val = values[1]
            if val != '':
                items['add_rec_end'] = int(val)

    if all_rec is not None:
        values = all_rec.split(',')
        if len(values) == 1:
            val = values[0]
            items['all_rec'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['all_rec_start'] = int(val)

            val = values[1]
            if val != '':
                items['all_rec_end'] = int(val)

    if source_id is not None:
        values = source_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['source_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['source_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['source_id_end'] = int(val)

    if s_user_phone is not None:
        search_items['user_phone'] = '%' + s_user_phone + '%'

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

    if l_user_phone is not None:
        values = l_user_phone.split(',')
        values = [val for val in values]
        set_items['user_phone'] = values

    if l_weight is not None:
        values = l_weight.split(',')
        values = [int(val) for val in values]
        set_items['weight'] = values

    if l_all_balance is not None:
        values = l_all_balance.split(',')
        values = [int(val) for val in values]
        set_items['all_balance'] = values

    if l_add_rec is not None:
        values = l_add_rec.split(',')
        values = [int(val) for val in values]
        set_items['add_rec'] = values

    if l_all_rec is not None:
        values = l_all_rec.split(',')
        values = [int(val) for val in values]
        set_items['all_rec'] = values

    if l_source_id is not None:
        values = l_source_id.split(',')
        values = [int(val) for val in values]
        set_items['source_id'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_fund_weight_log(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_fund_weight_log(items, search_items, set_items)

    return FilterResFundWeightLog(data=data, total=c)

@router.get(f'/fund_zqlog/get', response_model=SFundZqlog, summary="获取执行日志详情")
async def get_fund_zqlog(fund_zqlog_id: int) -> SFundZqlog:
    return d_db.get_fund_zqlog(fund_zqlog_id)

@router.get(f'/fund_zqlog/filter', response_model=FilterResFundZqlog, summary="获取执行日志列表")
async def filter_fund_zqlog(
        id: Optional[str] = None,
        zhouqi: Optional[str] = None,
        balance: Optional[str] = None,
        register_time: Optional[str] = None,
        fenpei_num: Optional[str] = None,
        status: Optional[str] = None,
        fenpei_users: Optional[str] = None,
        user_id: Optional[str] = None,
        balance_pro: Optional[str] = None,
        l_id: Optional[str] = None,
        l_zhouqi: Optional[str] = None,
        l_balance: Optional[str] = None,
        l_register_time: Optional[str] = None,
        l_fenpei_num: Optional[str] = None,
        l_status: Optional[str] = None,
        l_fenpei_users: Optional[str] = None,
        l_user_id: Optional[str] = None,
        l_balance_pro: Optional[str] = None,
        s_fenpei_users: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResFundZqlog:
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

    if zhouqi is not None:
        values = zhouqi.split(',')
        if len(values) == 1:
            val = values[0]
            items['zhouqi'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['zhouqi_start'] = int(val)

            val = values[1]
            if val != '':
                items['zhouqi_end'] = int(val)

    if balance is not None:
        values = balance.split(',')
        if len(values) == 1:
            val = values[0]
            items['balance'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['balance_start'] = int(val)

            val = values[1]
            if val != '':
                items['balance_end'] = int(val)

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

    if fenpei_num is not None:
        values = fenpei_num.split(',')
        if len(values) == 1:
            val = values[0]
            items['fenpei_num'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['fenpei_num_start'] = int(val)

            val = values[1]
            if val != '':
                items['fenpei_num_end'] = int(val)

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

    if fenpei_users is not None:
        values = fenpei_users.split(',')
        if len(values) == 1:
            val = values[0]
            items['fenpei_users'] = val
        else:
            val = values[0]
            if val != '':
                items['fenpei_users_start'] = val

            val = values[1]
            if val != '':
                items['fenpei_users_end'] = val

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

    if balance_pro is not None:
        values = balance_pro.split(',')
        if len(values) == 1:
            val = values[0]
            items['balance_pro'] = float(val)
        else:
            val = values[0]
            if val != '':
                items['balance_pro_start'] = float(val)

            val = values[1]
            if val != '':
                items['balance_pro_end'] = float(val)

    if s_fenpei_users is not None:
        search_items['fenpei_users'] = '%' + s_fenpei_users + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_zhouqi is not None:
        values = l_zhouqi.split(',')
        values = [int(val) for val in values]
        set_items['zhouqi'] = values

    if l_balance is not None:
        values = l_balance.split(',')
        values = [int(val) for val in values]
        set_items['balance'] = values

    if l_register_time is not None:
        values = l_register_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['register_time'] = values

    if l_fenpei_num is not None:
        values = l_fenpei_num.split(',')
        values = [int(val) for val in values]
        set_items['fenpei_num'] = values

    if l_status is not None:
        values = l_status.split(',')
        values = [int(val) for val in values]
        set_items['status'] = values

    if l_fenpei_users is not None:
        values = l_fenpei_users.split(',')
        values = [val for val in values]
        set_items['fenpei_users'] = values

    if l_user_id is not None:
        values = l_user_id.split(',')
        values = [int(val) for val in values]
        set_items['user_id'] = values

    if l_balance_pro is not None:
        values = l_balance_pro.split(',')
        values = [float(val) for val in values]
        set_items['balance_pro'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_fund_zqlog(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_fund_zqlog(items, search_items, set_items)

    return FilterResFundZqlog(data=data, total=c)

@router.get(f'/fund_pond/run', summary="执行资金池分润")
async def get_fund_pond_run(fund_id: int):
    fund_info = d_found.get_fund_by_id(fund_id)
    if not fund_info:
        raise HTTPException(status_code=203, detail='未知资金池！')
    if fund_info.stat != 0:
        raise HTTPException(status_code=203, detail='执行资金池错误！')

    # send_time = user_phone_code[0].send_time
    #         seconds = user_phone_code[0].expired_time
    #         time_now = datetime.datetime.now()
    #         over_time = send_time + datetime.timedelta(seconds=seconds)
    #         if time_now > over_time:
    #             raise HTTPException(status_code=201, detail='验证码过期')

    #更新资金池合法分钱会员
    fund_info = None
    d_found.update_fund_users()

    #用户分润
    fund_info = d_found.get_fund_by_id(fund_id)
    balance = fund_info.balance
    if fund_info.users:
        fund_info.users.strip()
    if fund_info.users:
        user_list = fund_info.users.split(',')
        weight_total = d_user.get_fund_user_count(user_list)
        for i in user_list:
            u_info = d_user.get_user_by_id(i)
            account_info = d_account.get_account_info(i)
            if account_info and u_info:
                prop = round(u_info.fund_weight_num / weight_total, 2)
                # 向上取整：math.ceil()
                # 向下取整：math.floor()
                # 四舍五入：round()
                this_balance = math.floor(balance * prop)
                balance -= this_balance
                #给用户增加余额
                total_balance = account_info.balance + this_balance
                d_account.update_account_by_id(account_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=u_info.id,
                    change=this_balance,
                    balance=total_balance,
                    type=global_define.balance_type[17],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(fund_id),
                    good_title=fund_info.date_num,
                    good_num=str(1),
                    out_trade_no=''
                ))
                #增加分润记录
                d_found.add_fund_zqlog(d_found.FundZqlogModel(
                    zhouqi=fund_info.id,
                    balance=this_balance,
                    fenpei_num=len(user_list),
                    status=0,
                    fenpei_users=f"余额：{total_balance}",
                    user_id=u_info.id,
                    balance_pro=prop
                ))
    # 更新资金池状态
    d_found.update_fund_by_id(fund_info.id, {"stat":1, "run_time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
    #创建新的资金池
    if fund_info.ftype == 0:
        d_found.create_fund()
    elif fund_info.ftype == 1:
        d_found.create_fund(2)
    elif fund_info.ftype == 2:
        d_found.create_fund(3)

    return {'code': 200, 'detail': 'success'}


@router.get(f'/fund_pond/run/users', summary="更新资金池分润对象")
async def get_fund_pond_run(fund_id: int):
    #更新资金池合法分钱会员
    d_found.update_fund_users_for_id(fund_id)
    return {'code': 200, 'detail': 'success'}


@router.get(f'/fund_pond/prop/fund', summary="更新用户三个资金池分润预测金额")
async def get_prop_fund():
    #更新资金池合法分钱会员
    d_found.update_prop_balance_to_user()
    return {'code': 200, 'detail': 'success'}

