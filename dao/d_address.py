from common import Dao
from model.schema import TAddress, TBanner, TPoster
from sqlalchemy import or_


def insert_address(address: TAddress):
    """
       收货地址插入数据库
    """
    with Dao() as db:
        db.add(address)
        db.commit()
        db.refresh(address)


def delete_address_by_id(address_id: int):
    with Dao() as db:
        db.query(TAddress).where(TAddress.id == address_id).delete()
        db.commit()


def get_address(user_id: int):
    """
    根据 user_id 查询对应的所有地址
    """
    with Dao() as db:
        q = db.query(TAddress)
        t_address_list = q.where(TAddress.user_id == user_id).all()
        return t_address_list


def update_address_by_id(address_id: int, item: dict):
    with Dao() as db:
        db.query(TAddress).where(TAddress.id == address_id).update(item)
        db.commit()

def get_address_by_id(address_id: int):
    with Dao() as db:
        return db.query(TAddress).where(TAddress.id == address_id).first()

def delete_banner_by_id(banner_id: int):
    with Dao() as db:
        db.query(TBanner).where(TBanner.id == banner_id).delete()
        db.commit()

def create_tposter(poster_data: TPoster):
    with Dao() as db:
        db.add(poster_data)
        db.commit()

def list_tposter(status: str = None):
    with Dao() as db:
        q = db.query(TPoster)
        if status is None:
            t_list = q.filter(or_(TPoster.status == None, TPoster.status != 'del')).order_by(TPoster.id.desc()).all()
        else:
            t_list = q.filter(TPoster.status == status).order_by(TPoster.id.desc()).all()
        return t_list

def list_tposter_front():
    with Dao() as db:
        t_list = db.query(TPoster.id, TPoster.poster_url, TPoster.description).filter(or_(TPoster.status == None, TPoster.status != 'del')).order_by(TPoster.id.desc()).all()
        return t_list

def delete_poster_by_id(poster_id: int):
    with Dao() as db:
        db.query(TPoster).where(TPoster.id == poster_id).update({"status":"del"})
        db.commit()

def get_poster_by_id(poster_id: int):
    with Dao() as db:
        return db.query(TPoster).where(TPoster.id == poster_id).first()
