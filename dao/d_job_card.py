from sqlalchemy.orm import Session
import datetime
from common import Dao
from typing import Literal
from model.schema import TJobCard, TCustomer, TUser, TMake, TModel, TCar


def get_job_card_basic_info_by_id(job_card_id: int):
    with Dao() as db:
        return db.query(TJobCard).where(
            TJobCard.id == job_card_id
        ).first()


def get_job_card_basic_info_by_company_id(company_id: int,
                                          from_time: datetime.datetime,
                                          to_time: datetime.datetime):
    with Dao() as db:
        return db.query(TJobCard).where(
            TJobCard.company_id == company_id
            and from_time < TJobCard.create_time < to_time
        ).all()


def get_job_cards_by_company_id_and_status(
        company_id: int,
        status: Literal['pending', 'ongoing', 'pickup']
    ):
    with Dao() as db:
        return db.query(TJobCard, TCustomer, TUser, TCar, TMake, TModel)\
            .join(TCustomer, TJobCard.customer_id == TCustomer.id, isouter=True)\
            .join(TUser, TJobCard.user_id == TUser.id, isouter=True) \
            .join(TCar, TCar.id == TJobCard.car_id, isouter=True) \
            .join(TMake, TMake.id == TCar.make_id, isouter=True)\
            .join(TModel, TModel.id == TCar.model_id, isouter=True)\
            .filter(TJobCard.company_id == company_id).filter(TJobCard.status == status).all()

def get_page_history_job_cards_by_company_id(
        company_id: int,
        page_size: int,
        page: int
    ):
        with Dao() as db:
            return db.query(TJobCard, TCustomer, TUser, TCar, TMake, TModel)\
                .join(TCustomer, TJobCard.customer_id == TCustomer.id, isouter=True)\
                .join(TUser, TJobCard.user_id == TUser.id, isouter=True) \
                .join(TCar, TCar.id == TJobCard.car_id, isouter=True) \
                .join(TMake, TMake.id == TCar.make_id, isouter=True)\
                .join(TModel, TModel.id == TCar.model_id, isouter=True)\
                .filter(TJobCard.company_id == company_id)\
                .filter(TJobCard.status == 'done')\
                .order_by(TJobCard.id.desc())\
                .offset((page-1) * page_size)\
                .limit(page_size)

def insert_job_card(item: TJobCard):
    with Dao() as db:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

def update_job_card(job_card_id: int,
                    items: dict):
    with Dao() as db:
        db.query(TJobCard).filter(TJobCard.id == job_card_id).update(items)
        db.commit()


def update(job_card_id: int, item: dict):
    with Dao() as db:
        db.query(TJobCard).filter(TJobCard.id == job_card_id).update(item)
        db.commit()
