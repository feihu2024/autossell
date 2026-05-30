from typing import Optional, List, Tuple
from sqlalchemy import or_, text, func

from common import Dao, global_define, global_function
from model.schema import TFundPartner, TFundFplog, TFund, TFundZqlog, TUser
import datetime, time, logging
from dao import d_account, d_user
from model.mall import m_account

#合伙人

def add_fund(zhouqi: int, good_id: int, order_id: int, balance: int):
    with Dao() as db:
        # 添加资金池
        db.add(TFund(
            zhouqi=zhouqi,
            good_id=good_id,
            order_id=order_id,
            balance=balance,
            fenpei_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            status=0
        ))
        db.commit()

def get_first_fund():
    with Dao() as db:
        return db.query(TFundZqlog).order_by(TFundZqlog.id.desc()).first()

def get_fund_list():
    with Dao() as db:
        return db.query(TFund).where(TFund.status == 0).all()

def get_fund_partner_list(zhouqi:int):
    with Dao() as db:
        return db.query(TFundPartner).where(TFundPartner.zhouqi == zhouqi).all()

def get_fundzqlog(zhouqi:int):
    with Dao() as db:
        return db.query(TFundZqlog).where(TFundZqlog.zhouqi == zhouqi).first()

def add_zhouqi_fund(zhouqi:int, balance:int, fund_id:int):
    with Dao() as db:
        fund_rs = db.query(TFundZqlog).where(TFundZqlog.zhouqi == zhouqi).first()
        if fund_rs:
            total_balance = fund_rs.balance + balance
            db.query(TFundZqlog).where(TFundZqlog.id == fund_rs.id).update({"balance": total_balance})
        else:
            db.add(TFundZqlog(
                zhouqi=zhouqi,
                balance=balance
            ))
        db.query(TFund).where(TFund.id == fund_id).update({"status": 1})
        db.commit()

#归集资金
def put_together_fund():
   fund_list = get_fund_list()
   for this_fund in fund_list:
       add_zhouqi_fund(this_fund.zhouqi, this_fund.balance, this_fund.id)

#某周期计算分资金池比例
def get_fund_proportion(zhouqi:int, parent_id:int):
    res = {'mycount':0, 'total':0}
    with Dao() as db:
        res['mycount'] = db.query(TFundPartner).where(TFundPartner.zhouqi == zhouqi).where(TFundPartner.parent_id == parent_id).count()
        res['total'] = db.query(TFundPartner).where(TFundPartner.zhouqi == zhouqi).count()
    return res

def get_partners(user_id: int):
    with Dao() as db:
        return db.query(TUser).where(TUser.partner_id == user_id).all()

def update_partner(user_id: int, partner_id: int):
    with Dao() as db:
        db.query(TUser).where(TUser.id == user_id).update({"partner_id": partner_id})
        db.commit()

def update_fund_zqlog(zhouqi: int, status: int = 1, fenpei_num:int = 0):
    with Dao() as db:
        db.query(TFundZqlog).where(TFundZqlog.zhouqi == zhouqi).update({"fenpei_num": fenpei_num, "status": status})
        db.commit()

def add_fund_fplog(zhouqi:int, balance_fen:int, balance_total:int, balance:int, user_id:int, prom:int, user_phone:str = '', user_name:str = '', user_id_fen:str = ''):
    with Dao() as db:
        db.add(TFundFplog(
            zhouqi=zhouqi,
            balance_fen=balance_fen,
            balance_total=balance_total,
            balance=balance,
            user_id=user_id,
            user_phone=user_phone,
            user_name=user_name,
            prom=prom,
            user_id_fen=user_id_fen
        ))
        db.commit()

#分配资金池资金
def fenpei_fund_balance(zhouqi: int):
    zhouqi_list = get_fund_partner_list(zhouqi)
    zhouqi_fundzqlog = get_fundzqlog(zhouqi)
    logging.info(f"start fenpei_fund_balance")
    if zhouqi_fundzqlog and zhouqi_fundzqlog.status < 1:
        total_zhouqi_list = len(zhouqi_list)
        logging.info(f"fenpei_fund_balance分配资金池：{zhouqi},total人数：{total_zhouqi_list}，总资金：{zhouqi_fundzqlog.balance}")
        while_num = 1
        while len(zhouqi_list) > 0:
            logging.info(f"分配跑圈：{while_num}")
            del_list = []
            del_userid_list = []
            del_list = list(reversed(del_list))

            if len(zhouqi_list) > 0:
                del_n = zhouqi_list[0].parent_id
                logging.info(f"合伙人：{del_n}")
                del_list.append(0)
                del_userid_list.append(zhouqi_list[0].user_id)
                for i, zq in enumerate(zhouqi_list[1:], start=1):
                    if zq.parent_id == del_n:
                        del_list.append(i)
                        del_userid_list.append(zq.user_id)
                str_list = ','.join([str(item) for item in del_list])
                str_list_user = ','.join([str(item) for item in del_userid_list])
                prom = round(len(del_list)/total_zhouqi_list, 2)
                user_account = d_account.get_account_info(del_n)
                logging.info(f"下属人：{str_list_user},序号:{str_list},比例：{prom}")
                if user_account:
                    balance = prom * zhouqi_fundzqlog.balance
                    balance_total = balance + user_account.balance
                    userinfo = d_user.get_user_by_id(del_n)
                    logging.info(f"分配资金：{balance},用户余额:{balance_total}")
                    d_account.update_account_balance(del_n, balance_total)
                    d_account.add_balance(m_account.BalanceModel(
                        user_id=del_n,
                        change=balance,
                        balance=balance_total,
                        type=global_define.balance_type[38],
                        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    ))
                    add_fund_fplog(zhouqi, balance, zhouqi_fundzqlog.balance, balance_total, del_n, prom * 100, userinfo.phone, userinfo.nickname, str_list)
                else:
                    logging.info(f"未找到资金账户:{del_n}")
            for i in del_list:
                del zhouqi_list[i]
            while_num += 1
        update_fund_zqlog(zhouqi, 1, while_num)
        return '完成分配'
    else:
        return '已分配过'


