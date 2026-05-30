from sqlalchemy.orm import Session

from common import dao
from model.schema import TPartQuota


@dao
def get_part_quota_by_job_card_id(job_card_id: int,
                                  db: Session):
    return db.query(TPartQuota).where(
        TPartQuota.job_card_id == job_card_id
    ).all()


@dao
def insert_part_quota(item: TPartQuota,
                      db: Session):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@dao
def update_part_quota(part_quota_id: int,
                      items: dict,
                      db: Session):
    db.query(TPartQuota).filter(TPartQuota.id == part_quota_id).update(items)
    db.commit()