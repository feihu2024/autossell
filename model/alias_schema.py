from sqlalchemy.orm import aliased

from model.schema import TUser


TOperator = aliased(TUser)