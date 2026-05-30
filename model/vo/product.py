import datetime

from pydantic import BaseModel, Field
from typing import Literal, Optional


class CreateProduct(BaseModel):
    name: str = Field(title='产品名称')
    stock: int = Field(title='存货数量')
    is_flash_sale: Optional[int] = Field(title='是否已经参加秒杀')
    category_id: int = Field(title='产品类型id')
    type: Literal['real', 'virtual'] = Field(title='产品类型，real: 实体产品， virtual: 虚拟产品')
    selling_price: int = Field(title='售价，单位为分')
    cost_price: int = Field(title='进价，单位为分')
    num_scales: Optional[int]
    image_url: str = Field(title='商品图片')
    priority: int = Field(title='优先级别，越小级别越高')
    sliver_coin: int = Field(title='购买后给与的银币数量')
    model_id: int = Field(title='规格id')
    expired_time: datetime.datetime = Field(title='过期时间')
    parent_product_id: int = Field(title='产品ID，套餐产品的父类产品ID')
    title: str = Field(title='标题')
    subtitle: str = Field(title='副标题')
    stock_cordon: int = Field(title='存量警戒线')
    status: Literal['active', 'inactive'] = Field(default='active', title='状态, active:激活，inactive：非激活')


class UpdateProduct(CreateProduct):
    id: int
