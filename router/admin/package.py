from typing import List, Optional
from pydantic import BaseModel

from fastapi import APIRouter, UploadFile, File, Depends, Header, HTTPException, Request
from fastapi.responses import FileResponse

from dao import d_package
from dao.mall.d_package import insert_package, update_package, get_package, delete_package, search_packages
from model import mall_res
from model.mall.models_all import Package
from model.schema import TPackage, TSupplier, TGood, TGoodSpec
from model.res.common import SuccessResponse
from model.res.package import PackageTimePairRes, PackageRes
from model.vo.package import PackageTimePairUpdate
from model import m_schema
from common import Dao
from fastapi import HTTPException
from pathlib import Path
from config import DIRS

router = APIRouter()

@router.get('/{file_name}', response_class=FileResponse)
async def get_file(file_name) -> str:
    return str(Path(DIRS.root_dir).absolute() / file_name)

#
# @router.post('/create')
# async def create(package: Package):
#     t_package = TPackage(
#         **package.dict()
#     )
#     t_package = insert_package(t_package)
#     return t_package
#
#
# @router.put('/update')
# async def update(package: Package):
#     t_package = update_package(package.id, package.dict())
#     return t_package
#
#
# @router.get('/get')
# async def get(id: int):
#     t_package = get_package(id)
#     return t_package
#
#
# @router.delete('/delete')
# async def get(id: int):
#     delete_package(id)
#
# @router.get('/del_package_time')
# async def get(package_time_id: int, delcode: str):
#     """
#     delcode=rQwj7lOE6*EE
#     """
#     if delcode != "rQwj7lOE6*EE":
#         raise HTTPException(status_code=404, detail={'status': 404, 'massage': 'data error'})
#     d_package.delete_package_time(package_time_id)
#     return {"status": 200, "detail": "success"}
#
# @router.get('/search')
# async def search(page: int, page_size: int):
#     t_package_list = search_packages(page, page_size)
#     return t_package_list
#
# @router.get('/packages', response_model=mall_res.Package)
# async def packages() -> mall_res.Package:
#     return mall_res.Package()
#
#
# @router.get('/flash_sale', response_model=mall_res.FlashPackages)
# async def flash_sale():
#     t_packages_products = d_package.get_all_packages()
#     packages = [mall_res.Package(
#         id=t_package.id,
#         original_price=t_package.amount * t_product.selling_price,
#         flash_sale_price=t_package.flash_sale_price,
#         amount=t_package.amount).original_price for t_package, t_product in t_packages_products]
#
#
# @router.get('/current/get', response_model=PackageTimePairRes, summary='今日秒杀列表')
# async def current_get(
#         package_time_id: int,
#         good_title: Optional[str] = None,
#         package_id: Optional[int] = None,
#         price_start: Optional[int] = None,
#         price_end: Optional[int] = None,
# ) -> PackageTimePairRes:
#     """
#     今日秒杀列表
#     """
#     items, count = d_package.get_current_package_time_pair(
#         package_time_id=package_time_id,
#         good_title=good_title,
#         package_id=package_id,
#         price_start=price_start,
#         price_end=price_end
#     )
#     filter_items = []
#     is_items = []
#     for i in items:
#         if i.package_time_pair is not None:
#             if i.package_time_pair.package_time_id == package_time_id:
#                 filter_items.append(i)
#                 is_items.append(i.package.id)
#
#     for i in items:
#         if i.package_time_pair is None:
#             filter_items.append(i)
#             is_items.append(i.package.id)
#         elif i.package.id not in is_items:
#             i.package_time_pair.package_num = 0
#             filter_items.append(i)
#             is_items.append(i.package.id)
#
#     return PackageTimePairRes(data=filter_items, total=count)
#
#
# class PackageData(BaseModel):
#     package: m_schema.SPackage
#     good: Optional[m_schema.SGood] = None
#     good_spec: Optional[m_schema.SGoodSpec] = None
#     supplier: Optional[m_schema.SSupplier] = None
#
# class ResPackageList(BaseModel):
#     data: List[PackageData]
#     total: int
#
#
# @router.get('/filter', response_model=ResPackageList, summary='秒杀包列表')
# async def filter(
#         good_id: Optional[int] = None,
#         package_id: Optional[int] = None,
#         good_title: Optional[str] = None,
#         name: Optional[str] = None,
#         phone: Optional[str] = None,
#         status: Optional[str] = None,
#         page: int = 1,
#         page_size: int = 10
# ) -> PackageRes:
#     """
#     秒杀包列表
#     """
#     with Dao() as db:
#         query = db.query(TPackage, TGood, TSupplier, TGoodSpec).outerjoin(TGood, TGood.id == TPackage.good_id).outerjoin(TSupplier, TSupplier.id == TGood.supplier_id).outerjoin(TGoodSpec, TGoodSpec.id == TPackage.spec_id)
#         if good_id:
#             query = query.filter(TPackage.good_id == good_id)
#         if package_id:
#             query = query.filter(TPackage.id == package_id)
#         if good_title:
#             query = query.filter(TGood.title.like(f'%{good_title}%'))
#         if name:
#             query = query.filter(TGood.name.like(f'%{name}%'))
#         if phone:
#             query = query.filter(TSupplier.phone.like(f'%{phone}%'))
#         if status:
#             query = query.filter(TPackage.status == status)
#         query = query.order_by(TPackage.id.desc())
#         query = query.offset((page - 1) * page_size).limit(page_size)
#         items = query.all()
#         count = query.count()
#         items = [
#             PackageData(
#                 package=m_schema.SPackage.from_orm(t_package),
#                 good=m_schema.SGood.from_orm(t_good) if t_good else None,
#                 supplier=m_schema.SSupplier.from_orm(t_supplier) if t_supplier else None,
#                 good_spec=m_schema.SGoodSpec.from_orm(t_spec) if t_spec else None
#             ) for t_package, t_good, t_supplier, t_spec in items]
#     return ResPackageList(data=items, total=count)
#
#
# @router.post('/current/update', response_model=SuccessResponse, summary='更新秒杀包时间状态')
# async def current_update(
#         items: List[PackageTimePairUpdate]
# ) -> SuccessResponse:
#     """
#     更新秒杀包时间状态
#     """
#     ids = []
#     for item in items:
#         ids.append(item.package_time_id)
#     d_package.delete_package_time_pair(ids)
#     for item in items:
#         d_package.update_or_insert_package_time_pair(item)
#     return SuccessResponse()
#
