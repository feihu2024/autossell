# coding: utf-8
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from model import m_schema

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CreateMallOrder(BaseModel):
    good_id: Optional[int]
    sku_id: Optional[int]
    user_id: Optional[int]
    sale_price: Optional[int]
    cost_price: Optional[int]
    create_time: Optional[datetime]
    paid_time: Optional[datetime]
    status: Optional[str]
    number: Optional[int] = Field(title='数量')

class AOrderRequest(BaseModel):
    order_id: Optional[int] = Field(title='订单编号')
    paider_id: Optional[int] = Field(title='付款人(用户)id')
    order_status_id: Optional[int] = Field(title='订单状态')
    order_status_ids: Optional[str] = Field(title='查询多个订单状态，如： 1,2,3')
    return_status_id: Optional[int] = Field(title='退单状态')
    good_name: Optional[str] = Field(title='商品名称')
    good_id: Optional[int] = Field(title='商品编号')
    good_type: Optional[int] = Field(title='商品类别,0:虚拟(卡券） 1:实体')
    out_trade_no: Optional[str] = Field(title='商户单号')
    customer_name: Optional[str] = Field(title='购买人名称')
    customer_phone: Optional[str] = Field(title='购买人电话')
    time_start: Optional[str] = Field(title='下单或退单开始时间，转换为时间戳提交')
    time_end: Optional[str] = Field(title='下单或退单结束时间，转换为时间戳提交')
    complete_start: Optional[str] = Field(title='订单完结开始时间，转换为时间戳提交')
    complete_end: Optional[str] = Field(title='订单完结结束时间，转换为时间戳提交')
    delivery_track_code: Optional[str] = Field(title='第三方物流单号  比如顺丰的单号')
    is_wholesale: Optional[int] = Field(title='是不是成为批发商订单，0为默认普通订单，1为批发商订单')
    admin_id: Optional[int] = Field(title='商家id', default=0)
    page: Optional[int] = Field(title='页码', default=1)
    page_size: Optional[int] = Field(title='一页总数', default=20)

class AOrderRequestShoper(BaseModel):
    order_id: Optional[int] = Field(title='订单编号')
    paider_id: Optional[int] = Field(title='付款人(用户)id')
    supplier_id: Optional[int] = Field(title='商家id')
    order_status_id: Optional[int] = Field(title='订单状态')
    order_status_ids: Optional[str] = Field(title='查询多个订单状态，如： 1,2,3')
    return_status_id: Optional[int] = Field(title='退单状态')
    good_name: Optional[str] = Field(title='商品名称')
    good_id: Optional[int] = Field(title='商品编号')
    good_type: Optional[int] = Field(title='商品类别,0:虚拟(卡券） 1:实体')
    out_trade_no: Optional[str] = Field(title='商户单号')
    customer_name: Optional[str] = Field(title='购买人名称')
    customer_phone: Optional[str] = Field(title='购买人电话')
    time_start: Optional[str] = Field(title='下单或退单开始时间，转换为时间戳提交')
    time_end: Optional[str] = Field(title='下单或退单结束时间，转换为时间戳提交')
    complete_start: Optional[str] = Field(title='订单完结开始时间，转换为时间戳提交')
    complete_end: Optional[str] = Field(title='订单完结结束时间，转换为时间戳提交')
    delivery_track_code: Optional[str] = Field(title='第三方物流单号  比如顺丰的单号')
    is_wholesale: Optional[int] = Field(title='是不是成为批发商订单，0为默认普通订单，1为批发商订单')
    admin_id: Optional[int] = Field(title='商家id', default=0)
    page: Optional[int] = Field(title='页码', default=1)
    page_size: Optional[int] = Field(title='一页总数', default=20)


class ASendMsg(BaseModel):
    s_Order: Optional[m_schema.SOrder] = Field(title='订单信息')
    s_User: Optional[m_schema.SUser] = Field(title='用户信息')
    s_Good: Optional[m_schema.SGood] = Field(title='商品信息')
    s_GoodType: Optional[m_schema.SGoodType] = Field(title='商品类型')
    s_State: Optional[m_schema.SOrderState] = Field(title='订单状态')
    s_PayChannel: Optional[m_schema.SPayChannel] = Field(title='支付渠道')
    s_Store: Optional[m_schema.SStore] = Field(title='店铺信息')
    s_StoreOwner: Optional[m_schema.SStoreOwner] = Field(title='店铺负责人信息')
    s_GoodSupplier: Optional[m_schema.SSupplier] = Field(title='供应商信息')
    s_GoodSupplierOwner: Optional[m_schema.SSupplierOwner] = Field(title='供应商负责人信息')
    s_order_income:Optional[int] = Field(title='订单收益')
    s_GoodSpec: Optional[m_schema.SGoodSpec] = Field(title='商品规格信息')

class ASendMsg_two(BaseModel):
    s_Order: Optional[m_schema.SOrder] = Field(title='订单信息')
    s_User: Optional[m_schema.SUser] = Field(title='用户信息')
    s_Good: Optional[m_schema.SGood] = Field(title='商品信息')

class ASendMsgList(BaseModel):
    data: Optional[List[ASendMsg]] = Field(title='发货订单数据')
    total: Optional[int]


class AReturnMsg(ASendMsg):
    s_ReturnState: Optional[m_schema.SOrderState] = Field(title='退单状态')
    s_OrderReturn: Optional[m_schema.SOrderReturn] = Field(title='退单信息')


class AReturnMsgList(BaseModel):
    data: Optional[List[AReturnMsg]] = Field(title='退货订单数据')
    total: Optional[int]


class AOrderMsgList(BaseModel):
    data: Optional[List[AReturnMsg]] = Field(title='全部订单数据')
    total: Optional[int]


class AOrderIncome(BaseModel):
    total_income: Optional[int] = Field(title='总销售额')
    current_income: Optional[int] = Field(title='当日销售额')
    month_income: Optional[int] = Field(title='本月销售额')
    average_income: Optional[int] = Field(title='日均销售额', default=10000000000)


class RealOrderDetail(BaseModel):
    order: Optional[m_schema.SOrder] = Field(title='订单明细')
    good: Optional[m_schema.SGood] = Field(title='商品明细')
    spec: Optional[m_schema.SGoodSpec] = Field(title='规格明细')
    channel: Optional[m_schema.SPayChannel] = Field(title='支付方式')
    total_price: Optional[int] = Field(title='总价')

class RealOrderDetail2(BaseModel):
    order: Optional[m_schema.SOrder] = Field(title='订单明细')
    user: Optional[m_schema.SUser] = Field(title='支付账户明细')

class CardOrderDetail(RealOrderDetail):
    TGoodRule: Optional[List[m_schema.SGoodRule]] = Field(title='使用规则')
    TGoodPackage: Optional[List[m_schema.SGoodPackage]] = Field(title='套餐包含')
    TStore: Optional[m_schema.SStore] = Field(title='店铺信息')
    order_state: Optional[m_schema.SOrderState] = Field(title='订单状态')
    TSupplier: Optional[m_schema.SSupplier] = Field(title='供应商信息')
    TGoodSpecCombo: Optional[List[m_schema.SGoodSpecCombo]]

class UserGoodsInfo(BaseModel):
    user_id: Optional[int] = Field(title='用户id')
    user_name: Optional[str] = Field(title='用户名字')
    user_nickname: Optional[str] = Field(title='用户昵称')
    avatar: Optional[str] = Field(title='头像地址')
    order_count: Optional[int] = Field(title='秒杀订单数量')
    paid_balance_total: Optional[int] = Field(title='价值总额')
    flash_cost_total: Optional[int] = Field(title='对付成本')

class PackageInfo(BaseModel):
    good_id: Optional[int] = Field(title='产品id')
    package_id: Optional[int] = Field(title='包id')
    amount: Optional[int] = Field(title='份数;the number of good in one amount一个包包含的产品的数量')
    flash_sale_price: Optional[int] = Field(title='秒杀价格;in cent,秒杀价格')
    num: Optional[int] = Field(title='包个数;一共有多少个包')
    stock: Optional[int] = Field(title='剩余包数量')
    seller_id: Optional[int] = Field(title='发布商品的卖家，如果id为空或者0，则为官方卖家')
    spec_id: Optional[int] = Field(title='规格id')
    share_fee: Optional[int] = Field(title='让利金额')
    status: Optional[str]
    good_name: Optional[str] = Field(title='产品名称')
    title: Optional[str] = Field(title='主标题')
    subtitle: Optional[str] = Field(title='副标题')
    cost_high: Optional[int] = Field(title='最高成本')
    cost_low: Optional[int] = Field(title='最低成本')
    sell_high: Optional[int] = Field(title='最高售价')
    sell_low: Optional[int] = Field(title='最低售价')
    image_url: Optional[str] = Field(title='图片url')
    price: Optional[int] = Field(title='包售价')
    cost: Optional[int] = Field(title='包成本')


class SearchExportFile(m_schema.CreateExportFile):
    page: Optional[int] = Field(title='当前页码')
    time_start: Optional[str] = Field(title='开始时间')
    time_end: Optional[str] = Field(title='结束时间')
    order: Optional[str] = Field(title='id排序asc(正序)/desc(倒序)')
    #page_size: Optional[str] = Field(title='文件生成地址')