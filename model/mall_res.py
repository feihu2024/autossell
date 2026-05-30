from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Package(BaseModel):
    id: int
    title: str = Field(title="标题")
    sub_title: str = Field(title="副标题")
    amount: int = Field(title="该数据包的份数")
    original_price: int = Field(title="原价，单位（分）")
    flash_sale_price: int = Field(title="秒杀价，单位(分)")
    image_urls: List[str] = Field(title='展示图片列表')


class FlashPackages(BaseModel):
    start_datetime: datetime = Field(title='秒杀开始时间')
    packages: List[Package]


class GoodResponseData(BaseModel):
    """
    * id: int = Field(title='商品ID')
    * title: str = Field(title="标题")
    * stock: int = Field(title='库存')
    * sale: int = Field(title='销量')
    * price: int = Field(title='销售价：单位分')
    * cover: str = Field(title='主图')
    """
    id: int = Field(title='商品ID')
    title: str = Field(title="标题")
    stock: int = Field(title='库存')
    sale: int = Field(title='销量')
    sale_price: int = Field(title='销售价：单位分')
    cover: str = Field(title='主图')
    status: int = Field(title='状态1上架0下架')


class GoodResponse(BaseModel):
    code: int = 0
    msg: str = 'success'
    data: List[GoodResponseData] = Field(title='商品列表')


class Attribute(BaseModel):
    name: str = Field(title='名称')
    value: str = Field(title='值')


class SpecsName(BaseModel):
    id: int
    name: str = Field(title='名称')


class SpecsValue(BaseModel):
    """
    * id: int = Field(title='sku id')
    * name: str = Field(title='规格值')
    """
    id: int = Field(title='sku id')
    name: str = Field(title='规格值')


class SpecsOption(BaseModel):
    id: int = Field(title='sku id')
    goods_id: int = Field(title='产品id')
    spec_value_names: str = Field(title='规格值')
    market_price: int = Field(title='市场价')
    sale_price: int = Field(title='售价')
    image: str = Field(title='该规格的图片')
    stock: int = Field(title='库存')


class Specs(BaseModel):
    names: List[SpecsName] = Field(title='规格名称')
    values: List[SpecsValue] = Field(title='当前规格值')
    options: List[SpecsOption] = Field(title='可选规格值')


class GoodDetailResponseData(BaseModel):
    """
    * id: int = Field(title='商品Id')
    * cover: str = Field(title='主图')
    * covers: List[str] = Field(title='轮播图')
    * market_price: int = Field(title='市场价，原价，单位：分')
    * sale_price: int = Field(title='销售价，单位：分')
    * title: str = Field('标题')
    * description: str = Field(title='描述')
    * attributes: List[Attribute] = Field(title='商品属性')
    * specs: Specs = Field(title='规格')
    * stock: int = Field(title='库存')
    """
    id: int = Field(title='商品Id')
    cover: str = Field(title='主图')
    covers: List[str] = Field(title='轮播图')
    market_price: int = Field(title='市场价，原价，单位：分')
    sale_price: int = Field(title='销售价，单位：分')
    title: str = Field('标题')
    description: str = Field(title='描述')
    attributes: List[Attribute] = Field(title='商品属性')
    specs: Specs = Field(title='规格')
    stock: int = Field(title='库存')


class GoodDetailResponse(BaseModel):
    code: int = 0
    message: str = 'success'
    data: GoodDetailResponseData


class ResponseData(BaseModel):
    code: int = 0
    message: str = 'success'


class CartResponse(BaseModel):
    code: int = 0
    message: str = 'success'
    order_id: Optional[int] = None


class CartData(BaseModel):
    """
    * id: int = Field(title='订单id')
    * user_id: int = Field(title='用户id')
    * good_id: int = Field(title='产品id')
    * sku_id: int = Field(title='规格id')
    * number: int = Field(title='数量')
    * sale_price: int = Field(title='产品单价')
    * cover: str = Field(title='图片')
    * title: str = Field(title='标题')
    * specs_value: str = Field(title='规格值')
    * create_time: datetime = Field(title='购物车创建时间')
    """
    id: int = Field(title='订单id')
    user_id: int = Field(title='用户id')
    good_id: int = Field(title='产品id')
    sku_id: int = Field(title='规格id')
    number: int = Field(title='数量')
    sale_price: int = Field(title='产品单价')
    cover: str = Field(title='图片')
    title: str = Field(title='标题')
    specs_value: str = Field(title='规格值')
    create_time: datetime = Field(title='购物车创建时间')


class CartsResponse(BaseModel):
    code: int = 0
    message: str = 'success'
    data: List[CartData]


class PreOrderResponseData(BaseModel):
    freight: int = Field(title='运费')
    skus: List[int] = Field(title='规格组')


class PreOrderResponse(BaseModel):
    code: int = 0
    message: str = 'success'
    data: List[PreOrderResponseData]
