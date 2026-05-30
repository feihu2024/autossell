from typing import Optional, List, Tuple
from sqlalchemy import or_, text, func

from common import Dao
from model.schema import *
from model.m_schema import *
from model.res.package import PackageTimePairRes, PackageTimePairData, PackageData
from model.vo.package import PackageTimePairUpdate
import datetime


def get_current_package_time_pair(
        package_time_id: int,
        good_title: Optional[str] = None,
        package_id: Optional[int] = None,
        price_start: Optional[int] = None,
        price_end: Optional[int] = None,
        page: int = 1,
        page_size: int = 10,
) -> Tuple[List[PackageTimePairRes], int]:
    with Dao() as db:
        query = db.query(TPackage, TGood, TGoodSpec, TPackageTimePair, TPackageTime)\
            .outerjoin(TGood, TGood.id == TPackage.good_id)\
            .outerjoin(TGoodSpec, TGoodSpec.id == TPackage.spec_id)\
            .outerjoin(TPackageTimePair, TPackageTimePair.package_id==TPackage.id)\
            .outerjoin(TPackageTime, TPackageTime.id==TPackageTimePair.package_time_id)

        #query = query.filter(or_(TPackageTimePair.package_time_id==package_time_id, TPackageTimePair.package_time_id==None))
        if good_title:
            query = query.filter(TGood.title.like(f'%{good_title}%'))
        if package_id:
            query = query.filter(TPackage.id == package_id)
        if price_start:
            query = query.filter(TPackage.flash_sale_price >= price_start)
        if price_end:
            query = query.filter(TPackage.flash_sale_price <= price_end)
        query = query.filter(TPackage.status >= 0)
        count = query.count()
        query = query.offset((page - 1) * page_size).limit(page_size)
        items = query.all()

        items = [PackageTimePairData(
            package=SPackage.parse_obj(item[0].__dict__),
            good=SGood.parse_obj(item[1].__dict__) if item[1] else None,
            good_spec=SGoodSpec.parse_obj(item[2].__dict__) if item[2] else None,
            package_time_pair=SPackageTimePair.parse_obj(item[3].__dict__) if item[3] else None,
            package_time=SPackageTime.parse_obj(item[4].__dict__) if item[4] else None
        ) for item in items]
        return items, count


def get_packages(
        package_id: Optional[int],
        good_id: Optional[int],
        good_title: Optional[str] = None,
        phone: Optional[str] = None,
        name: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
) -> Tuple[List[PackageTimePairRes], int]:
    with Dao() as db:
        query = db.query(TPackage, TGood, TGoodSpec, TSupplier)\
            .outerjoin(TGood, TGood.id==TPackage.good_id)\
            .outerjoin(TGoodSpec, TGoodSpec.id==TPackage.spec_id)\
            .outerjoin(TSupplier, TSupplier.id==TGood.supplier_id)
        if good_title:
            query = query.filter(TGood.title.like(f'%{good_title}%'))
        if package_id:
            query = query.filter(TPackage.id == package_id)
        if good_id:
            query = query.filter(TGood.id == good_id)
        if phone:
            query = query.filter(TSupplier.phone.like(f'%{phone}%'))
        if name:
            query = query.filter(TSupplier.name.like(f'%{name}%'))
        if status:
            query = query.filter(TPackage.status == status)

        count = query.count()
        query = query.offset((page - 1) * page_size).limit(page_size)
        items = query.all()

        items = [PackageData(
            package=SPackage.parse_obj(item[0].__dict__),
            good=SGood.parse_obj(item[1].__dict__) if item[1] else None,
            good_spec=SGoodSpec.parse_obj(item[2].__dict__) if item[2] else None,
        ) for item in items]
        return items, count

def delete_package_time_pair(ids: list):
    with Dao() as db:
        db.query(TPackageTimePair).filter(TPackageTimePair.package_time_id.in_(ids)).delete()
        db.commit()
        #db.query(TPackageTimePair).filter(TPackageTimePair.package_time_id == item.package_time_id).delete()
        #db.commit()

def update_or_insert_package_time_pair(item: PackageTimePairUpdate):
    with Dao() as db:
        t_package_time_pair = TPackageTimePair(**item.dict())
        db.add(t_package_time_pair)
        db.commit()
        return t_package_time_pair
    #修改增加秒杀项目  逻辑
    # with Dao() as db:
    #     t_package_time_pair = db.query(TPackageTimePair).filter(
    #         TPackageTimePair.package_id == item.package_id,
    #         TPackageTimePair.package_time_id == item.package_time_id
    #     ).first()
    #     if t_package_time_pair:
    #         #t_package_time_pair.status = item.status
    #         t_package_time_pair.package_num = item.package_num
    #     else:
    #         t_package_time_pair = TPackageTimePair(**item.dict())
    #         db.add(t_package_time_pair)
    #     db.commit()
    #     return t_package_time_pair

def get_flash_baseinfo(user_id: int = 0):
    with Dao() as db:
        sql_str = f"select t_good.id as good_id,forder.paid_amount,forder.paid_balance,(forder.number-forder.sold) as slod_val,(forder.number-forder.sold)*forder.flash_price*forder.number AS sol_cost,forder.`status`,t_good.title,t_good.sell_high,forder.create_time,t_good.expired_time, t_good_text.description as details,t_good.image_url,forder.paid_time,forder.id as package_order_id,forder.flash_price,forder.flash_price*forder.number AS total_price,t_good_spec.price as goot_spec_price,forder.id as forder_id from (((t_flash_order AS forder INNER JOIN t_package ON forder.package_id=t_package.id) INNER JOIN t_good ON t_package.good_id=t_good.id) INNER JOIN t_good_text ON t_good.id=t_good_text.good_id) INNER JOIN t_good_spec ON t_good.id=t_good_spec.good_id WHERE forder.user_id = {user_id} and forder.status>=0"
        res = db.execute(text(sql_str))
        res_fetch = res.fetchall()
        return res_fetch
        '''  为方便调试，后期转query语法  '''

def get_package_info(package_id: int = 0):
    with Dao() as db:
        sql_str = f"select t_good.id as good_id,t_package.id as package_id,t_package.amount,t_package.flash_sale_price,t_package.num,t_package.stock,t_package.seller_id,t_package.spec_id,t_package.share_fee,t_package.`status`,t_good.`name` as good_name,t_good.title,t_good.subtitle,t_good.cost_high,t_good.cost_low,t_good.sell_high,t_good.sell_low,t_good_spec.image,t_good_spec.price,t_good_spec.cost from (t_package INNER JOIN t_good ON t_package.good_id=t_good.id) INNER JOIN t_good_spec ON t_package.spec_id=t_good_spec.id WHERE t_package.id={package_id}"
        res = db.execute(text(sql_str))
        res_fetch = res.fetchall()
        return res_fetch
        '''  为方便调试，后期转query语法  '''

def update_package(package_id: int, status_val: int):
    with Dao() as db:
        db.query(TFlashOrder)\
            .filter_by(id=package_id)\
            .update(
            {
                "status":status_val
            }
        )
        db.commit()

def get_flash_order_status():
    with Dao() as db:
        return db.query(TPackageOrderStatus).all()

def get_flash_order_count(user_id:int = 0, status:[int] = [0]):
    with Dao() as db:
        return db.query(TFlashOrder).filter(TFlashOrder.user_id == user_id).filter(TFlashOrder.status.in_(status)).count()

def get_flash_order_count2(user_id:int = 0):
    with Dao() as db:
        paid_num = 0
        paid_amount = db.query(func.sum(TFlashOrder.paid_amount)).filter(TFlashOrder.user_id == user_id).filter(TFlashOrder.status.in_([1,2,3,4])).scalar()
        if paid_amount is None:
            paid_amount = 0
        paid_balance = db.query(func.sum(TFlashOrder.paid_balance)).filter(TFlashOrder.user_id == user_id).filter(TFlashOrder.status.in_([1,2,3,4])).scalar()
        if paid_balance is None:
            paid_balance = 0
        paid_num = paid_amount + paid_balance
        if paid_num is None:
            return 0
        else:
            return paid_num


def get_package(package_id: int = 0):
    with Dao() as db:
        return db.query(TPackage).filter(TPackage.id == package_id).first()

def get_flash_order_ids(user_id:int = 0):
    ids = []
    with Dao() as db:
        res = db.query(TFlashOrder.id).filter(TFlashOrder.user_id == user_id).all()
        for i in res:
            ids.append(i[0])
    return ids

def get_order_package_forid(flash_order_id:int = 0):
    with Dao() as db:
        return db.query(TFlashOrder, TPackage).outerjoin(TPackage, TFlashOrder.package_id == TPackage.id)\
                .filter(TFlashOrder.id == flash_order_id).first()

def update_flash_order_express(express_id:int, status:int, express_num:str = None, detail:str = None):
    update_json = {"status": status}
    if status == 1:
        update_json['apply_time'] = datetime.datetime.now()
    elif status == 2:
        update_json['delivery_time'] = datetime.datetime.now()
        update_json['express_num'] = express_num
    elif status in (3,4):
        update_json['complete_time'] = datetime.datetime.now()
    else:  #删除
        update_json['complete_time'] = datetime.datetime.now()
        update_json['status'] = -1
    if detail is not None:
        update_json['detail'] = detail

    with Dao() as db:
        db.query(TPackageExpress).filter(TPackageExpress.id == express_id).update(update_json)
        db.commit()

def get_package_express(express_id:int):
    with Dao() as db:
        return db.query(TPackageExpress).filter(TPackageExpress.id == express_id).first()

def delete_package_time(id: int):
    with Dao() as db:
        db.query(TPackageTime).where(TPackageTime.id == id).delete()
        db.commit()