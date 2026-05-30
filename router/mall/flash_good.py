#!/usr/bin/env python
import datetime
import time
from typing import Optional

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func

from common import Dao
from dao import d_db, d_query, d_package
from model import schema
from utils.time import now_timestamp_tz
from model.mall import m_order
from model.schema import TFlashOrder, TPackage
from model import mall_res

router = APIRouter()

@router.get('/time_ranges')
async def time_range(user_id: int):
    """获取所有的时间段"""
    today_time = time.localtime().tm_hour * 60 * 60 + time.localtime().tm_min * 60 + time.localtime().tm_sec
    return d_db.filter_package_time(items={"end_time_start":today_time}, search_items={}, set_items={})


@router.get('/packages')
async def packages(package_time_id: int, page: int = 1, page_size: int = 10):
    """获取所有的套餐"""
    query_data = d_query.FilterQueryData.parse_obj({
        "table": "package",
        "joins": [
            {"table": "package_time_pair", "on_left": "id", "on_right": "package_id"},
            {"table": "good", "on_left": "good_id", "on_right": "id"},
            {"table": "good_spec", "on_left": "spec_id", "on_right": "id"}
        ],
        "filters": [
            {"field": "package_time_pair.package_time_id", "value": package_time_id}],
        "page": page,
        "page_size": page_size
    })

    data = d_query.filter_items(query_data)
    return {"code": 0, "message": "success", "data": data['data'], "total": data['total']}


class AOrder(BaseModel):
    user_id: int = Field(0, title='用户id')
    package_id: int = Field(0, title='秒杀包id')
    package_time_pair_id:int = Field(0, title='时间段id')

class AOrder_pifa(BaseModel):
    user_id: int = Field(0, title='用户id')
    package_id: int = Field(0, title='规格id')
    backage_num:int = Field(0, title='批发包数量')

class UpdatePackage(BaseModel):
    package_id: int = Field(0, title='秒杀包id')
    action: str = Field(..., title='提交行为updateval、删除del')
    status_val: int = Field(0, title='update时的值')

@router.post('/order')
async def order(data: AOrder):
    with Dao() as db:
        package: Optional[schema.TPackage] = db.query(schema.TPackage).filter(
            schema.TPackage.id == data.package_id).first()
        package_time_pair: Optional[schema.TPackageTimePair] = db.query(schema.TPackageTimePair).filter(
            schema.TPackageTimePair.id == data.package_time_pair_id).first()

        if package is None or package_time_pair is None:
            raise HTTPException(400, "套餐不存在")

        if package_time_pair.package_num <= 0:
            raise HTTPException(400, "套餐已售罄")

        ####### 计算订单金额是否超出 #################
        # 获取秒杀订单总金额
        # total_fee = db.query(func.sum((TPackage.amount - TFlashOrder.sold) * TPackage.flash_sale_price))\
        #     .outerjoin(TPackage, TFlashOrder.package_id == TPackage.id)\
        #     .filter(schema.TFlashOrder.user_id == data.user_id).scalar()
        total_fee = 0
        order_limit = db.query(TFlashOrder, TPackage).outerjoin(TPackage, TFlashOrder.package_id == TPackage.id)\
            .filter(schema.TFlashOrder.user_id == data.user_id).all()
        for to, tt in order_limit:
            tt.amount = 0 if tt.amount is None else tt.amount
            to.sold = 0 if to.sold is None else to.sold
            tt.flash_sale_price = 0 if tt.flash_sale_price is None else tt.flash_sale_price
            #total_fee += (tt.amount - to.sold) * tt.flash_sale_price
            total_fee += (tt.amount - to.sold) * tt.flash_sale_price

        fee = package.flash_sale_price * package.amount
        if total_fee is None:
            total_fee = 0
        total_fee += fee

        # 获取限制额度
        limit_fee = db.query(schema.TSetting.flash_order_money_max).scalar()
        if total_fee > limit_fee:
            raise HTTPException(400, "已超持单最高金额")


        now = int(now_timestamp_tz()) % (3600 * 24)
        res = db.query(schema.TPackageTimePair, schema.TPackageTime) \
            .outerjoin(schema.TPackageTime, schema.TPackageTimePair.package_time_id == schema.TPackageTime.id) \
            .filter(schema.TPackageTimePair.package_id == data.package_id) \
            .filter(schema.TPackageTime.start_time <= now) \
            .filter(schema.TPackageTime.end_time >= now).first()
        if res is None or res[0] is None:
            raise HTTPException(400, "套餐不在可预约时间内")

        # db.query(schema.TPackage).filter(schema.TPackage.id == data.package_id).update(
        #     {"stock": schema.TPackage.stock - 1})
        db.query(schema.TPackageTimePair).filter(schema.TPackageTimePair.id == data.package_time_pair_id)\
        .update({"package_num": schema.TPackageTimePair.package_num - 1})
        db.flush()

        flash_order = schema.TFlashOrder(
            package_id=data.package_id,
            user_id=data.user_id,
            create_time=datetime.datetime.now(),
            flash_price=fee,
            number=package.amount,
            sold=0,
            status=0,  # 未支付
            spec_id=package.spec_id
        )
        db.add(flash_order)
        db.commit()
        db.refresh(flash_order)

        return {"code": 0, "message": "success", "data": {"order_id": flash_order.id}}


@router.post('/order_pifa')
async def order_pifa(data: AOrder_pifa):
    with Dao() as db:
        good_spec: Optional[schema.TGoodSpec] = db.query(schema.TGoodSpec).filter(
            schema.TGoodSpec.id == data.package_id).first()

        if good_spec is None:
            raise HTTPException(400, "没有该批发规格")

        if good_spec.stock is None:
            good_spec.stock = 0
        if good_spec.num_sale is None:
            good_spec.num_sale = 0
        if good_spec.price is None:
            good_spec.price = 0
        goods_num = good_spec.pifa_num * data.backage_num
        total_goods_num = goods_num + good_spec.num_sale

        if good_spec.stock < total_goods_num:
            raise HTTPException(400, "库存不足")


        fee = good_spec.price * data.backage_num
        # if total_fee is None:
        #     total_fee = 0
        # total_fee += fee

        # 获取限制额度
        # limit_fee = db.query(schema.TSetting.flash_order_money_max).scalar()
        # if total_fee > limit_fee:
        #     raise HTTPException(400, "已超持单最高金额")

        db.query(schema.TGoodSpec).filter(schema.TGoodSpec.id == data.package_id)\
        .update({"num_sale": total_goods_num})
        db.flush()

        flash_order = schema.TFlashOrder(
            package_id=100,
            user_id=data.user_id,
            create_time=datetime.datetime.now(),
            flash_price=fee,
            number=goods_num,
            sold=0,
            status=0,  # 未支付
            spec_id=data.package_id
        )
        db.add(flash_order)
        db.commit()
        db.refresh(flash_order)

        return {"code": 0, "message": "success", "data": {"order_id": flash_order.id}}

class AAgree(BaseModel):
    user_id: int


@router.post('/agree')
async def agree(data: AAgree):
    """同意协议"""
    with Dao() as db:
        db.query(schema.TUser).filter(schema.TUser.id == data.user_id).update({"is_agree": 1})
        db.commit()
        return {"code": 0, "message": "success"}

@router.get('/flash_sale', response_model=mall_res.FlashPackages)
async def flash_sale():
    t_packages_products = d_package.get_all_packages()
    packages = [mall_res.Package(
        id=t_package.id,
        original_price=t_package.amount * t_product.selling_price,
        flash_sale_price=t_package.flash_sale_price,
        amount=t_package.amount,
        image_urls = t_product.image_url.split(',')
    ).original_price for t_package, t_product in t_packages_products]

    now = datetime.datetime.now()
    flash_time = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=10)

    return mall_res.FlashPackages(start_datetime=flash_time, packages=packages)


@router.get(f'/get_flash_goods', response_model=list, summary='获取用户秒杀订单列表')
async def get_flash_goods(user_id: int = 0):
    """
        "good_id":
        "paid_amount":   支付金额余额
        "paid_balance":  支付金额
        "sold_val":   剩余份数
        "sol_cost":  剩余价值
        "status":  支付状态
        "title":    good表标题
        "sell_high":    goodb表最高售价
        "create_time": "2023-05-27T14:39:54",
        "expired_time": "2023-06-29T16:00:00",
        "details":    详情
        "image_url":   图片地址
        "paid_time":
        "package_order_id":
        "flash_price": 套餐单价
        total_price:套餐总价
        goot_spec_price   商品单价，t_good_spec表
    """
    flash_user = d_package.get_flash_baseinfo(user_id)
    re = []
    for i in flash_user:
        re.append({"good_id":i[0], "paid_amount":i[1], "paid_balance":i[2], "sold_val":i[3], "sol_cost":i[4], "status":i[5], "title":i[6], "sell_high":i[7], "create_time":i[8],"expired_time":i[9], "details":i[10], "image_url":i[11],"paid_time":i[12],"package_order_id":i[13],"flash_price":i[14],"total_price":i[15],"goot_spec_price":i[16],"forder_id":i[17] })
    return re

@router.get(f'/get_package', response_model=m_order.PackageInfo, summary='通过包id获取组合包数据')
async def get_package(package_id: int = 0):
    """
            package_id,   包id
            good_id,   商品id
            amount,  # 份数;the number of good in one amount一个包包含的产品的数量
            flash_sale_price,  # 秒杀价格;in cent,秒杀价格
            num , #包个数;一共有多少个包
            stock,   #剩余包数量
            seller_id,  # 发布商品的卖家，如果id为空或者0，则为官方卖家'
            spec_id, 规格id
            share_fee,让利金额
            status，
            good_name，产品名称
            title，主标题
            subtitle，副标题
            cost_high,最高成本
            cost_low，最低成本
            sell_high,最高售价
            sell_low ，最低售价
            image_url, 图片url
            price， 包售价
            cost, 包成本
    """
    package_info = d_package.get_package_info(package_id)
    if len(package_info) > 0:
        re_model = m_order.PackageInfo(
            package_id = package_info[0][1],
            good_id = package_info[0][0],
            amount = package_info[0][2],  # 份数;the number of good in one amount一个包包含的产品的数量
            flash_sale_price = package_info[0][3],  # 秒杀价格;in cent,秒杀价格
            num = package_info[0][4], #包个数;一共有多少个包
            stock = package_info[0][5],   #剩余包数量
            seller_id = package_info[0][6],  # Optional[int] = Field(title='发布商品的卖家，如果id为空或者0，则为官方卖家')
            spec_id = package_info[0][7],   #Optional[int] = Field(title='规格id')
            share_fee = package_info[0][8],  # Optional[int] = Field(title='让利金额')
            status = package_info[0][9],   #Optional[str]
            good_name = package_info[0][10],  #: Optional[str] = Field(title='产品名称')
            title = package_info[0][11],     #: Optional[str] = Field(title='主标题')
            subtitle = package_info[0][12],   #: Optional[str] = Field(title='副标题')
            cost_high = package_info[0][13],   #: Optional[str] = Field(title='最高成本')
            cost_low = package_info[0][14],     #: Optional[str] = Field(title='最低成本')
            sell_high = package_info[0][15],    # Optional[str] = Field(title='最高售价')
            sell_low = package_info[0][16],    # Optional[str] = Field(title='最低售价')
            image_url = package_info[0][17],   #: Optional[str] = Field(title='图片url')
            price = package_info[0][18],  #Optional[int] = Field(title='包售价')
            cost = package_info[0][19]         #: Optional[int] = Field(title='包成本')
        )
        return re_model
    else:
        return {}

@router.post(f'/update_package', summary='修改秒杀包订单状态update、删除del')
async def update_package(item: UpdatePackage):
    if item.action == 'updateval':
        d_package.update_package(item.package_id, item.status_val)
        return {"code": 0, "message": "update success"}
    else:
        d_package.update_package(item.package_id, -1)
        return {"code": 0, "message": "del success"}

@router.get(f'/get_flash_goods_status',summary='获取用户秒杀订单列表的修改状态')
async def get_flash_goods_status():
    """
    取值：
        -1:"删除",
        "未付款",
        "已付款",
        "已上架",
        "已完成"
    """
    res = d_package.get_flash_order_status()
    re = {}
    for i in res:
        re[i.id] = i.title
    return re
