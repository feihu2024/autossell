from sqlalchemy.orm import Session
from typing import List

from common import Dao
from model.schema import TOperation, TOperationCategory


def get_operation_by_job_card_id(job_card_id: int):
    with Dao() as db:
        return db.query(TOperation).where(
            TOperation.job_card_id == job_card_id
        ).all()


def insert_operation(item: TOperation):
    with Dao() as db:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item


def update_operation(operation_id: int,
                     items: dict):
    with Dao() as db:
        db.query(TOperation).filter(TOperation.id == operation_id).update(items)
        db.commit()


def get_operation_categories() -> List[TOperationCategory]:
    with Dao() as db:
        return db.query(TOperationCategory).all()
