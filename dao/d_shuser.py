from sqlalchemy.orm import Session
from common import Dao, global_define
from model.schema import TShUser,TShRose,TShShop,TShUserlevel,TShCzyushe,TShProduct,TShConsumption
from sqlalchemy import or_, and_, func, text
from typing import List, Optional
import time
from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel, Field


class consumModel(BaseModel):
    pro_name: Optional[str] = Field(None, title='消费产品名称')
    pro_id: Optional[int] = Field(None, title='消费产品ID')
    balance: Optional[int] = Field(None, title='消费金额')
    shop_id: Optional[int] = Field(None, title='店铺id')
    pinpai_id: Optional[int] = Field(None, title='品牌id')
    manager_id: Optional[int] = Field(None, title='操作员id')
    user_id: Optional[int] = Field(None, title='消费会员id')
    user_phone: Optional[str] = Field(None, title='消费者电话')
    user_name: Optional[str] = Field(None, title='消费者姓名')
    shareuser_id: Optional[int] = Field(None, title='分成会员id')
    shareuser_balance: Optional[int] = Field(None, title='分成会员获得金额')
    cons_type: Optional[int] = Field(None, title='消费类型,0储值消费,1第三方消费')

#设置默认级别参数
class defalutLevelModel(BaseModel):
    le_id: Optional[int] = Field(None, title='基本ID')
    shop_id: Optional[int] = Field(None, title='店铺id')
    pinpai_id: Optional[int] = Field(None, title='品牌id')
    status: Optional[int] = Field(None, title='状态')

#顾客消费，给推荐人分成
def update_recommend(data:consumModel):
    with Dao() as db:
        userinfo = db.query(TShUser).filter(TShUser.id == data.shareuser_id).first()
        if userinfo:
            real_add_balance = data.shareuser_balance
            if userinfo.givetarget <= userinfo.givebalance:
                real_add_balance = 0
            elif userinfo.givetarget <= (userinfo.givebalance + data.shareuser_balance):
                real_add_balance = userinfo.givetarget - userinfo.givebalance

            #增加计算金额
            total_balance = userinfo.givefee + real_add_balance
            #增加已分配额
            total_givebalance = userinfo.givebalance + real_add_balance
            db.query(TShUser).filter(TShUser.id == data.shareuser_id).update({
                "givefee":total_balance,
                "givebalance":total_givebalance
            })
            db.commit()
            return True
        else:
            return False

def update_deflevel(pinpai_id: int, level_id: int):
    with Dao() as db:
        db.query(TShUserlevel).filter(TShUserlevel.pinpai_id == pinpai_id).update({
            "status": 0
        })
        db.flush()
        db.query(TShUserlevel).filter(TShUserlevel.id == level_id).update({
            "status": 1
        })
        db.commit()

# 顾客消费
def update_clientuser(data:consumModel):
    with Dao() as db:
        userinfo = db.query(TShUser).filter(TShUser.id == data.user_id).first()
        if userinfo:
            up_balance = userinfo.balance  #余额
            up_givefee = userinfo.givefee  #增额
            #余额+增额 不足支付
            if data.balance > (up_balance + up_givefee):
                return False
            if userinfo.balance >= data.balance:
                up_balance = userinfo.balance - data.balance
            else:
                up_balance=0
                up_givefee = userinfo.givefee - (data.balance - userinfo.balance)

            db.query(TShUser).filter(TShUser.id == data.user_id).update({
                "balance": up_balance,
                "givefee": up_givefee
            })
            add_consum = TShConsumption(
                pro_name = data.pro_name,
                balance = data.balance,
                shop_id = data.shop_id,
                pinpai_id = data.pinpai_id,
                manager_id = data.manager_id,
                user_id = data.user_id,
                shareuser_id = data.shareuser_id,
                shareuser_balance = data.shareuser_balance,
                pro_id = data.pro_id,
                user_phone = data.user_phone,
                user_name = data.user_name,
                lbalance = up_balance,
                lgivefee = up_givefee,
                lgivebalance = userinfo.givebalance,
                lgivetarget = userinfo.givetarget,
                cons_type = 0
            )
            db.add(add_consum)
            db.commit()
            return True
        else:
            return False


# 顾客第三方无卡消费
def update_clientuser_other(data:consumModel):
    with Dao() as db:
        add_consum = TShConsumption(
            pro_name = data.pro_name,
            balance = data.balance,
            shop_id = data.shop_id,
            pinpai_id = data.pinpai_id,
            manager_id = data.manager_id,
            user_id = data.user_id,
            shareuser_id = data.shareuser_id,
            shareuser_balance = data.shareuser_balance,
            pro_id = data.pro_id,
            user_phone = data.user_phone,
            user_name = data.user_name,
            lbalance = 0,
            lgivefee = 0,
            lgivebalance = 0,
            lgivetarget = 0,
            cons_type = 1
        )
        db.add(add_consum)
        db.commit()
        return True