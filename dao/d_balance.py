from common import Dao, global_define
from model.schema import TBalance, TFlashOrderReturn, TLockBalance
from sqlalchemy import or_, and_, func
from typing import List, Optional
from sqlalchemy import text
import time
from pydantic import BaseModel, Field
from dao import d_flash_order_return, d_good, d_user, d_account
from fastapi.exceptions import HTTPException
from model.mall import m_account

class SearchBalance(BaseModel):
    user_id: Optional[int] = Field(None,title='关联t_user表id')
    type: Optional[str] = Field(None,title='资金类型：1:层级收益,2:见点收益,3:推荐收益,4:团长收益,5:管理变动收益')
    description: Optional[str] = Field(None,title='资金备注，团长收益这里是逗号分隔的订单id')
    create_time: Optional[str] = Field(None,title='时间段：time1,time2')
    is_comein: Optional[int] = Field(None, title='收入(1)/支出(0)')
    # admin_id: Optional[int] = Field(None, title='商家管理id')
    page: int = Field(1, title='当前页码，默认第1页')
    page_size: int = Field(20, title='返回每页数据，默认每页20条数据')


def search_comein(items: SearchBalance):
    with Dao() as db:
        res = db.query(TBalance)
        res_balance = db.query(func.sum(TBalance.change).label('total_balance'))
        if items.user_id:
            res = res.filter(TBalance.user_id == items.user_id)
            res_balance = res_balance.filter(TBalance.user_id == items.user_id)

        # res = res.filter(TBalance.description.like(f"%{items.description}%"))
        res = res.filter(or_(TBalance.type == global_define.balance_type[1], \
                                             TBalance.type == global_define.balance_type[2], \
                                             TBalance.type == global_define.balance_type[3], \
                                             TBalance.type == global_define.balance_type[7]))

        res_balance = res_balance.filter(or_(TBalance.type == global_define.balance_type[1],\
                                             TBalance.type == global_define.balance_type[2],\
                                             TBalance.type == global_define.balance_type[3],\
                                             TBalance.type == global_define.balance_type[7]))
        # res_balance = res_balance.filter(or_(TBalance.description.like(f"%{global_define.balance_type[1]}%"),\
        #                                      TBalance.description.like(f"%{global_define.balance_type[2]}%"),\
        #                                      TBalance.description.like(f"%{global_define.balance_type[3]}%"),\
        #                                      TBalance.description.like(f"%{global_define.balance_type[7]}%")))
        # if items.admin_id:
        #     good_ids = d_good.get_goodids_for_adminid(items.admin_id)
        #     res = res.filter(TBalance.good_id.in_(good_ids))

        res = res.order_by(TBalance.id.desc())
        total = res.count()
        total_balance = res_balance.scalar()
        search_list = res.offset(items.page * items.page_size - items.page_size).limit(items.page_size).all()
        return {"total":total, "total_balance":total_balance, "data": search_list}


def search_comein_tuijian(items: SearchBalance):
    with Dao() as db:
        res = db.query(TBalance)
        res_balance = db.query(func.sum(TBalance.change).label('total_balance'))
        if items.user_id:
            res = res.filter(TBalance.user_id == items.user_id)
            res_balance = res_balance.filter(TBalance.user_id == items.user_id)

        res = res.filter(or_(TBalance.type == global_define.balance_type[1], TBalance.type == global_define.balance_type[7]))
        res_balance = res_balance.filter(or_(TBalance.type == global_define.balance_type[1], TBalance.type == global_define.balance_type[7]))
        # res_balance = res_balance.filter(or_(TBalance.description.like(f"%{global_define.balance_type[1]}%"),\
        #                                      TBalance.description.like(f"%{global_define.balance_type[2]}%"),\
        #                                      TBalance.description.like(f"%{global_define.balance_type[3]}%"),\
        #                                      TBalance.description.like(f"%{global_define.balance_type[7]}%")))
        # if items.admin_id:
        #     good_ids = d_good.get_goodids_for_adminid(items.admin_id)
        #     res = res.filter(TBalance.good_id.in_(good_ids))

        res = res.order_by(TBalance.id.desc())
        total = res.count()
        total_balance = res_balance.scalar()
        search_list = res.offset(items.page * items.page_size - items.page_size).limit(items.page_size).all()
        return {"total":total, "total_balance":total_balance, "data": search_list}

def search_comein_fenhong(items: SearchBalance):
    with Dao() as db:
        res = db.query(TBalance)
        res_balance = db.query(func.sum(TBalance.change).label('total_balance'))
        if items.user_id:
            res = res.filter(TBalance.user_id == items.user_id)
            res_balance = res_balance.filter(TBalance.user_id == items.user_id)

        res = res.filter(TBalance.type == global_define.balance_type[2])
        res_balance = res_balance.filter(TBalance.type == global_define.balance_type[2])
        # res_balance = res_balance.filter(or_(TBalance.description.like(f"%{global_define.balance_type[1]}%"),\
        #                                      TBalance.description.like(f"%{global_define.balance_type[2]}%"),\
        #                                      TBalance.description.like(f"%{global_define.balance_type[3]}%"),\
        #                                      TBalance.description.like(f"%{global_define.balance_type[7]}%")))
        # if items.admin_id:
        #     good_ids = d_good.get_goodids_for_adminid(items.admin_id)
        #     res = res.filter(TBalance.good_id.in_(good_ids))

        res = res.order_by(TBalance.id.desc())
        total = res.count()
        total_balance = res_balance.scalar()
        search_list = res.offset(items.page * items.page_size - items.page_size).limit(items.page_size).all()
        return {"total":total, "total_balance":total_balance, "data": search_list}

def search_balance(items: SearchBalance):
    with Dao() as db:
        res = db.query(TBalance)
        res_balance = db.query(func.sum(TBalance.change).label('total_balance'))
        if items.user_id:
            res = res.filter(TBalance.user_id == items.user_id)
            res_balance = res_balance.filter(TBalance.user_id == items.user_id)
        if items.type:
            split_type = items.type.split(',')
            if len(split_type) == 1:
                res = res.filter(TBalance.type.like(f"%{items.type}%"))
                res_balance = res_balance.filter(TBalance.type.like(f"%{items.type}%"))
            elif len(split_type) == 2:
                res = res.filter(or_(TBalance.type == split_type[0], TBalance.type == split_type[1]))
                res_balance = res_balance.filter(or_(TBalance.type == split_type[0], TBalance.type == split_type[1]))
            elif len(split_type) == 3:
                res = res.filter(or_(TBalance.type == split_type[0], TBalance.type == split_type[1], TBalance.type == split_type[2]))
                res_balance = res_balance.filter(or_(TBalance.type == split_type[0], TBalance.type == split_type[1], TBalance.type == split_type[2]))
        if items.description:
            res = res.filter(TBalance.description.like(f"%{items.description}%"))
            res_balance = res_balance.filter(TBalance.description.like(f"%{items.description}%"))
        if items.create_time:
            times = items.create_time.split(',')
            res = res.filter(TBalance.create_time > times[0])
            res = res.filter(TBalance.create_time < times[1])
            res_balance = res_balance.filter(TBalance.create_time > times[0])
            res_balance = res_balance.filter(TBalance.create_time < times[1])
        if items.is_comein == 0:
            items.is_comein=-2
        if items.is_comein:
            if items.is_comein <= 0:
                res = res.filter(TBalance.change < 0)
                res_balance = res_balance.filter(TBalance.change < 0)
            else:
                res = res.filter(TBalance.change > 0)
                res_balance = res_balance.filter(TBalance.change > 0)
        # if items.admin_id:
        #     good_ids = d_good.get_goodids_for_adminid(items.admin_id)
        #     res = res.filter(TBalance.good_id.in_(good_ids))

        res = res.order_by(TBalance.id.desc())
        total = res.count()
        total_balance = res_balance.scalar()
        search_list = res.offset(items.page * items.page_size - items.page_size).limit(items.page_size).all()
        return {"total":total, "total_balance":total_balance, "data": search_list}


def search_lock_balance(items: SearchBalance):
    with Dao() as db:
        res = db.query(TLockBalance)
        res_balance = db.query(func.sum(TLockBalance.change).label('total_balance'))
        if items.user_id:
            res = res.filter(TLockBalance.user_id == items.user_id)
            res_balance = res_balance.filter(TLockBalance.user_id == items.user_id)
        if items.type:
            res = res.filter(TLockBalance.type.like(f"%{items.type}%"))
            res_balance = res_balance.filter(TLockBalance.type.like(f"%{items.type}%"))
        if items.description:
            res = res.filter(TLockBalance.description.like(f"%{items.description}%"))
            res_balance = res_balance.filter(TLockBalance.description.like(f"%{items.description}%"))
        if items.create_time:
            times = items.create_time.split(',')
            res = res.filter(TLockBalance.create_time > times[0])
            res = res.filter(TLockBalance.create_time < times[1])
            res_balance = res_balance.filter(TLockBalance.create_time > times[0])
            res_balance = res_balance.filter(TLockBalance.create_time < times[1])
        if items.is_comein == 0:
            items.is_comein=-2
        if items.is_comein:
            if items.is_comein <= 0:
                res = res.filter(TLockBalance.change < 0)
                res_balance = res_balance.filter(TLockBalance.change < 0)
            else:
                res = res.filter(TLockBalance.change > 0)
                res_balance = res_balance.filter(TLockBalance.change > 0)
        res = res.order_by(TLockBalance.id.desc())
        total = res.count()
        total_balance = res_balance.scalar()
        search_list = res.offset(items.page * items.page_size - items.page_size).limit(items.page_size).all()
        return {"total":total, "total_balance":total_balance, "data": search_list}


def search_days(user_id:int):
    if user_id <= 0:
        raise HTTPException(400, "非法用户")
    return d_flash_order_return.get_flash_order_return(user_id)
    #with Dao() as db:
    #    return db.query(TFlashOrderReturn).filter(TFlashOrderReturn.user_id == user_id).first()

def invited_user_money(user_id:int, money:int = 0, type_str:str = "", good_id:int = 0, good_title:str = "", good_num:int = 0, out_trade_no:str = ""):
    uinfo = d_user.get_user_by_id(user_id)
    if uinfo and money > 0:
        parent_info = d_account.get_account_info_add(user_id)
        if parent_info:
            total_balance = parent_info.balance + money
            d_account.update_account_by_id(parent_info.id, {"balance": total_balance})
            d_account.add_balance(m_account.BalanceModel(
                user_id=parent_info.user_id,
                change=money,
                balance=total_balance,
                type=type_str,
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                good_id=str(good_id),
                good_title=good_title,
                good_num=str(good_num),
                out_trade_no=out_trade_no
            ))

def invited_user_coin(user_id:int, coin:int = 0, type_str:str = "", good_id:int = 0, good_title:str = "", good_num:int = 0, out_trade_no:str = ""):
    uinfo = d_user.get_user_by_id(user_id)
    if uinfo and coin > 0:
        parent_info = d_account.get_account_info_add(user_id)
        if parent_info:
            total_balance = parent_info.coin + coin
            d_account.update_account_coin(user_id, total_balance)
            d_account.insert_coin(m_account.CoinModel(
                user_id=parent_info.user_id,
                change=coin,
                coin=total_balance,
                type=type_str,
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                description=f"{str(good_id)},{good_title},{str(good_num)}",
                out_trade_no=out_trade_no
            ))