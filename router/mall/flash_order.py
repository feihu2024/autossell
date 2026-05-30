#!/usr/bin/env python
# encoding: utf-8
import json
import logging
import time, datetime
import uuid
from typing import Optional, List, Text

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field
from wechatpayv3 import WeChatPayType, SignType

from common import Dao, global_define
from config import DOMAIN
from config import WX
from dao import d_db, d_user, d_package, d_flash_order_return, d_settings, d_account, d_groupsir, d_order,d_good
from model import schema
from model.schema import TUser, TUserAccount, TFlashOrder, TPackageExpress, TPackage, TGood, TGoodSpec
from service.mall import s_flash_order
from service.wx_service import wxpay
from model.mall import m_account

router = APIRouter()


class AFlashOrderPay(BaseModel):
    flash_order_ids: List[int]
    user_id: int
    total_price: int


@router.post('/pay')
async def pay(data: AFlashOrderPay):
    with Dao() as db:
        user: Optional[TUser] = db.query(TUser).filter(TUser.id == data.user_id).first()
        if user is None:
            raise HTTPException(400, "用户不存在")

        user_account: Optional[TUserAccount] = db.query(TUserAccount).filter(
            TUserAccount.user_id == data.user_id).first()
        if user_account is None:
            user_account = TUserAccount(user_id=data.user_id, balance=0)
            db.add(user_account)
            db.commit()
            db.refresh(user_account)
            db.refresh(user)

    fee_to_pay = 0
    out_trade_no = f"{int(time.time())}{user_account.user_id:08d}{uuid.uuid4().hex[-4:]}"

    total_balance = user_account.balance

    for flash_order_id in data.flash_order_ids:
        flash_order: Optional[schema.TFlashOrder] = d_db.get_flash_order(flash_order_id)
        if flash_order is None:
            raise HTTPException(400, "订单不存在")
        if flash_order.status != 0:
            raise HTTPException(400, "订单状态不正确")

        # package: Optional[schema.TPackage] = d_db.get_package(flash_order.package_id)
        # if package is None:
        #     raise HTTPException(400, "套餐不存在")
        # fee = package.flash_sale_price * package.amount
        package_spec: Optional[schema.TGoodSpec] = d_db.get_good_spec(flash_order.spec_id)
        if package_spec is None:
            raise HTTPException(400, "规格套餐不存在")

        fee = flash_order.flash_price

        real_balance_cost = min(fee, total_balance)
        total_balance = total_balance - real_balance_cost
        fee = fee - real_balance_cost
        assert fee >= 0

        fee_to_pay += fee
        with Dao() as db:
            db.query(TFlashOrder).filter(TFlashOrder.id == flash_order.id).update(
                {"out_trade_no": out_trade_no, "paid_balance": real_balance_cost, "paid_amount": fee})
            db.commit()

    if data.total_price != fee_to_pay:
        logging.error(f'前端金额为: {data.total_price}分，后端计算金额为:{fee_to_pay}分，金额不一致')
        raise HTTPException(status_code=400, detail='前后端价格不一致')

    body = {'code': 200, 'detail': '不需要支付'}
    if fee_to_pay:
        logging.info('start to wxpay')
        res = wxpay.pay(
            out_trade_no=out_trade_no,
            amount={'total': fee_to_pay, 'currency': 'CNY'},
            description='秒杀商品',
            payer={'openid': user.open_id},
            notify_url=f"{DOMAIN}/wx/notify/flash_pay",
            pay_type=WeChatPayType.JSAPI
        )

        if res[0] == 200:
            logging.info(res[1])
            if isinstance(res[1], Text):
                data = json.loads(res[1])
            body = {
                "appId": WX.appId,
                "timeStamp": str(int(time.time())),
                "nonceStr": uuid.uuid4().hex[:32],
                "package": f"prepay_id={data['prepay_id']}",
                "signType": "RSA"
            }
            body['paySign'] = wxpay.sign(
                data=[body['appId'], body['timeStamp'], body['nonceStr'], body['package']],
                sign_type=SignType.RSA_SHA256)
        else:
            logging.error(res[1])
            raise HTTPException(status_code=400, detail=res[1]['message'])
    else:
        logging.info('no need to pay')
        s_flash_order.pay_success(amount=fee_to_pay, out_trade_no=out_trade_no)
    return body


class ASaleStatus(BaseModel):
    flash_order_id: int
    user_id: int
    single_status: int = Field(..., description='是否单份代卖')
    #whole_status: int = Field(..., description='是否整份代卖')


@router.post('/sale_status')
async def sale_status(data: ASaleStatus):
    with Dao() as db:
        flash_order = db.query(TFlashOrder).filter(TFlashOrder.id == data.flash_order_id).first()
        if flash_order is None:
            raise HTTPException(400, "订单不存在")
        
        if flash_order.status is None:
            raise HTTPException(400, "订单状态不正确")
        
        if flash_order.status == 0:
            raise HTTPException(400, "订单未支付")

        if flash_order.status != 1:
            raise HTTPException(400, "订单状态不正确")

        flash_order.single_status = data.single_status
        #flash_order.whole_status = data.whole_status
        flash_order.put_on_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        flash_order.status = 2
        db.commit()

class AApplyDelivery(BaseModel):
    flash_order_id: int
    user_id: int
    amount: int = Field(title='提货数量')
    address_id: int = Field(title='地址id')


@router.post(f'/apply_delivery')
async def apply_delivery(data: AApplyDelivery):
    """申请提货"""
    # 获取订单信息
    with Dao() as db:
        order, package, good, good_spec = db.query(TFlashOrder, TPackage, TGood, TGoodSpec).outerjoin(TPackage, TFlashOrder.package_id == TPackage.id).outerjoin(TGood, TPackage.good_id == TGood.id).outerjoin(TGoodSpec, TFlashOrder.spec_id == TGoodSpec.id)\
            .filter(TFlashOrder.id == data.flash_order_id).first()

        # 检查订单是否可以取货
        if order is None:
            raise HTTPException(400, "订单不存在")
        order: TFlashOrder

        if order.status not in [1, 2]: # 待上架或者转卖中
            raise HTTPException(400, "订单状态不正确")

        # 剩余商品数量
        stock = order.number - order.sold - order.return_sold # 总商品数量减去售出数量
        if stock < data.amount:
            raise HTTPException(400, "订单商品数量不够")
        if good_spec.stock < data.amount:
            raise HTTPException(400, "商品库存不足")

        # 更新订单信息
        #order.sold += data.amount
        order.return_sold += data.amount
        order_sole = order.return_sold + order.sold
        if order_sole >= order.number:
            order.status = 7
            order.complete_time = datetime.datetime.now()
        good_spec.stock -= data.amount
        db.flush()
        db.commit()
        #db.refresh(order, good_spec)

        status_id = 1
        if good.type == 0:
            status_id = 5
        # 记录新的邮寄订单
        package_express = TPackageExpress(
            flash_order_id=order.id,
            status=status_id, # 待发货/未使用
            amount=data.amount,
            address_id=data.address_id,
            apply_time=datetime.datetime.now()
        )
        db.add(package_express)
        db.flush()

        db.commit()
    return {'code': 0, 'detail': '申请成功'}

@router.post(f'/retun_flash_order')
async def return_flash_order(data: d_flash_order_return.FlashOrderReturn):
    """
    一单一退，24小时倒计时后出现退货按钮; 2023/10/7暂时取消时间限制和收益分配
    """
    #计算付款时间到现在的时长
    user_info = d_user.get_user_by_id(data.user_id)
    order_info = d_flash_order_return.get_flash_order(data.flash_order_id, data.user_id)
    if not user_info or not order_info:
        raise HTTPException(400, f"用户{data.user_id} 或 订单{data.flash_order_id}，不存在。")
    if order_info.is_assign_income != 0:
        raise HTTPException(400, f"订单{data.flash_order_id}，已经分配过收益。")
    package_info = d_package.get_package(order_info.package_id)
    good_info = d_good.get_good_data(package_info.good_id)

    #未到时长，不允许退货
    income_day = False
    now_time = datetime.datetime.now()

    # if order_info.put_on_time is None:
    #     raise HTTPException(402, f"订单{data.flash_order_id}，上架时间错误。")
    # else:
        #2023.10.9变更对比时间为订单创建时间
        # put_on_time = order_info.put_on_time + datetime.timedelta(hours=global_define.setting_orders["rerun_flash_order_times"])
    put_on_time = order_info.create_time + datetime.timedelta(hours=d_settings.get_settings().flash_order_owner_times)
    if put_on_time > now_time:
        raise HTTPException(401, f"订单{data.flash_order_id}，上架未到时间。")

    #到时长，计算收益天数
    income_info = d_flash_order_return.get_flash_order_return(data.user_id)
    now_date = now_time.date()
    if income_info.income_days > 0:
        if income_info.latest_time is not None and now_date > income_info.latest_time.date():
            d_flash_order_return.reduce_flash_order_return(data.user_id)
            income_day = True
        else:
            income_day = True

    #计算本人收益额
    user_balance = 0
    user_income = 0
    parent_income = 0
    top_income = 0
    groupsir_income = 0
    subsidy_income = 0
    if order_info.single_status is None:
        order_info.single_status = 0
    if order_info.single_status > 0:   #整份代卖
        user_balance = package_info.flash_sale_price * package_info.amount
    else:
        order_info.sold = 0 if order_info.sold is None else order_info.sold
        user_balance = package_info.flash_sale_price * (package_info.amount - order_info.sold - order_info.return_sold)
    if user_balance > 0 and income_day:
        income_retio = d_settings.get_settings().flash_order_income_retio
        user_income = user_balance * income_retio / 1000
    account_info = d_account.get_account_info(data.user_id)
    if not account_info:
        raise HTTPException(401, f"未找到用户账户{data.user_id}")

    #层级收益
    if user_info.parent_id is not None:
        if user_info.parent_id > 0:
            parent_info = d_account.get_account_info_add(user_info.parent_id)
            if parent_info:
                parent_income = d_settings.get_settings().flash_order_income_layer * user_income / 100
            if parent_info and parent_income > 0:
                total_balance = parent_info.balance + parent_income
                d_account.update_account_by_id(parent_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=parent_info.user_id,
                    change=parent_income,
                    balance=total_balance,
                    type=global_define.balance_type[1],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(good_info.id),
                    good_title=str(good_info.title),
                    good_num=str(order_info.number)
                ))
    #顶级
    top_user_id = d_user.get_top_id(data.user_id)
    if top_user_id is not None:
        if top_user_id > 0:
            top_user_info = d_account.get_account_info_add(top_user_id)
            if top_user_info:
                top_income = d_settings.get_settings().flash_order_income_toper * user_income / 100
            if top_user_info and top_income > 0:
                total_balance = top_user_info.balance + top_income
                d_account.update_account_by_id(top_user_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=top_user_id,
                    change=top_income,
                    balance=total_balance,
                    type=global_define.balance_type[2],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(good_info.id),
                    good_title=str(good_info.title),
                    good_num=str(order_info.number)
                ))
    #团长
    groupsir_user_info = d_groupsir.get_member_for_user(data.user_id)
    if groupsir_user_info:
        groupsir_parent_info = groupsir_user_info
        if groupsir_user_info.parent_id > 0:
            groupsir_parent_info = d_groupsir.get_member_for_user(groupsir_user_info.parent_id)
        groupsir_account_info = d_account.get_account_info_add(groupsir_parent_info.user_id)
        if groupsir_account_info:
            groupsir_income = d_settings.get_settings().flash_order_income_groupsir * user_income / 100
        if groupsir_account_info and groupsir_income > 0:
            total_balance = groupsir_account_info.balance + groupsir_income
            d_account.update_account_by_id(groupsir_account_info.id, {"balance": total_balance})
            d_account.add_balance(m_account.BalanceModel(
                user_id=groupsir_parent_info.user_id,
                change=groupsir_income,
                balance=total_balance,
                type=global_define.balance_type[4],
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                good_id=str(good_info.id),
                good_title=str(good_info.title),
                good_num=str(order_info.number)
            ))

    #直推人团队补贴收益
    if user_info.invited_user_id is not None:
        if user_info.invited_user_id > 0:
            invited_info = d_account.get_account_info_add(user_info.parent_id)
            if invited_info:
                subsidy_income = d_settings.get_settings().flash_order_income_subsidy * user_income / 100
            if invited_info and subsidy_income > 0:
                total_balance = invited_info.balance + subsidy_income
                d_account.update_account_by_id(invited_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=invited_info.user_id,
                    change=subsidy_income,
                    balance=total_balance,
                    type=global_define.balance_type[23],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(good_info.id),
                    good_title=str(good_info.title),
                    good_num=str(order_info.number)
                ))

    #更新收益和订单状态
    total_balance = account_info.balance + user_balance + user_income    #启用收益时，再用
    #total_balance = account_info.balance + user_balance
    d_account.update_account_by_id(account_info.id, {"balance": total_balance})
    d_flash_order_return.finish_flash_order(TFlashOrder(
        id=order_info.id,
        status = 7,  # 已退货，已完成
        complete_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        is_assign_income = 1,
        detail = f"[{now_time}#持有：{user_income}#层：{parent_income}#点：{top_income}#团：{groupsir_income}#团补：{subsidy_income}]"
    ))

    #更新持有人收益记录
    d_account.add_balance(m_account.BalanceModel(
        user_id=data.user_id,
        change=user_balance + user_income,
        balance=total_balance,
        type=global_define.balance_type[6],
        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        good_id=str(good_info.id),
        good_title=str(good_info.title),
        good_num=str(order_info.number)
    ))

    return {'status': 200, 'detail': '申请退货成功'}

@router.post(f'/flash_order_stats')
async def flash_order_stats(user_id: int):
    """
    POST请求，get参数user_id携带查询用户的id
    返回：
        "status": 4,  状态值
        "num": 2,   此状态数量
        "title": "已出售" ,  此状态值的文本意义
    """
    if user_id <= 0:
        raise HTTPException(400, "非法用户")
    status_list = {-1:"删除",0:"待付款",1:"待上架",2:"转卖中",3:"退款中",4:"已出售",5:"已取消",6:"回购申请中",7:"已完成",8:"已付款",9:"已上架"}
    res = d_flash_order_return.get_flash_order_stats(user_id)
    for k in status_list:
        has = False
        for r in res:
            if r["status"] == k:
                has = True
        if not has:
            res.append({"status":k, "num":0, "title":status_list.get(k)})
    return res

@router.post(f'/flash_order_sell')
async def flash_order_sell(user_id: int):
    """
    TOrderSource.amount，表示当前订单中有都少份是秒杀包用户的;
    t_package.flash_sale_price * t_source.amount,表示当前秒杀包的秒杀价格；
    t_spec.price * t_source.amount,表示当前秒杀包的出售价格；
    出售价格与秒杀价格只差，是秒杀用户的收益部分
    """
    flash_order_ids = d_package.get_flash_order_ids(user_id)
    return d_order.get_order_source_for_user(flash_order_ids)
