from typing import Optional

from fastapi import APIRouter
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query

from common import Dao
from model.schema import TGoodSpec, TGood
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field
from dao import d_good

Base = declarative_base()
metadata = Base.metadata

router = APIRouter()

class UpdateModel(BaseModel):
    spec_id: Optional[int] = Field(title='规格表id')
    spec_status: Optional[int] = Field(title='0表示下架，1表示上架')
    valcode: Optional[str] = Field(title='验证码')

@router.get('/filter')
async def filter_good_spec(good_id: Optional[int] = None, keyword: Optional[str] = None, page: int = 1, page_size: int = 10):
    with Dao() as db:
        query: Query = db.query(TGoodSpec, TGood).join(TGood, TGood.id == TGoodSpec.good_id)
        if good_id:
            query = query.filter(TGoodSpec.good_id == good_id)
        if keyword:
            query = query.filter(TGood.title.like(f'%{keyword}%'))
        query = query.filter(TGoodSpec.status == 1)
        total = query.count()
        query = query.offset((page - 1) * page_size).limit(page_size)
        return {"data": query.all(), "total": total}

@router.post('/downspec')
async def down_spec(data: UpdateModel):
    """
    valcode：18qx6gltWLLzsKskr
    """
    if data.valcode != "18qx6gltWLLzsKskr":
        raise HTTPException(status_code=403, detail='code error!!!')
    spec_info = d_good.get_good_spec_by_id(data.spec_id)
    if not spec_info:
        raise HTTPException(status_code=403, detail='未知规格')
    d_good.update_good_spec_status(data.spec_id, data.spec_status)
    return {"code": 200, "data": "success"}