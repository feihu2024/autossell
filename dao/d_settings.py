import datetime,time
from common import Dao
from model import schema
from model import m_schema
from router import r_schema
from typing import List, Optional
from sqlalchemy import text
from pydantic import BaseModel, Field

# class CreateCity(BaseModel):
#     recommend_num: Optional[int] = Field(title='定义推荐系升级人数')
#     flash_order_income: Optional[float] = Field(title='定义秒杀产品24小时停留收益比千分之')
#     tuan_order_income: Optional[float] = Field(title='定义团长秒杀产品收益比（千分之）')
#     flash_order_max: Optional[int] = Field(title='秒杀用户持单量限制(未完成出售订单)')
#


def update_settings(data: dict):
    with Dao() as db:
        db.query(schema.TSetting).update(data)
        db.commit()

def get_settings():
    with Dao() as db:
        return db.query(schema.TSetting).first()

def get_city_by_id(cid: int):
    with Dao() as db:
        return db.query(schema.TCity).filter(schema.TCity.id == cid).first()

def get_city_tops():
    with Dao() as db:
        return db.query(schema.TCity).filter(schema.TCity.parid == 0).all()

def get_city_subs(parid:int):
    with Dao() as db:
        return db.query(schema.TCity).filter(schema.TCity.parid == parid).all()

def get_city_by_name(cname:str):
    with Dao() as db:
        return db.query(schema.TCity).filter(schema.TCity.cname == cname).first()

def insert_city(data:m_schema.CreateCity):
    with Dao() as db:
        db.add(schema.TCity(
            cname=data.cname,
            parid=data.parid,
            status=data.status
        ))
        db.commit()

def update_city_cname(data:m_schema.SCity):
    with Dao() as db:
        db.query(schema.TCity).filter(schema.TCity.id == data.id).update({"cname":data.cname})
        db.commit()