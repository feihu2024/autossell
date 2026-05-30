import datetime, time, json
from model import m_schema
from dao import d_db, d_account, d_package, d_order, d_balance, d_user, d_query, d_bigorder, d_video_task
from router import r_query
from model.mall import m_account
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Request
from model.address import UserAddress
from common import global_define, global_function
import logging
from .user import verify_token

# router = APIRouter()
router = APIRouter(dependencies=[Depends(verify_token)])

#
# @router.post(f'/create')
# async def create_account(item: m_account.CreateAccount):
#     """创建账户"""
#     t_account = m_account.TUserAccount(**item.dict())
#     t_account = d_account.create_account(t_account)
#     return m_account.SCreateAccount(**t_account.__dict__)

#
# @router.delete(f'/delete')
# async def delete_account(account_id: int):
#     d_account.delete_account_by_id(account_id)
#     # 删除不存在的条目不会报错，如何解决？
#     return {'code': 200, 'message': 'success'}

#
# @router.post(f'/update', summary="修改用户金额和积分")
# async def update_account(item: m_account.GetCoinBalance):
#     """根据账户id更新账户"""
#     if item.user_action == 'balance':
#         d_account.update_account_by_id(item.id, {"balance":item.balance})
#         d_account.insert_bank(m_account.BalanceModel(
#             user_id=item.user_id,
#             change=item.balance,
#             balance=item.balance,
#             create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#         ))
#     elif item.user_action == 'lock_balance':
#         d_account.update_lock_balance_by_id(item.id, {"lock_balance":item.lock_balance})
#     else:
#         d_account.update_account_by_id(item.id, {"coin":item.coin})
#         d_account.insert_coin(m_account.CoinModel(
#             user_id=item.user_id,
#             change=item.coin,
#             coin=item.coin,
#             create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#         ))
#     return {'code': 200, 'message': 'success'}

#
# @router.post(f'/prepare_withdraw', response_model=dict, summary='用户准备提现')
# async def user_prepare_with_draw(user_id: int):
#     query_str = {"table": "user_bank",
#                  "joins": [{"table": "user", "on_left": "user_id", "on_right": "id", "method": "right"}],
#                  "filters": [{"field": "user.id", "value": user_id}]}
#     return await r_query.get(r_query.QueryData.parse_obj(query_str))


@router.post(f'/start_withdraw', response_model=dict, summary='用户申请提现')
async def user_start_with_draw(request: Request,data: m_account.WithdrawModel):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    data.user_id = user_id
    s_user: m_schema.SUser = d_db.get_user(user_id=data.user_id)
    if s_user is not None:
            # fee_pro = 0
            # if s_user.level_id == 0:
            #     if data.fee_type == 1:
            #         fee_pro = global_define.setting_withdraw['fans'][0]
            #     elif data.fee_type == 2:
            #         fee_pro = global_define.setting_withdraw['fans'][1]
            # elif s_user.level_id == 1:
            #     if data.fee_type == 1:
            #         fee_pro = global_define.setting_withdraw['member'][0]
            #     elif data.fee_type == 2:
            #         fee_pro = global_define.setting_withdraw['member'][1]
            # elif s_user.level_id == 2:
            #     if data.fee_type == 1:
            #         fee_pro = global_define.setting_withdraw['boss'][0]
            #     elif data.fee_type == 2:
            #         fee_pro = global_define.setting_withdraw['boss'][1]
            # else:
            #     if data.fee_type == 1:
            #         fee_pro = global_define.setting_withdraw['bigboss'][0]
            #     elif data.fee_type == 2:
            #         fee_pro = global_define.setting_withdraw['bigboss'][1]
            # if fee_pro != data.fee_pro:
            #     return {'code': 200, 'message': '前后端扣费比例不一致'}

            user_accounts = d_account.get_account_info( data.user_id)
            # if not user_accounts or user_accounts.balance < data.amount:
            #     return {'code': 304, 'message': '资金账户错误'}

            if not s_user.phone:
                return {'code': 304, 'message': '联系方式错误'}

            if not data.type_id:
                return {'code': 304, 'message': '提现类型错误'}

            # 提现范围：大于10元，小于500元
            if data.amount < global_define.withdraw_config['low_balance'] or data.amount > global_define.withdraw_config['max_balance']:
                return {'code': 304, 'message': '提现金额错误'}

            # 支付密码验证
            # if len(data.tran_pass) < 6 or data.tran_pass != s_user.tran_pass:
            #     return {'code': 304, 'message': '支付密码无效'}

            if data.fee_type == 1:
                if not user_accounts or user_accounts.lock_balance < data.amount:
                    return {'code': 304, 'message': '资金账户错误'}
                total_balance = user_accounts.lock_balance - data.amount
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
                new_draw = m_schema.CreateUserWithdraw(amount=data.amount, user_withdraw_status_id=0,
                                                       user_id=data.user_id,
                                                       create_time=datetime.datetime.now(),
                                                       update_time=datetime.datetime.now(),
                                                       fee_type=data.fee_type,
                                                       fee_pro=global_define.withdraw_config['ded_bouns'],  # 默认提现比例 10%
                                                       out_batch_no=global_function.get_randoms(30),
                                                       batch_name="用户提现",
                                                       batch_remark=global_define.balance_type[16],
                                                       out_detail_no=global_function.get_randoms(30),
                                                       user_name=s_user.name,
                                                       user_phone=s_user.phone,
                                                       type_id=data.type_id,
                                                       user_bank_id=data.user_bank_id,
                                                       user_bank_other=data.user_bank_other,
                                                       surp_local_balance=total_balance
                                                       )
                base_info = d_db.insert_user_withdraw(new_draw)
            else:
                double_count_ls = d_bigorder.get_bigorder_set('double_count')  # 复投上限
                if s_user.pai_buydui <= double_count_ls.val_int:
                    return {'code': 304, 'message': '无余额提现权限，请联系管理员！'}

                if not user_accounts or user_accounts.balance < data.amount:
                    return {'code': 304, 'message': '余额资金账户错误'}

                total_balance = user_accounts.balance - data.amount
                d_account.update_account_by_id(user_accounts.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=data.user_id,
                    change=-data.amount,
                    balance=total_balance,
                    type=global_define.balance_type[6],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                ))
                new_draw = m_schema.CreateUserWithdraw(amount=data.amount, user_withdraw_status_id=0,
                                                       user_id=data.user_id,
                                                       create_time=datetime.datetime.now(),
                                                       update_time=datetime.datetime.now(),
                                                       fee_type=data.fee_type,
                                                       fee_pro=global_define.withdraw_config['ded_bouns'],
                                                       out_batch_no=global_function.get_randoms(30),
                                                       batch_name="用户提现",
                                                       batch_remark=global_define.balance_type[6],
                                                       out_detail_no=global_function.get_randoms(30),
                                                       user_name=s_user.name,
                                                       user_phone=s_user.phone,
                                                       type_id=data.type_id,
                                                       user_bank_id=data.user_bank_id,
                                                       user_bank_other=data.user_bank_other,
                                                       surp_balance=total_balance
                                                       )
                base_info = d_db.insert_user_withdraw(new_draw)

            return {'code': 200, 'message': 'success'}
    else:
        return {'code': 304, 'message': '该用户不存在'}

# @router.post(f'/user_bank/create', response_model=m_schema.SUserBank, summary="用户添加银行卡（默认)")
# async def create_user_default_bank(item: m_schema.CreateUserBank) -> m_schema.SUserBank:
#     if item.is_default == 1:
#         banks: List[m_schema.SUserBank] = d_db.filter_user_bank(items={'user_id': item.user_id}, search_items={},
#                                                                 set_items={}, page=1, page_size=100)
#         for bank in banks:
#             if bank.is_default:
#                 bank.is_default = 0
#                 d_db.update_user_bank(bank)
#
#         return d_db.insert_user_bank(item)
#     else:
#         return d_db.insert_user_bank(item)

#
# @router.post(f'/user_bank/set_default', response_model=dict, summary="设置默认银行卡")
# def set_default_address(user_id: int, bank_id: int):
#     """将用户地址列表下的某个地址设置为默认地址"""
#     banks: List[m_schema.SUserBank] = d_db.filter_user_bank(items={'user_id': user_id}, search_items={},
#                                                             set_items={})
#     for bank in banks:
#         if bank.id == bank_id:
#             bank.is_default = 1
#             d_db.update_user_bank(item=bank)
#         else:
#             bank.is_default = 0
#             d_db.update_user_bank(item=bank)
#     return {'code': 200, 'message': 'success'}
#
# @router.get(f'/get', response_model=list, summary="获取银行卡信息")
# def get_user_account(user_id:int = 0):
#     account_info = d_account.get_acount_list(user_id)
#     re = []
#     for i in account_info:
#         i = i.__dict__
#         #re.append({"id":i.get('id'), "user_id":i.get('user_id'), "balance":i.get('balance'), "lock_balance":i.get('lock_balance'), "coin":i.get('coin'), "description":i.get('description'), "create_time":i.get('create_time'), "bank_name":i.get('bank_name'), "id_card":i.get('id_card')})
#         re.append({"id":i.get('id'), "bank_name":i.get('bank_name'), "username":i.get('username'), "id_card":i.get('id_card'), "user_id":i.get('user_id'), "phone":i.get('phone'), "bank_address":i.get('bank_address'), "is_default":i.get('is_default')})
#     return re

@router.get(f'/get_coin_balance', response_model=m_account.SCreateAccount, summary="获取账户余额购物券额度")
def get_user_coin_balance(request: Request):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    account_info = d_account.get_coin_balance_list(user_id)
    re = None
    for i in account_info:
        re = i.__dict__
        #re.append({"id":i.get('id'), "user_id":i.get('user_id'), "balance":i.get('balance'), "lock_balance":i.get('lock_balance'), "coin":i.get('coin'), "description":i.get('description'), "create_time":i.get('create_time'), "bank_name":i.get('bank_name'), "id_card":i.get('id_card')})
    return re
#
# @router.post(f'/update_bank', response_model=dict, summary="修改银行卡信息t_user_bank")
# def update_bank(items: m_account.GetUserBank):
#     d_account.update_bank(items.bank_id, {"id_card": items.id_card, "bank_name": items.bank_name})
#     return {'code': 200, 'message': 'success'}
#
# @router.post(f'/get_coin_balance_income', summary="获取用户余额、积分、预收益")
# def get_user_coin_balance_income(user_id:int = 0):
#     """
#     计算条件：订单未计算收益，且在已支付或发货中。
#     返回值：balance，余额；lock_balance，锁定余额；coin，积分；freeze_balance，冻结额；flash_order_balance，近杀包出2个月秒售预收益额;order_id_income，预收益订单1,2,3；latest_preincome，最近一次正收益
#     """
#     re_val = [{"balance":0, "lock_balance":0, "coin":0, "freeze_balance":0, "flash_order_balance":0, "order_id_income":[], "latest_preincome":0}]
#     account_info = d_account.get_coin_balance(user_id)
#     if account_info:
#         re_val[0]['balance'] = account_info.balance
#         re_val[0]['lock_balance'] = account_info.lock_balance
#         re_val[0]['coin'] = account_info.coin
#         re_val[0]['freeze_balance'] = account_info.freeze_balance
#
#     #最近一笔预收益
#     preincome = d_order.get_user_willcomein_order(user_id)
#     if preincome:
#         l, g, s = preincome[0]
#         if l and g and s:
#             #分享
#             if l.recommender_id is not None and l.recommender_id > 0 and s.share_fee is not None:
#                 if s.supplier_fee > 0 and l.recommender_id == user_id:
#                     re_val[0]['latest_preincome'] += l.number * s.share_fee
#
#             #层级
#             if l.parent_uid is not None and l.parent_uid > 0 and s.parent_fee is not None:
#                 if s.parent_fee > 0 and l.parent_uid == user_id:
#                     re_val[0]['latest_preincome'] += l.number * s.parent_fee
#
#             # 直推
#             if l.invited_uid is not None and l.invited_uid > 0 and s.recommender_fee is not None:
#                 if s.recommender_fee > 0 and l.invited_uid == user_id:
#                     re_val[0]['latest_preincome'] += l.number * s.recommender_fee
#
#             # 供货介绍人的收益
#             if l.supplier_uid is not None and l.supplier_uid > 0 and s.supplier_fee is not None:
#                 if s.supplier_fee > 0 and l.supplier_uid == user_id:
#                     re_val[0]['latest_preincome'] += l.number * s.supplier_fee
#             # 见点
#             if l.top_uid is not None and l.top_uid > 0 and s.top_fee is not None:
#                 if s.top_fee > 0 and l.top_uid == user_id:
#                     re_val[0]['latest_preincome'] += l.number * s.top_fee
#         else:
#             logging.info(f"预收益信息")
#             if l:
#                 logging.info(f"order:{l.id}")
#             if g:
#                 logging.info(f"good:{g.id}")
#             if s:
#                 logging.info(f"good_spec:{s.id}")
#
#     flash_order_ids = d_package.get_flash_order_ids(user_id)
#     if len(flash_order_ids) > 0:
#         flash_orders = d_order.get_user_falsh_orders(flash_order_ids)
#         if flash_orders is not None:
#             for t_order_source, t_order, t_good_spec in flash_orders:
#                 get_res = d_package.get_order_package_forid(t_order_source.source_id)
#                 if get_res is not None and t_good_spec is not None:
#                     t_order, t_package = get_res
#                     if t_good_spec.price is None:
#                         t_good_spec.price = 0
#                     if t_package.flash_sale_price is None:
#                         t_package.flash_sale_price = 0
#                     this_balance = t_good_spec.price * t_order_source.amount - t_package.flash_sale_price * t_order_source.amount - t_package.devide_cost * t_order_source.amount
#                     re_val[0]["order_id_income"].append(t_order.id)
#                     re_val[0]["flash_order_balance"] += this_balance
#
#     #flash_order_balance 暂时不用，代最近一次预收益字段
#     re_val[0]["flash_order_balance"] = re_val[0]['latest_preincome']
#     return re_val
#
# @router.post(f'/get_balance_income_list', summary="获取预收益列表")
# def get_balance_income_list(user_id:int = 0):
#     """
#     计算条件：订单未计算收益，且在已支付1或发货中2。|
#         "type": "秒杀单商品售出",  |
#         "detail": "客户订单未完结",|
#         "good_name": null, 商品标题名称|
#         "good_id": 1, 商品id|
#         "good_spec_id": 1, 使用规格id|
#         "t_order_create_time": null, 客户订单创建时间|
#         "t_order_num": 10, 客户订单包含秒杀包商品数量|
#         "t_order_income": 200， 本次秒杀包出售收益额|
#     """
#     re_val = []
#     flash_order_ids = d_package.get_flash_order_ids(user_id)
#     if len(flash_order_ids) > 0:
#         flash_orders = d_order.get_user_falsh_orders2(flash_order_ids)
#         if flash_orders is not None:
#             for t_order_source, t_order, t_good_spec, t_good in flash_orders:
#                 get_res = d_package.get_order_package_forid(t_order_source.source_id)
#                 if get_res is not None and t_good_spec is not None:
#                     f_order, t_package = get_res
#                     if t_good_spec.price is None:
#                         t_good_spec.price = 0
#                     if t_package.flash_sale_price is None:
#                         t_package.flash_sale_price = 0
#                     # this_balance = t_good_spec.price * t_order_source.amount - t_package.flash_sale_price * t_order_source.amount
#                     this_balance = t_package.devide_cost * t_order_source.amount
#                     re_val.append({"type": global_define.balance_type[10],"detail": "客户订单未完结","good_name": t_good.title, "good_id":t_good.id, \
#                                    "good_spec_id": t_good_spec.id, "t_order_create_time": t_order.create_time, "t_order_num": t_order_source.amount, \
#                                    "t_order_income": this_balance,"order_id": t_order.id,"source_order_id": t_order_source.id})
#     #分享收益 1 | 未发货    2 | 已发货   9 | 未使用
#     orders_list = d_order.get_user_willcomein_order(user_id)
#     for l,g,s in orders_list:
#         if g is None or s is None:
#             continue
#         if l.zdyspec:
#             l_zdyspec = json.loads(l.zdyspec)
#             # 分享
#             if l.recommender_id is not None and l.recommender_id > 0 and l.is_wholesale != 2:
#                 if float(l_zdyspec['分享']) > 0 and l.recommender_id == user_id:
#                     re_val.append(
#                         {"type": global_define.balance_type[13], "detail": "客户订单未完结", "good_name": g.title,\
#                          "good_id": g.id, \
#                          "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,\
#                          "t_order_income": float(l_zdyspec['分享'])*100, "order_id": l.id})
#
#             # 层级
#             if l.parent_uid is not None and l.parent_uid > 0 and l.is_wholesale != 2:
#                 if float(l_zdyspec['层级']) > 0 and l.parent_uid == user_id:
#                     re_val.append(
#                         {"type": global_define.balance_type[1], "detail": "客户订单未完结", "good_name": g.title,\
#                          "good_id": g.id, \
#                          "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,\
#                          "t_order_income":  float(l_zdyspec['层级'])*100, "order_id": l.id})
#             # 直推
#             is_invited_fee = False
#             if l.invited_uid is not None and l.invited_uid > 0:
#                 if float(l_zdyspec['直推']) > 0 and l.invited_uid == user_id:
#                     is_invited_fee = True
#                     re_val.append(
#                         {"type": global_define.balance_type[14], "detail": "客户订单未完结", "good_name": g.title,\
#                          "good_id": g.id, \
#                          "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,\
#                          "t_order_income":  float(l_zdyspec['直推'])*100, "order_id": l.id})
#             # 直推2
#             if l.invited_uid is not None and l.invited_uid > 0 and not is_invited_fee:
#                 if float(l_zdyspec['直推']) > 0 and l.invited_uid == user_id:
#                     re_val.append(
#                         {"type": global_define.balance_type[30], "detail": "客户订单未完结", "good_name": g.title,\
#                          "good_id": g.id, \
#                          "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,\
#                          "t_order_income":  float(l_zdyspec['直推'])*100, "order_id": l.id})
#             # 供货介绍人的收益
#             if l.supplier_uid is not None and l.supplier_uid > 0 and l.is_wholesale != 2:
#                 if float(l_zdyspec['供货']) > 0 and l.supplier_uid == user_id:
#                     re_val.append(
#                         {"type": global_define.balance_type[15], "detail": "客户订单未完结", "good_name": g.title,\
#                          "good_id": g.id, \
#                          "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,\
#                          "t_order_income":  float(l_zdyspec['供货'])*100, "order_id": l.id})
#             # 见点
#             if l.top_uid is not None and l.top_uid > 0 and l.is_wholesale != 2:
#                 if float(l_zdyspec['老板']) > 0 and l.top_uid == user_id:
#                     re_val.append(
#                         {"type": global_define.balance_type[2], "detail": "客户订单未完结", "good_name": g.title,\
#                          "good_id": g.id, \
#                          "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,\
#                          "t_order_income":  float(l_zdyspec['老板'])*100, "order_id": l.id})
#             # 平级奖
#             if l.eqlevel_uid is not None and l.eqlevel_uid > 0 and l.is_wholesale != 2:
#                 if float(l_zdyspec['平级']) > 0 and l.eqlevel_uid == user_id:
#                     re_val.append(
#                         {"type": global_define.balance_type[22], "detail": "客户订单未完结", "good_name": g.title,\
#                          "good_id": g.id, \
#                          "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,\
#                          "t_order_income":  float(l_zdyspec['平级'])*100, "order_id": l.id})
#             #随机收益
#             if l.random_fee_uid is not None and l.random_fee_uid > 0:
#                 if float(l_zdyspec['随机分']) > 0 and l.random_fee_uid == user_id:
#                     re_val.append(
#                         {"type": global_define.balance_type[32], "detail": "客户订单未完结", "good_name": g.title,\
#                          "good_id": g.id, \
#                          "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,\
#                          "t_order_income":  float(l_zdyspec['随机分'])*100, "order_id": l.id})
#                     # 随机收益 推荐人收益 幸运奖
#                     if l.random_invited_uid is not None and l.random_invited_uid > 0:
#                         re_val.append(
#                             {"type": global_define.balance_type[36], "detail": "客户订单未完结", "good_name": g.title, \
#                              "good_id": g.id, \
#                              "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number, \
#                              "t_order_income": float(l_zdyspec['随机分']) * 100, "order_id": l.id})
#
#             #团长收益
#             if l.tuan_uid is not None and l.tuan_uid > 0:
#                 try:
#                     tuan_fee = float(l_zdyspec['团长'])
#                 except:
#                     tuan_fee = 0
#                 if tuan_fee > 0 and l.tuan_uid == user_id:
#                     re_val.append(
#                         {"type": global_define.balance_type[33], "detail": "客户订单未完结", "good_name": g.title,\
#                          "good_id": g.id, \
#                          "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,\
#                          "t_order_income":  tuan_fee*100, "order_id": l.id})
#
#             #上级团长
#             if l.retuan_uid is not None and l.retuan_uid > 0:
#                 try:
#                     retuan_fee = float(l_zdyspec['上级团'])
#                 except:
#                     retuan_fee = 0
#                 if retuan_fee > 0 and l.retuan_uid == user_id:
#                     re_val.append(
#                         {"type": global_define.balance_type[34], "detail": "客户订单未完结", "good_name": g.title,\
#                          "good_id": g.id, \
#                          "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,\
#                          "t_order_income":  retuan_fee*100, "order_id": l.id})
#
#             # 间推收益
#             if l.ininvited_uid is not None and l.ininvited_uid > 0:
#                 try:
#                     jiantui_fee = float(l_zdyspec['间推'])
#                 except:
#                     jiantui_fee = 0
#                 if jiantui_fee > 0 and l.ininvited_uid == user_id:
#                     re_val.append(
#                         {"type": global_define.balance_type[35], "detail": "客户订单未完结",
#                          "good_name": g.title, \
#                          "good_id": g.id, \
#                          "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number, \
#                          "t_order_income": jiantui_fee * 100, "order_id": l.id})
#         else:
#             #分享
#             if l.recommender_id is not None and l.recommender_id > 0 and s.share_fee is not None and l.is_wholesale != 2:
#                 if s.share_fee > 0 and l.recommender_id == user_id:
#                     re_val.append({"type": global_define.balance_type[13], "detail": "客户订单未完结","good_name": g.title, "good_id": g.id,\
#                                    "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number, "t_order_income": s.share_fee, "order_id": l.id})
#
#             #层级
#             if l.parent_uid is not None and l.parent_uid > 0 and s.parent_fee is not None and l.is_wholesale != 2:
#                 if s.parent_fee > 0 and l.parent_uid == user_id:
#                     re_val.append({"type": global_define.balance_type[1], "detail": "客户订单未完结", "good_name": g.title, "good_id": g.id, \
#                                    "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,\
#                                    "t_order_income": s.parent_fee, "order_id": l.id})
#             # 直推
#             is_invited_fee = False
#             if l.invited_uid is not None and l.invited_uid > 0 and s.recommender_fee is not None:
#                 if s.recommender_fee > 0 and l.invited_uid == user_id:
#                     is_invited_fee = True
#                     re_val.append({"type": global_define.balance_type[14], "detail": "客户订单未完结", "good_name": g.title, "good_id": g.id, \
#                                    "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,\
#                                    "t_order_income": s.recommender_fee, "order_id": l.id})
#             # 直推2
#             if l.invited_uid is not None and l.invited_uid > 0 and s.recommender2_fee is not None:
#                 if s.recommender2_fee > 0 and l.invited_uid == user_id:
#                     re_val.append({"type": global_define.balance_type[30], "detail": "客户订单未完结", "good_name": g.title, "good_id": g.id, \
#                                    "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,\
#                                    "t_order_income": s.recommender2_fee, "order_id": l.id})
#             # 供货介绍人的收益
#             if l.supplier_uid is not None and l.supplier_uid > 0 and s.supplier_fee is not None and l.is_wholesale != 2:
#                 if s.supplier_fee > 0 and l.supplier_uid == user_id:
#                     re_val.append({"type": global_define.balance_type[15], "detail": "客户订单未完结", "good_name": g.title, "good_id": g.id, \
#                                    "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,\
#                                    "t_order_income": s.supplier_fee, "order_id": l.id})
#             # 见点
#             if l.top_uid is not None and l.top_uid > 0 and s.top_fee is not None and l.is_wholesale != 2:
#                 if s.top_fee > 0 and l.top_uid == user_id:
#                     re_val.append({"type": global_define.balance_type[2], "detail": "客户订单未完结", "good_name": g.title, "good_id": g.id, \
#                                    "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,\
#                                    "t_order_income": s.top_fee, "order_id": l.id})
#             # 平级奖
#             if l.eqlevel_uid is not None and l.eqlevel_uid > 0 and s.eqlevel_fee is not None and l.is_wholesale != 2:
#                 if s.eqlevel_fee > 0 and l.eqlevel_uid == user_id:
#                     re_val.append({"type": global_define.balance_type[22], "detail": "客户订单未完结", "good_name": g.title, "good_id": g.id,
#                                    "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,\
#                                    "t_order_income": s.eqlevel_fee, "order_id": l.id})
#     return re_val



    #
    # uinfo = d_user.get_user_by_id(user_id)
    # uids = []
    # comein_name = global_define.balance_type[1]
    # is_inv = True
    # if uinfo.parent_id is not None and uinfo.parent_id == 0:
    #     uids = d_user.get_invited_user_ids(user_id)
    #     comein_name = global_define.balance_type[14]
    # else:
    #     uids = d_user.get_invparent_user_ids(user_id)
    #     is_inv = False
    # inv_list = d_order.get_user_invparent_order(uids)
    # for l,g,s in inv_list:
    #     if g is None or s is None:
    #         continue
    #     comein_balance = s.parent_fee
    #     if is_inv:
    #         comein_balance = s.recommender_fee
    #     re_val.append({"type": comein_name, "detail": "客户订单未完结","good_name": g.title, "good_id": g.id,\
    #                    "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number, "t_order_income": comein_balance})
    #
    # #供货介绍人的收益
    # introducer_list = d_order.get_user_introducer_order(user_id)
    # for l,g,s in introducer_list:
    #     if g is None or s is None:
    #         continue
    #     re_val.append({"type": global_define.balance_type[15], "detail": "客户订单未完结","good_name": g.title, "good_id": g.id,\
    #                    "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number, "t_order_income": s.supplier_fee})
    # #见点
    # if uinfo.parent_id is not None and uinfo.parent_id == 0:
    #     member_ids = d_user.get_member_ids([user_id])
    #     top_list = d_order.get_user_invparent_order(member_ids)
    #     for l, g, s in top_list:
    #         if g is None or s is None or l.create_time < uinfo.level_top_time:
    #             continue
    #         re_val.append({"type": global_define.balance_type[2], "detail": "客户订单未完结", "good_name": g.title, "good_id": g.id, \
    #                        "good_spec_id": s.id, "t_order_create_time": l.create_time, "t_order_num": l.number,
    #                        "t_order_income": s.top_fee})
    #


@router.get(f"/getuser_balancelog", summary="获取资金记录")
async def search_balance(request: Request, page:int = 1):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    item = d_balance.SearchBalance(
        user_id=user_id,
        page=page,
        page_size=20
    )
    return d_balance.search_balance(item)

@router.get(f"/getuser_incomelog", summary="获取收益记录")
async def getuser_incomelog(request: Request, page:int = 1):
    """
    统计以下收益：
    1:直推收益",
    2:"大公排收益",
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    item = d_balance.SearchBalance(
        user_id=user_id,
        page=page,
        page_size=20
    )
    return d_balance.search_comein(item)

@router.get(f"/getuser_addlog", summary="获取增量(收入)资金记录")
async def getuser_addlog(request: Request, page:int = 1):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    item = d_balance.SearchBalance(
        user_id=user_id,
        is_comein=1,
        page=page,
        page_size=20
    )
    return d_balance.search_balance(item)

@router.get(f"/getuser_minuslog", summary="获取减少(支出)资金记录")
async def getuser_minuslog(request: Request, page:int = 1):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    item = d_balance.SearchBalance(
        user_id=user_id,
        is_comein=0,
        page=page,
        page_size=20
    )
    return d_balance.search_balance(item)

@router.get(f"/vtask/getuser_log", summary="获取视频条数用户消费日志记录")
async def vtask_getuser_log(request: Request, good_id:int = None, page:int = 1, page_size:int = 20):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    item = d_video_task.SearchVideoTask(
        user_id=user_id,
        page=page,
        page_size=20
    )
    if good_id is not None:
        item.good_id = good_id
    return d_video_task.get_vrecharge_log_for_user(item)

@router.get(f"/vtask/getowner_log", summary="获取视频条数码主消费日志记录")
async def vtask_getowner_log(request: Request, good_id:int = None, page:int = 1, page_size:int = 20):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    item = d_video_task.SearchVideoTask(
        owner_id=user_id,
        page=page,
        page_size=20
    )
    if good_id is not None:
        item.good_id = good_id
    return d_video_task.get_vrecharge_log_for_owner(item)


@router.get(f"/vtask/getuser_recharge", summary="获取用户激活充值码列表")
async def vtask_getuser_recharge(request: Request, good_id:int = None, level_id:int = 0, act_id:int = -1, page:int = 1, page_size:int = 20):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    item = d_video_task.SearchVideoTask(
        user_id=user_id,
        page=page,
        page_size=20,
        video_level=level_id,
        is_act=act_id
    )
    if good_id is not None:
        item.good_id = good_id
    return d_video_task.get_vrecharge_for_user(item)

@router.get(f"/vtask/getowner_recharge", summary="获取码主充值码列表")
async def vtask_getowner_recharge(request: Request, good_id:int = None, level_id:int = 0, page:int = 1, page_size:int = 20):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    item = d_video_task.SearchVideoTask(
        owner_id=user_id,
        page=page,
        page_size=20,
        video_level=level_id
    )
    if good_id is not None:
        item.good_id = good_id
    return d_video_task.get_vrecharge_for_owner(item)

@router.get(f'/vtask/video_level', summary="获取视频分发身份列表")
async def get_video_level(request: Request):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    return global_define.video_level


@router.get(f"/user/turn/log", summary="获取用户转账记录")
async def getuser_turnlog(request: Request, page_num:int = 1):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    item = d_balance.SearchBalance(
        user_id=user_id,
        type=f"{global_define.balance_type[4]},{global_define.balance_type[8]}",
        page=page_num,
        page_size=20
    )
    return d_balance.search_balance(item)

# @router.get(f"/getuser_withdrawlog", summary="获取用户提现记录")
# async def getuser_withdrawlog(request: Request, page_num:int = 1):
#     welcomesession = request.headers.get('welcomesession')
#     user_id = d_user.get_login_id(welcomesession)
#     item = d_balance.SearchBalance(
#         user_id=user_id,
#         type=global_define.balance_type[6],
#         page=page_num,
#         page_size=20
#     )
#     return d_balance.search_balance(item)
#
# @router.get(f"/getuser_invitedlog", summary="获取用户直推记录")
# async def getuser_invitedlog(request: Request, page_num:int = 1):
#     """
#     统计以下收益：
#     1:直推收益,
#     2:分红推荐收益,
#     """
#     welcomesession = request.headers.get('welcomesession')
#     user_id = d_user.get_login_id(welcomesession)
#     item = d_balance.SearchBalance(
#         user_id=user_id,
#         page=page_num,
#         page_size=20
#     )
#     return d_balance.search_comein_tuijian(item)
#
# @router.get(f"/getuser_dividendlog", summary="获取用户分红记录")
# async def getuser_dividendlog(request: Request, page_num:int = 1):
#     welcomesession = request.headers.get('welcomesession')
#     user_id = d_user.get_login_id(welcomesession)
#     item = d_balance.SearchBalance(
#         user_id=user_id,
#         # type=global_define.balance_type[2],
#         page=page_num,
#         page_size=20
#     )
#     return d_balance.search_comein_fenhong(item)
#
# @router.get(f"/getuser_randomlog", summary="获取用户随机分奖励记录")
# async def getuser_randomlog(request: Request, page_num:int = 1):
#     welcomesession = request.headers.get('welcomesession')
#     user_id = d_user.get_login_id(welcomesession)
#     item = d_balance.SearchBalance(
#         user_id=user_id,
#         type=global_define.balance_type[3],
#         page=page_num,
#         page_size=20
#     )
#     return d_balance.search_balance(item)

@router.get(f"/get/invitlog", summary="获取用户推荐资金收入/支出记录")
async def get_invitlog(request: Request, page:int = 1, page_size:int = 10):
    """
        lock_balance
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "lock_balance",
        "selects": ["lock_balance"],
        "filters": [
            {
                "field": "lock_balance.user_id",
                "value": user_id
            }
        ],
        "order_by": [{"field": "lock_balance.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res

@router.get(f"/get/buycoinlog", summary="获取用户购物券资金收入/支出记录")
async def get_buycoinlog(request: Request, page:int = 1, page_size:int = 10):
    """
        t_coin
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "coin",
        "selects": ["coin"],
        "filters": [
            {
                "field": "coin.user_id",
                "value": user_id
            }
        ],
        "order_by": [{"field": "coin.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res

@router.get(f"/get/withdraw", summary="获取用户提现记录")
async def get_withdraw(request: Request, page:int = 1, page_size:int = 10):
    """
        t_coin
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "user_withdraw",
        "selects": ["user_withdraw"],
        "filters": [
            {
                "field": "user_withdraw.user_id",
                "value": user_id
            }
        ],
        "order_by": [{"field": "user_withdraw.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res

@router.post(f"/tranbalance", summary="余额转账")
async def tranbalance(item: m_account.UserTran):
    userinfo = d_user.get_user_by_id(item.user_id)
    traninfo = d_user.get_user_by_id(item.tran_id)
    if userinfo and traninfo:
        useraccount = d_account.get_account_info(item.user_id)
        tranaccount = d_account.get_account_info(item.tran_id)
        if useraccount and tranaccount:
            if item.balance > useraccount.balance:
                return {'status': 400, 'message': f"转账金额有误"}
            useraccount_balance = useraccount.balance - item.balance
            tranaccount_balance = tranaccount.balance + item.balance
            d_account.update_account_by_id(useraccount.id, {"balance": useraccount_balance})
            d_account.update_account_by_id(tranaccount.id, {"balance": tranaccount_balance})
            d_account.add_tran_log(item.user_id,userinfo.phone,userinfo.nickname,useraccount_balance,item.tran_id,traninfo.phone,traninfo.nickname,tranaccount_balance,item.balance)
            user_banalce_out = m_account.BalanceModel(
                user_id=item.user_id,
                change=-item.balance,
                balance=useraccount_balance,
                type=global_define.balance_type[8],
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                good_id=0,
                good_title=f"{traninfo.id},{traninfo.phone}",
                good_num=0,
                out_trade_no=''
            )
            d_account.add_balance(user_banalce_out)
            tran_banalce_add = m_account.BalanceModel(
                user_id=item.tran_id,
                change=item.balance,
                balance=tranaccount_balance,
                type=global_define.balance_type[4],
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                good_id=0,
                good_title=f"{userinfo.id},{userinfo.phone}",
                good_num=0,
                out_trade_no=''
            )
            d_account.add_balance(tran_banalce_add)
            return {'status': 200, 'message': f"access"}
        else:
            return {'status': 400, 'message': f"未知账户"}
    else:
        return {'status': 400, 'message': f"未知用户"}

@router.get(f"/get/fund", summary="获取用户对应的资金池")
async def get_fund(request: Request):
    """
  `id` int NOT NULL AUTO_INCREMENT COMMENT '序号id',
  `date_num` varchar(100) DEFAULT NULL COMMENT '期id(初级one20250818,高级two20250818,顶级three20250818)',
  `stat` tinyint DEFAULT '0' COMMENT '是否结算,默认0待结算1已结算',
  `balance` int DEFAULT '0' COMMENT '金额',
  `run_balance` int DEFAULT '0' COMMENT '执行金额',
  `register_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `end_time` timestamp NULL DEFAULT NULL COMMENT '截止时间',
  `run_time` timestamp NULL DEFAULT NULL COMMENT '执行时间',
  `users` text COMMENT '当前达标人(逗号分开的会员id)',
  `detail` text COMMENT '备注',
  `ftype` tinyint DEFAULT '0' COMMENT '资金类型:0初级1高级2顶级',
  `users_time` timestamp NULL DEFAULT NULL COMMENT '会员归集时间',
    """
    page: int = 1
    page_size:int = 10
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    fund_list = d_account.get_user_for_fund(user_id)
    return fund_list

@router.get(f"/get/fundls", summary="获取有效资金池列表")
async def get_fundls(request: Request):
    """
        t_coin
    """
    page: int = 1
    page_size:int = 10
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "fund_pond",
        "selects": ["fund_pond"],
        "filters": [
            {
                "field": "fund_pond.stat",
                "value": 0
            }
        ],
        "order_by": [{"field": "fund_pond.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res

@router.get(f"/get/user_set", summary="获取资金池配置数据")
async def get_user_set(request: Request):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    """
        this_inv_real_user   本期有效推荐人数
        this_inv_fund_user   本期奖金池需要推荐的人数        
        next_level_count   升级下一级用户推荐数量
        this_inv_level_user   总有效推荐人数
    """
    re_val = {'this_inv_real_user': 0, 'this_inv_fund_user': 0, 'next_level_count': 0, 'this_inv_level_user':0}
    uinfo = d_user.get_user_by_id(user_id)
    if uinfo:
        inv_total = d_user.get_bagorder_user_count(user_id)
        re_val['next_level_count'] = inv_total
        if uinfo.level_id == 0:
            level_one = d_bigorder.get_bigorder_set('level_one')  # level_one.val_int
            re_val['next_level_count'] = level_one.val_int
        elif uinfo.level_id == 1:
            #register_time
            fund_info = d_account.get_user_fund_first(1)
            fund_one = d_bigorder.get_bigorder_set('fund_one')  # fund_one.val_int
            level_two = d_bigorder.get_bigorder_set('level_two')  # level_two.val_int
            re_val['next_level_count'] = level_two.val_int
            re_val['this_inv_fund_user'] = fund_one.val_int
        elif uinfo.level_id == 2:
            fund_info = d_account.get_user_fund_first(2)
            fund_two = d_bigorder.get_bigorder_set('fund_two')  # fund_two.val_int
            level_three = d_bigorder.get_bigorder_set('level_three')  # level_three.val_int
            re_val['next_level_count'] = level_three.val_int
            re_val['this_inv_fund_user'] = fund_two.val_int
        elif uinfo.level_id == 3:
            fund_info = d_account.get_user_fund_first(3)
            fund_three = d_bigorder.get_bigorder_set('fund_three')  # fund_three.val_int
            re_val['next_level_count'] = 10000
            re_val['this_inv_fund_user'] = fund_three.val_int

    return re_val

@router.post(f'/video/act', summary="激活用户充值码，并给用户充值条数")
async def create_video_act(request: Request, item: d_video_task.ActModel):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    re_val = {'code': 1}
    if user_id == item.user_id and item.address_id > 0:
         re_val['code'] = d_video_task.act_recharge_code(user_id, item.act_code, item.address_id)
    else:
        re_val['code'] = -1
    return re_val