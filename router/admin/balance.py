from fastapi import APIRouter, Depends, Header, Request
#from sqlalchemy.ext.declarative import declarative_base
from model.schema import TBalance
from dao import d_balance, d_account, d_prize, d_db, d_user
from fastapi.exceptions import HTTPException
from model.mall import m_account
from common import global_define, global_function
import time
import logging
from service.wx_service import wxpay
import math
from model import m_schema
from router.admin.user import verify_token
from typing import Optional, List
from datetime import datetime


#Base = declarative_base()
#metadata = Base.metadata

router = APIRouter(dependencies=[Depends(verify_token)])

# @router.post(f"/search_balance", summary="获取/检索所有会员资金记录")
# async def search_balance(item: d_balance.SearchBalance):
#     # if item.user_id is None:
#     #     raise HTTPException(400, "未知用户")
#     # if item.user_id <= 0:
#     #     raise HTTPException(400, "未找到用户")
#     return d_balance.search_balance(item)
#
# @router.post(f"/search_balance_admin", summary="获取某商家相关收益记录")
# async def search_balance_admin(item: d_balance.SearchBalance):
#     # if item.user_id is None:
#     #     raise HTTPException(400, "未知用户")
#     # if item.user_id <= 0:
#     #     raise HTTPException(400, "未找到用户")
#     return d_balance.search_balance(item)
#
# @router.post(f"/search_lockbalance", summary="获取锁定额变动记录")
# async def search_lockbalance(item: d_balance.SearchBalance):
#     return d_balance.search_lock_balance(item)
#


@router.get(f'/withdraw_filter', response_model=m_schema.FilterResUserWithdraw, summary="提现记录")
async def filter_user_withdraw(
        id: Optional[str] = None,
        amount: Optional[str] = None,
        user_withdraw_status_id: Optional[str] = None,
        create_time: Optional[str] = None,
        update_time: Optional[str] = None,
        user_id: Optional[str] = None,
        type_id: Optional[str] = None,
        user_bank_id: Optional[str] = None,
        operator_id: Optional[str] = None,
        fee_type: Optional[str] = None,
        fee_pro: Optional[str] = None,
        out_batch_no: Optional[str] = None,
        batch_name: Optional[str] = None,
        batch_remark: Optional[str] = None,
        out_detail_no: Optional[str] = None,
        user_name: Optional[str] = None,
        user_phone: Optional[str] = None,
        fee_balance: Optional[str] = None,
        deduct_balance: Optional[str] = None,
        l_id: Optional[str] = None,
        l_amount: Optional[str] = None,
        l_user_withdraw_status_id: Optional[str] = None,
        l_create_time: Optional[str] = None,
        l_update_time: Optional[str] = None,
        l_user_id: Optional[str] = None,
        l_type_id: Optional[str] = None,
        l_user_bank_id: Optional[str] = None,
        l_operator_id: Optional[str] = None,
        l_fee_type: Optional[str] = None,
        l_fee_pro: Optional[str] = None,
        l_out_batch_no: Optional[str] = None,
        l_batch_name: Optional[str] = None,
        l_batch_remark: Optional[str] = None,
        l_out_detail_no: Optional[str] = None,
        l_user_name: Optional[str] = None,
        l_user_phone: Optional[str] = None,
        l_fee_balance: Optional[str] = None,
        l_deduct_balance: Optional[str] = None,
        s_out_batch_no: Optional[str] = None,
        s_batch_name: Optional[str] = None,
        s_batch_remark: Optional[str] = None,
        s_out_detail_no: Optional[str] = None,
        s_user_name: Optional[str] = None,
        s_user_phone: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> m_schema.FilterResUserWithdraw:
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

    if amount is not None:
        values = amount.split(',')
        if len(values) == 1:
            val = values[0]
            items['amount'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['amount_start'] = int(val)

            val = values[1]
            if val != '':
                items['amount_end'] = int(val)

    if user_withdraw_status_id is not None:
        values = user_withdraw_status_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['user_withdraw_status_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['user_withdraw_status_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['user_withdraw_status_id_end'] = int(val)

    if create_time is not None:
        values = create_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['create_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['create_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['create_time_end'] = datetime.fromtimestamp(int(val))

    if update_time is not None:
        values = update_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['update_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['update_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['update_time_end'] = datetime.fromtimestamp(int(val))

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

    if user_bank_id is not None:
        values = user_bank_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['user_bank_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['user_bank_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['user_bank_id_end'] = int(val)

    if operator_id is not None:
        values = operator_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['operator_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['operator_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['operator_id_end'] = int(val)

    if fee_type is not None:
        values = fee_type.split(',')
        if len(values) == 1:
            val = values[0]
            items['fee_type'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['fee_type_start'] = int(val)

            val = values[1]
            if val != '':
                items['fee_type_end'] = int(val)

    if fee_pro is not None:
        values = fee_pro.split(',')
        if len(values) == 1:
            val = values[0]
            items['fee_pro'] = float(val)
        else:
            val = values[0]
            if val != '':
                items['fee_pro_start'] = float(val)

            val = values[1]
            if val != '':
                items['fee_pro_end'] = float(val)

    if out_batch_no is not None:
        values = out_batch_no.split(',')
        if len(values) == 1:
            val = values[0]
            items['out_batch_no'] = val
        else:
            val = values[0]
            if val != '':
                items['out_batch_no_start'] = val

            val = values[1]
            if val != '':
                items['out_batch_no_end'] = val

    if batch_name is not None:
        values = batch_name.split(',')
        if len(values) == 1:
            val = values[0]
            items['batch_name'] = val
        else:
            val = values[0]
            if val != '':
                items['batch_name_start'] = val

            val = values[1]
            if val != '':
                items['batch_name_end'] = val

    if batch_remark is not None:
        values = batch_remark.split(',')
        if len(values) == 1:
            val = values[0]
            items['batch_remark'] = val
        else:
            val = values[0]
            if val != '':
                items['batch_remark_start'] = val

            val = values[1]
            if val != '':
                items['batch_remark_end'] = val

    if out_detail_no is not None:
        values = out_detail_no.split(',')
        if len(values) == 1:
            val = values[0]
            items['out_detail_no'] = val
        else:
            val = values[0]
            if val != '':
                items['out_detail_no_start'] = val

            val = values[1]
            if val != '':
                items['out_detail_no_end'] = val

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

    if fee_balance is not None:
        values = fee_balance.split(',')
        if len(values) == 1:
            val = values[0]
            items['fee_balance'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['fee_balance_start'] = int(val)

            val = values[1]
            if val != '':
                items['fee_balance_end'] = int(val)

    if deduct_balance is not None:
        values = deduct_balance.split(',')
        if len(values) == 1:
            val = values[0]
            items['deduct_balance'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['deduct_balance_start'] = int(val)

            val = values[1]
            if val != '':
                items['deduct_balance_end'] = int(val)

    if s_out_batch_no is not None:
        search_items['out_batch_no'] = '%' + s_out_batch_no + '%'

    if s_batch_name is not None:
        search_items['batch_name'] = '%' + s_batch_name + '%'

    if s_batch_remark is not None:
        search_items['batch_remark'] = '%' + s_batch_remark + '%'

    if s_out_detail_no is not None:
        search_items['out_detail_no'] = '%' + s_out_detail_no + '%'

    if s_user_name is not None:
        search_items['user_name'] = '%' + s_user_name + '%'

    if s_user_phone is not None:
        search_items['user_phone'] = '%' + s_user_phone + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_amount is not None:
        values = l_amount.split(',')
        values = [int(val) for val in values]
        set_items['amount'] = values

    if l_user_withdraw_status_id is not None:
        values = l_user_withdraw_status_id.split(',')
        values = [int(val) for val in values]
        set_items['user_withdraw_status_id'] = values

    if l_create_time is not None:
        values = l_create_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['create_time'] = values

    if l_update_time is not None:
        values = l_update_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['update_time'] = values

    if l_user_id is not None:
        values = l_user_id.split(',')
        values = [int(val) for val in values]
        set_items['user_id'] = values

    if l_type_id is not None:
        values = l_type_id.split(',')
        values = [int(val) for val in values]
        set_items['type_id'] = values

    if l_user_bank_id is not None:
        values = l_user_bank_id.split(',')
        values = [int(val) for val in values]
        set_items['user_bank_id'] = values

    if l_operator_id is not None:
        values = l_operator_id.split(',')
        values = [int(val) for val in values]
        set_items['operator_id'] = values

    if l_fee_type is not None:
        values = l_fee_type.split(',')
        values = [int(val) for val in values]
        set_items['fee_type'] = values

    if l_fee_pro is not None:
        values = l_fee_pro.split(',')
        values = [float(val) for val in values]
        set_items['fee_pro'] = values

    if l_out_batch_no is not None:
        values = l_out_batch_no.split(',')
        values = [val for val in values]
        set_items['out_batch_no'] = values

    if l_batch_name is not None:
        values = l_batch_name.split(',')
        values = [val for val in values]
        set_items['batch_name'] = values

    if l_batch_remark is not None:
        values = l_batch_remark.split(',')
        values = [val for val in values]
        set_items['batch_remark'] = values

    if l_out_detail_no is not None:
        values = l_out_detail_no.split(',')
        values = [val for val in values]
        set_items['out_detail_no'] = values

    if l_user_name is not None:
        values = l_user_name.split(',')
        values = [val for val in values]
        set_items['user_name'] = values

    if l_user_phone is not None:
        values = l_user_phone.split(',')
        values = [val for val in values]
        set_items['user_phone'] = values

    if l_fee_balance is not None:
        values = l_fee_balance.split(',')
        values = [int(val) for val in values]
        set_items['fee_balance'] = values

    if l_deduct_balance is not None:
        values = l_deduct_balance.split(',')
        values = [int(val) for val in values]
        set_items['deduct_balance'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_user_withdraw(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_user_withdraw(items, search_items, set_items)

    return m_schema.FilterResUserWithdraw(data=data, total=c)


@router.get(f'/detail_withdraw', summary='用户申请提现详情')
async def user_detail_withdraw(withdraw_id:int):
    """
    type_id,提现类型（1表示银行卡，2表示微信零钱）；fee_type，扣费类型（1表示扣费倒锁定余额，2表示直接扣费）；
    user_withdraw_status_id，状态（1申请中，2已审核，3	已拒绝，4，已失败）
    """
    return d_account.get_user_withdraw(withdraw_id)

# @router.get(f'/deny_withdraw', summary='审核拒绝提现')
# async def user_deny_withdraw(withdraw_id:int):
#     deny_info = d_account.get_user_withdraw(withdraw_id)
#     if not deny_info:
#         raise HTTPException(400, "未知数据")
#     if deny_info['TUserWithdraw'].user_withdraw_status_id != 1:
#         raise HTTPException(400, "提现数据错误")
#
#     d_account.update_user_withdraw_status(deny_info['TUserWithdraw'].id, 3)
#     total_balance = deny_info[2].balance +  deny_info[0].amount
#     d_account.update_account_by_id(deny_info[2].id, {"balance":total_balance})
#     d_account.add_balance(m_account.BalanceModel(
#         user_id=deny_info[0].user_id,
#         change=deny_info[0].amount,
#         balance=total_balance,
#         type=global_define.balance_type[20],
#         create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#     ))
#     return {'code': 200, 'message': 'success'}

# @router.get(f'/reback_withdraw', summary='重新提现')
# async def reback_withdraw(withdraw_id:int):
#     deny_info = d_account.get_user_withdraw(withdraw_id)
#     if not deny_info:
#         raise HTTPException(400, "未知数据")
#     # if deny_info['TUserWithdraw'].user_withdraw_status_id != 1:
#     #     raise HTTPException(400, "提现数据错误")
#
#     d_account.update_user_withdraw_status(deny_info['TUserWithdraw'].id, 1)
#     return {'status': 200, 'message': 'success'}
#

@router.post(f'/commit_withdraw', summary='管理直接提现金额')
async def commit_withdraw(data: m_account.WithdrawModel):
    """
    :type_id,提现类型（1表示银行卡，2表示微信零钱）；fee_type，扣费类型（1表示扣费倒锁定余额，2表示直接扣费）；
    :user_withdraw_status_id，状态（1申请中，2已审核，3	已拒绝，4，已失败）
    """
    s_user: m_schema.SUser = d_db.get_user(user_id=data.user_id)
    if s_user:
        logging.info('start to withdraw')
        logging.info(f"post参数:{data}")
        user_accounts = d_account.get_account_info(data.user_id)

        if not s_user.phone:
            return {'code': 304, 'message': '联系方式错误'}
        if not data.type_id:
            return {'code': 304, 'message': '提现类型错误'}

        # 提现范围：大于100元，小于500元
        if data.amount < global_define.withdraw_config['low_balance'] or data.amount > global_define.withdraw_config['max_balance']:
            return {'code': 304, 'message': '提现金额错误'}
        #
        # # 支付密码验证
        # if len(data.tran_pass) < 6 or data.tran_pass != s_user.tran_pass:
        #     return {'code': 200, 'message': '支付密码无效'}
        #推荐余额提现
        base_info = None
        if data.fee_type == 1:
            logging.info('推荐余额提现')
            if not user_accounts or user_accounts.lock_balance < data.amount:
                return {'code': 304, 'message': '资金账户错误'}
            new_draw = m_schema.CreateUserWithdraw(amount=data.amount, user_withdraw_status_id=0, user_id=data.user_id,
                                                   create_time=datetime.now(),
                                                   update_time=datetime.now(),
                                                   fee_type=data.fee_type,
                                                   fee_pro=global_define.withdraw_config['ded_bouns'], #默认提现比例 10%
                                                   out_batch_no=global_function.get_randoms(30),
                                                   batch_name="用户余额提现",
                                                   batch_remark=global_define.balance_type[16],
                                                   out_detail_no=global_function.get_randoms(30),
                                                   user_name=s_user.name,
                                                   user_phone=s_user.phone,
                                                   type_id=data.type_id,
                                                   user_bank_id=data.user_bank_id,
                                                   user_bank_other=data.user_bank_other
                                                   )
            base_info = d_db.insert_user_withdraw(new_draw)
            logging.info(f"insert_user_withdraw：{base_info}")
            total_balance = user_accounts.lock_balance - data.amount
            logging.info(f"原推荐金额：{user_accounts.lock_balance}，剩余推荐金额：{total_balance}")
            d_account.update_account_by_id(user_accounts.id, {"lock_balance": total_balance})
            d_account.add_lock_balance(m_account.LockBalanceModel(
                user_id=data.user_id,
                change=-data.amount,
                lock_balance=total_balance,
                type=global_define.balance_type[16],
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                description='',
                out_trade_no=''
            ))
        # 余额提现
        else:
            logging.info('余额提现')
            if not user_accounts or user_accounts.balance < data.amount:
                return {'code': 304, 'message': '余额资金账户错误'}
            new_draw = m_schema.CreateUserWithdraw(amount=data.amount, user_withdraw_status_id=0, user_id=data.user_id,
                                                   create_time=datetime.now(),
                                                   update_time=datetime.now(),
                                                   fee_type=data.fee_type,
                                                   fee_pro=global_define.withdraw_config['ded_bouns'],
                                                   out_batch_no=global_function.get_randoms(30),
                                                   batch_name="用户余额提现",
                                                   batch_remark=global_define.balance_type[6],
                                                   out_detail_no=global_function.get_randoms(30),
                                                   user_name=s_user.name,
                                                   user_phone=s_user.phone,
                                                   type_id=data.type_id,
                                                   user_bank_id=data.user_bank_id,
                                                   user_bank_other=data.user_bank_other
                                                   )
            base_info = d_db.insert_user_withdraw(new_draw)
            logging.info(f"insert_user_withdraw：{base_info}")
            total_balance = user_accounts.balance - data.amount
            logging.info(f"原金额：{user_accounts.balance}，剩余推荐金额：{total_balance}")
            d_account.update_account_by_id(user_accounts.id, {"balance": total_balance})
            d_account.add_balance(m_account.BalanceModel(
                user_id=data.user_id,
                change=-data.amount,
                balance=total_balance,
                type=global_define.balance_type[6],
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            ))

        deduct_balance = math.ceil(base_info.amount * global_define.withdraw_config['ded_bouns'])
        fee_balance = base_info.amount - deduct_balance
        res = wxpay.transfer_batch(
            out_batch_no=base_info.out_batch_no,
            batch_name=base_info.batch_name,
            batch_remark=base_info.batch_remark,
            total_amount=fee_balance,
            total_num=1,
            transfer_detail_list=[{"out_detail_no": base_info.out_detail_no, "transfer_amount": fee_balance, "transfer_remark": base_info.batch_remark, "openid": s_user.open_id}],
            transfer_scene_id="1001"
        )
        logging.info(res)
        logging.info(f"提现申请ID: {base_info.id}")
        if res[0] == 200:
            # d_account.update_user_withdraw_balance(base_info.id, fee_balance, deduct_balance)
            d_account.update_user_withdraw_status(base_info.id, 1)
            # if base_info["fee_type"] == 1:
            #     total_lock_balance = base_info[2].lock_balance + deduct_balance
            #     d_account.update_account_by_id(base_info[2].id, {"lock_balance": total_lock_balance})
            #     d_account.add_lock_balance(m_account.LockBalanceModel(
            #         user_id=base_info[0].user_id,
            #         change=deduct_balance,
            #         lock_balance=total_lock_balance,
            #         type=global_define.balance_type[21],
            #         create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            #     ))
        else:
            d_account.update_user_withdraw_status(base_info.id, 4)
        return {'code': 200, 'message': 'success'}


@router.post(f'/pass_withdraw', summary='审核通过提现')
async def user_pass_withdraw(data: m_account.PassWithdrawModel):
    """
    :type_id,提现类型（1表示银行卡，2表示微信零钱）；fee_type，扣费类型（1表示扣费倒锁定余额，2表示直接扣费）；
    :user_withdraw_status_id，状态（1申请中，2已审核，3	已拒绝，4，已失败）
    """
    base_info = d_account.get_user_withdraw(data.withdraw_id)
    if not base_info:
        raise HTTPException(400, "未知数据")
    if base_info['TUserWithdraw'].user_withdraw_status_id != 0:
        raise HTTPException(400, "状态错误")
    if base_info['TUserWithdraw'].amount > global_define.withdraw_config['max_balance']:
        max_balance = global_define.withdraw_config['max_balance'] / 100
        raise HTTPException(400, f"提现金额最多不能超过{max_balance}")
    if data.amount != base_info[0].amount:
        raise HTTPException(400, "提现金额不一致")
    if data.fee_type != base_info[0].fee_type:
        raise HTTPException(400, "提现方式不一致")
    if data.fee_pro != base_info[0].fee_pro:
        raise HTTPException(400, "提现比例不一致")
    #deduct_balance = round(base_info[0].amount * base_info[0].fee_pro)
    deduct_balance = math.ceil(base_info[0].amount * global_define.withdraw_config['ded_bouns'])
    fee_balance = base_info[0].amount - deduct_balance
    # if data.fee_balance != fee_balance:
    #     raise HTTPException(400, "提现税后金额不一致")
    # if data.deduct_balance != deduct_balance:
    #     raise HTTPException(400, "提现税金不一致")

    # user_accounts = d_account.get_account_info(data.user_id)
    # if data.fee_type == 1:
    #     logging.info('推荐余额提现')
    #     if not user_accounts or user_accounts.lock_balance < data.amount:
    #         return {'code': 304, 'message': '资金账户错误'}
    #     total_balance = user_accounts.lock_balance - data.amount
    #     logging.info(f"原推荐金额：{user_accounts.lock_balance}，剩余推荐金额：{total_balance}")
    #     d_account.update_account_by_id(user_accounts.id, {"lock_balance": total_balance})
    #     d_account.add_lock_balance(m_account.LockBalanceModel(
    #         user_id=data.user_id,
    #         change=-data.amount,
    #         lock_balance=total_balance,
    #         type=global_define.balance_type[16],
    #         create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    #         description='',
    #         out_trade_no=''
    #     ))
    # # 余额提现
    # else:
    #     logging.info('余额提现')
    #     if not user_accounts or user_accounts.balance < data.amount:
    #         return {'code': 304, 'message': '余额资金账户错误'}
    #     total_balance = user_accounts.balance - data.amount
    #     logging.info(f"原金额：{user_accounts.balance}，剩余推荐金额：{total_balance}")
    #     d_account.update_account_by_id(user_accounts.id, {"balance": total_balance})
    #     d_account.add_balance(m_account.BalanceModel(
    #         user_id=data.user_id,
    #         change=-data.amount,
    #         balance=total_balance,
    #         type=global_define.balance_type[6],
    #         create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #     ))

    logging.info('start to withdraw')
    res = wxpay.transfer_batch(
        out_batch_no=base_info[0].out_batch_no,
        batch_name=base_info[0].batch_name,
        batch_remark=base_info[0].batch_remark,
        total_amount=fee_balance,
        total_num=1,
        transfer_detail_list=[{"out_detail_no": base_info[0].out_detail_no, "transfer_amount": fee_balance, "transfer_remark": base_info[0].batch_remark, "openid": base_info[1].open_id}],
        transfer_scene_id="1001"
    )
    logging.info(res)
    logging.info(f"提现申请ID: {base_info[0].id}")
    if res[0] == 200:
        d_account.update_user_withdraw_balance(base_info[0].id, fee_balance, deduct_balance)
        d_account.update_user_withdraw_status(base_info[0].id, 1)
        #
        #
        # if base_info[0].fee_type == 1:
        #     total_lock_balance = base_info[2].lock_balance + deduct_balance
        #     d_account.update_account_by_id(base_info[2].id, {"lock_balance": total_lock_balance})
        #     d_account.add_lock_balance(m_account.LockBalanceModel(
        #         user_id=base_info[0].user_id,
        #         change=deduct_balance,
        #         lock_balance=total_lock_balance,
        #         type=global_define.balance_type[21],
        #         create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #     ))
    else:
        d_account.update_user_withdraw_status(base_info[0].id, 4)
    return {'code': 200, 'message': 'success'}

# @router.post(f'/withdraw_moneypic', summary='更新转账截图url')
# async def withdraw_moneypic(data: m_account.MoneyPic):
#     """
#     存储七牛图片url
#     """
#     d_account.update_user_withdraw_balance(data.withdraw_id, data.money_pic)
#     return {'code': 200, 'message': 'success'}

#
# @router.post(f'/add_user_prize', summary='给用户增加奖励')
# async def add_user_prize(data: d_prize.TPrize):
#     """
#     用户列表增加  推荐批发奖励  按钮，点击提交接口参数，其中奖励状态status为10（系统设置，可调整为本奖励额度，方便识别）
#     """
#     if data.user_id is None or data.status is None:
#         raise HTTPException(400, "数据错误")
#     is_have = d_prize.is_prize(data)
#     if is_have:
#         raise HTTPException(400, f"{data.user_id}, 该用户已经奖励")
#     d_prize.insert_prize(data)
#     return {'code': 200, 'message': 'success'}

@router.post(f'/update_user_balance', summary='管理员修改用户余额、购物券资产，指定推荐人')
async def update_user_balance(data: d_prize.update_balan_model):
    """
    给用户充值接口，四个参数不能为空。
    user_ids，以逗号分隔的用户id(1,2,3,4)；
    type， 类型：1表示增加余额，2表示增加购物券；，3指定推荐人
    add_count， 增加数量（分）；或推荐人用户id
    manager_id，操作管理员id；
    """
    user_list = data.user_ids.split(',')
    re_val = {}
    if not data.type in [1,2,3]:
        raise HTTPException(400, f"{data.type}, 未知类型")
    if data.manager_id is None:
        raise HTTPException(400, f"未知管理员")
    if data.user_ids is None or data.add_count is None:
        raise HTTPException(400, f"数据错误")
    if data.add_count < 0:
        raise HTTPException(400, f"非法赠额")
    success_total = 0
    for uid in user_list:
        uuid = int(uid)
        user_info = d_account.get_account_info_add(uuid)
        if not user_info:
            re_val[uuid] = '未知资金账户'
            continue
        if uuid in re_val:
            continue

        if data.type == 1: # 增加余额
            if data.add_count == 0:
                total_balance = 0
            else:
                total_balance = user_info.balance + data.add_count
            d_account.update_account_by_id(user_info.id, {'balance': total_balance})
            s_balance = m_account.BalanceModel(
                user_id=user_info.user_id,
                change=data.add_count,
                balance=total_balance,
                type=global_define.balance_type[14],
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                good_id=0,
                good_title=f"原余额:{user_info.balance}",
                good_num='',
                out_trade_no=''
            )
            d_account.add_balance(s_balance)
            re_val[uuid] = f"{uid}增加余额{data.add_count},总余额{total_balance}"
            success_total += 1
        elif data.type == 2: #增加积分
            total_coin = user_info.coin + data.add_count
            d_account.update_account_by_id(user_info.id, {'coin': total_coin})
            s_coin = m_account.CoinModel(
                user_id=user_info.user_id,
                change=data.add_count,
                coin=total_coin,
                type=global_define.balance_type[15],
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                description = global_define.balance_type[15],
                out_trade_no=''
            )
            d_account.insert_coin(s_coin)
            re_val[uuid] = f"{uid}增加积分{data.add_count},总积分{total_coin}"
            success_total += 1
        elif data.type == 3: #改变推荐关系
            uu_info = d_user.get_user_by_id(uuid)
            d_user.update_invited_user_id(uu_info.id, data.add_count)
            re_val[uuid] = f"{uid}原推荐人{uu_info.invited_user_id},变更为{data.add_count}"
            success_total += 1

    if data.type == 1:  # 增加余额
        d_db.insert_balance_give(item=m_schema.CreateBalanceGive(
            user_ids=data.user_ids,
            coin=0,
            balance=data.add_count,
            type=data.type,
            description=re_val.__str__(),
            create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            operator_id=data.manager_id,
            sucess_num=success_total
        ))
    elif data.type == 2:  # 增加积分
        d_db.insert_balance_give(item=m_schema.CreateBalanceGive(
            user_ids=data.user_ids,
            coin=data.add_count,
            balance=0,
            type=data.type,
            description=re_val.__str__(),
            create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            operator_id=data.manager_id,
            sucess_num=success_total
        ))
    elif data.type == 3:  # 更新推荐人
        d_db.insert_balance_give(item=m_schema.CreateBalanceGive(
            user_ids=data.user_ids,
            coin=data.add_count,
            balance=0,
            type=data.type,
            description=re_val.__str__(),
            create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            operator_id=data.manager_id,
            sucess_num=success_total
        ))
    return re_val


@router.get(f'/balance_give/filter', response_model=m_schema.FilterResBalanceGive)
async def filter_balance_give(
        id: Optional[str] = None,
        user_ids: Optional[str] = None,
        coin: Optional[str] = None,
        balance: Optional[str] = None,
        type: Optional[str] = None,
        description: Optional[str] = None,
        create_time: Optional[str] = None,
        operator_id: Optional[str] = None,
        sucess_num: Optional[str] = None,
        give_txt: Optional[str] = None,
        l_id: Optional[str] = None,
        l_user_ids: Optional[str] = None,
        l_coin: Optional[str] = None,
        l_balance: Optional[str] = None,
        l_type: Optional[str] = None,
        l_description: Optional[str] = None,
        l_create_time: Optional[str] = None,
        l_operator_id: Optional[str] = None,
        l_sucess_num: Optional[str] = None,
        l_give_txt: Optional[str] = None,
        s_user_ids: Optional[str] = None,
        s_description: Optional[str] = None,
        s_give_txt: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> m_schema.FilterResBalanceGive:
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

    if type is not None:
        values = type.split(',')
        if len(values) == 1:
            val = values[0]
            items['type'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['type_start'] = int(val)

            val = values[1]
            if val != '':
                items['type_end'] = int(val)

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

    if create_time is not None:
        values = create_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['create_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['create_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['create_time_end'] = datetime.fromtimestamp(int(val))

    if operator_id is not None:
        values = operator_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['operator_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['operator_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['operator_id_end'] = int(val)

    if sucess_num is not None:
        values = sucess_num.split(',')
        if len(values) == 1:
            val = values[0]
            items['sucess_num'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['sucess_num_start'] = int(val)

            val = values[1]
            if val != '':
                items['sucess_num_end'] = int(val)

    if give_txt is not None:
        values = give_txt.split(',')
        if len(values) == 1:
            val = values[0]
            items['give_txt'] = val
        else:
            val = values[0]
            if val != '':
                items['give_txt_start'] = val

            val = values[1]
            if val != '':
                items['give_txt_end'] = val

    if s_user_ids is not None:
        search_items['user_ids'] = '%' + s_user_ids + '%'

    if s_description is not None:
        search_items['description'] = '%' + s_description + '%'

    if s_give_txt is not None:
        search_items['give_txt'] = '%' + s_give_txt + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_user_ids is not None:
        values = l_user_ids.split(',')
        values = [val for val in values]
        set_items['user_ids'] = values

    if l_coin is not None:
        values = l_coin.split(',')
        values = [int(val) for val in values]
        set_items['coin'] = values

    if l_balance is not None:
        values = l_balance.split(',')
        values = [int(val) for val in values]
        set_items['balance'] = values

    if l_type is not None:
        values = l_type.split(',')
        values = [int(val) for val in values]
        set_items['type'] = values

    if l_description is not None:
        values = l_description.split(',')
        values = [val for val in values]
        set_items['description'] = values

    if l_create_time is not None:
        values = l_create_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['create_time'] = values

    if l_operator_id is not None:
        values = l_operator_id.split(',')
        values = [int(val) for val in values]
        set_items['operator_id'] = values

    if l_sucess_num is not None:
        values = l_sucess_num.split(',')
        values = [int(val) for val in values]
        set_items['sucess_num'] = values

    if l_give_txt is not None:
        values = l_give_txt.split(',')
        values = [val for val in values]
        set_items['give_txt'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_balance_give(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_balance_give(items, search_items, set_items)

    return m_schema.FilterResBalanceGive(data=data, total=c)


@router.get(f'/coin/filter', response_model=m_schema.FilterResCoin)
async def filter_coin(
        id: Optional[str] = None,
        user_id: Optional[str] = None,
        change: Optional[str] = None,
        coin: Optional[str] = None,
        type: Optional[str] = None,
        description: Optional[str] = None,
        create_time: Optional[str] = None,
        out_trade_no: Optional[str] = None,
        l_id: Optional[str] = None,
        l_user_id: Optional[str] = None,
        l_change: Optional[str] = None,
        l_coin: Optional[str] = None,
        l_type: Optional[str] = None,
        l_description: Optional[str] = None,
        l_create_time: Optional[str] = None,
        l_out_trade_no: Optional[str] = None,
        s_type: Optional[str] = None,
        s_description: Optional[str] = None,
        s_out_trade_no: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> m_schema.FilterResCoin:
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

    if change is not None:
        values = change.split(',')
        if len(values) == 1:
            val = values[0]
            items['change'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['change_start'] = int(val)

            val = values[1]
            if val != '':
                items['change_end'] = int(val)

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

    if create_time is not None:
        values = create_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['create_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['create_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['create_time_end'] = datetime.fromtimestamp(int(val))

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

    if s_type is not None:
        search_items['type'] = '%' + s_type + '%'

    if s_description is not None:
        search_items['description'] = '%' + s_description + '%'

    if s_out_trade_no is not None:
        search_items['out_trade_no'] = '%' + s_out_trade_no + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_user_id is not None:
        values = l_user_id.split(',')
        values = [int(val) for val in values]
        set_items['user_id'] = values

    if l_change is not None:
        values = l_change.split(',')
        values = [int(val) for val in values]
        set_items['change'] = values

    if l_coin is not None:
        values = l_coin.split(',')
        values = [int(val) for val in values]
        set_items['coin'] = values

    if l_type is not None:
        values = l_type.split(',')
        values = [val for val in values]
        set_items['type'] = values

    if l_description is not None:
        values = l_description.split(',')
        values = [val for val in values]
        set_items['description'] = values

    if l_create_time is not None:
        values = l_create_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['create_time'] = values

    if l_out_trade_no is not None:
        values = l_out_trade_no.split(',')
        values = [val for val in values]
        set_items['out_trade_no'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_coin(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_coin(items, search_items, set_items)

    return m_schema.FilterResCoin(data=data, total=c)


@router.get(f'/balance/filter', response_model=m_schema.FilterResBalance)
async def filter_balance(
        id: Optional[str] = None,
        user_id: Optional[str] = None,
        change: Optional[str] = None,
        balance: Optional[str] = None,
        type: Optional[str] = None,
        description: Optional[str] = None,
        create_time: Optional[str] = None,
        user_withdraw_id: Optional[str] = None,
        operator_id: Optional[str] = None,
        out_trade_no: Optional[str] = None,
        good_id: Optional[str] = None,
        good_title: Optional[str] = None,
        good_num: Optional[str] = None,
        titlelog: Optional[str] = None,
        user_nick: Optional[str] = None,
        phone: Optional[str] = None,
        l_id: Optional[str] = None,
        l_user_id: Optional[str] = None,
        l_change: Optional[str] = None,
        l_balance: Optional[str] = None,
        l_type: Optional[str] = None,
        l_description: Optional[str] = None,
        l_create_time: Optional[str] = None,
        l_user_withdraw_id: Optional[str] = None,
        l_operator_id: Optional[str] = None,
        l_out_trade_no: Optional[str] = None,
        l_good_id: Optional[str] = None,
        l_good_title: Optional[str] = None,
        l_good_num: Optional[str] = None,
        l_titlelog: Optional[str] = None,
        l_user_nick: Optional[str] = None,
        l_phone: Optional[str] = None,
        s_type: Optional[str] = None,
        s_description: Optional[str] = None,
        s_out_trade_no: Optional[str] = None,
        s_good_id: Optional[str] = None,
        s_good_title: Optional[str] = None,
        s_good_num: Optional[str] = None,
        s_titlelog: Optional[str] = None,
        s_user_nick: Optional[str] = None,
        s_phone: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> m_schema.FilterResBalance:
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

    if change is not None:
        values = change.split(',')
        if len(values) == 1:
            val = values[0]
            items['change'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['change_start'] = int(val)

            val = values[1]
            if val != '':
                items['change_end'] = int(val)

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

    if create_time is not None:
        values = create_time.split(',')
        if len(values) == 1:
            val = values[0]
            items['create_time'] = datetime.fromtimestamp(int(val))
        else:
            val = values[0]
            if val != '':
                items['create_time_start'] = datetime.fromtimestamp(int(val))

            val = values[1]
            if val != '':
                items['create_time_end'] = datetime.fromtimestamp(int(val))

    if user_withdraw_id is not None:
        values = user_withdraw_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['user_withdraw_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['user_withdraw_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['user_withdraw_id_end'] = int(val)

    if operator_id is not None:
        values = operator_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['operator_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['operator_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['operator_id_end'] = int(val)

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

    if good_title is not None:
        values = good_title.split(',')
        if len(values) == 1:
            val = values[0]
            items['good_title'] = val
        else:
            val = values[0]
            if val != '':
                items['good_title_start'] = val

            val = values[1]
            if val != '':
                items['good_title_end'] = val

    if good_num is not None:
        values = good_num.split(',')
        if len(values) == 1:
            val = values[0]
            items['good_num'] = val
        else:
            val = values[0]
            if val != '':
                items['good_num_start'] = val

            val = values[1]
            if val != '':
                items['good_num_end'] = val

    if titlelog is not None:
        values = titlelog.split(',')
        if len(values) == 1:
            val = values[0]
            items['titlelog'] = val
        else:
            val = values[0]
            if val != '':
                items['titlelog_start'] = val

            val = values[1]
            if val != '':
                items['titlelog_end'] = val

    if user_nick is not None:
        values = user_nick.split(',')
        if len(values) == 1:
            val = values[0]
            items['user_nick'] = val
        else:
            val = values[0]
            if val != '':
                items['user_nick_start'] = val

            val = values[1]
            if val != '':
                items['user_nick_end'] = val

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

    if s_type is not None:
        search_items['type'] = '%' + s_type + '%'

    if s_description is not None:
        search_items['description'] = '%' + s_description + '%'

    if s_out_trade_no is not None:
        search_items['out_trade_no'] = '%' + s_out_trade_no + '%'

    if s_good_id is not None:
        search_items['good_id'] = '%' + s_good_id + '%'

    if s_good_title is not None:
        search_items['good_title'] = '%' + s_good_title + '%'

    if s_good_num is not None:
        search_items['good_num'] = '%' + s_good_num + '%'

    if s_titlelog is not None:
        search_items['titlelog'] = '%' + s_titlelog + '%'

    if s_user_nick is not None:
        search_items['user_nick'] = '%' + s_user_nick + '%'

    if s_phone is not None:
        search_items['phone'] = '%' + s_phone + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_user_id is not None:
        values = l_user_id.split(',')
        values = [int(val) for val in values]
        set_items['user_id'] = values

    if l_change is not None:
        values = l_change.split(',')
        values = [int(val) for val in values]
        set_items['change'] = values

    if l_balance is not None:
        values = l_balance.split(',')
        values = [int(val) for val in values]
        set_items['balance'] = values

    if l_type is not None:
        values = l_type.split(',')
        values = [val for val in values]
        set_items['type'] = values

    if l_description is not None:
        values = l_description.split(',')
        values = [val for val in values]
        set_items['description'] = values

    if l_create_time is not None:
        values = l_create_time.split(',')
        values = [datetime.fromtimestamp(int(val)) for val in values]
        set_items['create_time'] = values

    if l_user_withdraw_id is not None:
        values = l_user_withdraw_id.split(',')
        values = [int(val) for val in values]
        set_items['user_withdraw_id'] = values

    if l_operator_id is not None:
        values = l_operator_id.split(',')
        values = [int(val) for val in values]
        set_items['operator_id'] = values

    if l_out_trade_no is not None:
        values = l_out_trade_no.split(',')
        values = [val for val in values]
        set_items['out_trade_no'] = values

    if l_good_id is not None:
        values = l_good_id.split(',')
        values = [val for val in values]
        set_items['good_id'] = values

    if l_good_title is not None:
        values = l_good_title.split(',')
        values = [val for val in values]
        set_items['good_title'] = values

    if l_good_num is not None:
        values = l_good_num.split(',')
        values = [val for val in values]
        set_items['good_num'] = values

    if l_titlelog is not None:
        values = l_titlelog.split(',')
        values = [val for val in values]
        set_items['titlelog'] = values

    if l_user_nick is not None:
        values = l_user_nick.split(',')
        values = [val for val in values]
        set_items['user_nick'] = values

    if l_phone is not None:
        values = l_phone.split(',')
        values = [val for val in values]
        set_items['phone'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_balance(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_balance(items, search_items, set_items)

    return m_schema.FilterResBalance(data=data, total=c)