from common import Dao
from model.schema import TModel
from typing import List


def get_all() -> List[TModel]:
    with Dao() as db:
        return db.query(TModel).all()


def get_by_make_id(make_id: int) -> List[TModel]:
    with Dao() as db:
        return db.query(TModel).filter(TModel.make_id == make_id).all()