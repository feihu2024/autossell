from common import Dao, global_define
from typing import List, Optional
from model import schema
from model import m_schema
from sqlalchemy import func, or_
from model.mall import m_order, m_account
from datetime import datetime, timedelta
from typing import Literal
from pydantic import BaseModel, Field
from dao import d_flash_order_return, d_good, d_account, d_user, d_video_task, d_address, d_balance
import time, re
import logging
import json
import uuid
from fastapi.exceptions import HTTPException

class AddOrderSource(BaseModel):
    order_id: Optional[int] = Field(None, title='订单id')
    source_id: Optional[int] = Field(None,title='订单来源，来再t_flash_order.id，如果是空或者-1表示平台')
    amount: Optional[int] = Field(None,title='商品数量')
    create_time: Optional[datetime] = Field(datetime.now(),title='创建时间')
    order_user_id: Optional[int] = Field(0,title='订单购买用户id')
    package_user_id: Optional[int] = Field(0,title='秒杀包用户id')

async def get_send_orders(item: m_order.AOrderRequest, order: Literal['asc', 'desc']):
    with Dao() as db:
        # join 多表联查，此处使用内连接
        # query = db.query(schema.TOrder, schema.TUser, schema.TGood, schema.TGoodType,
        #                  schema.TOrderState, schema.TPayChannel, schema.TStore, schema.TStoreOwner,
        #                  schema.TSupplier, schema.TSupplierOwner,(func.coalesce(schema.TOrder.paid_amount,0) + func.coalesce(schema.TOrder.paid_balance,0) + func.coalesce(schema.TOrder.paid_lock_balance,0) - func.coalesce(schema.TOrder.cost_price,0)).label("order_income"),\
        #                  schema.TGoodSpec) \
        query = db.query(schema.TOrder, schema.TUser, schema.TGood,
        (func.coalesce(schema.TOrder.paid_amount, 0) + func.coalesce(schema.TOrder.paid_balance, 0) + func.coalesce(schema.TOrder.paid_lock_balance,0) - func.coalesce(schema.TOrder.cost_price, 0)).label("order_income"), \
         )\
        .outerjoin(schema.TUser, schema.TOrder.paider_id == schema.TUser.id) \
        .outerjoin(schema.TGood, schema.TOrder.good_id == schema.TGood.id)

        if item.good_type is not None:
            query = query.where(schema.TGood.type == item.good_type)
        # else:
        #     query = query.where(schema.TGood.type == 1)
        if item.good_id is not None:
            query = query.where(schema.TGood.id == item.good_id)
        if item.good_name is not None:
            query = query.where(schema.TGood.title.like(f'%{item.good_name}%'))
        if item.customer_name is not None:
            query = query.where(schema.TUser.username.like(f'%{item.customer_name}%'))
        if item.customer_phone is not None:
            query = query.where(schema.TUser.phone == item.customer_phone)
        if item.out_trade_no is not None:
            query = query.where(schema.TOrder.out_trade_no.like(f'%{item.out_trade_no}%'))
        if item.order_id is not None:
            query = query.where(schema.TOrder.id == item.order_id)
        if item.paider_id is not None:
            query = query.where(schema.TOrder.paider_id == item.paider_id)
        if item.delivery_track_code is not None:
            query = query.where(schema.TOrder.delivery_track_code == item.delivery_track_code)
        if item.is_wholesale is not None:
            query = query.where(schema.TOrder.is_wholesale == item.is_wholesale)
        if item.order_status_ids is not None:
            ids = item.order_status_ids.split(',')
            query = query.where(schema.TOrder.status_id.in_(ids))
        else:
            if item.order_status_id is not None:
                query = query.where(schema.TOrder.status_id == item.order_status_id)
            # else: # 隐藏未付款订单
            #     query = query.where(schema.TOrder.status_id > 0)
        if item.time_start is not None:
            query = query.where(schema.TOrder.create_time >= datetime.fromtimestamp(int(item.time_start)))
        if item.time_end is not None:
            query = query.where(schema.TOrder.create_time <= datetime.fromtimestamp(int(item.time_end)))
        if item.admin_id > 0:
            query = query.where(schema.TGood.admin_id == item.admin_id)

        total_size = query.count()

        if order == 'asc':
            query = query.order_by(schema.TOrder.id.asc())
        elif order == 'desc':
            query = query.order_by(schema.TOrder.id.desc())
        items = query.offset(item.page * item.page_size - item.page_size).limit(item.page_size).all()

        send_list: List[m_order.ASendMsg_two] = [
            m_order.ASendMsg_two(s_Order=m_schema.SOrder.parse_obj(item[0].__dict__) if item[0] else None,
                             s_User=m_schema.SUser.parse_obj(item[1].__dict__) if item[1] else None,
                             s_Good=m_schema.SGood.parse_obj(item[2].__dict__) if item[2] else None
                             ) for item in items]

        return m_order.ASendMsgList(data=send_list, total=total_size)



async def get_send_shoper_orders(item: m_order.AOrderRequestShoper, order: Literal['asc', 'desc']):
    with Dao() as db:
        # join 多表联查，此处使用内连接
        # query = db.query(schema.TOrder, schema.TUser, schema.TGood, schema.TGoodType,
        #                  schema.TOrderState, schema.TPayChannel, schema.TStore, schema.TStoreOwner,
        #                  schema.TSupplier, schema.TSupplierOwner,(func.coalesce(schema.TOrder.paid_amount,0) + func.coalesce(schema.TOrder.paid_balance,0) + func.coalesce(schema.TOrder.paid_lock_balance,0) - func.coalesce(schema.TOrder.cost_price,0)).label("order_income"),\
        #                  schema.TGoodSpec) \
        query = db.query(schema.TOrder, schema.TUser, schema.TGood,
        (func.coalesce(schema.TOrder.paid_amount, 0) + func.coalesce(schema.TOrder.paid_balance, 0) + func.coalesce(schema.TOrder.paid_lock_balance,0) - func.coalesce(schema.TOrder.cost_price, 0)).label("order_income"), \
         )\
        .outerjoin(schema.TUser, schema.TOrder.paider_id == schema.TUser.id) \
        .outerjoin(schema.TGood, schema.TOrder.good_id == schema.TGood.id)

        if item.good_type is not None:
            query = query.where(schema.TGood.type == item.good_type)
        # else:
        #     query = query.where(schema.TGood.type == 1)
        if item.good_id is not None:
            query = query.where(schema.TGood.id == item.good_id)
        if item.good_name is not None:
            query = query.where(schema.TGood.title.like(f'%{item.good_name}%'))
        if item.customer_name is not None:
            query = query.where(schema.TUser.username.like(f'%{item.customer_name}%'))
        if item.customer_phone is not None:
            query = query.where(schema.TUser.phone == item.customer_phone)
        if item.out_trade_no is not None:
            query = query.where(schema.TOrder.out_trade_no.like(f'%{item.out_trade_no}%'))
        if item.order_id is not None:
            query = query.where(schema.TOrder.id == item.order_id)
        if item.paider_id is not None:
            query = query.where(schema.TOrder.paider_id == item.paider_id)
        if item.delivery_track_code is not None:
            query = query.where(schema.TOrder.delivery_track_code == item.delivery_track_code)
        if item.is_wholesale is not None:
            query = query.where(schema.TOrder.is_wholesale == item.is_wholesale)
        if item.order_status_ids is not None:
            ids = item.order_status_ids.split(',')
            query = query.where(schema.TOrder.status_id.in_(ids))
        else:
            if item.order_status_id is not None:
                query = query.where(schema.TOrder.status_id == item.order_status_id)
            # else: # 隐藏未付款订单
            #     query = query.where(schema.TOrder.status_id > 0)
        if item.time_start is not None:
            query = query.where(schema.TOrder.create_time >= datetime.fromtimestamp(int(item.time_start)))
        if item.time_end is not None:
            query = query.where(schema.TOrder.create_time <= datetime.fromtimestamp(int(item.time_end)))
        if item.admin_id > 0:
            query = query.where(schema.TGood.admin_id == item.admin_id)

        #锁定商家订单
        query = query.where(schema.TOrder.supplier_id == item.supplier_id)

        total_size = query.count()

        if order == 'asc':
            query = query.order_by(schema.TOrder.id.asc())
        elif order == 'desc':
            query = query.order_by(schema.TOrder.id.desc())
        items = query.offset(item.page * item.page_size - item.page_size).limit(item.page_size).all()

        send_list: List[m_order.ASendMsg_two] = [
            m_order.ASendMsg_two(s_Order=m_schema.SOrder.parse_obj(item[0].__dict__) if item[0] else None,
                             s_User=m_schema.SUser.parse_obj(item[1].__dict__) if item[1] else None,
                             s_Good=m_schema.SGood.parse_obj(item[2].__dict__) if item[2] else None
                             ) for item in items]

        return m_order.ASendMsgList(data=send_list, total=total_size)


async def get_return_orders(item: m_order.AOrderRequest) -> m_order.AOrderMsgList:
    with Dao() as db:
        # join 多表联查，此处使用内连接
        query = db.query(schema.TOrder, schema.TUser, schema.TGood, schema.TGoodType,
                         schema.TOrderState, schema.TPayChannel, schema.TStore, schema.TStoreOwner,
                         schema.TSupplier, schema.TSupplierOwner, schema.TOrderReturn) \
            .outerjoin(schema.TOrder, schema.TOrderReturn.order_id == schema.TOrder.id) \
            .outerjoin(schema.TUser, schema.TOrder.paider_id == schema.TUser.id) \
            .outerjoin(schema.TGood, schema.TOrder.good_id == schema.TGood.id) \
            .outerjoin(schema.TGoodType, schema.TGood.type == schema.TGoodType.id) \
            .outerjoin(schema.TOrderState, schema.TOrderReturn.status_id == schema.TOrderState.id) \
            .outerjoin(schema.TPayChannel, schema.TOrder.paid_channel_id == schema.TPayChannel.id) \
            .outerjoin(schema.TStore, schema.TOrder.store_id == schema.TStore.id) \
            .outerjoin(schema.TStoreOwner, schema.TStoreOwner.id == schema.TStore.owner_id) \
            .outerjoin(schema.TSupplier, schema.TGood.supplier_id == schema.TSupplier.id) \
            .outerjoin(schema.TSupplierOwner, schema.TSupplier.owner_id == schema.TSupplierOwner.id)

        if item.good_type is not None:
            query = query.where(schema.TGood.type == item.good_type)
        if item.good_id is not None:
            query = query.where(schema.TGood.id == item.good_id)
        if item.good_name is not None:
            query = query.where(schema.TOrder.good_name.like(f'%{item.good_name}%'))
        if item.customer_name is not None:
            query = query.where(schema.TUser.username.like(f'%{item.customer_name}%'))
        if item.customer_phone is not None:
            query = query.where(schema.TUser.phone == item.customer_phone)
        if item.order_id is not None:
            query = query.where(schema.TOrderReturn.id == item.order_id)
        if item.time_start is not None:
            query = query.where(schema.TOrderReturn.return_submit_time >= datetime.fromtimestamp(int(item.time_start)))
        if item.time_end is not None:
            query = query.where(schema.TOrderReturn.return_submit_time <= datetime.fromtimestamp(int(item.time_end)))
        if item.return_status_id is not None:
            query = query.where(schema.TOrderReturn.status_id == item.return_status_id)

        total_size = query.count()
        items = query.offset(item.page * item.page_size - item.page_size).limit(item.page_size).all()

        return_list: List[m_order.AReturnMsg] = [
            m_order.AReturnMsg(s_Order=m_schema.SOrder.parse_obj(item[0].__dict__) if item[0] else None,
                               s_User=m_schema.SUser.parse_obj(item[1].__dict__) if item[1] else None,
                               s_Good=m_schema.SGood.parse_obj(item[2].__dict__) if item[2] else None,
                               s_GoodType=m_schema.SGoodType.parse_obj(item[3].__dict__) if item[3] else None,
                               s_ReturnState=m_schema.SOrderState.parse_obj(item[4].__dict__ if item[4] else None),
                               s_PayChannel=m_schema.SPayChannel.parse_obj(item[5].__dict__) if item[5] else None,
                               s_Store=m_schema.SStore.parse_obj(item[6].__dict__) if item[6] else None,
                               s_StoreOwner=m_schema.SStoreOwner.parse_obj(item[7].__dict__) if item[7] else None,
                               s_GoodSupplier=m_schema.SSupplier.parse_obj(item[8].__dict__) if item[8] else None,
                               s_GoodSupplierOwner=m_schema.SSupplierOwner.parse_obj(item[9].__dict__)
                               if item[9] else None,
                               s_OrderReturn=m_schema.SOrderReturn.parse_obj(item[10].__dict__) if item[10] else None
                               ) for item in items]

        return m_order.AOrderMsgList(data=return_list, total=total_size)


async def get_all_orders(item: m_order.AOrderRequest, order: Literal['asc', 'desc'] = 'asc') -> m_order.AOrderMsgList:
    with Dao() as db:
        # join 多表联查，此处使用内连接
        query = db.query(schema.TOrder, schema.TUser, schema.TGood, schema.TGoodType,
                         schema.TOrderState, schema.TPayChannel, schema.TStore, schema.TStoreOwner,
                         schema.TSupplier, schema.TSupplierOwner, schema.TOrderReturn) \
            .outerjoin(schema.TOrderReturn, schema.TOrderReturn.order_id == schema.TOrder.id) \
            .outerjoin(schema.TUser, schema.TOrder.paider_id == schema.TUser.id) \
            .outerjoin(schema.TGood, schema.TOrder.good_id == schema.TGood.id) \
            .outerjoin(schema.TGoodType, schema.TGood.type == schema.TGoodType.id) \
            .outerjoin(schema.TOrderState, schema.TOrder.status_id == schema.TOrderState.id) \
            .outerjoin(schema.TPayChannel, schema.TOrder.paid_channel_id == schema.TPayChannel.id) \
            .outerjoin(schema.TStore, schema.TOrder.store_id == schema.TStore.id) \
            .outerjoin(schema.TStoreOwner, schema.TStoreOwner.id == schema.TStore.owner_id) \
            .outerjoin(schema.TSupplier, schema.TGood.supplier_id == schema.TSupplier.id) \
            .outerjoin(schema.TSupplierOwner, schema.TSupplier.owner_id == schema.TSupplierOwner.id)

        if item.good_type is not None:
            query = query.where(schema.TGood.type == item.good_type)
        else:
            query = query.where(schema.TGood.type == 0)
        if item.good_id is not None:
            query = query.where(schema.TGood.id == item.good_id)
        if item.good_name is not None:
            query = query.where(schema.TOrder.good_name.like(f'%{item.good_name}%'))
        if item.customer_name is not None:
            query = query.where(schema.TUser.username.like(f'%{item.customer_name}%'))
        if item.customer_phone is not None:
            query = query.where(schema.TUser.phone == item.customer_phone)
        if item.order_id is not None:
            query = query.where(schema.TOrderReturn.id == item.order_id)
        if item.time_start is not None:
            query = query.where(schema.TOrderReturn.return_submit_time >= datetime.fromtimestamp(int(item.time_start)))
        if item.time_end is not None:
            query = query.where(schema.TOrderReturn.return_submit_time <= datetime.fromtimestamp(int(item.time_end)))
        if item.complete_start is not None:
            query = query.where(schema.TOrder.complete_time >= datetime.fromtimestamp(int(item.complete_start)))
        if item.complete_end is not None:
            query = query.where(schema.TOrder.complete_time <= datetime.fromtimestamp(int(item.complete_end)))
        if item.order_status_id is not None:
            query = query.where(schema.TOrder.status_id == item.order_status_id)

        total_size = query.count()
        if order == 'asc':
            query = query.order_by(schema.TOrder.id.asc())
        elif order == 'desc':
            query = query.order_by(schema.TOrder.id.desc())

        items = query.offset(item.page * item.page_size - item.page_size).limit(item.page_size).all()

        order_list: List[m_order.AReturnMsg] = [
            m_order.AReturnMsg(s_Order=m_schema.SOrder.parse_obj(item[0].__dict__) if item[0] else None,
                               s_User=m_schema.SUser.parse_obj(item[1].__dict__) if item[1] else None,
                               s_Good=m_schema.SGood.parse_obj(item[2].__dict__) if item[2] else None,
                               s_GoodType=m_schema.SGoodType.parse_obj(item[3].__dict__) if item[3] else None,
                               s_State=m_schema.SOrderState.parse_obj(item[4].__dict__ if item[4] else None),
                               s_PayChannel=m_schema.SPayChannel.parse_obj(item[5].__dict__) if item[5] else None,
                               s_Store=m_schema.SStore.parse_obj(item[6].__dict__) if item[6] else None,
                               s_StoreOwner=m_schema.SStoreOwner.parse_obj(item[7].__dict__) if item[7] else None,
                               s_GoodSupplier=m_schema.SSupplier.parse_obj(item[8].__dict__) if item[8] else None,
                               s_GoodSupplierOwner=m_schema.SSupplierOwner.parse_obj(item[9].__dict__)
                               if item[9] else None,
                               s_OrderReturn=m_schema.SOrderReturn.parse_obj(item[10].__dict__) if item[10] else None
                               ) for item in items]

        return m_order.AOrderMsgList(data=order_list, total=total_size)


async def get_total_income() -> int:
    with Dao() as db:
        total_income: int = db.query(func.sum(schema.TOrder.paid_amount)).scalar()
        if total_income is None:
            return 0
        else:
            return total_income


async def get_current_income() -> int:
    # 获取当日零时
    time_now = datetime.now()
    zero_today = time_now - timedelta(hours=time_now.hour, minutes=time_now.minute, seconds=time_now.second,
                                      microseconds=time_now.microsecond)

    with Dao() as db:
        current_income: int = db.query(func.sum(schema.TOrder.paid_amount)). \
            filter(schema.TOrder.paid_time > zero_today).scalar()
        if current_income is None:
            return 0
        else:
            return current_income


async def get_month_income() -> int:
    # 获取当月零时
    time_now = datetime.now()
    this_month_start = datetime(time_now.year, time_now.month, 1)
    with Dao() as db:
        month_income: int = db.query(func.sum(schema.TOrder.paid_amount)). \
            filter(schema.TOrder.paid_time > this_month_start).scalar()
        if month_income is None:
            return 0
        else:
            return month_income

def get_user_orders_count(user_id:int = 0):
    with Dao() as db:
        #1未发货,2已发货,7已签收,8已完结,9未使用,10已使用
        paid_num = 0
        paid_amound = db.query(func.sum(schema.TOrder.paid_amount))\
            .filter(schema.TOrder.paider_id == user_id)\
            .filter(schema.TOrder.status_id.in_([1,2,7,8,9,10])).scalar()
        if paid_amound is None:
            paid_amound =0
        paid_balance = db.query(func.sum(schema.TOrder.paid_balance))\
            .filter(schema.TOrder.paider_id == user_id)\
            .filter(schema.TOrder.status_id.in_([1,2,7,8,9,10])).scalar()
        if paid_balance is None:
            paid_balance = 0
        paid_lock_balance = db.query(func.sum(schema.TOrder.paid_lock_balance))\
            .filter(schema.TOrder.paider_id == user_id)\
            .filter(schema.TOrder.status_id.in_([1,2,7,8,9,10])).scalar()
        if paid_lock_balance is None:
            paid_lock_balance = 0
        paid_num = paid_amound + paid_balance + paid_lock_balance
        if paid_num is None:
            return 0
        else:
            return paid_num

def get_user_falsh_orders(flash_order_ids:list = []):
    with Dao() as db:
        res = db.query(schema.TOrderSource, schema.TOrder, schema.TGoodSpec)\
            .outerjoin(schema.TOrder, schema.TOrderSource.order_id == schema.TOrder.id)\
            .outerjoin(schema.TGoodSpec, schema.TOrder.spec_id == schema.TGoodSpec.id)\
            .filter(schema.TOrderSource.source_id.in_(flash_order_ids))\
            .filter(schema.TOrder.status_id.in_([1,2,9]))\
            .filter(schema.TOrder.is_assign_income==0).all()
        return res

def get_user_falsh_orders2(flash_order_ids:list = []):
    with Dao() as db:
        res = db.query(schema.TOrderSource, schema.TOrder, schema.TGoodSpec, schema.TGood)\
            .outerjoin(schema.TOrder, schema.TOrderSource.order_id == schema.TOrder.id)\
            .outerjoin(schema.TGoodSpec, schema.TOrder.spec_id == schema.TGoodSpec.id) \
            .outerjoin(schema.TGood, schema.TOrder.good_id == schema.TGood.id) \
            .filter(schema.TOrderSource.source_id.in_(flash_order_ids))\
            .filter(schema.TOrder.status_id.in_([1,2,9]))\
            .filter(schema.TOrder.is_assign_income==0).order_by(schema.TOrder.id.desc()).all()
        return res

def get_user_share_order(user_id:int):
    with Dao() as db:
        res = db.query(schema.TOrder, schema.TGood, schema.TGoodSpec) \
            .outerjoin(schema.TGood, schema.TOrder.good_id == schema.TGood.id) \
            .outerjoin(schema.TGoodSpec, schema.TOrder.spec_id == schema.TGoodSpec.id) \
            .filter(schema.TOrder.status_id.in_([1,2,9]))\
            .filter(schema.TOrder.recommender_id==user_id).all()
        return res

def get_user_willcomein_order(user_id:int):
    with Dao() as db:
        # .filter(schema.TOrder.is_wholesale.in_([0, 1])) \
        res = db.query(schema.TOrder, schema.TGood, schema.TGoodSpec) \
            .outerjoin(schema.TGood, schema.TOrder.good_id == schema.TGood.id) \
            .outerjoin(schema.TGoodSpec, schema.TOrder.spec_id == schema.TGoodSpec.id) \
            .filter(schema.TOrder.status_id.in_([1,2,9])) \
            .filter(schema.TOrder.is_assign_income == 0) \
            .filter(schema.TOrder.use_coin == 0) \
            .filter(or_(schema.TOrder.recommender_id==user_id, schema.TOrder.parent_uid==user_id, schema.TOrder.top_uid==user_id,\
                        schema.TOrder.invited_uid==user_id, schema.TOrder.supplier_uid==user_id, schema.TOrder.eqlevel_uid==user_id, schema.TOrder.random_fee_uid==user_id, schema.TOrder.tuan_uid==user_id, schema.TOrder.retuan_uid==user_id, schema.TOrder.random_invited_uid==user_id, schema.TOrder.ininvited_uid==user_id))\
            .order_by(schema.TOrder.id.desc()).all()
        return res

def get_user_invparent_order(user_ids:list):
    with Dao() as db:
        res = db.query(schema.TOrder, schema.TGood, schema.TGoodSpec) \
            .outerjoin(schema.TGood, schema.TOrder.good_id == schema.TGood.id) \
            .outerjoin(schema.TGoodSpec, schema.TOrder.spec_id == schema.TGoodSpec.id) \
            .filter(schema.TOrder.status_id.in_([1,2,9]))\
            .filter(schema.TOrder.paider_id.in_(user_ids)).all()
        return res

def get_user_introducer_order(user_id:int):
    with Dao() as db:
        res = db.query(schema.TOrder, schema.TGood, schema.TGoodSpec) \
            .outerjoin(schema.TGood, schema.TOrder.good_id == schema.TGood.id) \
            .outerjoin(schema.TGoodSpec, schema.TOrder.spec_id == schema.TGoodSpec.id) \
            .filter(schema.TOrder.status_id.in_([1,2,9]))\
            .filter(schema.TGood.introducer_id==user_id).all()
        return res

def get_out_trade_order(out_trade_no:str):
    with Dao() as db:
        res = db.query(schema.TOrder, schema.TGood, schema.TGoodSpec) \
            .outerjoin(schema.TGood, schema.TOrder.good_id == schema.TGood.id) \
            .outerjoin(schema.TGoodSpec, schema.TOrder.spec_id == schema.TGoodSpec.id) \
            .filter(schema.TOrder.status_id == 0,schema.TOrder.is_assign_income == 0)\
            .filter(schema.TOrder.out_trade_no==out_trade_no).all()
        return res

def get_out_trade_order(out_trade_no:str):
    with Dao() as db:
        res = db.query(schema.TOrder, schema.TUser) \
            .outerjoin(schema.TUser, schema.TOrder.paider_id == schema.TUser.id) \
            .filter(schema.TOrder.out_trade_no==out_trade_no).all()
        return res

def assign_income_order(data: schema.TOrder):
    if data.status_id is None:
        data.status_id = 8
    with Dao() as db:
        db.query(schema.TOrder).filter(schema.TOrder.id == data.id).update({
            "complete_time": data.complete_time,
            "is_assign_income": data.is_assign_income,
            # "status_id": data.status_id,
            "detail": data.detail
        })
        db.commit()

def assign_income_order2(data: schema.TOrder):
    if data.status_id is None:
        data.status_id = 8
    with Dao() as db:
        db.query(schema.TOrder).filter(schema.TOrder.id == data.id).update({
            "complete_time": data.complete_time,
            "status_id": data.status_id
        })
        db.commit()

def assign_income_pifaorder(data: schema.TOrder):
    with Dao() as db:
        db.query(schema.TOrder).filter(schema.TOrder.id == data.id).update({
            "complete_time": data.complete_time,
            "is_assign_income": data.is_assign_income,
            "detail": data.detail
        })
        db.commit()

def update_order_source(order: schema.TOrder):
    #for order in data:
    good_num = order.number
    with Dao() as db:
        flash_order = db.query(schema.TFlashOrder, schema.TPackage, schema.TGood, schema.TGoodSpec).outerjoin(schema.TPackage, schema.TFlashOrder.package_id == schema.TPackage.id) \
            .outerjoin(schema.TGood, schema.TPackage.good_id == schema.TGood.id) \
            .outerjoin(schema.TGoodSpec, schema.TFlashOrder.spec_id == schema.TGoodSpec.id) \
            .filter(schema.TFlashOrder.spec_id == order.spec_id, schema.TFlashOrder.status.in_([2, 4])).order_by(schema.TFlashOrder.sold.asc()).all()
            #.filter(schema.TFlashOrder.spec_id == order.spec_id, schema.TFlashOrder.status.in_([2,4])).order_by(schema.TFlashOrder.put_on_time.asc()).all()

        for forder, fpackage, fgood, fgoodspec in flash_order:
            if good_num > 0:
                account_info = {"user_id": forder.user_id, "change":0, "good_num":0}
                #是否整份代卖
                if forder.sold is None:
                    forder.sold = 0
                if forder.single_status is None:
                    forder.single_status = 0
                if forder.single_status > 0:
                    if good_num >= fpackage.amount:
                        #添加订单来源
                        add_order_source(AddOrderSource(order_id=order.id, source_id=forder.id, amount=fpackage.amount, create_time=datetime.now(), order_user_id=order.paider_id, package_user_id=forder.user_id))
                        #更新秒杀包订单数量和状态
                        d_flash_order_return.sell_flash_order(forder.id, fpackage.amount, 7)
                        good_num = good_num - fpackage.amount
                        account_info['change'] = fpackage.flash_sale_price * fpackage.amount
                        account_info['good_num'] = fpackage.amount
                else:
                    flash_order_num = fpackage.amount - forder.sold - forder.return_sold
                    if good_num >= flash_order_num:
                        #添加订单来源
                        add_order_source(AddOrderSource(order_id=order.id, source_id=forder.id, amount=flash_order_num, create_time=datetime.now(), order_user_id=order.paider_id, package_user_id=forder.user_id))
                        #更新秒杀包订单数量和状态
                        d_flash_order_return.sell_flash_order(forder.id, fpackage.amount, 7)
                        good_num = good_num - flash_order_num
                        account_info['change'] = fpackage.flash_sale_price * flash_order_num
                        account_info['good_num'] = flash_order_num
                    else:
                        #添加订单来源
                        add_order_source(AddOrderSource(order_id=order.id, source_id=forder.id, amount=good_num, create_time=datetime.now(), order_user_id=order.paider_id, package_user_id=forder.user_id))
                        #更新秒杀包订单数量和状态
                        d_flash_order_return.sell_flash_order(forder.id, forder.sold + good_num)
                        account_info['change'] = fpackage.flash_sale_price * good_num
                        account_info['good_num'] = good_num
                        good_num = 0

                #更新秒杀用户收益
                user_account_info = d_account.get_account_info_add(account_info['user_id'])
                if account_info['change'] > 0:
                    total_balance = user_account_info.balance + account_info['change']
                    d_account.update_account_by_id(user_account_info.id, {"balance": total_balance})
                    d_account.add_balance(m_account.BalanceModel(
                        user_id=account_info['user_id'],
                        change=account_info['change'],
                        balance=total_balance,
                        type=global_define.balance_type[26],
                        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        good_id=str(fgood.id),
                        good_title=str(fgood.title),
                        good_num=str(account_info['good_num']),
                        out_trade_no=order.out_trade_no
                    ))
    #秒杀包商品订购完，下单平台商品
    if good_num > 0:
        add_order_source(AddOrderSource(order_id=order.id, source_id=-1, amount=good_num, create_time=datetime.now(), order_user_id=order.paider_id, package_user_id=-1))
        good_num = 0
    # 更新商品库存
    #d_good.update_good_stock(order.good_id, order.spec_id, good_num)

def add_order_source(data: AddOrderSource):
    re_id = 0
    with Dao() as db:
        add_data = schema.TOrderSource(
            order_id=data.order_id,
            source_id=data.source_id,
            amount=data.amount,
            create_time=data.create_time,
            order_user_id=data.order_user_id,
            package_user_id=data.package_user_id
        )
        db.add(add_data)
        db.flush()
        re_id = add_data.id
        db.commit()
    return re_id

def get_order_source(order_id:int):
    with Dao() as db:
        return db.query(schema.TOrderSource).filter(schema.TOrderSource.order_id == order_id).all()

def get_order_stats(user_id: int):
    with Dao() as db:
        return db.query(schema.TOrder.status_id, func.count(1).label("num"), schema.TOrderState.state).outerjoin(schema.TOrderState, schema.TOrder.status_id == schema.TOrderState.id)\
                .group_by(schema.TOrder.status_id).filter(schema.TOrder.paider_id == user_id).all()

def get_order_source_for_user(source_ids:list):
    with Dao() as db:
        return db.query(schema.TOrderSource, schema.TOrder, schema.TFlashOrder, schema.TUser, schema.TPackage, schema.TGoodSpec, schema.TGood)\
                .outerjoin(schema.TOrder, schema.TOrderSource.order_id==schema.TOrder.id) \
                .outerjoin(schema.TFlashOrder, schema.TOrderSource.source_id == schema.TFlashOrder.id) \
                .outerjoin(schema.TUser, schema.TOrder.paider_id == schema.TUser.id)\
                .outerjoin(schema.TPackage, schema.TFlashOrder.package_id == schema.TPackage.id)\
                .outerjoin(schema.TGoodSpec, schema.TOrder.spec_id == schema.TGoodSpec.id) \
                .outerjoin(schema.TGood, schema.TGood.id == schema.TOrder.good_id) \
            .filter(schema.TOrderSource.source_id.in_(source_ids)).order_by(schema.TOrderSource.id.desc()).all()

def del_cart(item: list):
    with Dao() as db:
        db.query(schema.TCart).filter(schema.TCart.id.in_(item)).delete()
        db.commit()

def update_cart_amount(user_id:int, cart_id:int, amount:int, update_state:str):
    with Dao() as db:
        cart_info = db.query(schema.TCart).filter(schema.TCart.id==cart_id, schema.TCart.user_id==user_id).first()
        if cart_info:
            if cart_info.amount is None:
                cart_info.amount = 0
            if update_state == "dec":
                cart_info.amount -= amount
            else:
                cart_info.amount += amount

            if cart_info.amount <= 0:
                db.query(schema.TCart).filter(schema.TCart.id==cart_id, schema.TCart.user_id==user_id).delete()
            db.commit()
        else:
            return False
    return True

def insert_exportfile(items: m_schema.CreateExportFile):
    add_instance = schema.TExportFile(
        user_id=items.user_id,
        export_url=items.export_url,
        type=items.type,
        description=items.description,
        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    )
    with Dao() as db:
        db.add(add_instance)
        db.commit()

def search_exportfile(items: m_order.SearchExportFile):
    with Dao() as db:
        query = db.query(schema.TExportFile)

        if items.user_id is not None:
            query = query.where(schema.TExportFile.user_id == items.user_id)
        if items.type is not None:
            query = query.where(schema.TExportFile.type == items.type)
        if items.time_start is not None:
            query = query.where(schema.TExportFile.create_time >= datetime.fromtimestamp(int(items.time_start)))
        if items.time_end is not None:
            query = query.where(schema.TExportFile.create_time <= datetime.fromtimestamp(int(items.time_end)))

        total_size = query.count()
        if items.order == 'asc':
            query = query.order_by(schema.TExportFile.id.asc())
        elif items.order == 'desc':
            query = query.order_by(schema.TExportFile.id.desc())

        items = query.offset(items.page * 20 - 20).limit(20).all()
        return {"data": items, "total": total_size}

def get_import_order(id:int, consignee_name:str, consignee_phone:str):
    with Dao() as db:
        return db.query(schema.TOrder).filter(schema.TOrder.id == id, schema.TOrder.consignee_name == consignee_name, schema.TOrder.consignee_phone == consignee_phone,\
                                              schema.TOrder.status_id == 1).first()

def create_export_content(data_d:list):
    re_content = ""
    for i in data_d:
        d = dict(i)
        if d['s_Order'] is None or d['s_Good'] is None:
            continue
        if d['s_Order'].paid_amount is None:
            d['s_Order'].paid_amount = 0
        if d['s_Order'].paid_balance is None:
            d['s_Order'].paid_balance = 0
        if d['s_Order'].delivery_fee is None:
            d['s_Order'].delivery_fee = 0
        if d['s_Order'].sale_price is None:
            d['s_Order'].sale_price = 0
        consignee_province = ""
        consignee_city = ""
        consignee_area = ""
        consignee_description = ""
        consignee_name = ""
        if d['s_Order'].consignee_province is not None:
            consignee_province = str(d['s_Order'].consignee_province)
        if d['s_Order'].consignee_city is not None:
            consignee_city = str(d['s_Order'].consignee_city)
        if d['s_Order'].consignee_area is not None:
            consignee_area = str(d['s_Order'].consignee_area)
        if d['s_Order'].consignee_description is not None:
            consignee_description = str(d['s_Order'].consignee_description)
        if d['s_Order'].consignee_name is not None:
            consignee_name = str(d['s_Order'].consignee_name)
        address = consignee_province + consignee_city + consignee_area
        re_content += ','.join([str(d['s_Order'].id), str(d['s_Order'].create_time), str(d['s_Order'].paider_id), '', '',
                             str(round(d['s_Order'].delivery_fee / 100, 2)), str(round((d['s_Order'].paid_amount + d['s_Order'].paid_balance) / 100, 2)), \
                             consignee_name, str(d['s_Order'].consignee_phone),
                             consignee_province, consignee_city,
                             consignee_area, str(address + consignee_description), \
                             str(d['s_Order'].good_id), str(d['s_Good'].title),
                             # "/".join([str(d['s_GoodSpec'].value), str(d['s_GoodSpec'].spec_num)]),
                             # str(d['s_Order'].number), str(round(d['s_Order'].sale_price / 100, 2)), str(d['s_Order'].status_id), str(d['s_GoodSpec'].spec_num)])
                             str(d['s_Order'].number), str(round(d['s_Order'].sale_price / 100, 2)), str(d['s_Order'].status_id)])
        re_content += '\r\n'
    return re_content

def get_tuan_pifaorder_count(user_ids: list):
    with Dao() as db:
        return db.query(schema.TOrder).filter(schema.TOrder.paider_id.in_(user_ids)).count()

def update_order_detail(order_id:int, detail:str):
    with Dao() as db:
        cart_info = db.query(schema.TOrder).filter(schema.TOrder.id==order_id).first()
        if cart_info:
            cart_info.user_detail = detail
            db.commit()
            return True
        else:
            return False

def update_order_detail_tut(order_id:int, detail:str):
    with Dao() as db:
        cart_info = db.query(schema.TOrder).filter(schema.TOrder.id==order_id).first()
        if cart_info:
            cart_info.detail_tut = detail
            db.commit()
            return True
        else:
            return False

def get_baodan_order_count(user_id:int):
    with Dao() as db:
        rescount = db.query(schema.TOrder, schema.TGood) \
            .outerjoin(schema.TGood, schema.TOrder.good_id == schema.TGood.id) \
            .filter(schema.TOrder.paider_id == user_id)\
            .filter(schema.TGood.type == 1).filter(schema.TOrder.status_id >= 1).count()
        return rescount

def get_baodan_order_count_for_users(user_ids:list):
    with Dao() as db:
        rescount = db.query(schema.TOrder, schema.TGood)\
            .outerjoin(schema.TGood, schema.TOrder.good_id == schema.TGood.id)\
            .filter(schema.TOrder.paider_id.in_(user_ids))\
            .filter(schema.TGood.type == 1).filter(schema.TOrder.status_id >= 1).count()
        return rescount

#获取用户报单产品，订单金额
def get_user_bdorders_paidsum(user_ids:list):
    with Dao() as db:
        paid_balance = db.query(func.sum(schema.TOrder.paid_balance)) \
            .outerjoin(schema.TGood, schema.TOrder.good_id == schema.TGood.id)\
            .filter(schema.TOrder.status_id.in_(user_ids))\
            .filter(schema.TGood.type == 1).filter(schema.TOrder.status_id >= 1).scalar()
        paid_amound = db.query(func.sum(schema.TOrder.paid_amount)) \
            .outerjoin(schema.TGood, schema.TOrder.good_id == schema.TGood.id)\
            .filter(schema.TOrder.status_id.in_(user_ids))\
            .filter(schema.TGood.type == 1).filter(schema.TOrder.status_id >= 1).scalar()
        if paid_balance is None:
            paid_balance = 0
        if paid_amound is None:
            paid_amound = 0
        return {'paid_amound':paid_amound, 'paid_balance':paid_balance}

#密卡查询
def get_bagpass_for_pass(pass_num:str):
    with Dao() as db:
        rs = db.query(schema.TBagPas, schema.TBagCagegory, schema.TBigorderInitbag) \
            .outerjoin(schema.TBagCagegory, schema.TBagCagegory.id == schema.TBagPas.pc_id) \
            .outerjoin(schema.TBigorderInitbag, schema.TBigorderInitbag.id == schema.TBagCagegory.bag_id) \
            .filter(schema.TBagPas.pass_num == pass_num).first()
        return rs

def get_order_data(order_id:int):
    with Dao() as db:
        return db.query(schema.TOrder).filter(schema.TOrder.id == order_id).first()

def get_findall_second_num(all_str:str, key_str:str):
    re_val = 0
    second_index = all_str.find(key_str, all_str.find(key_str)+1)
    if second_index > 0:
        second_str = all_str[second_index:second_index+10]
        try:
            re_val = int(re.findall(r'\d+', second_str)[0])
        except:
            pass
    return re_val



def add_order_and_balance(good_id:int, user_id:int, address_id:int, recharge_user_id:int):
    #good_info[0]['TGood']
    #good_info[0]['TGoodCategory']
    #good_info[0]['TGoodRule']
    #good_info[0]['TGoodText']
    #good_info[0]['TSupplier']
    good_info = d_good.get_good_data(good_id)
    user_info = d_user.get_user_by_id(user_id)  #码主任信息
    # task_info = d_video_task.get_video_task(task_id)
    address = d_address.get_address_by_id(address_id)
    recharge_user_info = d_user.get_user_by_id(recharge_user_id)   #激活人信息
    if not good_info or not user_info or not address or not recharge_user_info:
        raise HTTPException(400, "数据错误")
    zdyspec = str(good_info.zdyspec)
    out_trade_no = f"{int(time.time())}{user_id:08d}{uuid.uuid4().hex[-4:]}"
    spec_price = get_findall_second_num(zdyspec, '售价') * 100
    # try:
    #     spec_price = float(json.loads(zdyspec)['售价']) * 100
    # except:
    #     pass
    memeber_price = get_findall_second_num(zdyspec, '会员价') * 100
    zhitui = get_findall_second_num(zdyspec, '直推') * 100
    jiantui = get_findall_second_num(zdyspec, '间推') * 100
    # fenxiang = get_findall_second_num(zdyspec, '分享') * 100
    # fenxiang_jiantui = get_findall_second_num(zdyspec, '分享推') * 100
    jihuo = get_findall_second_num(zdyspec, '激活') * 100
    this_tuan_fee = get_findall_second_num(zdyspec, '推团') * 100
    this_retuan_fee = get_findall_second_num(zdyspec, '间团') * 100
    supplier_fee = get_findall_second_num(zdyspec, '供货') * 100
    coin_fee = get_findall_second_num(zdyspec, '购券') * 100
    live_fee = 0
    share_tui = get_findall_second_num(zdyspec, '分享') * 100
    share_midd_tui = get_findall_second_num(zdyspec, '分享推') * 100
    # invited_uid = invited_uid,
    # invited_two_uid = middle_invited_id,
    # tuan_uid = tuan_uid,
    # retuan_uid = retuan_uid,
    # share_invited_uid = item.recommender_id,
    # share_invited_two_uid = middle_recommender_id
    # jihuo_uid = 0
    invited_user_id = 0
    invited_user_two_id = 0
    tuan_uid = 0
    retuan_uid = 0
    jihuo_uid = recharge_user_id
    live_uid = 0

    #激活奖
    if jihuo > 0:
        d_balance.invited_user_money(user_info.id, jihuo, global_define.balance_type[34], good_info.id, f"{good_info.id}|{good_info.title}", 1, out_trade_no)
    #购物券
    if coin_fee > 0:
        d_balance.invited_user_coin(recharge_user_id, coin_fee, global_define.balance_type[49], good_info.id, f"{good_info.id}|{good_info.title}", 1, out_trade_no)

    # 直推级奖
    if recharge_user_info.invited_user_id is None:
        recharge_user_info.invited_user_id = 0
    if zhitui > 0 and recharge_user_info.invited_user_id > 0:
        parent_info = d_user.get_user_by_id(recharge_user_info.invited_user_id)
        if parent_info:
            #直推收益
            invited_user_id = user_info.invited_user_id
            d_balance.invited_user_money(parent_info.id, zhitui, global_define.balance_type[33], good_info.id, f"{good_info.id}|{good_info.title}", 1, out_trade_no)

            #间推收益
            if parent_info.invited_user_id is None:
                parent_info.invited_user_id = 0
            if jiantui > 0 and parent_info.invited_user_id > 0:
                parent_parent_info = d_user.get_user_by_id(parent_info.invited_user_id)
                if parent_parent_info:
                    invited_user_two_id = parent_info.invited_user_id
                    d_balance.invited_user_money(parent_info.id, zhitui, global_define.balance_type[45], good_info.id,\
                                                 f"{good_info.id}|{good_info.title}", 1, out_trade_no)

    # 团长分配收益
    if this_tuan_fee > 0:
        if user_info.is_tuan > 0:
            retuan_uid = recharge_user_info.tuan_id
            d_balance.invited_user_money(recharge_user_info.id, this_tuan_fee, global_define.balance_type[37], good_info.id, \
                                         f"{good_info.id}|{good_info.title}", 1, out_trade_no)
        else:
            if recharge_user_info.tuan_id > 0:
                tuan_info = d_user.get_user_by_id(recharge_user_info.tuan_id)
                retuan_uid = tuan_info.tuan_id
                d_balance.invited_user_money(recharge_user_info.tuan_id, this_tuan_fee, global_define.balance_type[37], good_info.id, \
                                             f"{good_info.id}|{good_info.title}", 1, out_trade_no)

        # 间推团长分配收益
        midd_tuan_info = d_user.get_user_by_id(retuan_uid)
        if midd_tuan_info and this_retuan_fee > 0:
            d_balance.invited_user_money(midd_tuan_info.id, this_retuan_fee, global_define.balance_type[38], good_info.id, \
                                         f"{good_info.id}|{good_info.title}", 1, out_trade_no)
            #
            # if midd_tuan_info.tuan_id > 0 and this_retuan_fee > 0:
            #     midd_tuan_account = d_account.get_account_info_add(midd_tuan_info.tuan_id)
            #     if midd_tuan_account:
            #         supplier_income = this_retuan_fee * 1
            #         retuan_uid = midd_tuan_account.id
            #         if midd_tuan_account.balance is None:
            #             midd_tuan_account.balance = 0
            #         total_balance = midd_tuan_account.balance + supplier_income
            #         d_account.update_account_by_id(midd_tuan_account.id, {"balance": total_balance})
            #         d_account.add_balance(m_account.BalanceModel(
            #             user_id=midd_tuan_account.tuan_id,
            #             change=supplier_income,
            #             balance=total_balance,
            #             type=global_define.balance_type[38],
            #             create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            #             good_id=str(good_info.id),
            #             good_title=good_info.title,
            #             good_num='1',
            #             out_trade_no=out_trade_no
            #         ))

    # 供货分配收益
    # if supplier_info.supplier_uid > 0 and supplier_fee > 0:
    #     supplier_info = d_account.get_account_info_add(supplier_info.supplier_uid)
    #     if supplier_info:
    #         supplier_income = supplier_fee * 1
    #         if supplier_info.balance is None:
    #             supplier_info.balance = 0
    #         total_balance = supplier_info.balance + supplier_income
    #         d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
    #         d_account.add_balance(m_account.BalanceModel(
    #             user_id=supplier_info.tuan_id,
    #             change=supplier_income,
    #             balance=total_balance,
    #             type=global_define.balance_type[39],
    #             create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    #             good_id=str(good_info.id),
    #             good_title=good_info.title,
    #             good_num='1',
    #             out_trade_no=out_trade_no
    #         ))

    # 居间收益
    if good_info.live_mid_uid > 0 and good_info.live_mid_money > 0:
        live_uid = good_info.live_mid_uid
        live_fee = good_info.live_mid_money
        live_mid_uinfo = d_user.get_user_by_id(good_info.live_mid_uid)
        d_balance.invited_user_money(live_mid_uinfo.id, good_info.live_mid_money, global_define.balance_type[47], good_info.id, f"{good_info.id}|{good_info.title}")

    now_time = datetime.now()
    insert_order = schema.TOrder(
        good_id=good_id,
        paider_id=user_id,
        sale_price=spec_price,
        create_time=datetime.now(),
        status_id=1,
        number=1,
        consignee_name=address.consignee if address else None,
        consignee_province=address.province if address else None,
        consignee_city=address.city if address else None,
        consignee_area=address.area if address else None,
        consignee_street=address.street if address else None,
        consignee_description=address.description if address else None,
        consignee_phone=address.phone if address else None,
        paid_coin=0,
        paid_lock_balance=0,
        paid_balance=0,
        paid_amount=spec_price,
        out_trade_no=out_trade_no,
        # recommender_id=data.recommender_id,
        detail=f"[good_id:{good_id}, user_id:{user_id}, address_id:{address_id}, recharge_user_id:{recharge_user_id}#{now_time}#推荐：{zhitui}#间推：{jiantui}#激活:{jiantui}#团长：{this_tuan_fee}#间团：{this_retuan_fee}#居间：{good_info.live_mid_money}]",
        # parent_uid = comein_users['parent_uid'],
        # top_uid=comein_users['top_uid'],
        invited_uid=invited_user_id,
        invited_two_uid=invited_user_two_id,
        # use_balance=data.use_balance,
        use_coin=0,
        # user_detail=data.user_detail,
        # random_fee_uid = random_fee_id,
        # delivery_fee = delivery_fee,
        # eqlevel_uid=comein_users['eqlevel_uid'],
        # good_option_id = item.good_option_id,
        # good_option_name = item.good_option_name,
        # user_detail = item.user_detail,
        # random_fee_uid = random_fee_id,
        zdyspec=zdyspec,
        zdyspec_good=zdyspec,
        zdyspec_good_index=0,
        tuan_uid = tuan_uid,
        retuan_uid = retuan_uid,
        # random_invited_uid = random_invited_id,
        act_uid=recharge_user_id,
        # isfirst=1
        is_video=1,
        live_mid_uid=live_uid,
        live_mid_money=live_fee
    )
    with Dao() as db:
        db.add(insert_order)
        db.commit()
