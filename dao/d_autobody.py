from common import Dao, global_define
from model.schema import *
from model.m_schema import *
from sqlalchemy import or_, and_, func
from typing import List, Optional
from sqlalchemy import text
import datetime, time, sys, math, json, redis
from pydantic import BaseModel, Field
from fastapi.exceptions import HTTPException
from dao import d_user, d_db, d_account, d_good, d_order, d_bigorder, d_balance

import logging

#
# class SearchVideoTask(BaseModel):
#     user_id: Optional[int] = Field(None,title='关联t_user表id')
#     # description: Optional[str] = Field(None,title='资金备注，团长收益这里是逗号分隔的订单id')
#     # create_time: Optional[str] = Field(None,title='时间段：time1,time2')
#     good_id: Optional[int] = Field(None, title='礼包筛选')
#     video_level: Optional[int] = Field(None, title='视频分发身份0达人,1店长,2服务商,3分公司')
#     is_act: Optional[int] = Field(None, title='是否被激活,0未激活,1已激活')
#     page: int = Field(1, title='当前页码，默认第1页')
#     page_size: int = Field(20, title='返回每页数据，默认每页20条数据')
#
# class ActModel(BaseModel):
#     user_id: Optional[int] = Field(0,title='激活用户id')
#     act_code: Optional[str] = Field(None, title='激活码')
#     address_id: Optional[int] = Field(0, title='地址id')
#
# class PicModel(BaseModel):
#     task_id: Optional[int] = Field(None,title='任务id')
#     receive_id: Optional[int] = Field(None, title='领取任务id')
#     up_pic: Optional[str] = Field(None, title='任务上传截图')
#
# class AuditModel(BaseModel):
#     video_id: Optional[int] = Field(None, title='视频任务id')
#     receive_id: Optional[int] = Field(None, title='领取视频任务id')
#     audit: Optional[int] = Field(None, title='0未审核,1通过审核,2未通过')
#     # audit_time '审核时间',
#     audit_adm: Optional[int] = Field(None, title='审核管理人id')
#     audit_info: Optional[str] = Field(None, title='审核备注100个汉字以内')

def close_autobody(at_id:int):
    with Dao() as db:
        db.query(TAutobody).filter(TAutobody.id == at_id).update({"stat": 1})
        db.commit()

def open_autobody(at_id:int):
    with Dao() as db:
        db.query(TAutobody).filter(TAutobody.id == at_id).update({"stat": 0})
        db.commit()

def del_autobody(at_id:int):
    with Dao() as db:
        db.query(TAutobody).filter(TAutobody.id == at_id).update({"stat": 1, "del_stat": 1})
        db.commit()

def update_autobody_order(at_id:int, order_id:int):
    with Dao() as db:
        db.query(TAutobody).filter(TAutobody.id == at_id).update({"order_id": order_id})
        db.commit()

def get_autobody_list(page:int = 1):
    re_val = {"data": 0, "total": 0}
    with Dao() as db:
        query = db.query(TAutobodyType)
        re_val["total"] = query.count()
        re_val["data"] = query.offset(page * 20 - 20).limit(20).all()

    return re_val

def get_autobody_by_id(body_id: int):
    with Dao() as db:
        return db.query(TAutobody).where(TAutobody.id == body_id).first()

def search_autobody_by_tag_title(search_str:str, page:int = 1):
    result_rs = {}
    with Dao() as db:
        search_rs = db.query(TAutobody).filter(or_(TAutobody.auto_tag.like(f'%{search_str}%'), TAutobody.at_name.like(f'%{search_str}%')))
        result_rs['toal'] = search_rs.count()
        result_rs['data'] = search_rs.order_by(TAutobody.id.desc()).offset(page * 20 - 20).limit(20).all()
        return result_rs