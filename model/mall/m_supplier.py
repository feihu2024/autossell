from pydantic import BaseModel, Field
from typing import List, Optional
from model import m_schema, schema
from common import Dao
from datetime import datetime
from fastapi.exceptions import HTTPException


class ASupplierMsg(BaseModel):
    SSupplier: Optional[m_schema.SSupplier] = Field(title='商家信息')
    SSupplierState: Optional[m_schema.SSupplierState] = Field(title='商家状态')
    SSupplierAmount: Optional[m_schema.SSupplierAmount] = Field(title='商家账户')
    SSupplierOwner: Optional[m_schema.SSupplierOwner] = Field(title='商家负责人')
    SUser: Optional[m_schema.SUser] = Field(title='商家推荐人')
    SStoreCount: Optional[int] = Field(title='店铺数量')


class ASupplierMsgList(BaseModel):
    data: Optional[List[ASupplierMsg]] = Field(title='商家数据')
    total: Optional[int]


class ARecordMsg(BaseModel):
    SSupplierAmount: Optional[m_schema.SSupplierAmount] = Field(title='商家账户')
    SSupplierChangeType: Optional[m_schema.SSupplierChangeType] = Field(title='账户变动类型')
    SOrder: Optional[m_schema.SOrder] = Field(title='关联订单')
    SGood: Optional[m_schema.SGood] = Field(title='关联商品')
    SStore: Optional[m_schema.SStore] = Field(title='关联店铺')


class ARecordMsgList(BaseModel):
    data: Optional[List[ARecordMsg]] = Field(title='资金记录数据')
    total: Optional[int]


class ASupplierLicense(BaseModel):
    SSupplierOwner: Optional[m_schema.SSupplierOwner] = Field(title='商家负责人信息')
    SSupplierLicense: Optional[m_schema.FilterResSupplierLicense] = Field(title='商家资质信息')


class RSupplierMsgAdd(BaseModel):
    TSupplier: Optional[m_schema.SSupplier] = Field(title='商家信息')
    TSupplierOwner: Optional[m_schema.SSupplierOwner] = Field(title='商家负责人信息')
    # TSupplierLicense: Optional[List[m_schema.SSupplierLicense]] = Field(title='商家营业执照')


class RSupplierMsg(RSupplierMsgAdd):
    TSupplierState: Optional[m_schema.SSupplierState] = Field(title='商家状态  驳回？ 通过？')


class MSupplierMsg(RSupplierMsg):
    TSupplierLicense: Optional[List[m_schema.CreateSupplierLicense]] = Field(title='商家营业执照')


class CreateUser(BaseModel):
    username: Optional[str] = Field(title='用户名')
    email: Optional[str] = Field(title='邮箱')
    nickname: Optional[str] = Field(title='昵称')
    phone: Optional[str] = Field(title='联系方式')
    id_card: Optional[str] = Field(title='身份证')
    level_id: Optional[int] = Field(title='用户等级 默认是0粉丝,1会员,2核心会员,3小团长')
    status: Optional[int] = Field(title='0: 已实名   1: 未实名,被is_agree替代')
    register_time: Optional[datetime] = Field(title='注册时间')
    avatar: Optional[str] = Field(title='头像url')
    invited_user_id: Optional[int] = Field(title='邀请人id')
    coin: Optional[int] = Field(title='积分')
    gender: Optional[int] = Field(title='0:  男  1:  女')
    last_active_time: Optional[datetime] = Field(title='最近登录时间')
    name: Optional[str] = Field(title='用户名')
    is_agree: Optional[int] = Field(title='是否已经校验')
    parent_id: Optional[int] = Field(title='父级用户')
    parent_id_history: Optional[str] = Field(title='曾经的上级(ID之间逗号分隔)')
    level_one_time: Optional[datetime] = Field(title='升级he合伙人会员时间')
    level_two_time: Optional[datetime] = Field(title='升级老板会员时间')
    level_three_time: Optional[datetime] = Field(title='升级大老板会员时间')
    level_top_time: Optional[datetime] = Field(title='升级推广顶级时间')
    wholesale_id: Optional[int] = Field(title='代理商角色id，默认0不是代理，1区代2市代3省代')
    wholesale_amount: Optional[int] = Field(title='批发商品累计消费额')
    paidui: Optional[int] = Field(title='排队分次数')
    tuan_id: Optional[int] = Field(title='所属团id,0表示未入团人员,>0表示所属团长id')
    tran_pass: Optional[str] = Field(title='转账密码')
    invited_code: Optional[str] = Field(title='邀请码')
    bigorder_id: Optional[int] = Field(title='公排id')
    layer_id: Optional[int] = Field(title='行号(所在层数)')
    cur_layer_id: Optional[int] = Field(title='当前行号从左到右排序号')
    cur_layer_total: Optional[int] = Field(title='当前行排序总数量')
    bigorder_parent_id: Optional[int] = Field(title='上级对应序号')
    entrust_status: Optional[int] = Field(title='委托状态0未接受1托管中')
    light_status: Optional[int] = Field(title='熄灯状态0正常1熄灯')
    voucher_total: Optional[int] = Field(title='商品购买券数量')
    endorders_total: Optional[int] = Field(title='完成订单数量')
    doubule_id: Optional[int] = Field(title='是否分身大于0为分身id')

class SUser(CreateUser):
    id: int = Field(title='标识id')

    class Config:
        orm_mode = True

def get_user(user_id: int) -> Optional[SUser]:
    with Dao() as db:
        t = db.query(schema.TUser).where(schema.TUser.id == user_id).first()
        if t:
            return SUser.parse_obj(t.__dict__)
        else:
            return None
