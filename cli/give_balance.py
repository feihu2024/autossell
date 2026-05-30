import datetime,time,sys,math
from pathlib import Path
from sqlalchemy import or_
root_dir = Path(__file__).parents[1]
model_dir = root_dir / 'model'
#print(root_dir)
# print(model_dir)
sys.path.append(str(root_dir))

from common import Dao, global_define
#from common.global_define import *
from model import schema, m_schema

from dao import d_user_account, d_account, d_user, d_package, d_order, d_groupsir, d_settings, d_supplier_account, d_supplier_income
from model.mall import m_account
from typing import Optional
from dao import d_db


def get_user_account(page:int):
    re_data = {"total": 0, "data": []}
    with Dao() as db:
        account_info = db.query(schema.TUserAccount)
        re_data['total'] = account_info.count()
        re_data['data'] = account_info.offset(page * 20 - 20).limit(20).all()
    return re_data

def get_user_account_wholesale(page:int, woholesale_id: int = 100):
    re_data = {"total": 0, "data": []}
    with Dao() as db:
        account_info = db.query(schema.TUserAccount, schema.TUser).outerjoin(schema.TUser, schema.TUserAccount.user_id == schema.TUser.id) \
            .filter(schema.TUser.wholesale_id == woholesale_id)
        re_data['total'] = account_info.count()
        re_data['data'] = account_info.offset(page * 20 - 20).limit(20).all()
    return re_data

def get_user_account_level(page:int, level_id: int = 0):
    re_data = {"total": 0, "data": []}
    with Dao() as db:
        account_info = db.query(schema.TUserAccount, schema.TUser).outerjoin(schema.TUser, schema.TUserAccount.user_id == schema.TUser.id) \
            .filter(schema.TUser.level_id == level_id)
        re_data['total'] = account_info.count()
        re_data['data'] = account_info.offset(page * 20 - 20).limit(20).all()
    return re_data

def assgin_balance(data, add_count):
    total_balance = data.balance + add_count
    d_account.update_account_by_id(data.id, {'balance': total_balance})
    s_balance = m_account.BalanceModel(
        user_id=data.user_id,
        change=add_count,
        balance=total_balance,
        type=global_define.balance_type[26],
        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        good_id=0,
        good_title='',
        good_num='',
        out_trade_no=''
    )
    d_account.add_balance(s_balance)
    print(f"{data.user_id}赠予金额{add_count}分，余额{total_balance}")

def assgin_coin(data, add_count):
    total_coin = data.coin + add_count
    d_account.update_account_by_id(data.id, {'coin': total_coin})
    s_coin = m_account.CoinModel(
        user_id=data.user_id,
        change=add_count,
        coin=total_coin,
        type=global_define.balance_type[27],
        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        description=global_define.balance_type[27],
        out_trade_no=''
    )
    d_account.insert_coin(s_coin)
    print(f"{data.user_id}赠予积分{add_count}分，余额{total_coin}")

def main():
    money = 10000  #单位分
    type = 1 #1,转账余额   2,转账积分
    print(f"资金转账启动：每账户赠予{money}分")
    accounts = get_user_account(1)
    account_num = 0
    if accounts['total'] > 0:
        print(f"共{accounts['total']} - 资金账户")
        for item in accounts['data']:
            if type == 1:
                assgin_balance(item, money)
            else:
                assgin_coin(item, money)
            account_num += 1
        pages = math.ceil(accounts['total'] / 20)
        i = 2
        while i <= pages:
            accounts = get_user_account(i)
            i += 1
            for item in accounts['data']:
                if type == 1:
                    assgin_balance(item, money)
                else:
                    assgin_coin(item, money)
                account_num += 1

    #增加赠送记录
    if type == 1:  # 增加余额
        d_db.insert_balance_give(item=m_schema.CreateBalanceGive(
            user_ids='all',
            coin=0,
            balance=money,
            type=type,
            description='任务执行全员赠送金额',
            create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            operator_id=0,
            sucess_num=account_num
        ))
    elif type == 2:  # 增加积分
        d_db.insert_balance_give(item=m_schema.CreateBalanceGive(
            user_ids='all',
            coin=money,
            balance=0,
            type=type,
            description='任务执行全员赠送积分',
            create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            operator_id=0,
            sucess_num=account_num
        ))
    print(f"资金转账完毕！")


#给指定批发商赠送余额
def main2():
    money = 10000  #单位分
    type = 1 #1,转账余额   2,转账积分
    wholesale_id = 100   #批发商角色Id
    user_ids = ''
    print(f"资金转账启动：每账户赠予{money}分")
    accounts = get_user_account_wholesale(1, wholesale_id)
    account_num = 0
    if accounts['total'] > 0:
        print(f"共{accounts['total']} - 资金账户")
        for item in accounts['data']:
            ucounts, users = item
            if type == 1:
                assgin_balance(ucounts, money)
            else:
                assgin_coin(ucounts, money)
            account_num += 1
            user_ids += str(users.id) + ','
        pages = math.ceil(accounts['total'] / 20)
        i = 2
        while i <= pages:
            accounts = get_user_account_wholesale(1, wholesale_id)
            i += 1
            for item in accounts['data']:
                ucounts, users = item
                if type == 1:
                    assgin_balance(ucounts, money)
                else:
                    assgin_coin(ucounts, money)
                account_num += 1
                user_ids += str(users.id) + ','

    #增加赠送记录
    if type == 1:  # 增加余额
        d_db.insert_balance_give(item=m_schema.CreateBalanceGive(
            user_ids=user_ids,
            coin=0,
            balance=money,
            type=type,
            description=f"批发商角色{wholesale_id}赠送金额",
            create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            operator_id=0,
            sucess_num=account_num
        ))
    elif type == 2:  # 增加积分
        d_db.insert_balance_give(item=m_schema.CreateBalanceGive(
            user_ids=user_ids,
            coin=money,
            balance=0,
            type=type,
            description=f"批发商角色{wholesale_id}赠送金额",
            create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            operator_id=0,
            sucess_num=account_num
        ))
    print(f"{user_ids}资金转账完毕！")



#给指定会员赠送余额
def main3():
    money = 10000  #单位分
    type = 1 #1,转账余额   2,转账积分
    level_id = 1   #会员Id
    user_ids = ''
    print(f"资金转账启动：每账户赠予{money}分")
    accounts = get_user_account_level(1, level_id)
    account_num = 0
    if accounts['total'] > 0:
        print(f"共{accounts['total']} - 资金账户")
        for item in accounts['data']:
            ucounts, users = item
            if type == 1:
                assgin_balance(ucounts, money)
            else:
                assgin_coin(ucounts, money)
            account_num += 1
            user_ids += str(users.id) + ','
        pages = math.ceil(accounts['total'] / 20)
        i = 2
        while i <= pages:
            accounts = get_user_account_level(1, level_id)
            i += 1
            for item in accounts['data']:
                ucounts, users = item
                if type == 1:
                    assgin_balance(ucounts, money)
                else:
                    assgin_coin(ucounts, money)
                account_num += 1
                user_ids += str(users.id) + ','

    #增加赠送记录
    if type == 1:  # 增加余额
        d_db.insert_balance_give(item=m_schema.CreateBalanceGive(
            user_ids=user_ids,
            coin=0,
            balance=money,
            type=type,
            description=f"会员角色{level_id}赠送金额",
            create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            operator_id=0,
            sucess_num=account_num
        ))
    elif type == 2:  # 增加积分
        d_db.insert_balance_give(item=m_schema.CreateBalanceGive(
            user_ids=user_ids,
            coin=money,
            balance=0,
            type=type,
            description=f"会员角色{level_id}赠送金额",
            create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            operator_id=0,
            sucess_num=account_num
        ))
    print(f"{user_ids}资金转账完毕！")

if __name__ == '__main__':
    #main()  # 全部
    #main2()  # 批发商角色
    main3()  # 会员角色