from common import Dao, global_define
from model.schema import TBalance, TFlashOrderReturn, TLockBalance, TUserAd, TUserAdbrand, TUserAdUinfo, TUserAdbrandMenu, TUserAdbrandFile
from sqlalchemy import or_, and_, func
from typing import List, Optional
from sqlalchemy import text
import time
from pydantic import BaseModel, Field
from dao import d_flash_order_return, d_good, d_user, d_account
from fastapi.exceptions import HTTPException
from model.mall import m_account

class AddAd(BaseModel):
    ad_id: Optional[int] = Field(None, title='广告id，用于修改')
    model_id: Optional[int] = Field(None,title='关联项目模型id')
    user_id: Optional[int] = Field(None, title='用户id')
    user_name: Optional[str] = Field(None, title='用户昵称')
    user_phone: Optional[str] = Field(None, title='用户电话')
    qr_code_user: Optional[str] = Field(None, title='用户微信')
    qr_code_enterprise: Optional[str] = Field(None, title='企业微信')

class AddAdUinfo(BaseModel):
    update_id: Optional[int] = Field(None, title='更新id，若不设置表示新增')
    user_id: Optional[int] = Field(None, title='用户id')
    user_name: Optional[str] = Field(None, title='用户昵称')
    user_phone: Optional[str] = Field(None, title='用户电话')
    qr_code_user: Optional[str] = Field(None, title='用户微信')
    qr_code_enterprise: Optional[str] = Field(None, title='企业微信')

def add_user_ad(items: AddAd):
    add_instance = TUserAd(
        user_id=items.user_id,
        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        adbrand_id=items.model_id
    )
    with Dao() as db:
        db.add(add_instance)
        db.commit()


def get_ad_count(user_id:int, model_id:int):
    num = 0
    with Dao() as db:
        num = db.query(TUserAd).filter(TUserAd.user_id == user_id).filter(TUserAd.adbrand_id == model_id).filter(TUserAd.is_del == 0).count()
    return num

def get_ad_info(ad_id:int):
    with Dao() as db:
        return db.query(TUserAd).filter(TUserAd.id == ad_id).first()

def get_brand_info(adbrand_id:int):
    with Dao() as db:
        return db.query(TUserAdbrand).filter(TUserAdbrand.id == adbrand_id).first()

def update_ad(item:AddAd):
    with Dao() as db:
        db.query(TUserAd).where(TUserAd.id == item.ad_id).update({"user_name": item.user_name, "user_phone":item.user_phone, \
                                                                 "qr_code_user":item.qr_code_user,"qr_code_enterprise":item.qr_code_enterprise})
        db.commit()


def del_ad(item:AddAd):
    with Dao() as db:
        db.query(TUserAd).where(TUserAd.id == item.ad_id).update({"is_del": 1})
        db.commit()

def del_brand(brand_id:int):
    with Dao() as db:
        db.query(TUserAdbrand).where(TUserAdbrand.id == brand_id).update({"is_del": 1})
        db.commit()

def set_brand_default(brand_id:int, default:int = 1):
        with Dao() as db:
            db.query(TUserAdbrand).where(TUserAdbrand.id == brand_id).update({"is_default": default})
            db.commit()

def update_adbrand_ad_del(ad_id: int):
    with Dao() as db:
        db.query(TUserAd).where(TUserAd.id == ad_id).update({"del_brand": 1})
        db.commit()

def get_adbrand_info(user_id:int, ad_id:int):
    with Dao() as db:
        # .outerjoin(TGoodSpec, TGoodSpec.good_id==TGood.id)\
        item = db.query(TUserAd, TUserAdbrand, TUserAdUinfo)\
                .outerjoin(TUserAdbrand, TUserAdbrand.id==TUserAd.adbrand_id) \
                .outerjoin(TUserAdUinfo, TUserAdUinfo.user_id==TUserAd.user_id) \
                .filter(TUserAd.id == ad_id).first()

        return item

def update_adbrand_ad_uinfo(data: AddAdUinfo):
    with Dao() as db:
        db.query(TUserAdUinfo).where(TUserAdUinfo.id == AddAdUinfo.update_id).update({"user_name": data.user_name,\
                                                                                      "user_phone": data.user_name,\
                                                                                      "qr_code_user": data.user_name,\
                                                                                      "qr_code_enterprise": data.qr_code_enterprise})
        db.commit()

def add_adbrand_ad_uinfo(items: AddAdUinfo):
    add_instance = TUserAdUinfo(
        user_id=items.user_id,
        user_name=items.user_name,
        user_phone=items.user_phone,
        qr_code_user=items.qr_code_user,
        qr_code_enterprise=items.qr_code_enterprise,
    )
    with Dao() as db:
        db.add(add_instance)
        db.commit()

def get_adbrand_ad_uinfo(adbrand_id:int):
    with Dao() as db:
        return db.query(TUserAdUinfo).filter(TUserAdUinfo.id == adbrand_id).first()

def get_adbrand_ad_uinfo_for_userid(user_id:int):
    with Dao() as db:
        return db.query(TUserAdUinfo).filter(TUserAdUinfo.user_id == user_id).first()
def delete_menu_by_id(menu_id: int):
    with Dao() as db:
        db.query(TUserAdbrandMenu).where(TUserAdbrandMenu.id == menu_id).update({"is_del": 1})
        # db.query(TUserAdbrandMenu).where(TUserAdbrandMenu.id == menu_id).delete()
        # db.query(TUserAdbrandFile).where(TUserAdbrandFile.menu_id == menu_id).delete()
        db.commit()