import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from common.db import Dao
from dao.mall import d_package
from model import mall_res
from model.m_schema import SPackage, SGoodSpec
from model.schema import TPackage, TFlashOrder, TGoodSpec

router = APIRouter()


class PackageOrder(BaseModel):
    user_id: int
    package_id: int

class PackageOrder_pifa(BaseModel):
    user_id: int
    package_id: int
    backage_num: int

class ResPackageOrder(BaseModel):
    code: int
    message: str


@router.post('/order', response_model=ResPackageOrder)
async def order(item: PackageOrder) -> ResPackageOrder:
    with Dao() as db:
        t_package = db.query(TPackage).where(TPackage.id == item.package_id).first()
        if t_package is None:
            return ResPackageOrder(code=1, message="没有该秒杀包")
        package = SPackage.parse_obj(t_package.__dict__)
        if package.stock < 1:
            return ResPackageOrder(code=2, message="已经秒杀完毕")
        t_flash_order = TFlashOrder(package_id=t_package.id, user_id=item.user_id, status="ordered", spec_id=t_package.spec_id)
        db.add(t_flash_order)
        db.commit()
        return ResPackageOrder(code=0, message='success')

@router.post('/order_pifa', response_model=ResPackageOrder)
async def order_pifa(item: PackageOrder_pifa) -> ResPackageOrder:
    with Dao() as db:
        t_good_spec = db.query(TGoodSpec).where(TGoodSpec.id == item.package_id).first()
        if t_good_spec is None:
            return ResPackageOrder(code=1, message="没有该批发规格")
        #package = SGoodSpec.parse_obj(t_package.__dict__)
        goods_num = t_good_spec['pifa_num'] * item.backage_num
        if t_good_spec['stock'] < goods_num:
            return ResPackageOrder(code=2, message="库存不足")
        t_flash_order = TFlashOrder(package_id=100, user_id=item.user_id, status="ordered", spec_id=t_good_spec.id, number=goods_num)
        db.add(t_flash_order)
        db.commit()
        return ResPackageOrder(code=0, message='success')