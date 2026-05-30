from sqlalchemy.orm import Session
import datetime
from common import Dao
from model.schema import TSchedule, TScheduleType, TUser


def get_schedule_by_user_id(
        user_id: int,
        from_time: datetime.datetime,
        to_time: datetime.datetime):
    with Dao() as db:
        return db.query(TSchedule).where(
            TSchedule.user_id == user_id
            and TSchedule.start_time < to_time
            and TSchedule.end_time > from_time).all()


def get_schedule_by_company_id(
        company_id: int,
        from_time: datetime.datetime,
        to_time: datetime.datetime):
    with Dao() as db:
        return db.query(TSchedule).join(TUser, TSchedule.user_id == TUser.id).filter(
            TUser.company_id == company_id
            and TSchedule.start_time < to_time
            and TSchedule.end_time > from_time
        ).all()


def insert_schedule(item: TSchedule):
    with Dao() as db:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

def get_schedule_types():
    with Dao() as db:
        return db.query(TScheduleType).all()


def get_schedule_type_by_id(type_id: int):
    with Dao() as db:
        return db.query(TScheduleType).where(TScheduleType.id == type_id).first()


def insert_schedule_type(item: TScheduleType):
    with Dao() as db:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item


def delete_schedule(schedule_id: int):
    with Dao() as db:
        db.query(TSchedule).where(TSchedule.id == schedule_id).delete()
        db.commit()


def delete_schedule_type(schedule_type_id: int):
    with Dao() as db:
        db.query(TScheduleType).where(TScheduleType.id == schedule_type_id).delete()
        db.commit()

def update_schedule(schedule_id: int, items: dict):
    with Dao() as db:
        db.query(TSchedule).filter(TSchedule.id == schedule_id).update(items)
        db.commit()


def update_schedule_type(schedule_type_id: int, items: dict):
    with Dao() as db:
        db.query(TScheduleType).filter(TScheduleType.id == schedule_type_id).update(items)
        db.commit()


def get_schedule_type_by_id(schedule_type_id: int):
    with Dao() as db:
        return db.query(TScheduleType).filter(TScheduleType.id == schedule_type_id).first()


def get_annual_leave_from_date(
        user_id: int,
        from_time: datetime.datetime):
    with Dao() as db:
        return db.query(TSchedule).join(TScheduleType, TSchedule.type_id == TScheduleType.id).filter(
            TSchedule.user_id == user_id
            and TScheduleType.name == 'annual leave'
            and TSchedule.end_time > from_time
        ).all()