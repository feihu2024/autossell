from sqlalchemy.orm import Session

from common import Dao
from model.schema import TCompany


def insert_garage(company: TCompany):
    with Dao() as db:
        db.add(company)
        db.commit()
        db.refresh(company)
        return company
