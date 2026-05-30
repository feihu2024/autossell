import math

from sqlalchemy.orm import Session
from common import Dao, global_define, global_function
from model.schema import TBalance, TCoin, TUser,TFlashOrder,TPackage,TGood,TOrder,TRandompro,TShoperorderfee,TFundPartner,TRoomContributelog, TFundPondLog, TFundWeightLog
from model.m_schema import *
from sqlalchemy import or_, and_, func
from typing import List, Optional
from model.mall import m_order
from sqlalchemy import text
import time
from datetime import datetime
from dao import d_settings, d_package, d_order, d_db, d_account, d_user, d_partner, d_bigorder
from fastapi import HTTPException
from model.mall import m_account
import logging
from config import SECRET_MALL
from jose import JWTError, jwt


def userpass_login_for_token(username: str, password: str):
    user = get_user_by_username(username=username)
    if not user:
        return ''
    if user.password == password:
        data = {
            'user_id': user.id,
            'time': time.time() + SECRET_MALL.VALID_TIME
        }
        token = {'welcomesession': get_login_token_encode(data), 'user_id': user.id}
        #raise HTTPException(status_code=200, detail={'token': token, 'massage': 'Success'}, headers={"data": '123'})
        return token
    else:
        return ''

def userpass_login_for_token_byphone(phone: str, password: str):
    user = get_user_by_phone(phone)
    if not user:
        return ''
    if user.password == password:
        data = {
            'user_id': user.id,
            'time': time.time() + SECRET_MALL.VALID_TIME
        }
        token = {'welcomesession': get_login_token_encode(data), 'user_id': user.id}
        #raise HTTPException(status_code=200, detail={'token': token, 'massage': 'Success'}, headers={"data": '123'})
        return token
    else:
        return ''

def userphone_login_for_token(phone: str):
    user = get_user_by_phone(phone)
    data = {
        'user_id': user.id,
        'time': time.time() + SECRET_MALL.VALID_TIME
    }
    token = {'token_val': get_login_token_encode(data), 'user_id': user.id}
    #raise HTTPException(status_code=200, detail={'token': token, 'massage': 'Success'}, headers={"data": '123'})
    return token

def userid_login_for_token(user_id: int):
    user = get_user_by_id(user_id)
    data = {
        'user_id': user.id,
        'time': time.time() + SECRET_MALL.VALID_TIME
    }
    token = {'token_val': get_login_token_encode(data), 'user_id': user.id}
    #raise HTTPException(status_code=200, detail={'token': token, 'massage': 'Success'}, headers={"data": '123'})
    return token


def get_login_token_encode(data:dict):
    return jwt.encode(data, SECRET_MALL.SECRET_MALL_KEY, algorithm=SECRET_MALL.ALGORITHM)

def get_login_token_decode(token:str):
    re_json = {}
    try:
        re_json = jwt.decode(token, SECRET_MALL.SECRET_MALL_KEY, algorithms=[SECRET_MALL.ALGORITHM])
    except Exception as e:
        print(e)
    return re_json

def is_login(token:str):
    data = get_login_token_decode(token)
    this_time = time.time()
    re_code = ''
    if data:
        if data.get('time') > this_time:
            data['time'] = this_time + SECRET_MALL.VALID_TIME
            re_code = get_login_token_encode(data)
    return re_code

def get_login_id(token:str):
    data = get_login_token_decode(token)
    this_time = time.time()
    re_code = 0
    if data:
        if data.get('time') > this_time:
            data['time'] = this_time + SECRET_MALL.VALID_TIME
            re_code = int(data['user_id'])
    return re_code


def login_shop_token(username: str, password: str, user_id:int):
    data = {
        'user_id': user_id,
        'time': time.time() + SECRET_MALL.VALID_TIME
    }
    token = {'token_val': get_login_token_encode(data), 'user_id': user_id}
    return token

def get_login_token_encode(data:dict):
    return jwt.encode(data, SECRET_MALL.SECRET_KEY, algorithm=SECRET_MALL.ALGORITHM)

def get_login_token_decode(token:str):
    re_json = {}
    try:
        re_json = jwt.decode(token, SECRET_MALL.SECRET_KEY, algorithms=[SECRET_MALL.ALGORITHM])
    except Exception as e:
        print(e)
    return re_json

def is_login(token:str):
    data = get_login_token_decode(token)
    this_time = time.time()
    re_code = ''
    if data:
        if data.get('time') > this_time:
            data['time'] = this_time + SECRET_MALL.VALID_TIME
            re_code = get_login_token_encode(data)
    return re_code

def get_login_id(token:str):
    data = get_login_token_decode(token)
    this_time = time.time()
    re_code = 0
    if data:
        if data.get('time') > this_time:
            data['time'] = this_time + SECRET_MALL.VALID_TIME
            re_code = int(data['user_id'])
    return re_code

def get_user_by_id(user_id: int):
    with Dao() as db:
        return db.query(TUser).where(TUser.id == user_id).first()


def get_user_by_username(username: str):
    with Dao() as db:
        return db.query(TUser).where(TUser.username == username).first()


def get_user_by_email(email: str) -> TUser:
    with Dao() as db:
        return db.query(TUser).where(TUser.email == email).first()


def get_user_by_phone(phone: str):
    with Dao() as db:
        return db.query(TUser).where(TUser.phone == phone).first()


def get_user_by_openid(openid: str) -> Optional[TUser]:
    with Dao() as db:
        return db.query(TUser).where(TUser.open_id == openid).first()

def get_user_by_bigorder_id(pareid: str) -> Optional[TUser]:
    with Dao() as db:
        return db.query(TUser).where(TUser.bigorder_id == pareid).first()

def get_user_by_code(code: str) -> Optional[TUser]:
    with Dao() as db:
        return db.query(TUser).where(TUser.invited_code == code).first()

def insert_user(user: TUser) -> TUser:
    with Dao() as db:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user



# def filter_user(item: m_schema.UserRequest, page: int = 1, page_size: int = 20):
#     with Dao() as db:
#         q = db.query(TUser)

#         if item.id is not None:
#             q = q.where(TUser.id == item.id)
#         if item.phone is not None:
#             q = q.where(TUser.phone == item.phone)
#         if item.username is not None:
#             q = q.where(TUser.username == item.username)
#         if item.id_card is not None:
#             q = q.where(TUser.id_card == item.id_card)
#         if item.nickname is not None:
#             q = q.where(TUser.nickname == item.nickname)
#         if item.level_id is not None:
#             q = q.where(TUser.level_id == item.level_id)
#         if item.gender is not None:
#             q = q.where(TUser.gender == item.gender)
#         if item.register_time:
#             q = q.where(TUser.register_time == item.register_time)
#         if item.status is not None:
#             q = q.where(TUser.status == item.status)

#         t_user_list = q.offset(page * page_size - page_size).limit(page_size).all()
#         size = t_user_list.__len__()
#         user_dict = {'data': [m_schema.SUser.parse_obj(t.__dict__) for t in t_user_list], 'size': size}
#         return user_dict

def get_user_baseinfo(user_id: int = 0):
    with Dao() as db:
        sql_str = f"select torder.user_id as user_id, t_user.username, t_user.nickname, t_user.avatar,count(torder.id) as order_count, sum(torder.paid_amount) as paid_balance_total, sum(torder.paid_balance) as flash_cost_total from ((t_flash_order as torder inner join t_user on torder.user_id = t_user.id) INNER JOIN t_package on torder.package_id=t_package.id) INNER JOIN t_good on t_package.good_id=t_good.id where torder.user_id={user_id}"
        res = db.execute(text(sql_str))
        res_fetch = res.fetchall()
        return res_fetch

        '''  为方便调试，后期转query语法
        q = db.query(
            TFlashOrder.user_id,
            TUser.username,
            TUser.nickname,
            TUser.avatar,
            func.count(TFlashOrder.id),
            func.sum(TFlashOrder.paid_amount),
            func.sum(TFlashOrder.paid_balance)
        ).join(
            TUser,
            TFlashOrder.user_id == TUser.id
        ).filter(TFlashOrder.user_id==user_id).all()

       
            .join(
            TPackage,
            TFlashOrder.package_id == TPackage.id
        ).join(
            TGood,
            TPackage.good_id == TGood.id
        )
         .where().all()
            '''
        # #待写

def update_last_active_time(user_id: int = 0):
    with Dao() as db:
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        db.query(TUser).where(TUser.id == user_id).update({"last_active_time": now_time})
        db.commit()

def update_user_openid(user_id: int = 0, open_id: str = None, union_id: str = None):
    with Dao() as db:
        db.query(TUser).where(TUser.id == user_id).update({"open_id": open_id, "union_id": union_id})
        db.commit()

def update_invited_user_id(user_id: int = 0, invited_user_id: int = 0):
    with Dao() as db:
        db.query(TUser).where(TUser.id == user_id).update({"invited_user_id": invited_user_id})
        db.commit()

#推广系，设置t_user的parent_id
def update_user_parent(user_id:int=0, parent_id:int=0):
    re = False
    with Dao() as db:
        user_info = db.query(TUser).where(TUser.id == user_id).first()
        if user_info:
            #要修改的父级与原来的相同，则不需要修改
            if user_info.parent_id != parent_id:
                if user_info.parent_id_history is not None:
                    re = db.query(TUser).where(TUser.id == user_id).update({"parent_id": parent_id, "parent_id_history":user_info.parent_id_history + "," + str(user_info.parent_id), "level_top_time":datetime.now()})
                else:
                    if user_info.parent_id is not None:
                        re = db.query(TUser).where(TUser.id == user_id).update({"parent_id": parent_id,"parent_id_history": str(user_info.parent_id), "level_top_time":datetime.now()})
                    else:
                        re = db.query(TUser).where(TUser.id == user_id).update({"parent_id": parent_id, "level_top_time":datetime.now()})
                db.commit()
    return re

#推广系，满足升级条件时，升级为顶级推广人
def update_user_top(user_id: int = 0):
    parent_info = get_user_by_id(user_id)
    if parent_info:
        user_count = get_lower_user_count(user_id)
        upload_count = d_settings.get_settings().recommend_num
        # 派生用户达到设置数量，而且不是顶级推荐人，会员级别达到1以上，则进行顶级升级
        is_up = True
        if user_count >= upload_count and parent_info.parent_id is None and parent_info.level_id >= 1:
            update_user_parent(user_id, 0)
            is_up = False

        if parent_info.parent_id is None:
            parent_info.parent_id = -1
        if user_count >= upload_count and parent_info.parent_id > 0 and parent_info.level_id >= 1 and is_up:
            with Dao() as db:
                list = db.query(TUser).where(TUser.parent_id == user_id).all()
                user_limit = d_settings.get_settings().parent_user_limit
                limit_num = 1
                for li in list:
                    if limit_num > user_limit:
                        break
                    if li.level_id > 0:
                        update_user_parent(li.id, parent_info.parent_id)
                        limit_num += 1
                #将用户推荐级别设置为顶级
                update_user_parent(user_id,0)

def update_sysuser_level(user_id:int = 0):
    user_info = get_user_by_id(user_id)
    if user_info and user_info.level_id < 4:
        update_date = {}
        if user_info.level_id == 0:
            update_date['level_id'] = 1
            update_date["level_one_time"] = datetime.now()
        elif user_info.level_id == 1:
            update_date['level_id'] = 2
            update_date["level_two_time"] = datetime.now()
            # update_date["is_partner"] = 1
        elif user_info.level_id == 2:
            update_date['level_id'] = 3
            update_date["level_three_time"] = datetime.now()
        if update_date:
            with Dao() as db:
                re = db.query(TUser).where(TUser.id == user_id).update(update_date)
                db.commit()
                return re
    return 0

#会员系，普通会员升级活跃会员   初级会员
def update_sysuser_active(user_id:int = 0):
    # sys_settings = d_settings.get_settings()
    #获取初级推荐人数配置
    level_one = d_bigorder.get_bigorder_set('level_one')
    user_info = get_user_by_id(user_id)
    re = 0
    if user_info and user_info.level_id <= 0:
        total_paid_num = get_bagorder_user_count(user_id)
        if total_paid_num >= level_one.val_int:
                re = update_sysuser_level(user_id)
                #升级会员的同时，赠与消费金额倍数的积分
                # acount_info = d_account.get_account_info(user_id)
                # if acount_info and order_paid_num > 0:
                #     add_coin = order_paid_num * global_define.multiple_coin
                #     total_coin = acount_info.coin + add_coin
                #     d_account.update_account_by_id(acount_info.id, {"coin":total_coin})
                #     coin_model = m_account.CoinModel(
                #         user_id=user_id,
                #         change=add_coin,
                #         coin=total_coin,
                #         type=global_define.balance_type[25],
                #         create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                #         description=global_define.balance_type[25]
                #     )
                #     d_account.insert_coin(coin_model)
                #赠予批发商身份2023.12.29取消
                #d_user.update_user_wholesale(user_id, global_define.wholesale_role.get("wholesale1"))

                #更新推荐人级别
                #if user_info.invited_user_id is not None:
                #    update_sysuser_high(user_info.invited_user_id)
    return re


#会员系，活跃会员升级为高级会员    高级会员
def update_sysuser_high(user_id:int = 0):
    # 获取初级推荐人数配置
    level_two = d_bigorder.get_bigorder_set('level_two')
    user_info = get_user_by_id(user_id)
    re = 0
    if user_info and user_info.level_id == 1:
        lower_count = get_bagorder_user_count(user_id)
        if lower_count >= level_two.val_int:
            logging.info('start to update_sysuser_high2，add_fund_partner')
            re = update_sysuser_level(user_id)
            # 增加合伙人记录
            # add_fund_partner(global_function.get_current_zhouqi(), user_id)
            # 更新推荐人级别
            # if user_info.invited_user_id is not None:
            #     update_sysuser_top(user_info.invited_user_id)
    return re

#会员系，高级会员升级为顶级会员   顶级会员
def update_sysuser_top(user_id:int = 0):
    # 获取初级推荐人数配置
    level_three = d_bigorder.get_bigorder_set('level_three')
    user_info = get_user_by_id(user_id)
    re = 0
    if user_info and user_info.level_id == 2:
        lower_count = get_bagorder_user_count(user_id)
        if lower_count >= level_three.val_int:
            re = update_sysuser_level(user_id)
    return re

#推广系， 下级会员统计
def get_lower_count(parent_id:int = 0, level:int = 0):
    with Dao() as db:
        return db.query(TUser).where(TUser.parent_id == parent_id).where(TUser.level_id > level).count()

#会员系， 下级会员统计
def get_lower_user_count(invited_user_id:int = 0, level:int = 0):
    with Dao() as db:
        return db.query(TUser).where(TUser.invited_user_id == invited_user_id).where(TUser.level_id >= level).count()

#获取购买过礼包订单的推荐人数
def get_bagorder_user_count(invited_user_id:int = 0, level:int = 0):
    with Dao() as db:
        return db.query(TUser).where(TUser.invited_user_id == invited_user_id).where(TUser.bagorder_num > 0).where(TUser.level_id >= level).count()

def get_users_for_level(levle_id:int, page:int = 1, page_size:int = 1000):
    with Dao() as db:
        return db.query(TUser).where(TUser.level_id == levle_id).offset(page * page_size - page_size).limit(page_size).all()

def get_users_in_level(levle_ids:list, page:int = 1, page_size:int = 1000):
    with Dao() as db:
        return db.query(TUser).filter(TUser.level_id.in_(levle_ids)).offset(page * page_size - page_size).limit(page_size).all()

def get_top_id(user_id:int = 0):
    with Dao() as db:
        user_info = db.query(TUser).where(TUser.id==user_id).first()
        if user_info is None:
            #raise HTTPException(f"未知用户：{user_id}")
            return 0
        re_id = user_info.id
        if user_info.parent_id is None:
            user_info.parent_id = 0
        if user_info.parent_id > 0:
            return get_top_id(user_info.parent_id)
        else:
            return re_id

def get_top_users(top_id:int = 0, data_list:list = [], id_list:list = []):
    data = {}
    id_list.append(top_id)
    with Dao() as db:
        lower_data = db.query(TUser).where(TUser.parent_id==top_id).all()
        data['total'] = len(lower_data)
        data['data'] = lower_data
        if data['total'] > 0:
            data_list.append(data)
        for ld in lower_data:
            if ld.id not in id_list:
                get_top_users(ld.id, data_list, id_list)
    return data_list

def get_recommend_users_tree(user_id:int = 0):
    top_id = get_top_id(user_id)
    user_info = get_user_by_id(top_id)
    re_data = []
    if user_info:
        re_data.append(user_info)
        tree_data = get_top_users(top_id,[],[])
        re_data.append(tree_data)
    return re_data

def search_test():
    with Dao() as db:
        query = db.query(TUser,TFlashOrder,(TUser.id + 100 + func.coalesce(TUser.parent_id)).label("my_add_id"))\
        .outerjoin(TFlashOrder, TUser.id==TFlashOrder.user_id)\
        .filter(TUser.id==3).all()
        return query

def get_invited_user(user_id:int):
    with Dao() as db:
        return db.query(TUser.id, TUser.phone, TUser.avatar, TUser.nickname, TUser.invited_user_id, \
                        TUser.tuan_id, TUser.video_level, TUser.is_tuan).filter(TUser.invited_user_id==user_id).all()

def get_invited_user_two(user_ids:list):
    search_rs = None
    with Dao() as db:
        search_rs = db.query(TUser.id, TUser.phone, TUser.avatar, TUser.nickname, TUser.invited_user_id, \
                        TUser.tuan_id, TUser.video_level, TUser.is_tuan).filter(TUser.invited_user_id.in_(user_ids)).all()
    return search_rs

def get_invited_user_to_page(user_id:int, page:int = 1):
    data = {}
    with Dao() as db:
        page_size = 10
        data['total'] = db.query(TUser).filter(TUser.invited_user_id == user_id).count()
        data['data'] = db.query(TUser).filter(TUser.invited_user_id==user_id).order_by(TUser.id.desc()).offset(page * page_size - page_size).limit(page_size).all()
        return data

def get_invparent_user(user_ids:list):
    with Dao() as db:
        return db.query(TUser).filter(TUser.parent_id.in_(user_ids)).all()

def get_bigorder_parent_user(bigorder_ids:list):
    with Dao() as db:
        return db.query(TUser).filter(TUser.bigorder_parent_id.in_(bigorder_ids)).all()

def get_invited_user_for_list(user_ids:list):
    # 查询：
    # [
    #     {
    #         "id": 943
    #     },
    #     {
    #         "id": 945
    #     }
    # ]
    re_ids = []
    with Dao() as db:
        search_rs = db.query(TUser.id).filter(TUser.invited_user_id.in_(user_ids)).all()
        for r in search_rs:
            re_ids.append(r["id"])
    return re_ids

def get_invited_user_for_list_notuan(user_ids:list):
    re_ids = []
    with Dao() as db:
        search_rs = db.query(TUser.id).filter(TUser.invited_user_id.in_(user_ids)).filter(TUser.is_tuan==0).all()
        for r in search_rs:
            re_ids.append(r["id"])
    return re_ids

#获取薅羊毛团长团队成员
def get_groupsir_user(user_id:int):
    data = {}
    with Dao() as db:
        re_list = db.query(TUser).filter(TUser.tuan_id==user_id).all()
        data['total'] = len(re_list)
        data['data'] = re_list
    return data

#获取下级团队列表
def get_groupsir_lower(user_id:int):
    data = {}
    with Dao() as db:
        re_list = db.query(TUser).filter(TUser.tuan_id==user_id).filter(TUser.is_tuan.in_([1,2,3,4,5,6])).all()
        data['total'] = len(re_list)
        data['data'] = re_list
    return data

#获取下级团会员列表
def get_groupsir_lower_user(user_id:int):
    data = {}
    with Dao() as db:
        re_list = db.query(TUser).filter(TUser.tuan_id==user_id).filter(TUser.is_tuan==0).all()
        data['total'] = len(re_list)
        data['data'] = re_list
    return data

def get_invparent_user_ids(user_id:int):
    ls = get_invparent_user([user_id])
    re_ids = []
    for i in ls:
        re_ids.append(i.id)
    return re_ids

def get_invited_user_ids(user_id:int):
    ls = get_invited_user(user_id)
    re_ids = []
    for i in ls:
        re_ids.append(i.id)
    return re_ids

#获取团队成员id
def get_tuan_ids(user_id:int):
    ls = get_groupsir_user(user_id)
    re_ids = []
    for i in ls['data']:
        re_ids.append(i.id)
    return re_ids

def get_member_ids_one(user_ids:list):
    re_ids = []
    with Dao() as db:
        res = db.query(TUser.id).filter(TUser.parent_id.in_(user_ids)).all()
        if res is not None:
            for r in res:
                re_ids.append(r.id)
    return re_ids

def get_member_ids(user_id:int):
    ids = []
    get_ids = get_member_ids_one([user_id])
    if len(get_ids) > 0:
        for i in get_ids:
            ids.append(i)
        get_ids = get_member_ids_one(get_ids)
        if len(get_ids) > 0:
            for i in get_ids:
                ids.append(i)
    return ids

def get_comein_users(user_id:int):
    re_val = {"parent_uid":None, "top_uid":None, "invited_uid":None, "supplier_uid":None, "eqlevel_uid":None}
    user_info = get_user_by_id(user_id)
    top_user_id = get_top_id(user_id)
    #if top_user_id != user_id and top_user_id > 0:
    if top_user_id > 0:
        top_info = get_user_by_id(top_user_id)
        if top_info:
            if top_info.parent_id is not None and top_info.level_id > 0:
                re_val['top_uid'] = top_user_id
                if top_info.invited_user_id is not None:
                    top_invited_info = get_user_by_id(top_info.invited_user_id)
                    if top_invited_info:
                        re_val['eqlevel_uid'] = top_info.invited_user_id

    #层级收益与推荐收益不能同时获取
    # if user_info.parent_id is not None:
    #     re_val['parent_uid'] = user_info.parent_id
    # elif user_info.invited_user_id is not None:
    #     re_val['invited_uid'] = user_info.invited_user_id
    #
    # if user_info.invited_user_id is not None and re_val['invited_uid'] is None and user_info.parent_id != user_info.invited_user_id:
    #     re_val['invited_uid'] = user_info.invited_user_id

    # 层级收益与推荐收益可以同时获取
    if user_info.parent_id is not None:
        re_val['parent_uid'] = user_info.parent_id
    if user_info.invited_user_id is not None:
        re_val['invited_uid'] = user_info.invited_user_id

    return re_val

def get_user_forcard(card: str):
    with Dao() as db:
        return db.query(TUser).filter(TUser.id_card == card).first()

def del_user(user_id: int):
    with Dao() as db:
        db.query(TUser).filter(TUser.id == user_id).delete()
        db.commit()

def update_user_base_info(user_id:int, nickname:str = None, avatar:str = None, phone:str = None, ercode:str = None):
    update_json = {}
    if nickname:
        update_json['nickname'] = nickname
    if avatar:
        update_json['avatar'] = avatar
    if phone:
        update_json['phone'] = phone
    if ercode:
        update_json['ercode'] = ercode
    if update_json:
        with Dao() as db:
            re = db.query(TUser).where(TUser.id == user_id).update(update_json)
            db.commit()

def update_user_wholesale(user_id: int, wholesale_id: int):
    with Dao() as db:
        re = db.query(TUser).where(TUser.id == user_id).update({"wholesale_id": wholesale_id})
        db.commit()

def update_light_status(user_id: int, light_status: int):
    with Dao() as db:
        re = db.query(TUser).where(TUser.id == user_id).update({"light_status": light_status})
        db.commit()

def update_level_status(user_id: int, level_status: int):
    with Dao() as db:
        re = db.query(TUser).where(TUser.id == user_id).update({"level_id": level_status})
        db.commit()


def get_wholesale_list(user_id: int):
    with Dao() as db:
        return db.query(TUser).filter(TUser.invited_user_id == user_id, TUser.wholesale_id == 100).all()

def update_user_wholesale_amount(user_id: int, wholesale_amount: int):
    with Dao() as db:
        re = db.query(TUser).where(TUser.id == user_id).update({"wholesale_amount": wholesale_amount})
        db.commit()

#修改用户复购次数
def update_user_pai_buydui(user_id: int, pai_buydui: int):
    with Dao() as db:
        re = db.query(TUser).where(TUser.id == user_id).update({"pai_buydui": pai_buydui})
        db.commit()

def user_random_pro_balance(prop_userid:int, prop_balance:int, order_id:int = 0, good_id:int = 0, good_title:str = '', good_num:int = 0, out_trade_no:str = '', good_wholeid:int = 1, details:str = ''):
    #select * from t_user where id > 800  order by rand() limit 1;
    num1 = False
    num2 = False
    # d_settings.get_settings().random_proportion
    # d_settings.get_settings().random_max
    # d_settings.get_settings().random_low
    #user_info = get_user_by_id(prop_userid)
    this_wholesale_id = 100
    if good_wholeid == 1:
        this_wholesale_id = 100
    elif good_wholeid == 2:
        this_wholesale_id = 200
    elif good_wholeid == 3:
        this_wholesale_id = 300
    #最小分配收益
    for i in range(4):
        if num1:
            break
        logging.warning(f"this_wholesale_id,random_low: {this_wholesale_id},{d_settings.get_settings().random_low}")
        random_rs = get_wholesale_padui_user(this_wholesale_id,  d_settings.get_settings().random_low)
        # logging.warning(f"random_rs: {random_rs}")
        if not random_rs:
            break
        with Dao() as db:
            #counts = db.query(TRandompro).where(TRandompro.pro_oneid == random_rs.id).count();
            if random_rs.paidui <= d_settings.get_settings().random_low:
                # 1联营会员，ws2_proportion   2仓库主，ws3_proportion  3巨省会员，ws1_proportion
                parent_info = d_account.get_account_info_add(random_rs.id)
                if good_wholeid == 1:
                    invited_income = prop_balance * d_settings.get_settings().ws2_proportion/100
                elif good_wholeid == 2:
                    invited_income = prop_balance * d_settings.get_settings().ws3_proportion/100
                elif good_wholeid == 3:
                    invited_income = prop_balance * d_settings.get_settings().ws1_proportion/100
                else:
                    invited_income = 0

                total_balance = round(parent_info.balance + invited_income)
                d_account.update_account_by_id(parent_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=parent_info.user_id,
                    change=invited_income,
                    balance=total_balance,
                    type=global_define.balance_type[31],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(good_id),
                    good_title=good_title,
                    good_num=str(good_num),
                    out_trade_no=out_trade_no
                ))
                #添加分成记录
                db.add(TRandompro(
                    pro_oneid = random_rs.id,
                    pro_twoid = prop_userid,
                    pro_price = prop_balance,
                    pro_num = d_settings.get_settings().random_proportion,
                    pro_balance = invited_income,
                    order_id = order_id,
                    out_trade_no = out_trade_no,
                    details = global_define.balance_type[31]
                ))
                # 增加分成次数
                update_paidui = {"paidui" : random_rs.paidui+1}
                db.query(TUser).where(TUser.id == random_rs.id).update(update_paidui)
                db.commit()
                num1 = True
    #最大分配收益
    if not num1:
        for i in range(4):
            if num2:
                break
            random_rs = get_wholesale_padui_user(this_wholesale_id,  d_settings.get_settings().random_max)
            if not random_rs:
                break
            with Dao() as db:
                #counts = db.query(TRandompro).where(TRandompro.pro_oneid == random_rs.id).count();
                if random_rs.paidui < d_settings.get_settings().random_max:
                    parent_info = d_account.get_account_info_add(random_rs.id)
                    invited_income = 0
                    if good_wholeid == 1:
                        invited_income = prop_balance * d_settings.get_settings().ws2_proportion / 100
                    elif good_wholeid == 2:
                        invited_income = prop_balance * d_settings.get_settings().ws3_proportion / 100
                    elif good_wholeid == 3:
                        invited_income = prop_balance * d_settings.get_settings().ws1_proportion / 100

                    total_balance = round(parent_info.balance + invited_income)
                    d_account.update_account_by_id(parent_info.id, {"balance": total_balance})
                    d_account.add_balance(m_account.BalanceModel(
                        user_id=parent_info.user_id,
                        change=invited_income,
                        balance=total_balance,
                        type=global_define.balance_type[31],
                        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        good_id=str(good_id),
                        good_title=good_title,
                        good_num=str(good_num),
                        out_trade_no=out_trade_no
                    ))
                    #添加分成记录
                    db.add(TRandompro(
                        pro_oneid = random_rs.id,
                        pro_twoid = prop_userid,
                        pro_price = prop_balance,
                        pro_num = d_settings.get_settings().random_proportion,
                        pro_balance = invited_income,
                        order_id = order_id,
                        out_trade_no = out_trade_no,
                        details = global_define.balance_type[31]
                    ))
                    # 增加分成次数
                    update_paidui = {"paidui": random_rs.paidui + 1}
                    db.query(TUser).where(TUser.id == random_rs.id).update(update_paidui)
                    db.commit()
                    num2 = True

    return num1 or num2

#2024.8.15根据批发商品类型排队分成逻辑
def user_shoperorderfee_pro_balance(prop_userid:int, prop_balance:int, order_id:int = 0, good_id:int = 0, good_title:str = '', good_num:int = 0, out_trade_no:str = '', good_wholeid:int = 1, details:str = ''):
    #select * from t_user where id > 800  order by rand() limit 1;
    num1 = True
    # d_settings.get_settings().random_proportion
    # d_settings.get_settings().random_max
    # d_settings.get_settings().random_low
    #user_info = get_user_by_id(prop_userid)
    this_wholesale_id = 100
    if good_wholeid == 1:
        this_wholesale_id = 100
    elif good_wholeid == 2:
        this_wholesale_id = 200
    elif good_wholeid == 3:
        this_wholesale_id = 300
    #排队分配收益
    shoperorderfee_info = get_wholesale_shoperorderfee(good_wholeid)
    if shoperorderfee_info:
        parent_info = d_account.get_account_info_add(shoperorderfee_info.user_id)
        pro_num = 0
        if good_wholeid == 1:
            pro_num = d_settings.get_settings().ws2_proportion
            invited_income = prop_balance * pro_num / 100
        elif good_wholeid == 2:
            pro_num = d_settings.get_settings().ws3_proportion
            invited_income = prop_balance * d_settings.get_settings().ws3_proportion / 100
        elif good_wholeid == 3:
            pro_num = d_settings.get_settings().ws1_proportion
            invited_income = prop_balance * d_settings.get_settings().ws1_proportion / 100
        else:
            invited_income = 0

        if invited_income > 0:
            total_balance = round(parent_info.balance + invited_income)
            d_account.update_account_by_id(parent_info.id, {"balance": total_balance})
            with Dao() as db:
                d_account.add_balance(m_account.BalanceModel(
                    user_id=parent_info.user_id,
                    change=invited_income,
                    balance=total_balance,
                    type=global_define.balance_type[31],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(good_id),
                    good_title=good_title,
                    good_num=str(good_num),
                    out_trade_no=out_trade_no
                ))
                # 添加分成记录
                db.add(TRandompro(
                    pro_oneid=parent_info.user_id,
                    pro_twoid=prop_userid,
                    pro_price=prop_balance,
                    pro_num=pro_num,
                    pro_balance=invited_income,
                    order_id=order_id,
                    out_trade_no=out_trade_no,
                    details=global_define.balance_type[31]
                ))
                # 增加分成次数
                update_paidui = {"fee_num": shoperorderfee_info.fee_num - 1}
                db.query(TShoperorderfee).where(TShoperorderfee.id == shoperorderfee_info.id).update(update_paidui)
                db.commit()
                logging.warning(f"good_wholeid,order_id,uid,to_uid: {good_wholeid},{order_id},{prop_userid},{parent_info.user_id}分润{invited_income}")
    else:
        logging.warning(f"good_wholeid,order_id: {good_wholeid},{order_id}未发现排队信息")

    return num1

#随机分
def user_shoperorderfee_pro_balance_jinny(source_userid:int, rand_balance:int, order_id:int = 0, good_id:int = 0, good_title:str = '', good_num:int = 0, out_trade_no:str = '', details:str = ''):
    #select * from t_user where id > 800  order by rand() limit 1;
    this_wholesale_id = 1  #level-1合伙人类型
    random_rs = get_wholesale_user_jinny(this_wholesale_id)
    # logging.warning(f"random_rs: {random_rs}")
    if random_rs:
        acount_info = d_account.get_account_info_add(random_rs.id)
        with Dao() as db:
            total_balance = round(acount_info.balance + rand_balance)
            d_account.update_account_by_id(acount_info.id, {"balance": total_balance})
            d_account.add_balance(m_account.BalanceModel(
                user_id=random_rs.id,
                change=rand_balance,
                balance=total_balance,
                type=global_define.balance_type[3],
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                good_id=str(good_id),
                good_title=good_title,
                good_num=str(good_num),
                out_trade_no=out_trade_no,
                user_nick=random_rs.nickname,
                phone=random_rs.phone,
                description=f"来源于用户{source_userid}，订单{order_id}"
            ))

    return True

#获取某一身份的随机批发商
def get_wholesale_user_jinny(wholesale_id):
    with Dao() as db:
        return db.query(TUser).where(TUser.level_id == wholesale_id).order_by(func.random()).first()

#获取一个排队分成批发商信息
def get_wholesale_shoperorderfee(wholesale_id):
    with Dao() as db:
        return db.query(TShoperorderfee).where(TShoperorderfee.fee_num > 0).where(TShoperorderfee.gtype == wholesale_id).order_by(TShoperorderfee.id.asc()).first()

#添加批发商商品排队分润  1联营会员2仓库主3巨省会员
def add_shoperorderfee(good_id, order_id, user_id, gtype):
    fee_num = 0
    if gtype == 1:
        fee_num = global_define.wholesale_shoperorderfee['wholesale1']
    elif gtype == 2:
        fee_num = global_define.wholesale_shoperorderfee['wholesale2']
    elif gtype == 3:
        fee_num = global_define.wholesale_shoperorderfee['wholesale3']
    with Dao() as db:
        # 添加排队分润
        db.add(TShoperorderfee(
            good_id=good_id,
            order_id=order_id,
            user_id=user_id,
            fee_num=fee_num,
            gtype=gtype,
            fee_count=fee_num
        ))
        db.commit()
    return True

#获取随机批发商
def get_wholesale_user():
    with Dao() as db:
        return db.query(TUser).where(TUser.wholesale_id > 0).order_by(func.random()).first()

#获取某一身份的随机批发商
def get_wholesale_user_user(wholesale_id):
    with Dao() as db:
        return db.query(TUser).where(TUser.wholesale_id == wholesale_id).order_by(func.random()).first()

#获取某一身份的排队分批发商
def get_wholesale_padui_user(wholesale_id:int, limit:int):
    with Dao() as db:
        return db.query(TUser).where(TUser.wholesale_id == wholesale_id).where(TUser.paidui <= limit).order_by(TUser.id.desc()).first()

#记录升级老板（合伙人）关联记录  `t_fund_partner
def add_fund_partner(zhouqi:int, user_id:int):
    info1 = get_user_by_id(user_id)
    logging.info('start to add_fund_partner')
    if info1:
        #把下级都转给他的上级
        partner_list = d_partner.get_partners(user_id)
        for li in partner_list:
            d_partner.update_partner(li.id, info1.partner_id)

        #找上级合伙人，增加上级合伙人关系
        if info1.partner_id > 0:
            info2 = get_user_by_id(info1.partner_id)
            if info2:
                if info2.level_id >= 2:
                    logging.info(f"zhouqi:{zhouqi},user_id:{user_id},parent_id:{info2.id}")
                    with Dao() as db:
                        # 添加
                        db.add(TFundPartner(
                            zhouqi=zhouqi,
                            user_id=user_id,
                            parent_id=info2.id
                        ))
                        db.commit()
                else:
                    info3 = get_user_by_id(info2.partner_id)
                    if info3:
                        if info3.level_id >= 2:
                            logging.info(f"zhouqi:{zhouqi},user_id:{user_id},parent_id:{info3.id}")
                            with Dao() as db:
                                # 添加
                                db.add(TFundPartner(
                                    zhouqi=zhouqi,
                                    user_id=user_id,
                                    parent_id=info3.id
                                ))
                                db.commit()
                        else:
                            info4 = get_user_by_id(info3.partner_id)
                            if info4:
                                if info4.level_id >= 2:
                                    logging.info(f"zhouqi:{zhouqi},user_id:{user_id},parent_id:{info4.id}")
                                    with Dao() as db:
                                        # 添加
                                        db.add(TFundPartner(
                                            zhouqi=zhouqi,
                                            user_id=user_id,
                                            parent_id=info4.id
                                        ))
                                        db.commit()
        #将老板升级为顶级合伙人
        d_partner.update_partner(user_id, 0)
    return True

#获取升级留下的合伙人下级成员
def get_partner_at_users(parent_id:int):
    data = {"code": 0, "data":'', 'total': 0}
    with Dao() as db:
        re_list = db.query(TUser).filter(TUser.invited_user_id!=TUser.partner_id).filter(TUser.partner_id==parent_id).all()
        data['total'] = len(re_list)
        data['data'] = re_list
    return data

def filter_user(items: dict, search_items: dict = {}, set_items: dict = {}, page: int = 1, page_size: int = 20) -> List[
    SUser]:
    with Dao() as db:
        q = db.query(TUser)

        if 'id' in items:
            q = q.where(TUser.id == items['id'])
        if 'id_start' in items:
            q = q.where(TUser.id >= items['id_start'])
        if 'id_end' in items:
            q = q.where(TUser.id <= items['id_end'])

        if 'username' in items:
            q = q.where(TUser.username == items['username'])
        if 'username_start' in items:
            q = q.where(TUser.username >= items['username_start'])
        if 'username_end' in items:
            q = q.where(TUser.username <= items['username_end'])

        if 'email' in items:
            q = q.where(TUser.email == items['email'])
        if 'email_start' in items:
            q = q.where(TUser.email >= items['email_start'])
        if 'email_end' in items:
            q = q.where(TUser.email <= items['email_end'])

        if 'open_id' in items:
            q = q.where(TUser.open_id == items['open_id'])
        if 'open_id_start' in items:
            q = q.where(TUser.open_id >= items['open_id_start'])
        if 'open_id_end' in items:
            q = q.where(TUser.open_id <= items['open_id_end'])

        if 'union_id' in items:
            q = q.where(TUser.union_id == items['union_id'])
        if 'union_id_start' in items:
            q = q.where(TUser.union_id >= items['union_id_start'])
        if 'union_id_end' in items:
            q = q.where(TUser.union_id <= items['union_id_end'])

        if 'password' in items:
            q = q.where(TUser.password == items['password'])
        if 'password_start' in items:
            q = q.where(TUser.password >= items['password_start'])
        if 'password_end' in items:
            q = q.where(TUser.password <= items['password_end'])

        if 'nickname' in items:
            q = q.where(TUser.nickname == items['nickname'])
        if 'nickname_start' in items:
            q = q.where(TUser.nickname >= items['nickname_start'])
        if 'nickname_end' in items:
            q = q.where(TUser.nickname <= items['nickname_end'])

        if 'phone' in items:
            q = q.where(TUser.phone == items['phone'])
        if 'phone_start' in items:
            q = q.where(TUser.phone >= items['phone_start'])
        if 'phone_end' in items:
            q = q.where(TUser.phone <= items['phone_end'])

        if 'id_card' in items:
            q = q.where(TUser.id_card == items['id_card'])
        if 'id_card_start' in items:
            q = q.where(TUser.id_card >= items['id_card_start'])
        if 'id_card_end' in items:
            q = q.where(TUser.id_card <= items['id_card_end'])

        if 'level_id' in items:
            q = q.where(TUser.level_id == items['level_id'])
        if 'level_id_start' in items:
            q = q.where(TUser.level_id >= items['level_id_start'])
        if 'level_id_end' in items:
            q = q.where(TUser.level_id <= items['level_id_end'])

        if 'status' in items:
            q = q.where(TUser.status == items['status'])
        if 'status_start' in items:
            q = q.where(TUser.status >= items['status_start'])
        if 'status_end' in items:
            q = q.where(TUser.status <= items['status_end'])

        if 'register_time' in items:
            q = q.where(TUser.register_time == items['register_time'])
        if 'register_time_start' in items:
            q = q.where(TUser.register_time >= items['register_time_start'])
        if 'register_time_end' in items:
            q = q.where(TUser.register_time <= items['register_time_end'])

        if 'avatar' in items:
            q = q.where(TUser.avatar == items['avatar'])
        if 'avatar_start' in items:
            q = q.where(TUser.avatar >= items['avatar_start'])
        if 'avatar_end' in items:
            q = q.where(TUser.avatar <= items['avatar_end'])

        if 'invited_user_id' in items:
            q = q.where(TUser.invited_user_id == items['invited_user_id'])
        if 'invited_user_id_start' in items:
            q = q.where(TUser.invited_user_id >= items['invited_user_id_start'])
        if 'invited_user_id_end' in items:
            q = q.where(TUser.invited_user_id <= items['invited_user_id_end'])

        if 'coin' in items:
            q = q.where(TUser.coin == items['coin'])
        if 'coin_start' in items:
            q = q.where(TUser.coin >= items['coin_start'])
        if 'coin_end' in items:
            q = q.where(TUser.coin <= items['coin_end'])

        if 'gender' in items:
            q = q.where(TUser.gender == items['gender'])
        if 'gender_start' in items:
            q = q.where(TUser.gender >= items['gender_start'])
        if 'gender_end' in items:
            q = q.where(TUser.gender <= items['gender_end'])

        if 'last_active_time' in items:
            q = q.where(TUser.last_active_time == items['last_active_time'])
        if 'last_active_time_start' in items:
            q = q.where(TUser.last_active_time >= items['last_active_time_start'])
        if 'last_active_time_end' in items:
            q = q.where(TUser.last_active_time <= items['last_active_time_end'])

        if 'name' in items:
            q = q.where(TUser.name == items['name'])
        if 'name_start' in items:
            q = q.where(TUser.name >= items['name_start'])
        if 'name_end' in items:
            q = q.where(TUser.name <= items['name_end'])

        if 'is_agree' in items:
            q = q.where(TUser.is_agree == items['is_agree'])
        if 'is_agree_start' in items:
            q = q.where(TUser.is_agree >= items['is_agree_start'])
        if 'is_agree_end' in items:
            q = q.where(TUser.is_agree <= items['is_agree_end'])

        if 'parent_id' in items:
            q = q.where(TUser.parent_id == items['parent_id'])
        if 'parent_id_start' in items:
            q = q.where(TUser.parent_id >= items['parent_id_start'])
        if 'parent_id_end' in items:
            q = q.where(TUser.parent_id <= items['parent_id_end'])

        if 'parent_id_history' in items:
            q = q.where(TUser.parent_id_history == items['parent_id_history'])
        if 'parent_id_history_start' in items:
            q = q.where(TUser.parent_id_history >= items['parent_id_history_start'])
        if 'parent_id_history_end' in items:
            q = q.where(TUser.parent_id_history <= items['parent_id_history_end'])

        if 'id' in set_items:
            q = q.where(TUser.id.in_(set_items['id']))

        if 'username' in set_items:
            q = q.where(TUser.username.in_(set_items['username']))

        if 'email' in set_items:
            q = q.where(TUser.email.in_(set_items['email']))

        if 'open_id' in set_items:
            q = q.where(TUser.open_id.in_(set_items['open_id']))

        if 'union_id' in set_items:
            q = q.where(TUser.union_id.in_(set_items['union_id']))

        if 'password' in set_items:
            q = q.where(TUser.password.in_(set_items['password']))

        if 'nickname' in set_items:
            q = q.where(TUser.nickname.in_(set_items['nickname']))

        if 'phone' in set_items:
            q = q.where(TUser.phone.in_(set_items['phone']))

        if 'id_card' in set_items:
            q = q.where(TUser.id_card.in_(set_items['id_card']))

        if 'level_id' in set_items:
            q = q.where(TUser.level_id.in_(set_items['level_id']))

        if 'status' in set_items:
            q = q.where(TUser.status.in_(set_items['status']))

        if 'register_time' in set_items:
            q = q.where(TUser.register_time.in_(set_items['register_time']))

        if 'avatar' in set_items:
            q = q.where(TUser.avatar.in_(set_items['avatar']))

        if 'invited_user_id' in set_items:
            q = q.where(TUser.invited_user_id.in_(set_items['invited_user_id']))

        if 'coin' in set_items:
            q = q.where(TUser.coin.in_(set_items['coin']))

        if 'gender' in set_items:
            q = q.where(TUser.gender.in_(set_items['gender']))

        if 'last_active_time' in set_items:
            q = q.where(TUser.last_active_time.in_(set_items['last_active_time']))

        if 'name' in set_items:
            q = q.where(TUser.name.in_(set_items['name']))

        if 'is_agree' in set_items:
            q = q.where(TUser.is_agree.in_(set_items['is_agree']))

        if 'parent_id' in set_items:
            q = q.where(TUser.parent_id.in_(set_items['parent_id']))

        if 'parent_id_history' in set_items:
            q = q.where(TUser.parent_id_history.in_(set_items['parent_id_history']))

        if 'username' in search_items:
            q = q.where(TUser.username.like(search_items['username']))

        if 'email' in search_items:
            q = q.where(TUser.email.like(search_items['email']))

        if 'open_id' in search_items:
            q = q.where(TUser.open_id.like(search_items['open_id']))

        if 'union_id' in search_items:
            q = q.where(TUser.union_id.like(search_items['union_id']))

        if 'password' in search_items:
            q = q.where(TUser.password.like(search_items['password']))

        if 'nickname' in search_items:
            q = q.where(TUser.nickname.like(search_items['nickname']))

        if 'phone' in search_items:
            q = q.where(TUser.phone.like(search_items['phone']))

        if 'id_card' in search_items:
            q = q.where(TUser.id_card.like(search_items['id_card']))

        if 'avatar' in search_items:
            q = q.where(TUser.avatar.like(search_items['avatar']))

        if 'name' in search_items:
            q = q.where(TUser.name.like(search_items['name']))

        if 'parent_id_history' in search_items:
            q = q.where(TUser.parent_id_history.like(search_items['parent_id_history']))
        q = q.order_by(TUser.id.desc())

        t_user_list = q.offset(page * page_size - page_size).limit(page_size).all()
        return [SUser.parse_obj(t.__dict__) for t in t_user_list]

def update_user_passwd(user_id:int, passwd:str):
    with Dao() as db:
        re = db.query(TUser).where(TUser.id == user_id).update({"password": passwd})
        db.commit()

def update_user_paypwd(user_id:int, passwd:str):
    with Dao() as db:
        re = db.query(TUser).where(TUser.id == user_id).update({"tran_pass": passwd})
        db.commit()

def get_user_for_list_roomgold(user_ids:list):
    with Dao() as db:
        search_rs = db.query(TUser.id, TUser.phone, TUser.avatar, TUser.nickname).filter(TUser.id.in_(user_ids)).all()
        return search_rs

def get_user_by_ids(user_ids:list):
    with Dao() as db:
        search_rs = db.query(TUser).filter(TUser.id.in_(user_ids)).all()
        return search_rs

# def get_user_by_ids_weight_num_count(user_ids:list):
#     with Dao() as db:
#         search_rs = db.query(TUser).filter(TUser.id.in_(user_ids)).all()
#         return search_rs

#获取贡献值来源
def get_user_for_list_roomgold_contribute(user_ids:list, room_ids:list):
    with Dao() as db:
        search_rs = db.query(TRoomContributelog).filter(TRoomContributelog.user_id.in_(user_ids)).filter(TRoomContributelog.room_id.in_(room_ids)).all()
        return search_rs

#升级金能源合伙人
def jny_parter_up(user_id:int):
    user_info = get_user_by_id(user_id)
    if user_info:
        if user_info.level_id < 1:
            invited_ids = get_invited_user_ids(user_id)
            count = d_order.get_baodan_order_count_for_users(invited_ids)
            if count >= global_define.room_config['up_partner']:
                with Dao() as db:
                    re = db.query(TUser).where(TUser.id == user_id).update({"level_id": 1, "level_one_time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
                    db.commit()

#更新会员权重指数，用户资金池分润
def update_user_weight_num(user_id:int=0, source_id:int=0, update_weight:int=0, all_rec:int=0):
    re = False
    with Dao() as db:
        user_info = db.query(TUser).where(TUser.id == user_id).first()
        if user_info:
            #更新权重
            total_weight = user_info.weight_num + update_weight
            user_info.weight_num = total_weight
            if total_weight % 5 == 0:
                user_info.fund_weight_num += 1
            db.flush()
            #写入日志
            fund_weight_log = TFundWeightLog(user_id=user_id,
                                           user_phone=user_info.phone,
                                           weight=update_weight,
                                           all_balance=total_weight,
                                           add_rec=1,
                                           all_rec=all_rec,
                                           source_id=source_id
                                           )
            db.add(fund_weight_log)
            db.flush()
            db.commit()

    return re

#获取指定会员群体的权重总和
def get_fund_user_count(users:list):
    # paid_amound = db.query(func.sum(schema.TOrder.paid_amount)) \
    #     .outerjoin(schema.TGood, schema.TOrder.good_id == schema.TGood.id) \
    #     .filter(schema.TOrder.status_id.in_(user_ids)) \
    #     .filter(schema.TGood.type == 1).filter(schema.TOrder.status_id >= 1).scalar()
    with Dao() as db:
        return db.query(func.sum(TUser.fund_weight_num)).filter(TUser.id.in_(users)).scalar()

def update_user_leve_hand(user_id:int, level_id:int, weight_num:int = 1):
    update_date = {}
    fund_weight_num = 1
    if weight_num > 5:
        fund_weight_num = int(weight_num / 5)
    if level_id == 1:
        update_date['level_id'] = 1
        update_date['fund_weight_num'] = fund_weight_num
        update_date["level_one_time"] = datetime.now()
    elif level_id == 2:
        update_date['level_id'] = 2
        update_date['fund_weight_num'] = fund_weight_num
        update_date["level_two_time"] = datetime.now()
        update_date["is_partner"] = 1
    elif level_id == 3:
        update_date['level_id'] = 3
        update_date['fund_weight_num'] = fund_weight_num
        update_date["level_three_time"] = datetime.now()
    if update_date:
        with Dao() as db:
            re = db.query(TUser).where(TUser.id == user_id).update(update_date)
            db.commit()

#修正用户级别脚本
def update_user_level():
    #get_bagorder_user_count
    page_size = 100
    page_count = math.ceil(1600 / page_size)
    totle_count = 0
    for i in range(page_count):
        m = i + 1
        user_ls = filter_user({},{},{},m,page_size)
        if user_ls:
            for uu in user_ls:
                inv_count = get_bagorder_user_count(uu.id)
                print(f"U:{uu.id},inv_count:{inv_count}")
                if inv_count >= 29:
                    #顶级
                    update_user_leve_hand(uu.id, 3, inv_count)
                elif inv_count >= 19:
                    #高级
                    update_user_leve_hand(uu.id, 2, inv_count)
                elif inv_count >= 3:
                    #初级
                    update_user_leve_hand(uu.id, 1, inv_count)
                totle_count += 1
    print(f"over!! totle_count: {totle_count}")


def update_user_video_level(user_id: int = 0, video_level: int = 0):
    with Dao() as db:
        db.query(TUser).where(TUser.id == user_id).update({"video_level": video_level})
        db.commit()

def update_user_sd_agent(user_id: int, sd_agent: int):
    with Dao() as db:
        re = db.query(TUser).where(TUser.id == user_id).update({"sh_agent": sd_agent})
        db.commit()
def get_sh_agent(user_id:int):
    user_info = get_user_by_id(user_id)
    re_user_id = 0
    if user_info:  # 第一层
        if user_info.sh_agent > 0:
            re_user_id = user_info.id
        else:  # 第二层
            if user_info.invited_user_id is not None:
                user_info_a = get_user_by_id(user_info.invited_user_id)
                if user_info_a: #第一层
                    if user_info_a.sh_agent > 0:
                        re_user_id = user_info_a.id
                    else: # 第二层
                        if user_info_a.invited_user_id is not None:
                            user_info_b = get_user_by_id(user_info_a.invited_user_id)
                            if user_info_b:
                                if user_info_b.sh_agent > 0:
                                    re_user_id = user_info_b.id
                                else: #第三层
                                    if user_info_b.invited_user_id is not None:
                                        user_info_c = get_user_by_id(user_info_b.invited_user_id)
                                        if user_info_c:
                                            if user_info_c.sh_agent > 0:
                                                re_user_id = user_info_c.id
                                            else: #第四层
                                                if user_info_c.invited_user_id is not None:
                                                    user_info_d = get_user_by_id(user_info_c.invited_user_id)
                                                    if user_info_d:
                                                        if user_info_d.sh_agent > 0:
                                                            re_user_id = user_info_d.id
                                                        else: #第五层
                                                            if user_info_d.invited_user_id is not None:
                                                                user_info_e = get_user_by_id(user_info_d.invited_user_id)
                                                                if user_info_e:
                                                                    if user_info_e.sh_agent > 0:
                                                                        re_user_id = user_info_e.id
                                                                    else: #低楼层
                                                                        if user_info_e.invited_user_id is not None:
                                                                            user_info_f = get_user_by_id(user_info_e.invited_user_id)
                                                                            if user_info_f:
                                                                                if user_info_f.sh_agent > 0:
                                                                                    re_user_id = user_info_f.id
                                                                                #else:
    return re_user_id

