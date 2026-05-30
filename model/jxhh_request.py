from pydantic import BaseModel, Field
from typing import Optional, List


class Sku(BaseModel):
    sku: int = Field(title='sku id')
    number: int = Field(title='数量')

class OrderBody(BaseModel):
    spu: List[Sku] = Field(title='商品组')
    consignee: str = Field(title='收货人')
    phone:str = Field(title='联系方式')
    province: str = Field(title='省份')
    city: str = Field(title='市')
    area: str = Field(title='区')
    street: str = Field(title='街道')
    description: Optional[str] = Field(title='地址详情')