from typing import Optional, List

from pydantic import BaseModel, Field

class CartRequest(BaseModel):
    user_id: int = Field(title='用户id')
    good_id: int = Field(title='商品id, 同product id')
    sku_id: int = Field(title='sku id,在option里，在规格里')
    number: int = Field(title='购买数量')


class OrderRequest(BaseModel):
    order_ids: List[int] = Field(title='订单id, 加入购物车时获取到')
    consignee: str = Field(title='收货人')
    phone:str = Field(title='联系方式')
    province: str = Field(title='省份')
    city: str = Field(title='市')
    area: str = Field(title='区')
    street: str = Field(title='街道')
    description: Optional[str] = Field(title='地址详情')
