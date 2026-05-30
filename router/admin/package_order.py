from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional
from common import Dao, global_define
from model import schema, m_schema
from fastapi.exceptions import HTTPException
from dao import d_package, d_account
from model.mall import m_account
import time

router = APIRouter()

class SearchFlashOder(BaseModel):
    order_id: Optional[int] = Field(None, title='订单id')
    package_id: Optional[int] = Field(None,title='关联t_package表id')
    status: Optional[int] = Field(None, title=' 0：未付款    1：已付款    2：未发货    3：已发货    4：已签收     5：退货申请    6：退货中    7：已退货    8：取消交易')
    create_time: Optional[str] = Field(None, title='订单创建时间,是一个时间段如： 2023.1.1,2023.5.1')
    paid_time: Optional[str] = Field(None, title='付款时间,是一个时间段如： 2023.1.1,2023.5.1')
    put_on_time: Optional[str] = Field(None, title='上架时间,是一个时间段如： 2023.1.1,2023.5.1')
    complete_time: Optional[str] = Field(None, title='完结时间,是一个时间段如： 2023.1.1,2023.5.1')
    user_id: Optional[int] = Field(None, title='关联t_user表id')
    single_status: Optional[int] = Field(None, title=' 是否单份代卖')
    spec_id: Optional[int] = Field(None, title='规格id')
    detail: Optional[str] = Field(None, title='订单备注,+=更新')
    is_assign_income: Optional[int] = Field(None, title='是否分配收益')
    phone: Optional[str] = Field(None, title='联系电话')
    page: int = Field(1, title='当前页码，默认第1页')
    page_size: int = Field(20, title='返回每页数据，默认每页20条数据')

class SearchFlashOder_put(BaseModel):
    order_id: Optional[int] = Field(None, title='秒杀包订单id')
    package_id: Optional[int] = Field(None,title='关联t_package表id')
    status: Optional[int] = Field(None, title=' 1: 申请中  2:  已发货  3: 拒绝发货  4：已签收')
    apply_time: Optional[str] = Field(None, title='申请发货时间,是一个时间段如： 2023.1.1,2023.5.1')
    delivery_time: Optional[str] = Field(None, title='发货时间,是一个时间段如： 2023.1.1,2023.5.1')
    complete_time: Optional[str] = Field(None, title='签收或完成时间,是一个时间段如： 2023.1.1,2023.5.1')
    user_id: Optional[int] = Field(None, title='关联t_user表id')
    detail: Optional[str] = Field(None, title='订单备注,+=更新')
    good_type: Optional[int] = Field(None,title='卡券/实体，0:虚拟(卡券） 1:实体')
    page: int = Field(1, title='当前页码，默认第1页')
    page_size: int = Field(20, title='返回每页数据，默认每页20条数据')

class UpdateFlashOrderExpress(BaseModel):
    express_id: Optional[int] = Field(None, title='提现订单id')
    status: Optional[int] = Field(None, title=' 1: 申请中  2:  已发货  3: 拒绝发货  4：已签收')
    express_num: Optional[str] = Field(None, title='物流号')
    detail: Optional[str] = Field(None, title='订单备注')

@router.get('/for_express_items')
async def for_express_items():
    """get all of the package orders which need to be delivered"""
    return {'code': 0, 'message': 'success', 'data': []}

@router.get('/for_express_item')
async def for_express_item(package_order_id: int):
    """get package order which need to be delivered"""
    return {'code': 0, 'message': 'success', 'data': {}}


@router.post('/delivered')
async def delivered():
    """set package order delivered"""
    return {'code': 0, 'message': 'success'}

@router.post(f'/get_flash_order_return')
async def get_flash_order_return(items:SearchFlashOder):
    with Dao() as db:
        res = db.query(schema.TFlashOrder, schema.TPackage, schema.TGoodSpec, schema.TGood, schema.TUser).outerjoin(schema.TPackage, schema.TFlashOrder.package_id == schema.TPackage.id)\
              .outerjoin(schema.TGoodSpec, schema.TFlashOrder.spec_id == schema.TGoodSpec.id)\
              .outerjoin(schema.TGood, schema.TPackage.good_id == schema.TGood.id)\
              .outerjoin(schema.TUser, schema.TFlashOrder.user_id == schema.TUser.id)
        if items.order_id is not None:
            res = res.filter(schema.TFlashOrder.id == items.order_id)
        if items.package_id is not None:
            res = res.filter(schema.TFlashOrder.package_id == items.package_id)
        if items.status is not None:
            res = res.filter(schema.TFlashOrder.status == items.status)
        else:
            res = res.filter(schema.TFlashOrder.status > 0)
            res = res.filter(schema.TFlashOrder.status > 0)
        if items.create_time:
            times = items.create_time.split(',')
            res = res.filter(schema.TFlashOrder.create_time > times[0], schema.TFlashOrder.create_time < times[1])
        if items.paid_time:
            times = items.paid_time.split(',')
            res = res.filter(schema.TFlashOrder.paid_time > times[0], schema.TFlashOrder.paid_time < times[1])
        if items.put_on_time:
            times = items.put_on_time.split(',')
            res = res.filter(schema.TFlashOrder.put_on_time > times[0], schema.TFlashOrder.put_on_time < times[1])
        if items.complete_time:
            times = items.complete_time.split(',')
            res = res.filter(schema.TFlashOrder.complete_time > times[0], schema.TFlashOrder.complete_time < times[1])
        if items.user_id is not None:
            res = res.filter(schema.TFlashOrder.user_id == items.user_id)
        if items.single_status is not None:
            res = res.filter(schema.TFlashOrder.single_status == items.single_status)
        if items.spec_id is not None:
            res = res.filter(schema.TFlashOrder.spec_id == items.spec_id)
        if items.detail:
            res = res.filter(schema.TFlashOrder.detail.like(f'%{items.detail}%'))
        if items.is_assign_income is not None:
            res = res.filter(schema.TFlashOrder.is_assign_income == items.is_assign_income)
        if items.phone is not None:
            res = res.filter(schema.TUser.phone == items.phone)
        res = res.order_by(schema.TFlashOrder.id.desc())

        total = res.count()
        search_list = res.offset(items.page * items.page_size - items.page_size).limit(items.page_size).all()
        return {"total":total, "data": search_list}


@router.post(f'/get_flash_order_put')
async def get_flash_order_put(items:SearchFlashOder_put):
    with Dao() as db:
        res = db.query(schema.TPackageExpress, schema.TFlashOrder, schema.TPackage, schema.TGoodSpec, schema.TGood, schema.TUser)\
            .outerjoin(schema.TFlashOrder,schema.TPackageExpress.flash_order_id == schema.TFlashOrder.id)\
            .outerjoin(schema.TPackage, schema.TFlashOrder.package_id == schema.TPackage.id)\
            .outerjoin(schema.TGoodSpec, schema.TFlashOrder.spec_id == schema.TGoodSpec.id)\
            .outerjoin(schema.TGood, schema.TPackage.good_id == schema.TGood.id)\
            .outerjoin(schema.TUser, schema.TFlashOrder.user_id == schema.TUser.id)
        if items.order_id is not None:
            res = res.filter(schema.TFlashOrder.id == items.order_id)
        if items.package_id is not None:
            res = res.filter(schema.TFlashOrder.package_id == items.package_id)
        if items.status is not None:
            res = res.filter(schema.TPackageExpress.status == items.status)
        if items.apply_time:
            times = items.apply_time.split(',')
            res = res.filter(schema.TPackageExpress.apply_time > times[0], schema.TPackageExpress.apply_time < times[1])
        if items.delivery_time:
            times = items.delivery_time.split(',')
            res = res.filter(schema.TPackageExpress.delivery_time > times[0], schema.TPackageExpress.delivery_time < times[1])
        if items.complete_time:
            times = items.complete_time.split(',')
            res = res.filter(schema.TPackageExpress.complete_time > times[0], schema.TPackageExpress.complete_time < times[1])
        if items.user_id is not None:
            res = res.filter(schema.TFlashOrder.user_id == items.user_id)
        if items.detail:
            res = res.filter(schema.TPackageExpress.detail.like(f'%{items.detail}%'))
        if items.good_type is not None:
            res = res.filter(schema.TGood.type == items.good_type)
        res = res.order_by(schema.TFlashOrder.id.desc())

        total = res.count()
        search_list = res.offset(items.page * items.page_size - items.page_size).limit(items.page_size).all()
        return {"total":total, "data": search_list}

@router.post(f'/update_flash_order_express')
async def update_flash_order_express(items:UpdateFlashOrderExpress):
    if items.express_id is None:
        raise HTTPException(400, "未知订单")
    if items.express_id <= 0:
        raise HTTPException(400, "未找到订单")
    #status=3,拒绝发货并退款
    if items.status == 3:
        with Dao() as db:
            package_express, flash_order = db.query(schema.TPackageExpress, schema.TFlashOrder).outerjoin(schema.TFlashOrder, schema.TPackageExpress.flash_order_id == schema.TFlashOrder.id)\
                .filter(schema.TPackageExpress.id == items.express_id).first()
            change_balance = package_express.amount * flash_order.flash_price
            user_info = d_account.get_account_info_add(flash_order.user_id)
            total_balance = user_info.balance + change_balance
            d_account.update_account_by_id(flash_order.user_id, {"balance": total_balance})
            d_account.add_balance(m_account.BalanceModel(
                user_id=flash_order.user_id,
                change=change_balance,
                balance=total_balance,
                type=global_define.balance_type[9],
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            ))

    d_package.update_flash_order_express(items.express_id, items.status, items.express_num, items.detail)
    return {'status': 200, 'message': 'success'}
