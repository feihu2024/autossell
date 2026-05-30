from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy import Column, Float, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

router = APIRouter()


class TAdmin(Base):
    __tablename__ = 't_admin'

    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String(45))
    gender = Column(String(20))
    email = Column(String(45))
    password = Column(String(45))
    phone = Column(String(45))
    id_card = Column(String(45))
    level_id = Column(Integer)
    status = Column(String(20))
    register_time = Column(TIMESTAMP, comment='in seconds')
    last_active_time = Column(TIMESTAMP, comment='最后登录时间')


class UserData(BaseModel):
    num: Optional[int] = Field(title='会员总数')
    daily_add: Optional[int] = Field(title='当日新增')
    active: Optional[int] = Field(title='活跃用户')
    male_ratio: Optional[float] = Field(title='男性占比')
    female_ratio: Optional[float] = Field(title='女性占比')


class InactiveUser(BaseModel):
    username: Optional[str]
    email: Optional[str]
    nickname: Optional[str] = Field(title='昵称')
    phone: Optional[str]
    id_card: Optional[str] = Field(title='身份证')
    level_id: Optional[int] = Field(title='等级')
    status: Optional[str]
    register_time: Optional[datetime] = Field(title='in seconds')
    avatar: Optional[str]


class SaleData(BaseModel):
    total_sale: Optional[int] = Field(title='商品销售总额')
    income: Optional[int] = Field(title='销售收益')
    current_sale: Optional[int] = Field(title='当日销售总额')
    flash_sale: Optional[int] = Field(title='总秒杀价值', default=6000)
    cost: Optional[int] = Field(title='兑付成本', default=1500)


class AdminRequest(BaseModel):
    username: str = Field(title='管理员账号', default='admin')
    password: str

class AddShoper(BaseModel):
    business_code: str = Field(title='业务申请编号', default='')

class AddManager(BaseModel):
    mod_id: Optional[int] = Field(title='进件表id', default=0)
    select_contact_type:Optional[str] =  Field(title='超级管理员类型', default='')
    contact_name: Optional[str] = Field(title='超级管理员姓名', default='')
    select_contact_id_doc_type: Optional[str] =  Field(title='超级管理员证件类型', default='')
    contact_id_number: Optional[str] = Field(title='超级管理员身份证件号码', default='')
    contact_id_doc_copy: Optional[str] = Field(title='超级管理员证件正面照片', default='')
    contact_id_doc_copy_wx: Optional[str] = Field(title='超级管理员证件正面照片微信media_id', default='')
    contact_id_doc_copy_back: Optional[str] = Field(title='超级管理员证件反面照片', default='')
    contact_id_doc_copy_back_wx: Optional[str] = Field(title='超级管理员证件反面照片微信media_id', default='')
    contact_period_begin: Optional[datetime] = Field(title='超级管理员证件有效期开始时间', default='')
    contact_period_end: Optional[datetime] = Field(title='超级管理员证件有效期结束时间', default='')
    contact_period_end_long: Optional[int] = Field(title='证件是否长期有效', default=0)
    business_authorization_letter: Optional[str] = Field(title='业务办理授权函', default='')
    business_authorization_letter_wx: Optional[str] = Field(title='业务办理授权函微信media_id', default='')
    openid: Optional[str] = Field(title='超级管理员微信OpenID', default='')
    mobile_phone: Optional[str] = Field(title='联系手机', default='')
    contact_email: Optional[str] = Field(title='联系邮箱', default='')
    contact_license_info: Optional[int] = Field(title='超管license表ID, 授权函license_copy_other1', default=0)

class AddShouyi(BaseModel):
    mod_id: Optional[int] = Field(title='license表ID', default=0)
    id_doc_type: Optional[str] = Field(title='证件类型', default='')
    id_card_copy: Optional[str] = Field(title='身份证人像面照片', default='')
    id_card_copy_wx: Optional[str] = Field(title='身份证人像面照片wx', default='')
    id_card_national: Optional[str] = Field(title='身份证国徽面照片', default='')
    id_card_national_wx: Optional[str] = Field(title='身份证国徽面照片wx', default='')
    id_card_name: Optional[str] = Field(title='身份证姓名', default='')
    id_card_number: Optional[str] = Field(title='身份证号码', default='')
    id_card_address: Optional[str] = Field(title='身份证居住地址', default='')
    id_card_period_begin: Optional[datetime] = Field(title='身份证有效期开始时间', default='')
    id_card_period_end: Optional[datetime] = Field(title='身份证有效期结束时间', default='')
    id_card_period_end_long: Optional[int] = Field(title='证件是否长期有效', default=0)

class AddBody(BaseModel):
    mod_id: Optional[int] = Field(title='进件表id', default=0)
    subject_business_license_info: Optional[int] = Field(title='营业执照license表ID', default=0)
    subject_certificate_info: Optional[int] = Field(title='登记证书license表ID', default=0)
    subject_certificate_letter_copy: Optional[int] = Field(title='单位证明函照片license表ID', default=0)
    subject_finance_institution_info: Optional[int] = Field(title='金融机构许可证信息license表ID', default=0)
    subject_identity_info: Optional[int] = Field(title='经营者 / 法人身份证件license表ID', default=0)
    select_subject_type: Optional[str] =  Field(title='主体类型', default='')
    finance_institution: Optional[int] = Field(title='是否是金融机构', default=0)
    li_license_copy: Optional[str] =  Field(title='营业执照照片', default='')
    li_license_copy_wx: Optional[str] =  Field(title='营业执照照片wx', default='')

    li_license_number: Optional[str] =  Field(title='营业执照, 注册号 / 统一社会信用代码', default='')
    li_merchant_name: Optional[str] =  Field(title='营业执照, 商户名称', default='')
    li_legal_person: Optional[str] =  Field(title='营业执照, 个体户经营者 / 法人姓名', default='')
    li_license_address: Optional[str] =  Field(title='营业执照, 注册地址', default='')
    li_period_begin: Optional[datetime] = Field(title='营业执照, 有效期限开始日期', default='')
    li_period_end: Optional[datetime] = Field(title='营业执照, 有效期限结束日期', default='')
    li_period_end_long: Optional[int] = Field(title='证件是否长期有效', default=0)
    ce_cert_copy: Optional[str] =  Field(title='登记证书照片', default='')
    ce_cert_copy_wx: Optional[str] =  Field(title='登记证书照片wx', default='')

    ce_cert_type: Optional[str] =  Field(title='登记证书类型', default='')
    ce_cert_number: Optional[str] =  Field(title='登记证书, 证书号', default='')
    ce_merchant_name: Optional[str] =  Field(title='登记证书, 商户名称', default='')
    ce_company_address: Optional[str] =  Field(title='登记证书, 注册地址', default='')
    ce_legal_person: Optional[str] =  Field(title='登记证书, 法定代表人', default='')
    ce_period_begin: Optional[datetime] = Field(title='登记证书, 有效期限开始日期', default='')
    ce_period_end:Optional[datetime] = Field(title='登记证书, 有有效期限结束日期', default='')
    ce_certificate_letter_copy: Optional[str] =  Field(title='单位证明函照片', default='')
    ce_certificate_letter_copy_wx: Optional[str] =  Field(title='单位证明函照片wx', default='')

    fi_finance_type: Optional[str] =  Field(title='金融机构类型', default='')
    fi_finance_license_pics: Optional[str] =  Field(title='金融机构许可证图片', default='')
    fi_finance_license_pics_wx: Optional[str] =  Field(title='金融机构许可证图片wx', default='')

    id_holder_type: Optional[str] = Field(title='法人证件, 证件持有人类型', default='')
    id_doc_type: Optional[str] = Field(title='法人证件, 证件类型', default='')
    id_authorize_letter_copy: Optional[str] = Field(title='法人证件, 法定代表人说明函', default='')
    id_authorize_letter_copy_wx: Optional[str] = Field(title='法人证件, 法定代表人说明函wx', default='')
    id_card_copy: Optional[str] = Field(title='法人证件, 身份证人像面照片', default='')
    id_card_copy_wx: Optional[str] = Field(title='法人证件, 身份证人像面照片wx', default='')
    id_card_national: Optional[str] = Field(title='法人证件, 身份证国徽面照片', default='')
    id_card_national_wx: Optional[str] = Field(title='法人证件, 身份证国徽面照片wx', default='')
    id_card_name: Optional[str] = Field(title='法人证件, 身份证姓名', default='')
    id_card_number: Optional[str] = Field(title='法人证件, 身份证号码', default='')
    id_card_address: Optional[str] = Field(title='法人证件, 身份证居住地址', default='')
    id_card_period_begin: Optional[datetime] = Field(title='法人证件, 身份证有效期开始时间', default='')
    id_card_period_end: Optional[datetime] = Field(title='法人证件, 身份证有效期结束时间', default='')

    id_doc_copy: Optional[str] = Field(title='法人证件, 证件正面照片', default='')
    id_doc_copy_back: Optional[str] = Field(title='法人证件, 证件反面照片', default='')
    id_doc_name: Optional[str] = Field(title='法人证件, 证件姓名', default='')
    id_doc_number: Optional[str] = Field(title='法人证件, 证件号码', default='')
    id_doc_address: Optional[str] = Field(title='法人证件, 证件居住地址', default='')
    id_doc_period_begin: Optional[datetime] = Field(title='法人证件, 证件有效期开始时间', default='')
    id_doc_period_end:  Optional[datetime] = Field(title='法人证件, 证件有效期结束时间', default='')
    id_owner: Optional[int] = Field(title='法人是否为受益人', default=1)
    # id_owner: ""  # 法人证件, 经营者 / 法人是否为受益人
    # id_ubo_info_list: []  # 最终受益人信息列表(UBO)

class AddBuy(BaseModel):
    mod_id: Optional[int] = Field(title='进件表id', default=0)
    sales_biz_store_info: Optional[int] = Field(title='线下场所场景license表ID', default=0)
    sales_mp_info: Optional[int] = Field(title='公众号场景license表ID', default=0)
    sales_mini_program_info: Optional[int] = Field(title='小程序场景license表ID', default=0)
    sales_app_info: Optional[int] = Field(title='App场景license表ID', default=0)
    sales_web_info: Optional[int] = Field(title='互联网网站场景license表ID', default=0)
    sales_wework_info: Optional[int] = Field(title='企业微信场景license表ID', default=0)
    merchant_shortname: Optional[str] = Field(title='商户简称', default='')
    service_phone: Optional[str] = Field(title='客服电话', default='')
    sales_scenes_type: Optional[str] = Field(title='经营场景类型', default='')
    biz_store_name: Optional[str] = Field(title='线下场所名称', default='')
    biz_address_code: Optional[str] = Field(title='线下场所省市编码', default='')
    biz_store_address: Optional[str] = Field(title='线下场所地址', default='')
    biz_store_entrance_pic: Optional[str] = Field(title='线下场所门头照片', default='')
    biz_store_entrance_pic_wx: Optional[str] = Field(title='微信id', default='')
    biz_indoor_pic: Optional[str] = Field(title='线下场所内部照片', default='')
    biz_indoor_pic_wx: Optional[str] = Field(title='微信id', default='')
    biz_sub_appid: Optional[str] = Field(title='线下场所对应的商家AppID', default='')
    mp_appid: Optional[str] = Field(title='服务商公众号AppID', default='')
    mp_sub_appid: Optional[str] = Field(title='商家公众号AppID', default='')
    mp_pics: Optional[str] = Field(title='公众号页面截图, 请提供展示商品 / 服务的页面截图 / 设计稿（最多5张），若公众号未建设完善或未上线请务必提供。', default='')
    mini_program_appid: Optional[str] = Field(title='服务商小程序APPID', default='')
    mini_program_sub_appid: Optional[str] = Field(title='商家小程序APPID', default='')
    mini_program_pics: Optional[str] = Field(title='小程序截图, 请提供展示商品 / 服务的页面截图 / 设计稿（最多5张），若小程序未建设完善或未上线', default='')
    app_appid: Optional[str] = Field(title='服务商应用APPID', default='')
    app_sub_appid: Optional[str] = Field(title='商家应用APPID', default='')
    app_pics: Optional[str] = Field(title='APP截图', default='')
    web_domain: Optional[str] = Field(title='互联网网站域名', default='')
    web_authorisation: Optional[str] = Field(title='网站授权函', default='')
    web_authorisation_wx: Optional[str] = Field(title='微信id', default='')
    web_appid: Optional[str] = Field(title='互联网网站对应的商家APPID', default='')
    sub_corp_id: Optional[str] = Field(title='商家企业微信CorpID', default='')
    sub_wework_pics: Optional[str] = Field(title='企业微信页面截图, 最多可上传5张照片', default='')

class AddBank(BaseModel):
    mod_id: Optional[int] = Field(title='进件表id', default=0)
    bank_account_type: Optional[str] = Field(title='账户类型', default='')
    account_name: Optional[str] = Field(title='开户名称', default='')
    account_bank: Optional[str] = Field(title='开户银行', default='')
    bank_address_code: Optional[str] = Field(title='开户银行省市编码', default='')
    bank_branch_id: Optional[str] = Field(title='开户银行联行号', default='')
    bank_name: Optional[str] = Field(title='开户银行全称（含支行）', default='')
    account_number: Optional[str] = Field(title='银行账号', default='')

class ShoperModel(BaseModel):
    modid: Optional[int] = Field(title='商家id', default=0)
    username: Optional[str] = Field(title='用户名称', default='')
    passwd: Optional[str] = Field(title='用户密码', default='')
    level: Optional[int] = Field(title='商家类型', default=0)

class SdAgent(BaseModel):
    user_id: Optional[int] = Field(title='用户id', default=0)
    sd_agent: Optional[int] = Field(title='市代设置', default=0)