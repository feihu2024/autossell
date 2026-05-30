from pydantic import BaseModel, Field
from typing import List, Optional
from model import m_schema
from datetime import datetime


class GoodCollect(BaseModel):
    good: m_schema.SGood = Field(title='商品')
    spec: m_schema.SGoodSpec = Field(title='商品规格')


class GoodCart(GoodCollect):
    cart: m_schema.SCart = Field(title='购物车')


class FilterGoodCollect(BaseModel):
    data: List[GoodCollect] = Field(title='商品收藏数据')
    total: int


class FilterGoodCart(BaseModel):
    data: List[GoodCart] = Field(title='购物车数据')
    total: int


class SearchGood(BaseModel):
    SGood: Optional[m_schema.SGood] = Field(title='商品区')
    SGoodRule: Optional[m_schema.SGoodRule] = Field(title='使用规则')
    SGoodPerson: Optional[m_schema.SGoodPerson] = Field(title='使用人数')
    SGoodPersonState: Optional[m_schema.SGoodPersonState] = Field(title='使用人数组合')
    SSupplier: Optional[m_schema.SSupplier] = Field(title='供应商')
    SGoodSpec: Optional[m_schema.SGoodSpec] = Field(title='规格')


class FilterSearchGood(BaseModel):
    data: Optional[List[SearchGood]] = Field(title='数据区')
    total: int



class AGood(m_schema.SGood):
    supplier_name: Optional[str]
    supplier_phone: Optional[str]
    store_name: Optional[str]
    store_phone: Optional[str]
    is_warning: Optional[int]  = Field(title='是否预警,大于0表示有规格的库存不足')


class AGoodList(BaseModel):
    data: List[AGood]
    total: int


class ADeliveryRule(BaseModel):
    province: Optional[str] = Field(title='省')
    is_reachable: Optional[int] = Field(title='是否可抵达    0：不可抵达     1：可抵达')
    delivery_fee: Optional[int] = Field(title='邮寄费用')


class AGoodSpec(BaseModel):
    price: Optional[int] = Field(title='售价')
    cost: Optional[int] = Field(title='成本')
    value: Optional[str] = Field(title='规格的值    例如：糖醋里脊的甜口、酸口')
    stock: Optional[int] = Field(title='库存')
    price_line: Optional[int] = Field(title='划价线')
    image: Optional[str] = Field(title='图片url')


class AGoodText(BaseModel):
    description: Optional[str] = Field(title='图文详情   图片和文字放在一起')
    create_time: Optional[datetime] = Field(title='创建时间')


class CreateRealGoodDetail(BaseModel):
    good: m_schema.CreateGood = Field(title='商品基本信息')
    images: Optional[List[str]] = Field(title='商品图片区')
    delivery_rules: Optional[List[m_schema.CreateDeliveryRule]] = Field(title='邮寄规则区')
    # supplier: Optional[m_schema.CreateSupplier] = Field(title='商家区')
    # introducer: Optional[m_schema.CreateUser] = Field(title='推广人区')
    # specs: Optional[List[m_schema.CreateGoodSpec]] = Field(title='商品规格区')
    texts: Optional[List[m_schema.CreateGoodText]] = Field(title='增加商品的图文描述')


class UpdateGoodDetail(BaseModel):
    good: m_schema.SGood
    good_image: List[m_schema.GoodImage]
    delivery_rule: List[m_schema.DeliveryRule]
    # good_rule: Optional[m_schema.GoodRule]
    # good_spec: List[m_schema.GoodSpec] = Field(title='商品规格区')
    # good_spec_combo: List[m_schema.GoodSpecCombo] = Field(title='商品规格组合')
    # good_spec_detail: List[m_schema.GoodSpecDetail] = Field(title='商品规格详情')
    good_text: Optional[m_schema.GoodText] = Field(title='商品图文详情')


class AddGoodDetail(BaseModel):
    rules: Optional[m_schema.CreateGoodRule] = Field(title='使用规则区')
    persons: Optional[List[m_schema.CreateGoodPerson]] = Field(title='套餐人数区')
    packages: Optional[List[m_schema.CreateGoodPackage]] = Field(title='套餐详情区')


class GoodCategory(BaseModel):
    id: int
    title: Optional[str] = Field(title='类别名称')


class ResCategory(BaseModel):
    data: List[GoodCategory]
    total: int

class GetGood(m_schema.SGood):
    parent_category_id: Optional[int] = Field(title='分类顶级id')
