from sqlalchemy.orm import Session
from common import Dao
#from model.mall.schema import TProduct
from typing import List

from model.schema import TCategory

#
# def insert_product(product: TProduct) -> TProduct:
#     with Dao() as db:
#         db.add(product)
#         db.commit()
#         db.refresh(product)
#         return product
#
# def update_product(product_id: int, product: dict) -> TProduct:
#     with Dao() as db:
#         db.query(TProduct).filter(TProduct.id == product_id).update(product)
#         db.commit()
#         return product
#
# def get_product(id: int) -> TProduct:
#     with Dao() as db:
#         return db.query(TProduct).where(TProduct.id == id).first()
#
# def delete_product(id: int):
#     with Dao() as db:
#         db.query(TProduct).where(TProduct.id == id).delete()
#         db.commit()
#
# def search_products(page: int, page_size:int) -> List[TProduct]:
#     with Dao() as db:
#         return db.query(TProduct)\
#         .offset((page-1) * page_size)\
#         .limit(page_size).all()


def get_categoreis() -> List[TCategory]:
    with Dao() as db:
        return db.query(TCategory).all()

def get_sub_category(parent_id:int = 0):
    with Dao() as db:
        return db.query(TCategory).filter(TCategory.parent_category_id == parent_id).all()

