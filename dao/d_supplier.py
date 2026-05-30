from common import Dao
from model import schema, m_schema
from typing import List, Optional
from router import r_schema
from dao import d_store
from sqlalchemy import and_
from datetime import datetime, timedelta

def get_user_by_username(username: str):
    with Dao() as db:
        return db.query(schema.TSupplierOwner).where(schema.TSupplierOwner.phone == username).first()

async def query_supplier(id, name, owner, phone, status, area,
                         register_start, register_end, expired_start, expired_end,
                         expired, page, page_size) -> dict:
    with Dao() as db:

        query = db.query(schema.TSupplier, schema.TSupplierState,
                         schema.TSupplierOwner, schema.TUser). \
            outerjoin(schema.TSupplierState, schema.TSupplier.status == schema.TSupplierState.id). \
            outerjoin(schema.TSupplierOwner, schema.TSupplier.owner_id == schema.TSupplierOwner.id). \
            outerjoin(schema.TUser, schema.TSupplier.recommender_id == schema.TUser.id)

        if id is not None:
            query = query.where(schema.TSupplier.id == id)
        if name is not None:
            query = query.where(schema.TSupplier.name.like(f'%{name}%'))
        if owner is not None:
            query = query.where(schema.TSupplierOwner.name.like(f'%{owner}%'))
        if phone is not None:
            query = query.where(schema.TSupplier.phone == phone)
        if status is not None:
            query = query.where(schema.TSupplier.status == status)
        if area is not None:
            query = query.where(schema.TSupplier.area.like(f'%{area}%'))
        if register_start is not None:
            time_start = datetime.fromtimestamp(int(register_start))
            query = query.where(schema.TSupplier.register_time >= time_start)

        if register_end is not None:
            time_end = datetime.fromtimestamp(int(register_end))
            query = query.where(schema.TSupplier.register_time <= time_end)

        if expired_start is not None:
            time_start = datetime.fromtimestamp(int(expired_start))
            query = query.where(schema.TSupplier.register_time >= time_start)

        if expired_end is not None:
            time_end = datetime.fromtimestamp(int(expired_end))
            query = query.where(schema.TSupplier.register_time <= time_end)

        if expired is not None:
            if int(expired) == 1:
                time_now = datetime.now()
                time_end = time_now + timedelta(days=60)
                query = query.where(schema.TSupplier.expired_time <= time_end)
            else:
                pass

        total_size = query.count()
        t_send_list = query.offset(page * page_size - page_size).limit(page_size).all()

        return {'data': t_send_list, 'total': total_size}


async def get_members_by_supplier_id(supplier_id: int, page: int, page_size: int) -> dict:
    f_stores: m_schema.FilterResStore = await r_schema.filter_store(supplier_id=str(supplier_id))
    members_total: dict = {'data': [], 'total': 0}
    for s_store in f_stores.data:
        store_members: dict = await d_store.get_members_by_store_id(store_id=s_store.id, page=page, page_size=page_size)
        members_total['total'] += store_members['total']
        members_total['data'] += store_members['data']

    return members_total


async def get_amount_by_supplier_id(supplier_id: int) -> m_schema.SSupplierAmount:
    with Dao() as db:
        query = db.query(schema.TSupplierAmount). \
            where(schema.TSupplierAmount.supplier_id == supplier_id). \
            order_by(schema.TSupplierAmount.create_time.desc()).first()

    return m_schema.SSupplierAmount.parse_obj(query.__dict__) if query else None


async def get_store_count(supplier_id: int) -> int:
    with Dao() as db:
        count = db.query(schema.TStore). \
            where(schema.TStore.supplier_id == supplier_id).count()

    return count


async def get_amount_record_list(supplier_id: int, page: int, page_size: int) -> dict:
    with Dao() as db:
        query = db.query(schema.TSupplierAmount, schema.TSupplierChangeType, schema.TOrder, schema.TGood,
                         schema.TStore). \
            outerjoin(schema.TSupplierChangeType, schema.TSupplierAmount.type == schema.TSupplierChangeType.id). \
            outerjoin(schema.TOrder, schema.TSupplierAmount.order_id == schema.TOrder.id). \
            outerjoin(schema.TGood, schema.TOrder.good_id == schema.TGood.id). \
            outerjoin(schema.TStore, schema.TOrder.store_id == schema.TStore.id). \
            where(schema.TSupplierAmount.supplier_id == supplier_id)

    total_size = query.count()
    t_record_list = query.offset(page * page_size - page_size).limit(page_size).all()

    return {'data': t_record_list, 'total': total_size}


async def query_supplier_members(supplier_id: str, user_id: Optional[str],
                                 consume_start: Optional[str], consume_end: Optional[str],
                                 username: Optional[str], phone: Optional[str]) -> dict:
    f_stores: m_schema.FilterResStore = await r_schema.filter_store(supplier_id=supplier_id)
    members_total: dict = {'data': [], 'total': 0}
    for store in f_stores.data:
        if consume_start and consume_end:
            paid_time_interval = consume_start + ',' + consume_end
            f_orders: m_schema.FilterResOrder = await r_schema.filter_order(store_id=str(store.id), paider_id=user_id,
                                                                            paid_time=paid_time_interval,
                                                                            s_paider_name=username, paider_phone=phone)
            members_total['total'] += f_orders.total
            members_total['data'] += f_orders.data
        else:
            f_orders: m_schema.FilterResOrder = await r_schema.filter_order(store_id=str(store.id), paider_id=user_id,
                                                                            s_paider_name=username, paider_phone=phone)
            members_total['total'] += f_orders.total
            members_total['data'] += f_orders.data

    return members_total


async def query_supplier_owner(supplier_id: int):
    with Dao() as db:
        q = db.query(schema.TSupplierOwner). \
            outerjoin(schema.TSupplier, schema.TSupplier.owner_id == schema.TSupplierOwner.id)
        q = q.where(schema.TSupplier.id == supplier_id).first()

    return q


def get_employee_by_openid(openid: str) -> Optional[schema.TSupplierOwner]:
    with Dao() as db:
        return db.query(schema.TSupplierOwner).where(schema.TSupplierOwner.open_id == openid).first()


def insert_employee(employee: schema.TSupplierOwner) -> schema.TSupplierOwner:
    with Dao() as db:
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee
