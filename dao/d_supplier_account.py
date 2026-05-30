from common import Dao
import time, datetime
from model.schema import TSupplierAmount

def create_account(item: TSupplierAmount):
    with Dao() as db:
        db.add(item)
        db.commit()
        db.refresh(item)
    return item

def get_account_info(user_id:int = 0):
    with Dao() as db:
        return db.query(TSupplierAmount).filter(TSupplierAmount.supplier_id == user_id).first()

def update_account_by_id(account_id: int, item: dict):
    with Dao() as db:
        if item.get("id"):
            item.pop("id")
        db.query(TSupplierAmount).where(TSupplierAmount.id == account_id).update(item)
        db.commit()