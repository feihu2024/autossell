from common import Dao
from model.schema import Base
from typing import TypeVar, List


T = TypeVar('T', bound=Base)


def insert_item(item: T) -> T:
    with Dao() as db:
        db.add(item)
        db.commit()
        db.refresh(item)
    return item


def insert_items(items: List[T]):
    with Dao() as db:
        db.add_all(items)
        db.commit()
