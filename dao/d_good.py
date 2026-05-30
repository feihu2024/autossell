import datetime
from common import Dao, global_define
from model import schema
from model.schema import TGood, TGoodSpec, TCategory, TGoodRule, TGoodText, TSupplier, TGoodSpecCombo, TGoodImage, TDeliveryRule, TGoodCategory
from model import m_schema
from model.mall import m_good
from router import r_schema
from typing import List, Optional
from model.mall.good_favs import TGoodFav
from sqlalchemy import text
import time

def insert_good_fav(item: TGoodFav):
    with Dao() as db:
        db.add(item)
        db.commit()
        db.refresh(item)


def remove_good_fav(user_id: int, good_id: int):
    with Dao() as db:
        q = db.query(TGoodFav).where(TGoodFav.user_id == user_id
                                     and TGoodFav.good_id == good_id)
        q.delete()
        db.commit()


def get_good_fvs(user_id: int):
    with Dao() as db:
        q = db.query(TGoodFav)
        t_good_favorites = q.where(TGoodFav.user_id == user_id).all()
        return t_good_favorites


async def delete_image_by_good_id(good_id: int):
    with Dao() as db:
        db.query(schema.TGoodImage).where(schema.TGoodImage.good_id == good_id).delete()
        db.commit()


async def delete_rules_by_good_id(good_id: int):
    with Dao() as db:
        db.query(schema.TDeliveryRule).where(schema.TDeliveryRule.good_id == good_id).delete()
        db.commit()


# async def delete_specs_by_good_id(good_id: int):
#     with Dao() as db:
#         db.query(schema.TGoodSpec).where(schema.TGoodSpec.good_id == good_id).delete()
#         db.commit()


async def delete_texts_by_good_id(good_id: int):
    with Dao() as db:
        db.query(schema.TGoodText).where(schema.TGoodText.good_id == good_id).delete()
        db.commit()


async def get_good_desc(good_id: int, good_name: str, status: int, good_type: int, coin_able: str, expired: int, is_video: int, page,
                        page_size):
    with Dao() as db:
        q = db.query(schema.TGood)
        if good_id is not None:
            q = q.where(schema.TGood.id == good_id)
        if good_name is not None:
            q = q.where(schema.TGood.title.like(f'%{good_name}%'))
        if status is not None:
            q = q.where(schema.TGood.status == status)
        if good_type is not None:
            q = q.where(schema.TGood.type == good_type)
        if coin_able is not None:
            q = q.where(schema.TGood.coinable == int(coin_able))
        if expired == 1:
            time_now = datetime.datetime.now()
            q = q.where(schema.TGood.expired_time > time_now)
            q = q.where(schema.TGood.expired_time < time_now + datetime.timedelta(days=30))
        if is_video is not None:
            q = q.where(schema.TGood.is_video == is_video)
        q = q.order_by(schema.TGood.id.desc())
        total = q.count()
        t_good_list = q.offset(page * page_size - page_size).limit(page_size).all()
        return m_schema.FilterResGood(data=[m_schema.SGood.parse_obj(t.__dict__) for t in t_good_list], total=total)

def get_good_spec(good_id: int):
    with Dao() as db:
        return db.query(schema.TGoodSpec).where(schema.TGoodSpec.good_id == good_id).filter(schema.TGoodSpec.status == 1).all()

def get_good_spec_by_id(spec_id: int):
    with Dao() as db:
        return db.query(schema.TGoodSpec).where(schema.TGoodSpec.id == spec_id).first()

async def get_good_detail(good_id, good_name, status, good_type, coinable, expired, is_video, page, page_size):
    """
    返回商品列表，包括商家店铺的名称电话
    """
    f_good = await get_good_desc(good_id=good_id, good_name=good_name, status=status, good_type=good_type,
                                 coin_able=coinable, expired=expired, is_video=is_video, page=page, page_size=page_size)
    a_good_list = m_good.AGoodList(data=[], total=f_good.total)
    s_goods: List[m_schema.SGood] = f_good.data
    for good in s_goods:
        a_good = m_good.AGood(supplier_name=None, supplier_phone=None, store_name=None, store_phone=None, **good.dict())

        s_supplier: m_schema.SSupplier = await r_schema.get_supplier(supplier_id=a_good.supplier_id)
        a_good.supplier_name = s_supplier.name if s_supplier else None
        a_good.supplier_phone = s_supplier.phone if s_supplier else None

        if s_supplier is not None:
            f_store: m_schema.FilterResStore = await r_schema.filter_store(supplier_id=str(s_supplier.id),
                                                                           page=1, page_size=1)
            a_good.store_name = f_store.data[0].name if f_store.data else None
            a_good.store_phone = f_store.data[0].phone if f_store.data else None

        a_good_list.data.append(a_good)

    return a_good_list

def get_good_info(good_id:int):
    with Dao() as db:
        # .outerjoin(TGoodSpec, TGoodSpec.good_id==TGood.id)\
        items = db.query(TGood, TGoodCategory, TGoodRule, TGoodText, TSupplier)\
                .outerjoin(TGoodCategory, TGoodCategory.id==TGood.category_id)\
                .outerjoin(TGoodRule, TGood.id==TGoodRule.good_id)\
                .outerjoin(TGoodText, TGoodText.good_id==TGood.id)\
                .outerjoin(TSupplier, TSupplier.id==TGood.supplier_id)\
                .filter(TGood.id == good_id).all()
                # .filter(TGood.id==good_id).filter(TGoodSpec.good_id==good_id).all()

        new_items = []
        for item in items:
            new_item = item._asdict()
            # t_good_spec_combos = db.query(TGoodSpecCombo).where(TGoodSpecCombo.good_spec_id==item['TGoodSpec'].id).all()
            # new_item['TGoodSpecCombo'] = t_good_spec_combos
            new_item['TGoodSpecCombo'] = []
            new_items.append(new_item)
        return new_items

def update_good_stock(good_id:int, spec_id:int, sell_num:int):
    with Dao() as db:
        good_info = db.query(TGood).filter(TGood.id == good_id).first()
        spec_info = db.query(TGoodSpec).filter(TGoodSpec.id == spec_id).first()
        if good_info.num_sale is None:
            good_info.num_sale = 0
        db.query(TGood).filter(TGood.id == good_id).update({"num_sale": good_info.num_sale + sell_num })
        db.commit()
        db.query(TGoodSpec).filter(TGoodSpec.id == spec_id).update({"stock": spec_info.stock - sell_num})
        db.commit()

def get_good_data(good_id:int):
    with Dao() as db:
        return db.query(TGood).filter(TGood.id == good_id).first()

def update_good_priority(good_id:int, priority_num:int):
    with Dao() as db:
        db.query(TGood).filter(TGood.id == good_id).update({"priority": priority_num})
        db.commit()
def get_delivery(good_id:int):
    with Dao() as db:
        return db.query(TDeliveryRule).filter(TDeliveryRule.good_id == good_id).all()

def update_good_spec_status(spec_id:int, status_val:int):
    with Dao() as db:
        db.query(TGoodSpec).filter(TGoodSpec.id == spec_id).update({"status": status_val})
        db.commit()

def get_goodids_for_adminid(admin_id:int):
    re_ids = []
    with Dao() as db:
        search_rs = db.query(TGood.id).filter(TGood.admin_id==admin_id).all()
        for r in search_rs:
            re_ids.append(r["id"])
    return re_ids

def get_good_for_ids(ids:list):
    with Dao() as db:
        return db.query(TGood).filter(TGood.id.in_(ids), TGood.status == 1).all()