import datetime,time,sys
from pathlib import Path
root_dir = Path(__file__).parents[1]
model_dir = root_dir / 'model'
#print(root_dir)
# print(model_dir)
sys.path.append(str(root_dir))

from common import Dao
from common.global_define import *
from model import schema, m_schema
# from router import r_schema
# from typing import List, Optional
# from pydantic import BaseModel, Field
#from dao import d_groupsir

def get_groupsir_id(groupsir_id: int = 0):
    groupsir_list = []
    with Dao() as db:
        re = db.query(schema.TGroupsir.user_id).filter(schema.TGroupsir.parent_id == groupsir_id).all()
        for i in re:
            groupsir_list.append(i.user_id)
        return groupsir_list

def get_flash_order_list(user_list:list = []):
    re_list = []
    with Dao() as db:
        res = db.query(schema.TFlashOrder).filter(schema.TFlashOrder.user_id.in_(user_list), schema.TFlashOrder.status == 4).all()
    for i in res:
        if i.paid_amount is None:
            i.paid_amount = 0
        if i.paid_balance is None:
            i.paid_balance = 0
        re_list.append({"id":i.id, "package_id":i.package_id, "status":i.status,\
                        "create_time":i.create_time, "paid_time":i.paid_time, "user_id":i.user_id,\
                        "number":i.number, "flash_price":i.flash_price, "flash_cost":i.flash_cost,\
                        "out_trade_no":i.out_trade_no, "paid_amount":i.paid_amount, "paid_balance":i.paid_balance,\
                        "single_status":i.single_status, "sold":i.sold, "whole_status":i.whole_status, "spec_id":i.spec_id})
    return re_list

def get_tuan_order_income():
    with Dao() as db:
        return db.query(schema.TSetting.tuan_order_income).scalar()

def update_groupsir_accoount(user_id:int, balance:float, orders:list):
    with Dao() as db:
        account_info = db.query(schema.TUserAccount).filter(schema.TUserAccount.user_id == user_id).first()
        if account_info:
            total_balance = account_info.balance + balance
            db.query(schema.TUserAccount).filter(schema.TUserAccount.user_id == user_id).update({"balance":total_balance})
            db.commit()
            add_balance_history(user_id, balance, total_balance, orders)
        else:
            print(f"{user_id},账户不存在")

def add_balance_history(user_id:int, add_balance:float, balance:float, orders:list):
    str_orders = ','.join(map(str,orders))
    insert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #add_dict = {"user_id":user_id, "change":add_balance, "balance":balance, "type":balance_type[4], "description":str_orders, "create_time":insert_time, "operator_id":0}
    insert_TBalance = schema.TBalance(user_id=user_id, change=add_balance, balance=balance, type=balance_type[4], description=str_orders, create_time=insert_time, operator_id=0)
    with Dao() as db:
        db.add(insert_TBalance)
        db.commit()

def main():
    groupsir_list = get_groupsir_id()
    groupsir_income = get_tuan_order_income()
    this_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print(groupsir_list)
    # print(groupsir_income)
    # return
    print(f"{this_date} - 团长收益任务启动")
    for me in groupsir_list:
        user_list = get_groupsir_id(me)
        if user_list:
            flash_orders = get_flash_order_list(user_list)
            if flash_orders:
                total_balance = 0
                order_ids = []
                for order in flash_orders:
                    pay_total = order["paid_amount"] + order["paid_balance"]
                    total_balance += pay_total
                    order_ids.append(order["id"])
                groupsir_money = total_balance * groupsir_income / 1000
                update_groupsir_accoount(me, groupsir_money, order_ids)
                print(f"{me}，共有团员{user_list}，{this_date}收益为{groupsir_money}")
            else:
                print(f"{me}，共有团员{user_list}，未有完成抢购订单")
        else:
            print(f"{me}，还未加入团员")
    print(f"{this_date} - 团长收益任务结束")


if __name__ == '__main__':
    main()
