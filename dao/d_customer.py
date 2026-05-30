from sqlalchemy.orm import Session
from common import Dao
from model.schema import TCustomer
from typing import List


def insert_customer(customer: TCustomer) -> TCustomer:
    with Dao() as db:
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer
