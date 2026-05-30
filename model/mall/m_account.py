# coding: utf-8
from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional

Base = declarative_base()
metadata = Base.metadata


class CreateAccount(BaseModel):
    user_id: Optional[int] = Field(title='用户id', default=0)
    balance: Optional[int] = Field(title='余额', default=0)
    lock_balance: Optional[int] = Field(title='锁定额', default=0)
    create_time: Optional[datetime] = Field(title='创建时间', default='0000-00-00 00:00:00')
    coin: Optional[int] = Field(title='积分', default=0)
    #bank_name: str = Field(title='开户行', default=None)
    #id_card: str = Field(title='银行账号', default=None)
    description: Optional[str] = Field(title='详细描述', default=None)


class SCreateAccount(CreateAccount):
    id: int = Field(title='id')


class UserAccount(BaseModel):
    user_id: int = Field(title='用户id')
    balance: int = Field(title='余额')
    lock_balance: int = Field(title='锁定额')
    coin: int = Field(title='积分')
    bank_name: str = Field(title='开户行')
    id_card: str = Field(title='银行账号')

class UserTran(BaseModel):
    user_id: int = Field(title='转账人用户id')
    tran_id: int = Field(title='接受人用户id')
    balance: int = Field(title='转账金额')
    passwd: str = Field(title='转账密码')

class TUserAccount(Base):
    __tablename__ = 't_user_account'

    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer)
    balance = Column(Integer)
    lock_balance = Column(Integer)
    coin = Column(Integer)
    description = Column(String(100))
    create_time = Column(DateTime, comment='创建时间')
    bank_name = Column(String(100), comment='开户行')
    id_card = Column(String(45), comment='银行卡号')

class GetUserAccount(UserAccount):
    pass

class GetCoinBalance(BaseModel):
    id: int = Field(title='id')
    user_action:str = Field(title='balance更新余额，lock_balance更新锁定额,coin更新积分')
    balance: int = Field(title='余额',default=0)
    lock_balance: int = Field(title='锁定额',default=0)
    coin: int = Field(title='积分', default=0)
    user_id: Optional[int] = Field(title='用户id')

class GetUserBank(BaseModel):
    bank_id: int = Field(title='id')
    bank_name: Optional[str] = Field(title='开户行')
    username: Optional[str] = Field(title='户主姓名')
    id_card: Optional[str] = Field(title='银行卡号')
    user_id: Optional[int] = Field(title='用户id')
    phone: Optional[str] = Field(title='户主电话')
    bank_address: Optional[str] = Field(title='开户行地址')

class CoinModel(BaseModel):
    id: Optional[int] = Field(title='id')
    user_id: Optional[int]  = Field(title='用户id')
    change: Optional[int] = Field(title='变动积分')
    coin: Optional[int] = Field(title='积分')
    type: Optional[str] = Field(title='类型')
    description: Optional[str] = Field(title='详细')
    create_time: Optional[datetime] = Field(title='创建时间', default='0000-00-00 00:00:00')
    out_trade_no: Optional[str] = Field(title='out_trade_no')

class BalanceModel(BaseModel):
    id: Optional[int] = Field(title='id')
    user_id: Optional[int] = Field(title='用户id')
    change: Optional[int] = Field(title='变动金额')
    balance: Optional[int] = Field(title='余额')
    type: Optional[str] = Field(title='类型')
    description: Optional[str] = Field(title='详细')
    create_time: Optional[datetime] = Field(title='创建时间', default='0000-00-00 00:00:00')
    user_withdraw_id: Optional[int] = Field(title='user_withdraw_id')
    operator_id: Optional[int] = Field(title='操作员ID')
    out_trade_no: Optional[str] = Field(title='out_trade_no')
    good_id: Optional[str] = Field(title='收益商品id')
    good_title: Optional[str] = Field(title='收益商品标题名称')
    good_num: Optional[str] = Field(title='收益商品数量')

class LockBalanceModel(BaseModel):
    id: Optional[int] = Field(title='id')
    user_id: Optional[int] = Field(title='用户id')
    change: Optional[int] = Field(title='变动金额')
    lock_balance: Optional[int] = Field(title='余额')
    type: Optional[str] = Field(title='类型')
    description: Optional[str] = Field(title='详细描述')
    create_time: Optional[datetime] = Field(title='创建时间', default='0000-00-00 00:00:00')
    out_trade_no: Optional[str] = Field(title='out_trade_no')

class WithdrawModel(BaseModel):
    amount: Optional[int] = Field(title='提现金额，单位分')
    user_id: Optional[int] = Field(title='用户id')
    type_id: Optional[int] = Field(title='提现类型:1表示到银行卡，2表示到微信零钱,3表示提现到支付宝', default=2)
    user_bank_id: Optional[str] = Field(title='当类型为银行卡时，该字段指向银行卡号，3填写支付宝账号')
    user_bank_other: Optional[str] = Field(title='转账账号其他备注信息')
    fee_type: Optional[int] = Field(title='扣费类型，1表示扣费推荐余额，2表示扣费余额', default=1)
    fee_pro: Optional[float] = Field(title='扣费比例')
    tran_pass: Optional[str] = Field(title='支付密码')
    invited_code: Optional[str] = Field(title='邀请码')

class PassWithdrawModel(BaseModel):
    withdraw_id: Optional[int] = Field(title='提现订单id')
    amount: Optional[int] = Field(title='提现金额，单位分')
    user_id: Optional[int] = Field(title='用户id')
    fee_type: Optional[int] = Field(title='扣费类型，1表示扣费倒锁定余额，2表示直接扣费', default=1)
    fee_pro: Optional[float] = Field(title='扣费比例')
    fee_balance: Optional[int] = Field(title='实际提现额(分)，有余数向整数加一，取整')
    deduct_balance: Optional[int] = Field(title='实际税费额(分)，有余数向整数加一，取整')

class MoneyPic(BaseModel):
    withdraw_id: Optional[int] = Field(title='提现订单id')
    money_pic: Optional[str] = Field(title='截图回传url')