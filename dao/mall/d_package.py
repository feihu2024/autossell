from sqlalchemy.orm import Session
from common import Dao
from model.schema import TPackage, TPackageTime
from typing import List, Union, Tuple


def insert_package(package: TPackage) -> TPackage:
    with Dao() as db:
        db.add(package)
        db.commit()
        db.refresh(package)
        return package

def update_package(package_id: int, package: dict) -> TPackage:
    with Dao() as db:
        db.query(TPackage).filter(TPackage.id == package_id).update(package)
        db.commit()
        return package

def get_package(id: int) -> TPackage:
    with Dao() as db:
        return db.query(TPackage).where(TPackage.id == id).first()

def search_packages(page: int, page_size:int) -> List[TPackage]:
    with Dao() as db:
        return db.query(TPackage).filter(TPackage.status >= 0)\
        .offset((page-1) * page_size)\
        .limit(page_size).all()

def delete_package(id: int):
    with Dao() as db:
        db.query(TPackage).where(TPackage.id == id).update({"status": -1})
        db.commit()

