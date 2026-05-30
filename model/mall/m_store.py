# coding: utf-8
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CreateStore(BaseModel):
    name: Optional[str] = Field(title='店名')
    phone: Optional[str]
    province: Optional[str]
    city: Optional[str]
    area: Optional[str]
    street: Optional[str]
    address: Optional[str]
    status: Optional[str]
    owner: Optional[str] = Field(title='店主')
    recommender_id: Optional[int] = Field(title='推荐人')
    register_time: Optional[datetime] = Field(title='in seconds')


class SMallStore(CreateStore):
    id: int


class Tstore(Base):
    __tablename__ = 't_store'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    phone = Column(String)
    province = Column(String)
    city = Column(String)
    area = Column(String)
    street = Column(String)
    address = Column(String)
    status = Column(String)
    owner = Column(String)
    recommender_id = Column(Integer)
    register_time = Column(TIMESTAMP, comment='注册时间')
