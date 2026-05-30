from sqlalchemy.orm import Session

from common import Dao
from model.schema import TInspection


def get_inspection_by_job_card_id(job_card_id: int):
    with Dao() as db:
        return db.query(TInspection).where(
            TInspection.job_card_id == job_card_id
        ).all()


def insert_inspection(item: TInspection) -> TInspection:
    with Dao() as db:
        db.add(item)
        db.commit()
        db.refresh(item)
    return item

def insert_inspections(items: TInspection):
    with Dao() as db:
        db.add_all(items)
        db.commit()


def update_inspection(inspection_id: int,
                      items: dict):
    with Dao() as db:
        db.query(TInspection).filter(TInspection.id == inspection_id).update(items)
        db.commit()
