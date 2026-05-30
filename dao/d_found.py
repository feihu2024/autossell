from common import Dao, global_define
from model.schema import TBigorderSet, TBigorderTwo, TUser, TBagPas, TBagCagegory, TFundPond, TFundPondLog, TBigorderInitbag, TFundWeightLog, TFundZqlog
from sqlalchemy import or_, and_, func
from typing import List, Optional
from sqlalchemy import text
import datetime, time, sys, math, json, redis
from pydantic import BaseModel, Field
from fastapi.exceptions import HTTPException
from dao import d_user, d_db, d_account, d_bigorder
from model.mall import m_account
import logging


# class SearchBalance(BaseModel):
#     user_id: Optional[int] = Field(None,title='关联t_user表id')
#     type: Optional[str] = Field(None,title='资金类型：1:层级收益,2:见点收益,3:推荐收益,4:团长收益,5:管理变动收益')
#     description: Optional[str] = Field(None,title='资金备注，团长收益这里是逗号分隔的订单id')
#     create_time: Optional[str] = Field(None,title='时间段：time1,time2')
#     is_comein: Optional[int] = Field(None, title='收入(1)/支出(0)')
#     # admin_id: Optional[int] = Field(None, title='商家管理id')
#     page: int = Field(1, title='当前页码，默认第1页')
#     page_size: int = Field(20, title='返回每页数据，默认每页20条数据')

class FundZqlogModel(BaseModel):
    # id = Column(Integer, primary_key=True, comment='标识id编号')
    zhouqi: Optional[int] = Field(title='属期id')
    balance: Optional[int]  = Field(title='分配金额')
    fenpei_num: Optional[int]  = Field(title='分配人数')
    status: Optional[int]  = Field(title='分配成功0分配失败1')
    fenpei_users: Optional[str] = Field(None,title='备注')
    user_id: Optional[int] = Field(title='获奖用户id')
    balance_pro: Optional[float] = Field(title='分配百分比')

#通过礼包归集资金池余额
def add_fund_pond(orderbag_id: int = 0):
    bag_rs = d_db.get_bigorder_initbag(orderbag_id)
    if bag_rs:
        if bag_rs.fund_one > 0:
            add_fund_one(bag_rs.fund_one, orderbag_id)
        if bag_rs.fund_two > 0:
            add_fund_two(bag_rs.fund_two, orderbag_id)
        if bag_rs.fund_three > 0:
            add_fund_three(bag_rs.fund_three, orderbag_id)

#初级资金池增加资金
def add_fund_one(balance:int = 0, shop_id:int = 0):
    with Dao() as db:
        one_ls = db.query(TFundPond).where(TFundPond.ftype == 0).order_by(TFundPond.id.desc()).first()
        if one_ls:
            if one_ls.stat == 0:
                total_balance = one_ls.balance + balance
                db.query(TFundPond).where(TFundPond.id == one_ls.id).update({"balance":total_balance})
                add_log = TFundPondLog(
                    add_balance=balance,
                    all_balance=total_balance,
                    source_id=shop_id,
                    source_cont = '初级资金池'
                )
                db.add(add_log)
                db.commit()

#高级资金池增加资金
def add_fund_two(balance:int = 0, shop_id:int = 0):
    with Dao() as db:
        one_ls = db.query(TFundPond).where(TFundPond.ftype == 1).order_by(TFundPond.id.desc()).first()
        if one_ls:
            if one_ls.stat == 0:
                total_balance = one_ls.balance + balance
                db.query(TFundPond).where(TFundPond.id == one_ls.id).update({"balance":total_balance})
                add_log = TFundPondLog(
                    add_balance=balance,
                    all_balance=total_balance,
                    source_id=shop_id,
                    source_cont = '高级资金池'
                )
                db.add(add_log)
                db.commit()

#顶级资金池增加资金
def add_fund_three(balance:int = 0, shop_id:int = 0):
    with Dao() as db:
        one_ls = db.query(TFundPond).where(TFundPond.ftype == 2).order_by(TFundPond.id.desc()).first()
        if one_ls:
            if one_ls.stat == 0:
                total_balance = one_ls.balance + balance
                db.query(TFundPond).where(TFundPond.id == one_ls.id).update({"balance":total_balance})
                add_log = TFundPondLog(
                    add_balance=balance,
                    all_balance=total_balance,
                    source_id=shop_id,
                    source_cont = '顶级资金池'
                )
                db.add(add_log)
                db.commit()

def get_curr_funds():
    with Dao() as db:
        return db.query(TFundPond).filter(TFundPond.stat == 0).all()

def get_fund_weight_count(user_id:int):
    this_cycle = get_fund_cycle()
    with Dao() as db:
        return db.query(TFundWeightLog).filter(TFundWeightLog.user_id == user_id).count()

def get_fund_by_id(fund_id:int):
    with Dao() as db:
        return db.query(TFundPond).filter(TFundPond.id == fund_id).first()

def update_fund_pond_users(fund_id: int, userls: str = ''):
    fund_info = get_fund_by_id(fund_id)
    if fund_info:
        update_date = {}
        update_date['users'] = userls
        update_date["users_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with Dao() as db:
            re = db.query(TFundPond).where(TFundPond.id == fund_id).update(update_date)
            db.commit()
            return re
    return 0

#增加资金池执行记录
def add_fund_zqlog(items: FundZqlogModel):
    add_instance = TFundZqlog(
        zhouqi=items.zhouqi,
        balance=items.balance,
        fenpei_num=items.fenpei_num,
        status=items.status,
        fenpei_users = items.fenpei_users,
        user_id=items.user_id,
        balance_pro=items.balance_pro
    )
    with Dao() as db:
        db.add(add_instance)
        db.commit()

def update_fund_by_id(fund_id: int, item: dict):
    with Dao() as db:
        if item.get("id"):
            item.pop("id")
        db.query(TFundPond).where(TFundPond.id == fund_id).update(item)
        db.commit()

def create_fund(level_id:int = 1):
    mm = datetime.datetime.now()
    date_num = f"one{mm.year}{mm.month}{mm.day}"
    add_instance = TFundPond(
        date_num=date_num,
        ftype=0
    )
    if level_id == 2:
        add_instance.date_num = f"two{mm.year}{mm.month}{mm.day}"
        add_instance.ftype = 1
    elif level_id == 3:
        add_instance.date_num = f"three{mm.year}{mm.month}{mm.day}"
        add_instance.ftype = 2
    with Dao() as db:
        db.add(add_instance)
        db.commit()

#更新资金池合法对象
def update_fund_users():
    fund_ls = get_curr_funds()
    is_run = []
    for ls in fund_ls:
        if ls.ftype in is_run:
            continue
        add_users = []
        if ls.ftype == 0:
            fund_one = d_bigorder.get_bigorder_set('fund_one')
            user_ls = d_user.get_users_for_level(1)
            for us in user_ls:
                u_count = get_fund_weight_count(us.id)
                if u_count >= fund_one:
                    add_users.append(us.id)
            usrs_str = ','.join(add_users)
            if usrs_str:
                update_fund_pond_users(ls.id, usrs_str)
        elif ls.ftype == 1:
            fund_two = d_bigorder.get_bigorder_set('fund_two')
            user_ls = d_user.get_users_for_level(2)
            for us in user_ls:
                u_count = get_fund_weight_count(us.id)
                if u_count >= fund_two:
                    add_users.append(us.id)
            usrs_str = ','.join(add_users)
            if usrs_str:
                update_fund_pond_users(ls.id, usrs_str)
        elif ls.ftype == 2:
            fund_three = d_bigorder.get_bigorder_set('fund_three')
            user_ls = d_user.get_users_for_level(3)
            for us in user_ls:
                u_count = get_fund_weight_count(us.id)
                if u_count >= fund_three:
                    add_users.append(us.id)
            usrs_str = ','.join(add_users)
            if usrs_str:
                update_fund_pond_users(ls.id, usrs_str)

        is_run.append(ls.ftype)

#获取本期资金池周期时间段
def get_fund_cycle():
    re_cycle=['2025-09-1 00:00:00', '2025-09-15 00:00:00']
    now = datetime.datetime.now()
    # year = now.year
    # month = now.month
    if now.day > 15:
        re_cycle[0] = f"{now.year}-{now.month}-15 00:00:00"
        re_cycle[1] = f"{now.year}-{now.month}-31 00:00:00"
    else:
        re_cycle[0] = f"{now.year}-{now.month}-1 00:00:00"
        re_cycle[1] = f"{now.year}-{now.month}-15 00:00:00"
    return re_cycle

#更新指定资金池合法对象
def update_fund_users_for_id(fund_id:int):
    fund_ls = get_fund_by_id(fund_id)
    if fund_ls:
        add_users = []
        if fund_ls.ftype == 0:
            fund_one = d_bigorder.get_bigorder_set('fund_one')
            user_ls = d_user.get_users_in_level([1,2,3])
            for us in user_ls:
                u_count = get_fund_weight_count(us.id)
                if u_count >= fund_one.val_int:
                    add_users.append(us.id)
                # add_users.append(us.id)
            add_users = [str(x) for x in add_users]
            usrs_str = ','.join(add_users)
            update_fund_pond_users(fund_ls.id, usrs_str)
        elif fund_ls.ftype == 1:
            fund_two = d_bigorder.get_bigorder_set('fund_two')
            # user_ls = d_user.get_users_for_level(2)
            user_ls = d_user.get_users_in_level([2,3])
            for us in user_ls:
                u_count = get_fund_weight_count(us.id)
                if u_count >= fund_two.val_int:
                    add_users.append(us.id)
                # add_users.append(us.id)
            add_users = [str(x) for x in add_users]
            usrs_str = ','.join(add_users)
            update_fund_pond_users(fund_ls.id, usrs_str)
        elif fund_ls.ftype == 2:
            fund_three = d_bigorder.get_bigorder_set('fund_three')
            user_ls = d_user.get_users_for_level(3)
            # user_ls = d_user.get_users_in_level([1,2,3])
            for us in user_ls:
                u_count = get_fund_weight_count(us.id)
                if u_count >= fund_three.val_int:
                    add_users.append(us.id)
                # add_users.append(us.id)
            add_users = [str(x) for x in add_users]
            usrs_str = ','.join(add_users)
            update_fund_pond_users(fund_ls.id, usrs_str)

#更新用户三个资金池分润预测金额
def update_prop_balance_to_user():
    fund_ls = get_curr_funds()
    for fund in fund_ls:
        if fund.users:
            user_li = fund.users.split(',')
            user_ls = d_user.get_user_by_ids(user_li)
            if user_ls:
                user_ls_weight_count = d_user.get_fund_user_count(user_li)
                for ls in user_ls:
                    account_info = d_account.get_account_info(ls.id)
                    prop = round(ls.fund_weight_num / user_ls_weight_count, 2)
                    # 向上取整：math.ceil()
                    # 向下取整：math.floor()
                    # 四舍五入：round()
                    this_balance = math.floor(fund.balance * prop)
                    if fund.ftype == 0:
                        d_account.update_account_by_id(account_info.id, {"forecast_one":this_balance, "prop_one":prop, "update_time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
                    elif fund.ftype == 1:
                        d_account.update_account_by_id(account_info.id, {"forecast_two": this_balance, "prop_two": prop,"update_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
                    elif fund.ftype == 2:
                        d_account.update_account_by_id(account_info.id, {"forecast_three": this_balance, "prop_three": prop,"update_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})






#
# def find_pc_for_num(pc_id: str):
#     with Dao() as db:
#         return db.query(TBagPas).where(TBagPas.pass_num == pc_id).first()
#
# # def insert_bagpass()
# def insert_bagpass(bag_data: TBagCagegory):
#     with Dao() as db:
#         db.add(bag_data)
#         db.commit()
#         db.refresh(bag_data)
#         return bag_data
#
# def insert_bagpass_list(bag_data: TBagPas):
#     with Dao() as db:
#         db.add(bag_data)
#         db.commit()
#         db.refresh(bag_data)
#         return bag_data
#
# def bagpass_active(bagpass_id: int, user_id:int):
#     with Dao() as db:
#         now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#         db.query(TBagPas).where(TBagPas.pass_num == bagpass_id).update({"stat": 1,"startime": now_time,"user_id": user_id})
#         db.commit()