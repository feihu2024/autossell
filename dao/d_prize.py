import datetime, time
from common import Dao, global_define
from model import schema
from router import r_schema
from pydantic import BaseModel, Field
from typing import List, Optional


class TPrize(BaseModel):
    user_id: Optional[int] = Field(None, title='提交人id')
    status: Optional[int] = Field(None, title='获奖标识')

class TPrizelist(TPrize):
    page: Optional[int] = Field(1, title='页码')
    page_size: Optional[int] = Field(10, title='每页条数')

class update_balan_model(BaseModel):
    user_ids: Optional[str] = Field(None, title='以逗号分隔的用户id(1,2,3,4)')
    type: Optional[int] = Field(None, title='类型：1表示增加余额，2表示增加购物券')
    add_count: Optional[int] = Field(None, title='增加数量（分）')
    manager_id:Optional[int] = Field(None, title='操作管理员id')

def insert_prize(data: TPrize):
    tprize = schema.TPrize(
        user_id=data.user_id,
        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        status=data.status
    )
    with Dao() as db:
        db.add(tprize)
        db.commit()
        db.refresh(tprize)

def is_prize(data:TPrizelist):
    is_val = True
    with Dao() as db:
        query = db.query(schema.TPrize).filter(schema.TPrize.user_id == data.user_id, schema.TPrize.status == data.status).first()
        if not query:
            is_val = False
    return is_val


def search_prize(data:TPrizelist):
    with Dao() as db:
        query = db.query(schema.TPrize)
        if data.status is None:
            query = query.filter(schema.TPrize.user_id == data.user_id)
        else:
            query = query.filter(schema.TPrize.user_id == data.user_id, schema.TPrize.status == data.status)
        query = query.order_by(schema.TPrize.id.desc())
        query = query.offset((data.page - 1) * data.page_size).limit(data.page_size)
        items = query.all()
        count = query.count()
        return {"total": count, "data": items}

#分页展示
# def get_filter(user_id=None, phone=None, page: int = 1, page_size: int = 10):
#     with Dao() as db:
#         query = db.query(schema.TComment)
#         if user_id is not None:
#             query = query.filter(schema.TComment.user_id == user_id)
#         if phone is not None:
#             query = query.filter(schema.TComment.phone == phone)
#         query = query.order_by(schema.TComment.id.desc())
#         query = query.offset((page - 1) * page_size).limit(page_size)
#         items = query.all()
#         count = query.count()
#         return {"total":count, "data": items}
