from common import Dao
from sqlalchemy.orm import Session
from model.schema import TCart
from typing import List


def insert_cars(cars: List[TCart]):
    with Dao() as db:
        db.add_all(cars)
        db.commit()


def insert_car(car: TCart):
    with Dao() as db:
        db.add(car)
        db.commit()
        db.refresh(car)
    return car

def get_cart(cart_id:int):
    with Dao() as db:
        return db.query(TCart).filter(TCart.id == cart_id).first()

def del_cart(cart_id:int):
    with Dao() as db:
        db.query(TCart).filter(TCart.id == cart_id).delete()
        db.commit()