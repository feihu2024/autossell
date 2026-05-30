from pydantic import BaseModel, Field
from typing import List, Optional


class Success(BaseModel):
    code: int = 200
    message: str = 'success'


class Fail(BaseModel):
    code: int = 0
    message: str = 'fail'


class UserAddress(BaseModel):
    id: int
    user_id: Optional[int] = Field(title='外键')
    consignee: Optional[str] = Field(title='收获人姓名')
    phone: Optional[str] = Field(title='联系方式')
    province: Optional[str] = Field(title='省')
    city: Optional[str] = Field(title='市')
    area: Optional[str] = Field(title='区')
    street: Optional[str] = Field(title='街道')
    description: Optional[str] = Field(title='详细地址')
    default_val: Optional[int] = Field(title='1:默认  0:非默认')


class AddressRequest(BaseModel):
    user_id: Optional[int] = Field(title='用户id')
    consignee: Optional[str] = Field(title='收货人姓名')
    phone: Optional[str] = Field(title='联系方式')
    province: Optional[str] = Field(title='省')
    city: Optional[str]
    area: Optional[str]
    street: Optional[str]
    description: Optional[str] = Field(title='详细地址')

