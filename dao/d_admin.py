import time
import datetime
from common import Dao
from model import m_admin, m_schema
from config import SECRET
from jose import JWTError, jwt
from sqlalchemy import func, and_
from model.schema import TUser, TAdmin
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from dao import d_db, d_query, d_supplier
from pydantic import BaseModel, Field
from typing import List, Optional
# from service.wx_service import wxpayservice, wxpayservice_se

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def login_for_token(username: str, password: str):
    user = get_admin_by_username(username=username)
    if not user:
        return ''
    if user.password == password:
        data = {
            'user_id': user.id,
            'time': time.time() + SECRET.VALID_TIME
        }
        token = {'token_val': get_login_token_encode(data), 'user_id': user.id}
        #raise HTTPException(status_code=200, detail={'token': token, 'massage': 'Success'}, headers={"data": '123'})
        return token
    else:
        return ''

def login_shop_for_token(username: str, password: str):
    user = d_supplier.get_user_by_username(username=username)
    if not user:
        return ''
    if user.password == password:
        data = {
            'user_id': user.id,
            'time': time.time() + SECRET.VALID_TIME
        }
        token = {'token_val': get_login_token_encode(data), 'user_id': user.id}
        #raise HTTPException(status_code=200, detail={'token': token, 'massage': 'Success'}, headers={"data": '123'})
        return token
    else:
        return ''

def login_shop_token(username: str, password: str, user_id:int):
    data = {
        'user_id': user_id,
        'time': time.time() + SECRET.VALID_TIME
    }
    token = {'token_val': get_login_token_encode(data), 'user_id': user_id}
    return token

def get_login_token_encode(data:dict):
    return jwt.encode(data, SECRET.SECRET_KEY, algorithm=SECRET.ALGORITHM)

def get_login_token_decode(token:str):
    re_json = {}
    try:
        re_json = jwt.decode(token, SECRET.SECRET_KEY, algorithms=[SECRET.ALGORITHM])
    except Exception as e:
        print(e)
    return re_json

def is_login(token:str):
    data = get_login_token_decode(token)
    this_time = time.time()
    re_code = ''
    if data:
        if data.get('time') > this_time:
            data['time'] = this_time + SECRET.VALID_TIME
            re_code = get_login_token_encode(data)
    return re_code

def get_login_id(token:str):
    data = get_login_token_decode(token)
    this_time = time.time()
    re_code = 0
    if data:
        if data.get('time') > this_time:
            data['time'] = this_time + SECRET.VALID_TIME
            re_code = int(data['user_id'])
    return re_code

def get_admin_by_username(username: str):
    with Dao() as db:
        return db.query(m_admin.TAdmin).where(m_admin.TAdmin.username == username).first()


class this_CreateAdmin(BaseModel):
    username: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    level_id: Optional[int]
    id_card: Optional[str]
    gender: Optional[str]
    register_time: Optional[datetime.datetime] = Field(title='创建时间')
    last_active_time: Optional[datetime.datetime]
    status: Optional[str]
    business_id: Optional[int] = Field(title='商家ID_busiess_content')
    admin_id: Optional[int] = Field(title='所属商家管理id')
    user_pic: Optional[str] = Field(title='头像url')
    user_info: Optional[str] = Field(title='用户备注')


class this_SAdmin(this_CreateAdmin):
    id: int

    class Config:
        orm_mode = True

def get_admin_by_id(admin_id: int) -> Optional[this_SAdmin]:
    # with Dao() as db:
    #     return db.query(TAdmin).where(TAdmin.id == admin_id).first()
    with Dao() as db:
        t = db.query(TAdmin).where(TAdmin.id == admin_id).first()
        if t:
            return this_SAdmin.parse_obj(t.__dict__)
        else:
            return None

def get_admin_by_businessid(busid: int):
    with Dao() as db:
        return db.query(TAdmin).where(TAdmin.business_id == busid).first()
def update_admin_info(data: m_admin.ShoperModel):
    with Dao() as db:
        re = db.query(TAdmin).where(TAdmin.business_id == data.modid).update({"username": data.username, "password":data.passwd, "level_id": data.level})
        db.commit()
        return re

def add_admin_info(data: m_admin.ShoperModel):
    add_admin = TAdmin(
        username=data.username,
        password=data.passwd,
        level_id=data.level,
        register_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        business_id=data.modid
    )
    with Dao() as db:
        db.add(add_admin)
        db.commit()

def query_users() -> m_admin.UserData:
    time_now = datetime.datetime.now()
    with Dao() as db:
        # 统计会员总量
        total_num = db.query(TUser).count()

        # 根据时间条件统计日增长活跃用户数量
        daily_add = db.query(TUser).filter(TUser.register_time >= time_now - datetime.timedelta(days=1)).count()

        # 根据最后登录时间统计活跃数量
        active_num = db.query(TUser).where(TUser.last_active_time >= time_now - datetime.timedelta(days=5)).count()

        # 根据性别条件统计男性用户的数量
        male = db.query(TUser).where(TUser.gender == 'male').count()
        # 根据性别条件统计女性用户的数量
        female = db.query(TUser).where(TUser.gender == 'female').count()

        # 计算男女用户的占比
        male_ratio: float = male / (male + female)
        female_ratio: float = female / (male + female)

        return m_admin.UserData(num=total_num, daily_add=daily_add,
                                active=active_num, male_ratio=male_ratio, female_ratio=female_ratio)


def silent_users(page: int = 1, page_size: int = 10):
    """根据最后登录时间统计非活跃用户"""
    time_now = datetime.datetime.now()
    with Dao() as db:
        silents = db.query(TUser). \
            where(TUser.last_active_time < time_now - datetime.timedelta(days=10)). \
            offset((page - 1) * page_size).limit(page_size).all()

        return silents


def query_daily_add(day: datetime.datetime.date) -> int:
    zero_time = datetime.time()
    zero_day = datetime.datetime.combine(day, zero_time)
    time_condition = and_(TUser.register_time >= zero_day,
                          TUser.register_time <= zero_day + datetime.timedelta(days=1))
    with Dao() as db:
        num = db.query(TUser).where(time_condition).count()
        db.commit()
        return num

def add_shoper_service(data:m_admin.AddShoper):
    res = d_db.insert_business_content(item=m_schema.CreateBusinessContent(
        business_code=data.business_code
    ))
    return res
#
# def applyment_submit_lowsir(out_request_no, organization_type, finance_institution, id_holder_type, id_doc_type, merchant_shortname, business_license_info, id_card_info, account_info, contact_info, sales_scene_info, finance_institution_info = None, ubo_info_list = None, id_doc_info=None, owner=True, authorize_letter_copy = None, settlement_info=None, qualifications=None, business_addition_pics=None, business_addition_desc=None):
#     """提交申请单
#         https://pay.weixin.qq.com/wiki/doc/apiv3_partner/apis/chapter7_1_1.shtml
#         请求URL：https://api.mch.weixin.qq.com/v3/ecommerce/applyments/
#         :param out_request_no: 业务申请编号，必填，示例值:'APPLYMENT_00000000001'
#         :param organization_type: 主体类型，必填, 示例值：2
#         :param finance_institution: 是否金融机构	，条件选填， 示例值：true
#         :param id_holder_type: 证件持有人类型	，条件选填， 示例值：LEGAL
#         :param id_doc_type: 经营者/法人证件类型，条件选填， 示例值：IDENTIFICATION_TYPE_MAINLAND_IDCARD
#         :param authorize_letter_copy: 法定代表人说明函，条件选填， 示例值：47ZC6GC-vnrbEny_Ie_An5-tCpqxucuxi-vByf3Gjm7KEIUv0OF4wFNIO4kqg05InE4d2I6_H7I4
#         :param owner: 经营者/法人是否为受益人，条件选填， 示例值：true
#         :param merchant_shortname: 商户简称	，必填， 示例值：腾讯
#         :param business_license_info: 营业执照/登记证书信息，条件选填， 示例值："business_license_info": {
#             "business_license_copy": "47ZC6GC-vnrbEny__Ie_An5-tCpqxucuxi-vByf3Gjm7KE53JXvGy9tqZm2XAUf-4KGprrKhpVBDIUv0OF4wFNIO4kqg05InE4d2I6_H7I4",
#             "business_license_number": "123456789012345678",
#             "business_time": "[\"2020-04-24\",\"长期\"]",
#             "cert_type": "CERTIFICATE_TYPE_2388",
#             "company_address": "深圳南山区科苑路",
#             "legal_person": "张三",
#             "merchant_name": "腾讯科技有限公司"
#         },
#         :param finance_institution_info: 金融机构许可证信息，条件选填， 示例值："finance_institution_info": {
#             "finance_license_pics": ["47ZC6GC-vnrbEny__Ie_An5-tCpqxucuxi-vByf3Gjm7KE53JXvGy9tqZm2XAUf-4KGprrKhpVBDIUv0OF4wFNIO4kqg05InE4d2I6_H7I4"],
#             "finance_type": "BANK_AGENT"
#         },
#         :param id_card_info: 经营者/法人身份证信息，条件选填， 示例值："id_card_info": {
#             "id_card_address": "AOZdYGISxo4y44/UgZ69bdu9X+tfMUJ9dl+LetjM45/zMbrYu+wWZ8gn4CTdo+D/m9MrPg+V4sm73oxqdQu/hj7aWyDl4GQtPXVdaztB9jVbVZh3QFzV+BEmytMNQp9dt1uWJktlfdDdLR3AMWyMB377xd+m9bSr/ioDTzagEcGe+vLYiKrzcroQv3OR0p3ppFYoQ3IfYeU/04S4t9rNFL+kyblK2FCCqQ11NdbbHoCrJc7NV4oASq6ZFonjTtgjjgKsadIKHXtb3JZKGZjduGdtkRJJp0/0eow96uY1Pk7Rq79Jtt7+I8juwEc4P4TG5xzchG/5IL9DBd+Z0zZXkw==",
#             "id_card_copy": "jTpGmxUX3FBWVQ5NJTZvlKX_gdU4cRz7z5NxpnFuAxhBTEO_PvWkfSCJ3zVIn001D8daLC-ehEuo0BJqRTvDujqhThn4ReFxikqJ5YW6zFQ",
#             "id_card_name": "pVd1HJ6zyvPedzGaV+X3qtmrq9bb9tPROvwia4ibL+F6mfjbzQIzfb3HHLEjZ4YiR/cJiCrZxnAqi+pjeKIEdkwzXRAI7FUhrfPK3SNjaBTEu9GmsugMIA9r3x887Q+ODuC8HH2nzAn7NGpE/e3yiHgWhk0ps5k5DP/2qIdGdONoDzZelrxCl/NWWNUyB93K9F+jC1JX2IMttdY+aQ6zBlw0xnOiNW6Hzy7UtC+xriudjD5APomty7/mYNxLMpRSvWKIjOv/69bDnuC4EL5Kz4jBHLiCyOb+tI0m2qhZ9evAM+Jv1z0NVa8MRtelw/wDa4SzfeespQO/0kjiwfqdfg==",
#             "id_card_national": "47ZC6GC-vnrbEny__Ie_An5-tCpqxucuxi-vByf3Gjm7KE53JXvGy9tqZm2XAUf-4KGprrKhpVBDIUv0OF4wFNIO4kqg05InE4d2I6_H7I4",
#             "id_card_number": "AOZdYGISxo4y44/UgZ69bdu9X+tfMUJ9dl+LetjM45/zMbrYu+wWZ8gn4CTdo+D/m9MrPg+V4sm73oxqdQu/hj7aWyDl4GQtPXVdaztB9jVbVZh3QFzV+BEmytMNQp9dt1uWJktlfdDdLR3AMWyMB377xd+m9bSr/ioDTzagEcGe+vLYiKrzcroQv3OR0p3ppFYoQ3IfYeU/04S4t9rNFL+kyblK2FCCqQ11NdbbHoCrJc7NV4oASq6ZFonjTtgjjgKsadIKHXtb3JZKGZjduGdtkRJJp0/0eow96uY1Pk7Rq79Jtt7+I8juwEc4P4TG5xzchG/5IL9DBd+Z0zZXkw==",
#             "id_card_valid_time": "2026-06-06",
#             "id_card_valid_time_begin": "2019-06-06"
#         },
#         :param id_doc_info: 经营者/法人其他类型证件信息，条件选填， 示例值："id_doc_info": {
#             "doc_period_begin": "2019-06-06",
#             "doc_period_end": "2020-01-02",
#             "id_doc_address": "jTpGmxUX3FBWVQ5NJTZvlKX_gdU4cRz7z5NxpnFuAxhBTEO_PvWkfSCJ3zVIn001D8daLC-ehEuo0BJqRTvDujqhThn4ReFxikqJ5YW6zFQ",
#             "id_doc_copy": "47ZC6GC-vnrbEny__Ie_An5-tCpqxucuxi-vByf3Gjm7KE53JXvGy9tqZm2XAUf-4KGprrKhpVBDIUv0OF4wFNIO4kqg05InE4d2I6_H7I4",
#             "id_doc_copy_back": "47ZC6GC-vnrbEny__Ie_An5-tCpqxucuxi-vByf3Gjm7KE53JXvGy9tqZm2XAUf-4KGprrKhpVBDIUv0OF4wFNIO4kqg05InE4d2I6_H7I4",
#             "id_doc_name": "jTpGmxUX3FBWVQ5NJTZvlKX_gdU4cRz7z5NxpnFuAxhBTEO_PvWkfSCJ3zVIn001D8daLC-ehEuo0BJqRTvDujqhThn4ReFxikqJ5YW6zFQ",
#             "id_doc_number": "jTpGmxUX3FBWVQ5NJTZvlKX_gdU4cRz7z5NxpnFuAxhBTEO_PvWkfSCJ3zVIn001D8daLC-ehEuo0BJqRTvDujqhThn4ReFxikqJ5YW6zFQ"
#         },
#         :param ubo_info_list: 最终受益人信息列表，条件选填， 示例值："ubo_info_list": [{
#             "ubo_id_doc_address": "pVd1HJ6zyvPedzGaV+X3qtmrq9bb9tPROvwia4ibL+F6mfjbzQIzfb3HHLEjZ4YiR/cJiCrZxnAqi+pjeKIEdkwzXRAI7FUhrfPK3SNjaBTEu9GmsugMIA9r3x887Q+ODuC8HH2nzAn7NGpE/e3yiHgWhk0ps5k5DP/2qIdGdONoDzZelrxCl/NWWNUyB93K9F+jC1JX2IMttdY+aQ6zBlw0xnOiNW6Hzy7UtC+xriudjD5APomty7/mYNxLMpRSvWKIjOv/69bDnuC4EL5Kz4jBHLiCyOb+tI0m2qhZ9evAM+Jv1z0NVa8MRtelw/wDa4SzfeespQO/0kjiwfqdfg==",
#             "ubo_id_doc_copy": "jTpGmxUXqRTvDujqhThn4ReFxikqJ5YW6zFQ",
#             "ubo_id_doc_copy_back": "jTpGmxUX3FBWVQ5NJTZvvDujqhThn4ReFxikqJ5YW6zFQ",
#             "ubo_id_doc_name": "AOZdYGISxo4y44/Ug4P4TG5xzchG/5IL9DBd+Z0zZXkw==",
#             "ubo_id_doc_number": "AOZdYGISxo4y44/Ug4P4TG5xzchG/5IL9DBd+Z0zZXkw==",
#             "ubo_id_doc_period_begin": "2019-06-06",
#             "ubo_id_doc_period_end": "2026-06-06",
#             "ubo_id_doc_type": "IDENTIFICATION_TYPE_MAINLAND_IDCARD"
#         }],
#         :param account_info: 结算账户信息，必填， 示例值："account_info": {
#             "account_bank": "工商银行",
#             "account_name": "AOZdYGISxo4y44/UgZ69bdu9X+tfMUJ9dl+LetjM45/zMbrYu+wWZ8gn4CTdo+D/m9MrPg+V4sm73oxqdQu/hj7aWyDl45IL9DBd+Z0zZXkw==",
#             "account_number": "d+xT+MQCvrLHUVDWv/8MR/dB7TkXM2YYZlokmXzFsWs35NXUot7C0NcxIrUF5FnxqCJHkNgKtxa6RxEYyba1+VBRLnqKGYQE8ZRGYoeorwC+w==",
#             "bank_account_type": "75",
#             "bank_address_code": "110000",
#             "bank_branch_id": "402713354941"
#         },
#         :param contact_info: 超级管理员信息	，必填， 示例值："contact_info": {
#             "business_authorization_letter": "47ZC6GC-vnrbEny_Ie_An5-tCpqxucuxi-vByf3Gjm7KEIUv0OF4wFNIO4kqg05InE4d2I6_H7I4",
#             "contact_email": "pVd1HJ6zyvPedzGaV+X3qtmrq9bb9tPROvwia4ibL+F6mfjbzQIzfb3HHLEjZ4YiR/cJiCrZxnAqi+pjeKIEdkwzXRAI7FUhrfPK3SNjaBTEu9GmsugMIA9r3x887Q+ODuC8HH2nzAn7NGpE/e3yiHgWhk0ps5k5DP/2qIdGdONoDzZelrxCl/NWWNUyB93K9F+jC1JX2IMttdY+aQ6zBlw0xnOiNW6Hzy7UtC+xriudjD5APomty7/mYNxLMpRSvWKIjOv/69bDnuC4EL5Kz4jBHLiCyOb+tI0m2qhZ9evAM+Jv1z0NVa8MRtelw/wDa4SzfeespQO/0kjiwfqdfg==",
#             "contact_id_card_number": "pVd1HJ6zyvPedzGaV+X3qtmrq9bb9tPROvwia4ibL+F6mfjbzQIzfb3HHLEjZ4YiR/cJiCrZxnAqi+pjeKIEdkwzXRAI7FUhrfPK3SNjaBTEu9GmsugMIA9r3x887Q+ODuC8HH2nzAn7NGpE/e3yiHgWhk0ps5k5DP/2qIdGdONoDzZelrxCl/NWWNUyB93K9F+jC1JX2IMttdY+aQ6zBlw0xnOiNW6Hzy7UtC+xriudjD5APomty7/mYNxLMpRSvWKIjOv/69bDnuC4EL5Kz4jBHLiCyOb+tI0m2qhZ9evAM+Jv1z0NVa8MRtelw/wDa4SzfeespQO/0kjiwfqdfg==",
#             "contact_id_doc_copy": "jTpGmxUX3FBWVQ5NJTZvvDujqhThn4ReFxikqJ5YW6zFQ",
#             "contact_id_doc_copy_back": "jTpGmxUX3FBWVQ5NJTZvvDujqhThn4ReFxikqJ5YW6zFQ",
#             "contact_id_doc_period_begin": "2019-06-06",
#             "contact_id_doc_period_end": "2026-06-06",
#             "contact_id_doc_type": "IDENTIFICATION_TYPE_MACAO",
#             "contact_name": "pVd1HJ6zyvPedzGaV+X3qtmrq9bb9tPROvwia4ibL+F6mfjbzQIzfb3HHLEjZ4YiR/cJiCrZxnAqi+pjeKIEdkwzXRAI7FUhrfPK3SNjaBTEu9GmsugMIA9r3x887Q+ODuC8HH2nzAn7NGpE/e3yiHgWhk0ps5k5DP/2qIdGdONoDzZelrxCl/NWWNUyB93K9F+jC1JX2IMttdY+aQ6zBlw0xnOiNW6Hzy7UtC+xriudjD5APomty7/mYNxLMpRSvWKIjOv/69bDnuC4EL5Kz4jBHLiCyOb+tI0m2qhZ9evAM+Jv1z0NVa8MRtelw/wDa4SzfeespQO/0kjiwfqdfg==",
#             "contact_type": "65",
#             "mobile_phone": "pVd1HJ6zyvPedzGaV+X3qtmrq9bb9tPROvwia4ibL+F6mfjbzQIzfb3HHLEjZ4YiR/cJiCrZxnAqi+pjeKIEdkwzXRAI7FUhrfPK3SNjaBTEu9GmsugMIA9r3x887Q+ODuC8HH2nzAn7NGpE/e3yiHgWhk0ps5k5DP/2qIdGdONoDzZelrxCl/NWWNUyB93K9F+jC1JX2IMttdY+aQ6zBlw0xnOiNW6Hzy7UtC+xriudjD5APomty7/mYNxLMpRSvWKIjOv/69bDnuC4EL5Kz4jBHLiCyOb+tI0m2qhZ9evAM+Jv1z0NVa8MRtelw/wDa4SzfeespQO/0kjiwfqdfg=="
#         },
#         :param sales_scene_info: 店铺信息，必填， 示例值："sales_scene_info": {
#             "mini_program_sub_appid": "wxa123344545577",
#             "store_name": "爱烧烤",
#             "store_qr_code": "jTpGmxUX3FBWVQ5NJTZvlKX_gdU4cRz7z5NxpnFuAxhBTEO_PvWkfSCJ3zVIn001D8daLC-ehEuo0BJqRTvDujqhThn4ReFxikqJ5YW6zFQ"
#         },
#         :param settlement_info: 结算规则，非必填， 示例值："settlement_info": {
#             "qualification_type": "零售批发/生活娱乐/其他",
#             "settlement_id": 719
#         },
#         :param qualifications: 特殊资质，非必填， 示例值：[\"jTpGmxUX3FBWVQ5NJInE4d2I6_H7I4\"]
#         :param business_addition_pics: 补充材料，非必填， 示例值：[\"jTpGmg05InE4d2I6_H7I4\"]
#         :param business_addition_desc: 补充说明，非必填， 示例值：特殊情况，说明原因
#         """
#
#     params = {}
#     if out_request_no:
#         params.update({'out_request_no': out_request_no})
#     else:
#         raise Exception('out_request_no is not assigned.')
#     organization_type = "2"  # 2：企业，营业执照上的主体类型一般为有限公司、有限责任公司。
#     if organization_type:
#         params.update({'organization_type': organization_type})
#     else:
#         raise Exception('organization_type is not assigned.')
#     if merchant_shortname:
#         params.update({'merchant_shortname': merchant_shortname})
#     else:
#         raise Exception('merchant_shortname is not assigned.')
#
#     if finance_institution:
#         params.update({'finance_institution': finance_institution})
#     if id_holder_type:
#         params.update({'id_holder_type': id_holder_type})
#     if id_doc_type:
#         params.update({'id_doc_type': id_doc_type})
#     if authorize_letter_copy:
#         params.update({'authorize_letter_copy': authorize_letter_copy})
#     if owner:
#         params.update({'owner': owner})
#     if qualifications:
#         params.update({'qualifications': qualifications})
#     if business_addition_pics:
#         params.update({'business_addition_pics': business_addition_pics})
#     if business_addition_desc:
#         params.update({'business_addition_desc': business_addition_desc})
#
#     #营业执照
#     if business_license_info:
#         params.update({'business_license_info': business_license_info})
#     #当证件持有人类型为经营者/法人且证件类型为“身份证”时填写
#     if id_card_info:
#         id_card_info['id_card_name'] = wxpayservice_se._core.encrypt(id_card_info['id_card_name'])
#         id_card_info['id_card_number'] = wxpayservice_se._core.encrypt(id_card_info['id_card_number'])
#         id_card_info['id_card_address'] = wxpayservice_se._core.encrypt(id_card_info['id_card_address'])
#         params.update({'id_card_info': id_card_info})
#     #结算账户信息 商家提现收款的银行账户信息
#     if account_info:
#         account_info['account_name'] = wxpayservice_se._core.encrypt(account_info['account_name'])
#         account_info['account_number'] = wxpayservice_se._core.encrypt(account_info['account_number'])
#         params.update({'account_info': account_info})
#     #店铺的超级管理员信息
#     if contact_info:
#         contact_info['contact_name'] = wxpayservice_se._core.encrypt(contact_info['contact_name'])
#         contact_info['contact_id_card_number'] = wxpayservice_se._core.encrypt(contact_info['contact_id_card_number'])
#         contact_info['mobile_phone'] = wxpayservice_se._core.encrypt(contact_info['mobile_phone'])
#         contact_info['contact_email'] = wxpayservice_se._core.encrypt(contact_info['contact_email'])
#         params.update({'contact_info': contact_info})
#     #店铺信息
#     if sales_scene_info:
#         params.update({'sales_scene_info': sales_scene_info})
#
#     path = '/v3/ecommerce/applyments/'
#
#     # return wxpayservice._core.request(path, method=RequestType.POST, data=params, cipher_data=True)
#     return wxpayservice_se._core.request(path, data=params, cipher_data=True)

