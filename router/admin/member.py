import datetime
from dao import d_db, d_supplier, d_user, d_account
from fastapi import APIRouter, Depends, Header, Request
from model.mall import m_supplier
from model import m_schema, schema
from model.m_schema import *
from router.mall import user
from typing import Optional, List
from router import r_schema
from service import wx_service
from model.res import auth
from service.auth_service import token_encode
from router.admin.user import verify_token
from common import global_define
from fastapi import HTTPException

router = APIRouter(dependencies=[Depends(verify_token)])

@router.get(f'/member/get', summary='返回某个用户的基本信息和账户信息')
async def get_user(user_id: int):
    re_data = {"user":None, "balance":None}
    re_data['user'] = d_user.get_user_by_id(user_id)
    re_data['balance'] = d_account.get_account_info(user_id)
    return re_data

@router.get(f'/member/get_user_level', summary='返回用户级别信息')
async def get_user_level():
    return global_define.users_level

@router.get(f'/member/get_user_wholesale', summary='返回用户身份信息')
async def get_user_wholesale():
    return global_define.wholesale_level


@router.post(f'/member/update', response_model=str, summary='修改用户的信息')
async def update_user(item: SUser) -> str:
    '''
    password/light_status/status/level_id ,不能在这里修改，需要删除提参
    '''
    # if item.password or item.status or item.light_status or item.level_id:
    if item.password or item.status or item.light_status:
        raise HTTPException(status_code=400, detail="password/light_status/status/level_id非法操作")
    d_db.update_user(item)
    return "success"

@router.post(f'/member/update_light_stat', response_model=str, summary='修改用户的熄灯状态')
async def update_light_stat(item: SUser) -> str:
    '''
    设置id和light_status
    '''
    d_user.update_light_status(item.id, item.light_status)
    return "success"

@router.post(f'/member/update_level_stat', response_model=str, summary='修改用户的级别')
async def update_level_stat(item: SUser) -> str:
    '''
    设置id和level_id
    '''
    d_user.update_level_status(item.id, item.level_id)
    return "success"

@router.get(f'/member/filter', response_model=FilterResUser, summary='用户列表/分身列表')
async def filter_user(
        id: Optional[str] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
        open_id: Optional[str] = None,
        union_id: Optional[str] = None,
        password: Optional[str] = None,
        nickname: Optional[str] = None,
        phone: Optional[str] = None,
        id_card: Optional[str] = None,
        level_id: Optional[str] = None,
        status: Optional[str] = None,
        register_time: Optional[str] = None,
        avatar: Optional[str] = None,
        invited_user_id: Optional[str] = None,
        coin: Optional[str] = None,
        gender: Optional[str] = None,
        last_active_time: Optional[str] = None,
        name: Optional[str] = None,
        is_agree: Optional[str] = None,
        parent_id: Optional[str] = None,
        parent_id_history: Optional[str] = None,
        level_one_time: Optional[str] = None,
        level_two_time: Optional[str] = None,
        level_three_time: Optional[str] = None,
        level_top_time: Optional[str] = None,
        wholesale_id: Optional[str] = None,
        wholesale_amount: Optional[str] = None,
        paidui: Optional[str] = None,
        tuan_id: Optional[str] = None,
        tran_pass: Optional[str] = None,
        invited_code: Optional[str] = None,
        bigorder_id: Optional[str] = None,
        layer_id: Optional[str] = None,
        cur_layer_id: Optional[str] = None,
        cur_layer_total: Optional[str] = None,
        bigorder_parent_id: Optional[str] = None,
        entrust_status: Optional[str] = None,
        light_status: Optional[str] = None,
        voucher_total: Optional[str] = None,
        endorders_total: Optional[str] = None,
        doubule_id: Optional[str] = None,
        entrust_startime: Optional[str] = None,
        entrust_endtime: Optional[str] = None,
        pai_buydui: Optional[str] = None,
        bagorder_num: Optional[str] = None,
        weight_num: Optional[str] = None,
        fund_weight_num: Optional[str] = None,
        video_level: Optional[str] = None,
        is_tuan: Optional[str] = None,
        ercode: Optional[str] = None,
        sh_agent: Optional[str] = None,
        l_id: Optional[str] = None,
        l_username: Optional[str] = None,
        l_email: Optional[str] = None,
        l_open_id: Optional[str] = None,
        l_union_id: Optional[str] = None,
        l_password: Optional[str] = None,
        l_nickname: Optional[str] = None,
        l_phone: Optional[str] = None,
        l_id_card: Optional[str] = None,
        l_level_id: Optional[str] = None,
        l_status: Optional[str] = None,
        l_register_time: Optional[str] = None,
        l_avatar: Optional[str] = None,
        l_invited_user_id: Optional[str] = None,
        l_coin: Optional[str] = None,
        l_gender: Optional[str] = None,
        l_last_active_time: Optional[str] = None,
        l_name: Optional[str] = None,
        l_is_agree: Optional[str] = None,
        l_parent_id: Optional[str] = None,
        l_parent_id_history: Optional[str] = None,
        l_level_one_time: Optional[str] = None,
        l_level_two_time: Optional[str] = None,
        l_level_three_time: Optional[str] = None,
        l_level_top_time: Optional[str] = None,
        l_wholesale_id: Optional[str] = None,
        l_wholesale_amount: Optional[str] = None,
        l_paidui: Optional[str] = None,
        l_tuan_id: Optional[str] = None,
        l_tran_pass: Optional[str] = None,
        l_invited_code: Optional[str] = None,
        l_bigorder_id: Optional[str] = None,
        l_layer_id: Optional[str] = None,
        l_cur_layer_id: Optional[str] = None,
        l_cur_layer_total: Optional[str] = None,
        l_bigorder_parent_id: Optional[str] = None,
        l_entrust_status: Optional[str] = None,
        l_light_status: Optional[str] = None,
        l_voucher_total: Optional[str] = None,
        l_endorders_total: Optional[str] = None,
        l_doubule_id: Optional[str] = None,
        l_entrust_startime: Optional[str] = None,
        l_entrust_endtime: Optional[str] = None,
        l_pai_buydui: Optional[str] = None,
        l_bagorder_num: Optional[str] = None,
        l_weight_num: Optional[str] = None,
        l_fund_weight_num: Optional[str] = None,
        l_video_level: Optional[str] = None,
        l_is_tuan: Optional[str] = None,
        l_ercode: Optional[str] = None,
        l_sh_agent: Optional[str] = None,
        s_username: Optional[str] = None,
        s_email: Optional[str] = None,
        s_open_id: Optional[str] = None,
        s_union_id: Optional[str] = None,
        s_password: Optional[str] = None,
        s_nickname: Optional[str] = None,
        s_phone: Optional[str] = None,
        s_id_card: Optional[str] = None,
        s_avatar: Optional[str] = None,
        s_name: Optional[str] = None,
        s_parent_id_history: Optional[str] = None,
        s_tran_pass: Optional[str] = None,
        s_invited_code: Optional[str] = None,
        s_ercode: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResUser:
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

    if username is not None:
        values = username.split(',')
        if len(values) == 1:
            val = values[0]
            items['username'] = val
        else:
            val = values[0]
            if val != '':
                items['username_start'] = val

            val = values[1]
            if val != '':
                items['username_end'] = val

    if email is not None:
        values = email.split(',')
        if len(values) == 1:
            val = values[0]
            items['email'] = val
        else:
            val = values[0]
            if val != '':
                items['email_start'] = val

            val = values[1]
            if val != '':
                items['email_end'] = val

    if open_id is not None:
        values = open_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['open_id'] = val
        else:
            val = values[0]
            if val != '':
                items['open_id_start'] = val

            val = values[1]
            if val != '':
                items['open_id_end'] = val

    if union_id is not None:
        values = union_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['union_id'] = val
        else:
            val = values[0]
            if val != '':
                items['union_id_start'] = val

            val = values[1]
            if val != '':
                items['union_id_end'] = val

    if password is not None:
        values = password.split(',')
        if len(values) == 1:
            val = values[0]
            items['password'] = val
        else:
            val = values[0]
            if val != '':
                items['password_start'] = val

            val = values[1]
            if val != '':
                items['password_end'] = val

    if nickname is not None:
        values = nickname.split(',')
        if len(values) == 1:
            val = values[0]
            items['nickname'] = val
        else:
            val = values[0]
            if val != '':
                items['nickname_start'] = val

            val = values[1]
            if val != '':
                items['nickname_end'] = val

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

    if id_card is not None:
        values = id_card.split(',')
        if len(values) == 1:
            val = values[0]
            items['id_card'] = val
        else:
            val = values[0]
            if val != '':
                items['id_card_start'] = val

            val = values[1]
            if val != '':
                items['id_card_end'] = val

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

    if avatar is not None:
        values = avatar.split(',')
        if len(values) == 1:
            val = values[0]
            items['avatar'] = val
        else:
            val = values[0]
            if val != '':
                items['avatar_start'] = val

            val = values[1]
            if val != '':
                items['avatar_end'] = val

    if invited_user_id is not None:
        values = invited_user_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['invited_user_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['invited_user_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['invited_user_id_end'] = int(val)

    if coin is not None:
        values = coin.split(',')
        if len(values) == 1:
            val = values[0]
            items['coin'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['coin_start'] = int(val)

            val = values[1]
            if val != '':
                items['coin_end'] = int(val)

    if gender is not None:
        values = gender.split(',')
        if len(values) == 1:
            val = values[0]
            items['gender'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['gender_start'] = int(val)

            val = values[1]
            if val != '':
                items['gender_end'] = int(val)

    if last_active_time is not None:
        values = last_active_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['last_active_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['last_active_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['last_active_time_end'] = datetime.fromtimestamp(int(val))

    if name is not None:
        values = name.split(',')
        if len(values) == 1:
            val = values[0]
            items['name'] = val
        else:
            val = values[0]
            if val != '':
                items['name_start'] = val

            val = values[1]
            if val != '':
                items['name_end'] = val

    if is_agree is not None:
        values = is_agree.split(',')
        if len(values) == 1:
            val = values[0]
            items['is_agree'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['is_agree_start'] = int(val)

            val = values[1]
            if val != '':
                items['is_agree_end'] = int(val)

    if parent_id is not None:
        values = parent_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['parent_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['parent_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['parent_id_end'] = int(val)

    if parent_id_history is not None:
        values = parent_id_history.split(',')
        if len(values) == 1:
            val = values[0]
            items['parent_id_history'] = val
        else:
            val = values[0]
            if val != '':
                items['parent_id_history_start'] = val

            val = values[1]
            if val != '':
                items['parent_id_history_end'] = val

    if level_one_time is not None:
        values = level_one_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['level_one_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['level_one_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['level_one_time_end'] = datetime.fromtimestamp(int(val))

    if level_two_time is not None:
        values = level_two_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['level_two_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['level_two_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['level_two_time_end'] = datetime.fromtimestamp(int(val))

    if level_three_time is not None:
        values = level_three_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['level_three_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['level_three_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['level_three_time_end'] = datetime.fromtimestamp(int(val))

    if level_top_time is not None:
        values = level_top_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['level_top_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['level_top_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['level_top_time_end'] = datetime.fromtimestamp(int(val))

    if wholesale_id is not None:
        values = wholesale_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['wholesale_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['wholesale_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['wholesale_id_end'] = int(val)

    if wholesale_amount is not None:
        values = wholesale_amount.split(',')
        if len(values) == 1:
            val = values[0]
            items['wholesale_amount'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['wholesale_amount_start'] = int(val)

            val = values[1]
            if val != '':
                items['wholesale_amount_end'] = int(val)

    if paidui is not None:
        values = paidui.split(',')
        if len(values) == 1:
            val = values[0]
            items['paidui'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['paidui_start'] = int(val)

            val = values[1]
            if val != '':
                items['paidui_end'] = int(val)

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

    if tran_pass is not None:
        values = tran_pass.split(',')
        if len(values) == 1:
            val = values[0]
            items['tran_pass'] = val
        else:
            val = values[0]
            if val != '':
                items['tran_pass_start'] = val

            val = values[1]
            if val != '':
                items['tran_pass_end'] = val

    if invited_code is not None:
        values = invited_code.split(',')
        if len(values) == 1:
            val = values[0]
            items['invited_code'] = val
        else:
            val = values[0]
            if val != '':
                items['invited_code_start'] = val

            val = values[1]
            if val != '':
                items['invited_code_end'] = val

    if bigorder_id is not None:
        values = bigorder_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['bigorder_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['bigorder_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['bigorder_id_end'] = int(val)

    if layer_id is not None:
        values = layer_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['layer_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['layer_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['layer_id_end'] = int(val)

    if cur_layer_id is not None:
        values = cur_layer_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['cur_layer_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['cur_layer_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['cur_layer_id_end'] = int(val)

    if cur_layer_total is not None:
        values = cur_layer_total.split(',')
        if len(values) == 1:
            val = values[0]
            items['cur_layer_total'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['cur_layer_total_start'] = int(val)

            val = values[1]
            if val != '':
                items['cur_layer_total_end'] = int(val)

    if bigorder_parent_id is not None:
        values = bigorder_parent_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['bigorder_parent_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['bigorder_parent_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['bigorder_parent_id_end'] = int(val)

    if entrust_status is not None:
        values = entrust_status.split(',')
        if len(values) == 1:
            val = values[0]
            items['entrust_status'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['entrust_status_start'] = int(val)

            val = values[1]
            if val != '':
                items['entrust_status_end'] = int(val)

    if light_status is not None:
        values = light_status.split(',')
        if len(values) == 1:
            val = values[0]
            items['light_status'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['light_status_start'] = int(val)

            val = values[1]
            if val != '':
                items['light_status_end'] = int(val)

    if voucher_total is not None:
        values = voucher_total.split(',')
        if len(values) == 1:
            val = values[0]
            items['voucher_total'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['voucher_total_start'] = int(val)

            val = values[1]
            if val != '':
                items['voucher_total_end'] = int(val)

    if endorders_total is not None:
        values = endorders_total.split(',')
        if len(values) == 1:
            val = values[0]
            items['endorders_total'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['endorders_total_start'] = int(val)

            val = values[1]
            if val != '':
                items['endorders_total_end'] = int(val)

    if doubule_id is not None:
        values = doubule_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['doubule_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['doubule_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['doubule_id_end'] = int(val)

    if entrust_startime is not None:
        values = entrust_startime.split(',')
        if len(values) == 1:
            val = values[0]
            items['entrust_startime'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['entrust_startime_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['entrust_startime_end'] = datetime.fromtimestamp(int(val))

    if entrust_endtime is not None:
        values = entrust_endtime.split(',')
        if len(values) == 1:
            val = values[0]
            items['entrust_endtime'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['entrust_endtime_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['entrust_endtime_end'] = datetime.fromtimestamp(int(val))

    if pai_buydui is not None:
        values = pai_buydui.split(',')
        if len(values) == 1:
            val = values[0]
            items['pai_buydui'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['pai_buydui_start'] = int(val)

            val = values[1]
            if val != '':
                items['pai_buydui_end'] = int(val)

    if bagorder_num is not None:
        values = bagorder_num.split(',')
        if len(values) == 1:
            val = values[0]
            items['bagorder_num'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['bagorder_num_start'] = int(val)

            val = values[1]
            if val != '':
                items['bagorder_num_end'] = int(val)

    if weight_num is not None:
        values = weight_num.split(',')
        if len(values) == 1:
            val = values[0]
            items['weight_num'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['weight_num_start'] = int(val)

            val = values[1]
            if val != '':
                items['weight_num_end'] = int(val)

    if fund_weight_num is not None:
        values = fund_weight_num.split(',')
        if len(values) == 1:
            val = values[0]
            items['fund_weight_num'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['fund_weight_num_start'] = int(val)

            val = values[1]
            if val != '':
                items['fund_weight_num_end'] = int(val)

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

    if is_tuan is not None:
        values = is_tuan.split(',')
        if len(values) == 1:
            val = values[0]
            items['is_tuan'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['is_tuan_start'] = int(val)

            val = values[1]
            if val != '':
                items['is_tuan_end'] = int(val)

    if ercode is not None:
        values = ercode.split(',')
        if len(values) == 1:
            val = values[0]
            items['ercode'] = val
        else:
            val = values[0]
            if val != '':
                items['ercode_start'] = val

            val = values[1]
            if val != '':
                items['ercode_end'] = val

    if sh_agent is not None:
        values = sh_agent.split(',')
        if len(values) == 1:
            val = values[0]
            items['sh_agent'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['sh_agent_start'] = int(val)

            val = values[1]
            if val != '':
                items['sh_agent_end'] = int(val)

    if s_username is not None:
        search_items['username'] = '%' + s_username + '%'

    if s_email is not None:
        search_items['email'] = '%' + s_email + '%'

    if s_open_id is not None:
        search_items['open_id'] = '%' + s_open_id + '%'

    if s_union_id is not None:
        search_items['union_id'] = '%' + s_union_id + '%'

    if s_password is not None:
        search_items['password'] = '%' + s_password + '%'

    if s_nickname is not None:
        search_items['nickname'] = '%' + s_nickname + '%'

    if s_phone is not None:
        search_items['phone'] = '%' + s_phone + '%'

    if s_id_card is not None:
        search_items['id_card'] = '%' + s_id_card + '%'

    if s_avatar is not None:
        search_items['avatar'] = '%' + s_avatar + '%'

    if s_name is not None:
        search_items['name'] = '%' + s_name + '%'

    if s_parent_id_history is not None:
        search_items['parent_id_history'] = '%' + s_parent_id_history + '%'

    if s_tran_pass is not None:
        search_items['tran_pass'] = '%' + s_tran_pass + '%'

    if s_invited_code is not None:
        search_items['invited_code'] = '%' + s_invited_code + '%'

    if s_ercode is not None:
        search_items['ercode'] = '%' + s_ercode + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_username is not None:
        values = l_username.split(',')
        values = [val for val in values]
        set_items['username'] = values

    if l_email is not None:
        values = l_email.split(',')
        values = [val for val in values]
        set_items['email'] = values

    if l_open_id is not None:
        values = l_open_id.split(',')
        values = [val for val in values]
        set_items['open_id'] = values

    if l_union_id is not None:
        values = l_union_id.split(',')
        values = [val for val in values]
        set_items['union_id'] = values

    if l_password is not None:
        values = l_password.split(',')
        values = [val for val in values]
        set_items['password'] = values

    if l_nickname is not None:
        values = l_nickname.split(',')
        values = [val for val in values]
        set_items['nickname'] = values

    if l_phone is not None:
        values = l_phone.split(',')
        values = [val for val in values]
        set_items['phone'] = values

    if l_id_card is not None:
        values = l_id_card.split(',')
        values = [val for val in values]
        set_items['id_card'] = values

    if l_level_id is not None:
        values = l_level_id.split(',')
        values = [int(val) for val in values]
        set_items['level_id'] = values

    if l_status is not None:
        values = l_status.split(',')
        values = [int(val) for val in values]
        set_items['status'] = values

    if l_register_time is not None:
        values = l_register_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['register_time'] = values

    if l_avatar is not None:
        values = l_avatar.split(',')
        values = [val for val in values]
        set_items['avatar'] = values

    if l_invited_user_id is not None:
        values = l_invited_user_id.split(',')
        values = [int(val) for val in values]
        set_items['invited_user_id'] = values

    if l_coin is not None:
        values = l_coin.split(',')
        values = [int(val) for val in values]
        set_items['coin'] = values

    if l_gender is not None:
        values = l_gender.split(',')
        values = [int(val) for val in values]
        set_items['gender'] = values

    if l_last_active_time is not None:
        values = l_last_active_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['last_active_time'] = values

    if l_name is not None:
        values = l_name.split(',')
        values = [val for val in values]
        set_items['name'] = values

    if l_is_agree is not None:
        values = l_is_agree.split(',')
        values = [int(val) for val in values]
        set_items['is_agree'] = values

    if l_parent_id is not None:
        values = l_parent_id.split(',')
        values = [int(val) for val in values]
        set_items['parent_id'] = values

    if l_parent_id_history is not None:
        values = l_parent_id_history.split(',')
        values = [val for val in values]
        set_items['parent_id_history'] = values

    if l_level_one_time is not None:
        values = l_level_one_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['level_one_time'] = values

    if l_level_two_time is not None:
        values = l_level_two_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['level_two_time'] = values

    if l_level_three_time is not None:
        values = l_level_three_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['level_three_time'] = values

    if l_level_top_time is not None:
        values = l_level_top_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['level_top_time'] = values

    if l_wholesale_id is not None:
        values = l_wholesale_id.split(',')
        values = [int(val) for val in values]
        set_items['wholesale_id'] = values

    if l_wholesale_amount is not None:
        values = l_wholesale_amount.split(',')
        values = [int(val) for val in values]
        set_items['wholesale_amount'] = values

    if l_paidui is not None:
        values = l_paidui.split(',')
        values = [int(val) for val in values]
        set_items['paidui'] = values

    if l_tuan_id is not None:
        values = l_tuan_id.split(',')
        values = [int(val) for val in values]
        set_items['tuan_id'] = values

    if l_tran_pass is not None:
        values = l_tran_pass.split(',')
        values = [val for val in values]
        set_items['tran_pass'] = values

    if l_invited_code is not None:
        values = l_invited_code.split(',')
        values = [val for val in values]
        set_items['invited_code'] = values

    if l_bigorder_id is not None:
        values = l_bigorder_id.split(',')
        values = [int(val) for val in values]
        set_items['bigorder_id'] = values

    if l_layer_id is not None:
        values = l_layer_id.split(',')
        values = [int(val) for val in values]
        set_items['layer_id'] = values

    if l_cur_layer_id is not None:
        values = l_cur_layer_id.split(',')
        values = [int(val) for val in values]
        set_items['cur_layer_id'] = values

    if l_cur_layer_total is not None:
        values = l_cur_layer_total.split(',')
        values = [int(val) for val in values]
        set_items['cur_layer_total'] = values

    if l_bigorder_parent_id is not None:
        values = l_bigorder_parent_id.split(',')
        values = [int(val) for val in values]
        set_items['bigorder_parent_id'] = values

    if l_entrust_status is not None:
        values = l_entrust_status.split(',')
        values = [int(val) for val in values]
        set_items['entrust_status'] = values

    if l_light_status is not None:
        values = l_light_status.split(',')
        values = [int(val) for val in values]
        set_items['light_status'] = values

    if l_voucher_total is not None:
        values = l_voucher_total.split(',')
        values = [int(val) for val in values]
        set_items['voucher_total'] = values

    if l_endorders_total is not None:
        values = l_endorders_total.split(',')
        values = [int(val) for val in values]
        set_items['endorders_total'] = values

    if l_doubule_id is not None:
        values = l_doubule_id.split(',')
        values = [int(val) for val in values]
        set_items['doubule_id'] = values

    if l_entrust_startime is not None:
        values = l_entrust_startime.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['entrust_startime'] = values

    if l_entrust_endtime is not None:
        values = l_entrust_endtime.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['entrust_endtime'] = values

    if l_pai_buydui is not None:
        values = l_pai_buydui.split(',')
        values = [int(val) for val in values]
        set_items['pai_buydui'] = values

    if l_bagorder_num is not None:
        values = l_bagorder_num.split(',')
        values = [int(val) for val in values]
        set_items['bagorder_num'] = values

    if l_weight_num is not None:
        values = l_weight_num.split(',')
        values = [int(val) for val in values]
        set_items['weight_num'] = values

    if l_fund_weight_num is not None:
        values = l_fund_weight_num.split(',')
        values = [int(val) for val in values]
        set_items['fund_weight_num'] = values

    if l_video_level is not None:
        values = l_video_level.split(',')
        values = [int(val) for val in values]
        set_items['video_level'] = values

    if l_is_tuan is not None:
        values = l_is_tuan.split(',')
        values = [int(val) for val in values]
        set_items['is_tuan'] = values

    if l_ercode is not None:
        values = l_ercode.split(',')
        values = [val for val in values]
        set_items['ercode'] = values

    if l_sh_agent is not None:
        values = l_sh_agent.split(',')
        values = [int(val) for val in values]
        set_items['sh_agent'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_user(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_user(items, search_items, set_items)

    return FilterResUser(data=data, total=c)


@router.get(f'/member/get_ordertree', summary='获取用户公排排序结构')
async def get_ordertree(user_id: int = 1642):
    '''
    从第二层json开始，data里面的p_id对应上一级的o_id，循环至最后一级data输出滑落图树状结构
    user_id不设置，默认是系统用户1642
    '''
    user_info = d_user.get_user_by_id(user_id)
    re_dict = {}
    bigorders = []
    is_end = False
    if user_info:
        #自己顶层
        bigorders.append(user_info.bigorder_id)
        user_list = []
        user_list.append({'u_id': user_info.id, 'o_id': user_info.bigorder_id, 'o_name': user_info.nickname, 'p_id': user_info.bigorder_parent_id, 'phone': user_info.phone})
        re_dict['data'] = user_list
        re_dict['next'] = {}
        #之下第一层
        next_info = d_user.get_bigorder_parent_user(bigorders)
        user_list = []
        bigorders = []
        for dd in next_info:
            user_list.append({'u_id': dd.id, 'o_id': dd.bigorder_id, 'o_name': dd.nickname, 'p_id': dd.bigorder_parent_id, 'phone': dd.phone})
            bigorders.append(dd.bigorder_id)
        if user_list:
            re_dict['next']['data'] = user_list
            re_dict['next']['next'] = {}
        else:
            is_end = True
        #之下第二层
        if not is_end:
            next_info = d_user.get_bigorder_parent_user(bigorders)
            user_list = []
            bigorders = []
            for dd in next_info:
                user_list.append({'u_id': dd.id, 'o_id': dd.bigorder_id, 'o_name': dd.nickname, 'p_id': dd.bigorder_parent_id, 'phone': dd.phone})
                bigorders.append(dd.bigorder_id)
            if user_list:
                re_dict['next']['next']['data'] = user_list
                re_dict['next']['next']['next'] = {}
            else:
                is_end = True
        #之下第三层
        if not is_end:
            next_info = d_user.get_bigorder_parent_user(bigorders)
            user_list = []
            bigorders = []
            for dd in next_info:
                user_list.append({'u_id': dd.id, 'o_id': dd.bigorder_id, 'o_name': dd.nickname, 'p_id': dd.bigorder_parent_id, 'phone': dd.phone})
                bigorders.append(dd.bigorder_id)
            if user_list:
                re_dict['next']['next']['next']['data'] = user_list
                re_dict['next']['next']['next']['next'] = {}
            else:
                is_end = True
        #之下第四层
        if not is_end:
            next_info = d_user.get_bigorder_parent_user(bigorders)
            user_list = []
            bigorders = []
            for dd in next_info:
                user_list.append({'u_id': dd.id, 'o_id': dd.bigorder_id, 'o_name': dd.nickname, 'p_id': dd.bigorder_parent_id, 'phone': dd.phone})
                bigorders.append(dd.bigorder_id)
            if user_list:
                re_dict['next']['next']['next']['next']['data'] = user_list
                re_dict['next']['next']['next']['next']['next'] = {}
            else:
                is_end = True
        #之下第五层
        if not is_end:
            next_info = d_user.get_bigorder_parent_user(bigorders)
            user_list = []
            bigorders = []
            for dd in next_info:
                user_list.append({'u_id': dd.id, 'o_id': dd.bigorder_id, 'o_name': dd.nickname, 'p_id': dd.bigorder_parent_id, 'phone': dd.phone})
                bigorders.append(dd.bigorder_id)
            if user_list:
                re_dict['next']['next']['next']['next']['next']['data'] = user_list
                re_dict['next']['next']['next']['next']['next']['next'] = {}
            else:
                is_end = True
        #之下第六层
        if not is_end:
            next_info = d_user.get_bigorder_parent_user(bigorders)
            user_list = []
            bigorders = []
            for dd in next_info:
                user_list.append({'u_id': dd.id, 'o_id': dd.bigorder_id, 'o_name': dd.nickname, 'p_id': dd.bigorder_parent_id, 'phone': dd.phone})
                bigorders.append(dd.bigorder_id)
            if user_list:
                re_dict['next']['next']['next']['next']['next']['next']['data'] = user_list
                re_dict['next']['next']['next']['next']['next']['next']['next'] = {}
            else:
                is_end = True
        #之下第七层
        if not is_end:
            next_info = d_user.get_bigorder_parent_user(bigorders)
            user_list = []
            bigorders = []
            for dd in next_info:
                user_list.append({'u_id': dd.id, 'o_id': dd.bigorder_id, 'o_name': dd.nickname, 'p_id': dd.bigorder_parent_id, 'phone': dd.phone})
                bigorders.append(dd.bigorder_id)
            if user_list:
                re_dict['next']['next']['next']['next']['next']['next']['next']['data'] = user_list
                re_dict['next']['next']['next']['next']['next']['next']['next']['next'] = {}
            else:
                is_end = True

        #之下第八层
        if not is_end:
            next_info = d_user.get_bigorder_parent_user(bigorders)
            user_list = []
            bigorders = []
            for dd in next_info:
                user_list.append({'u_id': dd.id, 'o_id': dd.bigorder_id, 'o_name': dd.nickname, 'p_id': dd.bigorder_parent_id, 'phone': dd.phone})
                bigorders.append(dd.bigorder_id)
            if user_list:
                re_dict['next']['next']['next']['next']['next']['next']['next']['next']['data'] = user_list
                re_dict['next']['next']['next']['next']['next']['next']['next']['next']['next'] = {}
            else:
                is_end = True

        #之下第九层
        if not is_end:
            next_info = d_user.get_bigorder_parent_user(bigorders)
            user_list = []
            bigorders = []
            for dd in next_info:
                user_list.append({'u_id': dd.id, 'o_id': dd.bigorder_id, 'o_name': dd.nickname, 'p_id': dd.bigorder_parent_id, 'phone': dd.phone})
                bigorders.append(dd.bigorder_id)
            if user_list:
                re_dict['next']['next']['next']['next']['next']['next']['next']['next']['next']['data'] = user_list
                re_dict['next']['next']['next']['next']['next']['next']['next']['next']['next']['next'] = {}
            else:
                is_end = True

        #之下第十层
        if not is_end:
            next_info = d_user.get_bigorder_parent_user(bigorders)
            user_list = []
            bigorders = []
            for dd in next_info:
                user_list.append({'u_id': dd.id, 'o_id': dd.bigorder_id, 'o_name': dd.nickname, 'p_id': dd.bigorder_parent_id, 'phone': dd.phone})
                bigorders.append(dd.bigorder_id)
            if user_list:
                re_dict['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['data'] = user_list
                re_dict['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next'] = {}
            else:
                is_end = True

        #之下第十一层
        if not is_end:
            next_info = d_user.get_bigorder_parent_user(bigorders)
            user_list = []
            bigorders = []
            for dd in next_info:
                user_list.append({'u_id': dd.id, 'o_id': dd.bigorder_id, 'o_name': dd.nickname, 'p_id': dd.bigorder_parent_id, 'phone': dd.phone})
                bigorders.append(dd.bigorder_id)
            if user_list:
                re_dict['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['data'] = user_list
                re_dict['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next'] = {}
            else:
                is_end = True

        # 之下第十二层
        if not is_end:
            next_info = d_user.get_bigorder_parent_user(bigorders)
            user_list = []
            bigorders = []
            for dd in next_info:
                user_list.append(
                    {'u_id': dd.id, 'o_id': dd.bigorder_id, 'o_name': dd.nickname, 'p_id': dd.bigorder_parent_id,
                     'phone': dd.phone})
                bigorders.append(dd.bigorder_id)
            if user_list:
                re_dict['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['data'] = user_list
                re_dict['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next'] = {}
            else:
                is_end = True

        # 之下第十三层
        if not is_end:
            next_info = d_user.get_bigorder_parent_user(bigorders)
            user_list = []
            bigorders = []
            for dd in next_info:
                user_list.append(
                    {'u_id': dd.id, 'o_id': dd.bigorder_id, 'o_name': dd.nickname, 'p_id': dd.bigorder_parent_id,
                     'phone': dd.phone})
                bigorders.append(dd.bigorder_id)
            if user_list:
                re_dict['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['data'] = user_list
                re_dict['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next'] = {}
            else:
                is_end = True

        # 之下第十四层
        if not is_end:
            next_info = d_user.get_bigorder_parent_user(bigorders)
            user_list = []
            bigorders = []
            for dd in next_info:
                user_list.append(
                    {'u_id': dd.id, 'o_id': dd.bigorder_id, 'o_name': dd.nickname, 'p_id': dd.bigorder_parent_id,
                     'phone': dd.phone})
                bigorders.append(dd.bigorder_id)
            if user_list:
                re_dict['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['data'] = user_list
                re_dict['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next'] = {}
            else:
                is_end = True

        # 之下第十五层
        if not is_end:
            next_info = d_user.get_bigorder_parent_user(bigorders)
            user_list = []
            bigorders = []
            for dd in next_info:
                user_list.append(
                    {'u_id': dd.id, 'o_id': dd.bigorder_id, 'o_name': dd.nickname, 'p_id': dd.bigorder_parent_id,
                     'phone': dd.phone})
                bigorders.append(dd.bigorder_id)
            if user_list:
                re_dict['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['data'] = user_list
                re_dict['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next']['next'] = {}
            else:
                is_end = True

    return re_dict
    # user_list = []
    # user_list.append({'o_id':1,'o_name':'nik','p_id':0,'phone':'133121212'})
    # re_dict['data']=user_list
    # re_dict['next'] = None
    # return {'data':[{'u_id':1, 'o_id':1,'o_name':'nik','p_id':0,'phone':'133121212'}],'next':{'data':[{'u_id':1, 'o_id':2,'o_name':'nik2','p_id':1,'phone':'144121212'},{'u_id':1, 'o_id':3,'o_name':'nik3','p_id':1,'phone':'155121212'}],'next':None}}

