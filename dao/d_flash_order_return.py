from common import Dao, global_define
from model.schema import TFlashOrderReturn, TFlashOrder, TPackageOrderStatus
from typing import List, Optional
from pydantic import BaseModel, Field
#import time, datetime
from datetime import datetime
from sqlalchemy import func

class flash_order_return(BaseModel):
    id: Optional[int] = Field(None, title='修改数据时使用')
    user_id: Optional[int] = Field(None, title='关联t_user表id')
    income_days: Optional[int] = Field(None, title='剩余秒杀退货收益天数')
    latest_time: Optional[datetime] = Field(None, title='最近一次退货时间')
    latest_income_user: Optional[int] = Field(None, title='最近一次退货收益')
    latest_income_layer: Optional[int] = Field(None, title='最近一次退货层级收益')
    latest_income_toper: Optional[int] = Field(None, title='最近一次退货见点收益')
    latest_income_groupsir: Optional[int] = Field(None, title='最近一次退货团长收益')

class FlashOrderReturn(BaseModel):
    flash_order_id: Optional[int] = Field(0, title='退货订单id')
    user_id: Optional[int] = Field(None, title='退货订单用户id')
    total_price: Optional[int] = Field(None, title='退货订单价格')

def insert_flash_order_return(data: TFlashOrderReturn):
    with Dao() as db:
        db.add(data)
        db.commit()

def get_flash_order_return(user_id:int = 0):
    with Dao() as db:
        order_info = db.query(TFlashOrderReturn).filter(TFlashOrderReturn.user_id == user_id).first()
        if not order_info:
            insert_data = TFlashOrderReturn(
                user_id=user_id,
                income_days=global_define.setting_orders['return_flash_order_income_days']
            )
            insert_flash_order_return(insert_data)
            db.flush()
            db.commit()
            order_info = db.query(TFlashOrderReturn).filter(TFlashOrderReturn.user_id == user_id).first()
        return order_info

def reduce_flash_order_return(user_id:int = 0):
    info = get_flash_order_return(user_id)
    with Dao() as db:
        db.query(TFlashOrderReturn).filter(TFlashOrderReturn.id == info.id).update({
            "income_days":info.income_days - 1,
            "latest_time":datetime.now()
        })
        db.commit()

def get_flash_order(order_id:int = 0, user_id:int = 0):
    with Dao() as db:
        if user_id > 0:
            return db.query(TFlashOrder).filter(TFlashOrder.id == order_id, TFlashOrder.user_id == user_id).first()
        else:
            return db.query(TFlashOrder).filter(TFlashOrder.id == order_id).first()

def finish_flash_order(data: TFlashOrder):
    with Dao() as db:
        db.query(TFlashOrder).filter(TFlashOrder.id == data.id).update({
            "status":data.status,  #已退货
            "complete_time": data.complete_time,
            "is_assign_income": data.is_assign_income,
            "detail": data.detail
        })
        db.commit()

def sell_flash_order(order_id:int, sell_num:int, sell_status:int = -1):
    update_data = {}
    if sell_status == 7:  #已出售完
        update_data = {"sold": sell_num, "status":7, "complete_time":datetime.now()}
    elif sell_status == -1:
        update_data = {"sold": sell_num}
    else:
        update_data = {"sold": sell_num, "status":sell_status}
    with Dao() as db:
        db.query(TFlashOrder).filter(TFlashOrder.id == order_id).update(update_data)
        db.commit()

def get_flash_order_stats(user_id: int):
    with Dao() as db:
        return db.query(TFlashOrder.status, func.count(1).label("num"), TPackageOrderStatus.title).outerjoin(TPackageOrderStatus, TFlashOrder.status == TPackageOrderStatus.id)\
                .group_by(TFlashOrder.status).filter(TFlashOrder.user_id == user_id).all()

