from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TGoodFav(Base):
    __tablename__ = 't_user_favs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, comment='用户id')
    good_id = Column(Integer, nullable=False, comment='商品id')

    def __int__(self, user_id, good_id):
        self.user_id = user_id
        self.good_id = good_id
