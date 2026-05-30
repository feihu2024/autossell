from common import Dao
from model.schema import Base, TMake
from typing import TypeVar, List


def get_all() -> List[TMake]:
    with Dao() as db:
        return db.query(TMake).all()