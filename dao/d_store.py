from common import Dao
from model import schema, m_schema
from typing import List
from sqlalchemy import and_
from datetime import date, datetime, timedelta
from sqlalchemy import func


def create_store(items: schema.TStore):
    """
    db.fresh 刷新实例，并包含来自数据库生成的 id
    """
    with Dao() as db:
        db.add(items)
        db.commit()
        db.refresh(items)
        return items


def get_store(store_id: int):
    with Dao() as db:
        return db.query(schema.TStore).where(schema.TStore.id == store_id).first()


def update_store(store_id: int, items: dict):
    with Dao() as db:
        db.query(schema.TStore).where(schema.TStore.id == store_id).update(items)
        db.commit()


def store_filter(items: dict, page: int = 1, page_size: int = 20):
    with Dao() as db:
        q = db.query(schema.TStore)

        if 'id' in items:
            q = q.where(schema.TStore.id == items['id'])
        if 'id_start' in items:
            q = q.where(schema.TStore.id >= items['id_start'])
        if 'id_end' in items:
            q = q.where(schema.TStore.id <= items['id_end'])

        if 'name' in items:
            q = q.where(schema.TStore.name == items['name'])
        if 'name_start' in items:
            q = q.where(schema.TStore.name >= items['name_start'])
        if 'name_end' in items:
            q = q.where(schema.TStore.name <= items['name_end'])

        if 'owner' in items:
            q = q.where(schema.TStore.owner == items['owner'])
        if 'name_start' in items:
            q = q.where(schema.TStore.owner >= items['owner_start'])
        if 'name_end' in items:
            q = q.where(schema.TStore.owner <= items['owner_end'])

        if 'phone' in items:
            q = q.where(schema.TStore.phone == items['phone'])
        if 'phone_start' in items:
            q = q.where(schema.TStore.phone >= items['phone_start'])
        if 'phone_end' in items:
            q = q.where(schema.TStore.phone <= items['phone_end'])

        if 'status' in items:
            q = q.where(schema.TStore.status == items['status'])
        if 'status_start' in items:
            q = q.where(schema.TStore.status >= items['status_start'])
        if 'status_end' in items:
            q = q.where(schema.TStore.status <= items['status_end'])

        if 'register_time' in items:
            q = q.where(schema.TStore.register_time == items['register_time'])
        if 'register_time_start' in items:
            q = q.where(schema.TStore.register_time >= items['register_time_start'])
        if 'register_time_end' in items:
            q = q.where(schema.TStore.register_time <= items['register_time_end'])

        t_store_list = q.offset(page * page_size - page_size).limit(page_size).all()
        return t_store_list


def store_count() -> int:
    with Dao() as db:
        total = db.query(schema.TStore).count()
        if total is None:
            return 0
        else:
            return total


def current_store_count() -> int:
    # 获取当日零时
    time_now = datetime.now()
    zero_today = time_now - timedelta(hours=time_now.hour, minutes=time_now.minute, seconds=time_now.second,
                                      microseconds=time_now.microsecond)

    with Dao() as db:
        current_count: int = db.query(schema.TStore).filter(schema.TStore.register_time > zero_today).count()
        return current_count


def cancel_store_count(status_id: int) -> int:
    with Dao() as db:
        cancel = db.query(schema.TStore).where(schema.TStore.status == status_id).count()

        return cancel


def review_store_count(status_id: int) -> int:
    with Dao() as db:
        review = db.query(schema.TStore).where(schema.TStore.status == status_id).count()

        return review


async def query_store(id, name, owner, owner_id, phone, status, area, supplier_id,
                      register_start, register_end, expired_start, expired_end,
                      expired, page, page_size) -> dict:
    with Dao() as db:
        query = db.query(schema.TStore, schema.TStoreState, schema.TStoreOwner, schema.TUser). \
            outerjoin(schema.TStoreState, schema.TStore.status == schema.TStoreState.id). \
            outerjoin(schema.TStoreOwner, schema.TStore.owner_id == schema.TStoreOwner.id). \
            outerjoin(schema.TUser, schema.TStore.recommender_id == schema.TUser.id)

        if id is not None:
            query = query.where(schema.TStore.id == id)
        if name is not None:
            query = query.where(schema.TStore.name.like(f'%{name}%'))
        if owner is not None:
            query = query.where(schema.TStoreOwner.name.like(f'%{owner}%'))
        if owner_id is not None:
            query = query.where(schema.TStoreOwner.id == owner_id)
        if phone is not None:
            query = query.where(schema.TStore.phone == phone)
        if status is not None:
            query = query.where(schema.TStore.status == status)
        if area is not None:
            query = query.where(schema.TStore.area.like(f'%{area}%'))
        if supplier_id is not None:
            query = query.where(schema.TStore.supplier_id == int(supplier_id))

        if register_start is not None:
            time_start = datetime.fromtimestamp(int(register_start))
            query = query.where(schema.TStore.register_time >= time_start)

        if register_end is not None:
            time_end = datetime.fromtimestamp(int(register_end))
            query = query.where(schema.TStore.register_time <= time_end)

        if expired_start is not None:
            time_start = datetime.fromtimestamp(int(expired_start))
            query = query.where(schema.TStore.register_time >= time_start)

        if expired_end is not None:
            time_end = datetime.fromtimestamp(int(expired_end))
            query = query.where(schema.TStore.register_time <= time_end)

        if expired is not None:
            if int(expired) == 1:
                time_now = datetime.now()
                time_end = time_now + timedelta(days=60)
                query = query.where(schema.TStore.expired_time <= time_end)
            else:
                pass

        query = query.order_by(schema.TStore.is_default.desc())
        total_size = query.count()
        t_send_list = query.offset(page * page_size - page_size).limit(page_size).all()

        return {'data': t_send_list, 'total': total_size}


async def get_amount_by_store_id(store_id: int) -> m_schema.SStoreAmount:
    with Dao() as db:
        query = db.query(schema.TStoreAmount). \
            where(schema.TStoreAmount.store_id == store_id). \
            order_by(schema.TStoreAmount.create_time).first()
    return m_schema.SStoreAmount.parse_obj(query.__dict__) if query else None
