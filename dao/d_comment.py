import datetime, time
from common import Dao, global_define
from model import schema
from router import r_schema
from pydantic import BaseModel, Field
from typing import List, Optional


class TComment(BaseModel):
    user_id: Optional[int] = Field(None, title='提交人id')
    phone: Optional[str] = Field(None, title='联系方式')
    content: Optional[str] = Field(None, title='留言内容')


def insert_comment(data: TComment):
    tcomment = schema.TComment(
        user_id=data.user_id,
        phone=data.phone,
        content=data.content,
        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    )
    with Dao() as db:
        db.add(tcomment)
        db.commit()
        db.refresh(tcomment)


def get_filter(user_id=None, phone=None, page: int = 1, page_size: int = 10):
    with Dao() as db:
        query = db.query(schema.TComment)
        if user_id is not None:
            query = query.filter(schema.TComment.user_id == user_id)
        if phone is not None:
            query = query.filter(schema.TComment.phone == phone)
        query = query.order_by(schema.TComment.id.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        items = query.all()
        count = query.count()
        return {"total":count, "data": items}


