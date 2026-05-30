from common import Dao
import time, datetime
from model.schema import TSupplierIncome

def add_income(items: TSupplierIncome):
    add_instance = TSupplierIncome(
        supplier_id=items.supplier_id,
        change=items.change,
        balance=items.balance,
        type=items.type,
        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        operator_id=TSupplierIncome.operator_id
    )
    with Dao() as db:
        db.add(add_instance)
        db.commit()