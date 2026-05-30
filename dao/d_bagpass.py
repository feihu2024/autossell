from common import Dao, global_define
from model.schema import TBigorderSet, TBigorderTwo, TUser, TBagPas, TBagCagegory
from sqlalchemy import or_, and_, func
from typing import List, Optional
from sqlalchemy import text
import datetime, time, sys, math, json, redis
from pydantic import BaseModel, Field
from fastapi.exceptions import HTTPException
from dao import d_user, d_db, d_account
from model.mall import m_account
import logging


class SearchBalance(BaseModel):
    user_id: Optional[int] = Field(None,title='关联t_user表id')
    type: Optional[str] = Field(None,title='资金类型：1:层级收益,2:见点收益,3:推荐收益,4:团长收益,5:管理变动收益')
    description: Optional[str] = Field(None,title='资金备注，团长收益这里是逗号分隔的订单id')
    create_time: Optional[str] = Field(None,title='时间段：time1,time2')
    is_comein: Optional[int] = Field(None, title='收入(1)/支出(0)')
    # admin_id: Optional[int] = Field(None, title='商家管理id')
    page: int = Field(1, title='当前页码，默认第1页')
    page_size: int = Field(20, title='返回每页数据，默认每页20条数据')

#查找卡密列表是否创建了某个批次
def find_pc(pc_id: int = 0):
    with Dao() as db:
        return db.query(TBagPas).where(TBagPas.pc_id == pc_id).first()

def find_pc_for_num(pc_id: str):
    with Dao() as db:
        return db.query(TBagPas).where(TBagPas.pass_num == pc_id).first()

# def insert_bagpass()
def insert_bagpass(bag_data: TBagCagegory):
    with Dao() as db:
        db.add(bag_data)
        db.commit()
        db.refresh(bag_data)
        return bag_data

def insert_bagpass_list(bag_data: TBagPas):
    with Dao() as db:
        db.add(bag_data)
        db.commit()
        db.refresh(bag_data)
        return bag_data

def bagpass_active(bagpass_id: int, user_id:int):
    with Dao() as db:
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        db.query(TBagPas).where(TBagPas.pass_num == bagpass_id).update({"stat": 1,"startime": now_time,"user_id": user_id})
        db.commit()