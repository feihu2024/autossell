#!/usr/bin/env python
# encoding: utf-8
import datetime
from typing import List, Optional
import logging
from common import global_define

from fastapi import HTTPException

from common import Dao
from model import schema
from model.schema import TFlashOrder, TPackage, TGood
from service.share_fee_service import share_package_fee_with_other


def pay_success(amount: int, out_trade_no: str):
    order_ids = []
    with Dao() as db:
        order_infos = db.query(TFlashOrder, TPackage, TGood)\
            .outerjoin(TPackage, TPackage.id == TFlashOrder.package_id) \
            .outerjoin(TGood, TPackage.good_id == TGood.id) \
            .filter(TFlashOrder.out_trade_no == out_trade_no).all()

        orders = []
        good_titles = []
        good_ids = []
        good_nums = []
        for order, package, tgood in order_infos:
            order: TFlashOrder
            package: TPackage
            tgood: TGood
            if order.status == 0:
                order.status = 1 # 待上架/已支付
                db.query(TFlashOrder).filter(TFlashOrder.id == order.id).update({"status": 1})
                db.flush()
                order_ids.append(int(order.id))

            orders.append(order)
            good_titles.append(tgood.title)
            good_ids.append(tgood.id)
            good_nums.append(order.number)

        if len(orders) > 0:
            user_id = orders[0].user_id
        else:
            logging.error(f"没有发现相关订单, out_trade_no: {out_trade_no}")
            raise HTTPException(status_code=500, detail={"code": 'FAILED', "detail": "失败,没有发现相关订单"})

        if user_id is None:
            raise HTTPException(status_code=500, detail={"code": 'FAILED', "detail": "失败,用户id为空"})

        user_account: Optional[schema.TUserAccount] = db.query(schema.TUserAccount).filter(
            schema.TUserAccount.user_id == user_id).first()
        if user_account is None:
            raise HTTPException(status_code=500, detail={"code": 'FAILED', "detail": "失败,没有发现该用户的账户"})

        balance_cost = sum([order.paid_balance for order in orders])
        amount_cost = sum([order.paid_amount for order in orders])

        if balance_cost:
            user_account.balance = user_account.balance - balance_cost
            balance_record = schema.TBalance(
                change=-balance_cost,
                user_id=user_id,
                balance=user_account.balance,
                create_time=datetime.datetime.now(),
                out_trade_no=out_trade_no,
                type=global_define.balance_type[12],
                description=global_define.balance_type[12],
                good_id=",".join([str(i) for i in good_ids]),
                good_title=",".join([str(i) for i in good_titles]),
                good_num=",".join([str(i) for i in good_nums])
            )
            db.add(balance_record)
            db.flush()

        if amount != amount_cost:
            raise HTTPException(status_code=500, detail={"code": 'FAILED', "detail": "支付金额不一致"})

        payment_record = schema.TUserPaymentHistory(fee=amount, description='购买商品', create_time=datetime.datetime.now())
        db.add(payment_record)
        db.flush()

        db.commit()
    
    for order_id in order_ids:
        share_package_fee_with_other(flash_order_id=order_id)
