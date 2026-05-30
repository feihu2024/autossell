from fastapi import APIRouter
from dao import d_admin, d_user, d_groupsir, d_order, d_db
import datetime, logging, json
from model import schema, m_schema
from common import Dao, global_define
# from fastapi.responses import JSONResponse
# from fastapi import HTTPException
from model.m_admin import AddShoper, AddManager, AddBody, AddBuy, AddBank, ShoperModel, TAdmin
# from service.wx_service import wxpayservice


router = APIRouter()

@router.post(f'/add_shoper', summary='创建服务商')
async def add_shoper(data: AddShoper):
    if len(data.business_code) > 0:
        return d_admin.add_shoper_service(data)
    else:
        return {"msg": "未知数据"}

@router.post(f'/save_manager', summary='保存超级管理员')
async def save_manager(data: AddManager):
    #license表 创建、保存处理
    contact_license_info = data.contact_license_info
    if data.contact_license_info > 0:
        d_db.update_business_license(item=m_schema.SBusinessLicense(
            id=contact_license_info,
            business_id=data.mod_id,
            # lic_type=global_define.lic_type['contact'],
            # lic_type_name=global_define.lic_type_name[0],
            lic_number=data.contact_id_number,  # 证件号码
            lic_copy=data.contact_id_doc_copy,  # 超级管理员证件正面照片
            lic_copy_wx=data.contact_id_doc_copy_wx,  # 超级管理员证件正面照片微信media_id
            lic_copy_back=data.contact_id_doc_copy_back,  # 超级管理员证件反面照片
            lic_copy_back_wx=data.contact_id_doc_copy_back_wx,  # 超级管理员证件反面照片微信media_id
            lic_period_begin=data.contact_period_begin,  # 超级管理员证件有效期开始时间
            lic_period_end=data.contact_period_end,  # 超级管理员证件有效期结束时间
            lic_period_end_long = data.contact_period_end_long,  #证件长期有效
            lic_copy_other1=data.business_authorization_letter,  # 业务办理授权函
            lic_copy_other1_wx=data.business_authorization_letter_wx  # 业务办理授权函微信
        ))
    else:
        # if len(data.contact_id_doc_copy) > 0 or len(data.contact_id_doc_copy_back) > 0 or len(data.business_authorization_letter) > 0:
        res = d_db.insert_business_license(item=m_schema.CreateBusinessLicense(
            business_id=data.mod_id,
            lic_type=global_define.lic_type['contact'],
            lic_type_name=global_define.lic_type_name[0],
            lic_number=data.contact_id_number,  # 证件号码
            lic_copy=data.contact_id_doc_copy,  # 超级管理员证件正面照片
            lic_copy_wx=data.contact_id_doc_copy_wx, #超级管理员证件正面照片微信media_id
            lic_copy_back=data.contact_id_doc_copy_back, #超级管理员证件反面照片
            lic_copy_back_wx=data.contact_id_doc_copy_back_wx, #超级管理员证件反面照片微信media_id
            lic_period_begin=data.contact_period_begin, #超级管理员证件有效期开始时间
            lic_period_end=data.contact_period_end, #超级管理员证件有效期结束时间
            lic_period_end_long=data.contact_period_end_long,  # 证件长期有效
            lic_copy_other1=data.business_authorization_letter,  #业务办理授权函
            lic_copy_other1_wx=data.business_authorization_letter_wx  #业务办理授权函微信
        ))
        contact_license_info = res.id

    d_db.update_business_content(item=m_schema.SBusinessContent(
        id=data.mod_id,
        contact_type=data.select_contact_type,  #超级管理员类型
        contact_name=data.contact_name,  #超级管理员姓名
        contact_id_doc_type=data.select_contact_id_doc_type,  #超级管理员证件类型
        contact_license_info=contact_license_info,  #超管license表ID,授权函license_copy_other1
        contact_openid=data.openid,  #超级管理员微信OpenID
        contact_mobile_phone=data.mobile_phone,
        contact_email=data.contact_email

    ))
    return {"status":200, "msg":'success'}


@router.post(f'/save_body', summary='保存主体资料')
async def save_body(data: AddBody):
    mod_id = data.mod_id
    subject_business_license_info = data.subject_business_license_info  #营业执照license表ID
    subject_certificate_info = data.subject_certificate_info #登记证书license表ID
    subject_certificate_letter_copy = data.subject_certificate_letter_copy #单位证明函照片license表ID
    subject_finance_institution_info = data.subject_finance_institution_info  #金融机构许可证信息license表ID
    subject_identity_info = data.subject_identity_info  #经营者 / 法人身份证件license表ID
    #营业执照信息
    if subject_business_license_info > 0:
        d_db.update_business_license(item=m_schema.SBusinessLicense(
            id=subject_business_license_info,
            # business_id=mod_id,
            lic_number=data.li_license_number,  # 证件号码 营业执照, 注册号 / 统一社会信用代码
            lic_copy=data.li_license_copy,  # 营业执照照片
            lic_copy_wx=data.li_license_copy_wx,  # 微信media_id
            lic_person1=data.li_merchant_name,  # 营业执照, 商户名称
            lic_person2=data.li_legal_person,  # 营业执照, 个体户经营者 / 法人姓名
            lic_address=data.li_license_address,  # 营业执照, 注册地址
            lic_period_begin=data.li_period_begin,  # 营业执照, 有效期限开始日期
            lic_period_end=data.li_period_end,  # 营业执照, 有效期限结束日期
            lic_period_end_long=data.li_period_end_long
        ))
    else:
        # if len(data.contact_id_doc_copy) > 0 or len(data.contact_id_doc_copy_back) > 0 or len(data.business_authorization_letter) > 0:
        res = d_db.insert_business_license(item=m_schema.CreateBusinessLicense(
            business_id=mod_id,
            lic_type=global_define.lic_type['license'],
            lic_type_name=global_define.lic_type_name[1],
            lic_number=data.li_license_number,  # 证件号码 营业执照, 注册号 / 统一社会信用代码
            lic_copy=data.li_license_copy,  # 营业执照照片
            lic_copy_wx=data.li_license_copy_wx,  # 微信media_id
            lic_person1=data.li_merchant_name,  #  营业执照, 商户名称
            lic_person2=data.li_legal_person, #营业执照, 个体户经营者 / 法人姓名
            lic_address=data.li_license_address,  #营业执照, 注册地址
            lic_period_begin=data.li_period_begin,  # 营业执照, 有效期限开始日期
            lic_period_end=data.li_period_end,  # 营业执照, 有效期限结束日期
            lic_period_end_long=data.li_period_end_long

        ))
        subject_business_license_info = res.id

    # 登记证书信息
    if subject_certificate_info > 0:
        d_db.update_business_license(item=m_schema.SBusinessLicense(
            id=subject_certificate_info,
            # business_id=mod_id,
            lic_copy=data.ce_cert_copy,  # 登记证书照片
            lic_copy_wx=data.ce_cert_copy_wx,  # 微信media_id
            lic_number=data.ce_cert_number,  # 登记证书, 证书号
            lic_person1=data.ce_merchant_name,  # 登记证书, 商户名称
            lic_person2=data.ce_legal_person,  # 登记证书, 法定代表人
            lic_address=data.ce_company_address,  # 登记证书, 注册地址
            lic_period_begin=data.ce_period_begin,  # 登记证书, 有效期限开始日期
            lic_period_end=data.ce_period_end,  # 登记证书, 有效期限结束日期
        ))
    else:
        # if len(data.contact_id_doc_copy) > 0 or len(data.contact_id_doc_copy_back) > 0 or len(data.business_authorization_letter) > 0:
        res = d_db.insert_business_license(item=m_schema.CreateBusinessLicense(
            business_id=mod_id,
            lic_type=global_define.lic_type['certificate'],
            lic_type_name=global_define.lic_type_name[2],
            lic_copy=data.ce_cert_copy,  # 登记证书照片
            lic_copy_wx=data.ce_cert_copy_wx,  # 微信media_id
            lic_number=data.ce_cert_number,  #登记证书, 证书号
            lic_person1=data.ce_merchant_name,  # 登记证书, 商户名称
            lic_person2=data.ce_legal_person,  # 登记证书, 法定代表人
            lic_address=data.ce_company_address,  # 登记证书, 注册地址
            lic_period_begin=data.ce_period_begin,  # 登记证书, 有效期限开始日期
            lic_period_end=data.ce_period_end,  # 登记证书, 有效期限结束日期
        ))
        subject_certificate_info = res.id

    # 位证明函照片信息
    if subject_certificate_letter_copy > 0:
        d_db.update_business_license(item=m_schema.SBusinessLicense(
            id=subject_certificate_letter_copy,
            # business_id=mod_id,
            lic_copy=data.ce_certificate_letter_copy,  # 单位证明函照片
            lic_copy_wx=data.ce_certificate_letter_copy_wx  # 微信media_id
        ))
    else:
        # if len(data.contact_id_doc_copy) > 0 or len(data.contact_id_doc_copy_back) > 0 or len(data.business_authorization_letter) > 0:
        res = d_db.insert_business_license(item=m_schema.CreateBusinessLicense(
            business_id=mod_id,
            lic_type=global_define.lic_type_name[3],
            lic_type_name=global_define.lic_type_name[3],
            lic_copy=data.ce_certificate_letter_copy,  # 单位证明函照片
            lic_copy_wx=data.ce_certificate_letter_copy_wx  # 微信media_id
        ))
        subject_certificate_letter_copy = res.id

    # 金融机构许可证信息
    if subject_finance_institution_info > 0:
        d_db.update_business_license(item=m_schema.SBusinessLicense(
            id=subject_finance_institution_info,
            # business_id=mod_id,
            lic_type_name=data.fi_finance_type,  # 金融机构类型
            lic_copy=data.fi_finance_license_pics,  # 金融机构许可证图片
            lic_copy_wx=data.fi_finance_license_pics_wx  # 微信media_id
        ))
    else:
        # if len(data.contact_id_doc_copy) > 0 or len(data.contact_id_doc_copy_back) > 0 or len(data.business_authorization_letter) > 0:
        res = d_db.insert_business_license(item=m_schema.CreateBusinessLicense(
            business_id=mod_id,
            lic_type=global_define.lic_type_name[4],
            lic_type_name=data.fi_finance_type,  #金融机构类型
            lic_copy=data.fi_finance_license_pics,  # 金融机构许可证图片
            lic_copy_wx=data.fi_finance_license_pics_wx  # 微信media_id
        ))
        subject_finance_institution_info = res.id

    # 经营者 / 法人身信息
    if subject_identity_info > 0:
        d_db.update_business_license(item=m_schema.SBusinessLicense(
            id=subject_identity_info,
            lic_type=data.id_holder_type,  # 法人证件, 证件类型  证件持有人类型
            lic_type_name=data.id_doc_type,  #法人证件类型
            lic_copy=data.id_card_copy,  # 法人证件, 身份证人像面照片
            lic_copy_wx=data.id_card_copy_wx,  # 微信media_id
            lic_copy_back=data.id_card_national,  # 法人证件, 身份证国徽面照片
            lic_copy_back_wx=data.id_card_national_wx,  # 微信media_id
            lic_copy_other1=data.id_authorize_letter_copy,  # 法人证件, 法定代表人说明函
            lic_copy_other1_wx=data.id_authorize_letter_copy_wx,  # 微信media_id
            lic_number=data.id_card_number,  # 法人证件, 身份证号码
            lic_person1=data.id_card_name,  # 法人证件, 身份证姓名
            lic_address=data.id_card_address,  # 法人证件, 身份证居住地址
            lic_period_begin=data.id_card_period_begin,  # 法人证件, 身份证有效期开始时间
            lic_period_end=data.id_card_period_end,  # 法人证件, 身份证有效期结束时间
        ))
    else:
        # if len(data.contact_id_doc_copy) > 0 or len(data.contact_id_doc_copy_back) > 0 or len(data.business_authorization_letter) > 0:
        res = d_db.insert_business_license(item=m_schema.CreateBusinessLicense(
            business_id=mod_id,
            lic_type_name=global_define.lic_type_name[5],
            lic_type=data.id_holder_type,  #法人证件, 证件类型
            lic_copy=data.id_card_copy,  # 法人证件, 身份证人像面照片
            lic_copy_wx=data.id_card_copy_wx,  # 微信media_id
            lic_copy_back=data.id_card_national,  # 法人证件, 身份证国徽面照片
            lic_copy_back_wx=data.id_card_national_wx,  # 微信media_id
            lic_copy_other1=data.id_authorize_letter_copy,  #法人证件, 法定代表人说明函
            lic_copy_other1_wx=data.id_authorize_letter_copy_wx,   #微信media_id
            lic_number = data.id_card_number,  # 法人证件, 身份证号码
            lic_person1=data.id_card_name,  # 法人证件, 身份证姓名
            lic_address=data.id_card_address, # 法人证件, 身份证居住地址
            lic_period_begin = data.id_card_period_begin,  # 法人证件, 身份证有效期开始时间
            lic_period_end = data.id_card_period_end,  # 法人证件, 身份证有效期结束时间
        ))
        subject_identity_info = res.id

    d_db.update_business_content(item=m_schema.SBusinessContent(
        id=data.mod_id,
        subject_type=data.select_subject_type,  # 主体类型
        subject_finance_institution=data.finance_institution,  # 是否是金融机构
        subject_business_license_info=subject_business_license_info,  # 营业执照license表ID
        subject_certificate_info=subject_certificate_info,  # 登记证书license表ID
        subject_certificate_letter_copy=subject_certificate_letter_copy,  # 单位证明函照片license表ID
        subject_finance_institution_info=subject_finance_institution_info,  #金融机构许可证信息license表ID
        subject_identity_info=subject_identity_info,  #经营者/法人身份证件license表ID
        subject_ubo_id_owner=data.id_owner  #法人是否为受益人
    ))
    return {"status": 200, "msg": 'success'}

@router.post(f'/save_addbuy', summary='保存经营资料')
async def save_addbuy(data: AddBuy):
    mod_id = data.mod_id
    sales_biz_store_info = data.sales_biz_store_info  #线下场所场景license表ID
    sales_mp_info = data.sales_mp_info  # 公众号场景license表ID
    sales_mini_program_info = data.sales_mini_program_info  # 小程序场景license表ID
    sales_app_info = data.sales_app_info  # App场景license表ID
    sales_web_info = data.sales_web_info  # 互联网网站场景license表ID
    sales_wework_info = data.sales_wework_info  # 企业微信场景license表ID
    # 线下场所场景license表ID
    if sales_biz_store_info > 0:
        d_db.update_business_license(item=m_schema.SBusinessLicense(
            id=sales_biz_store_info,
            lic_name=data.biz_store_name,  #线下场所名称
            lic_person1=data.biz_address_code,  #线下场所省市编码
            lic_address=data.biz_store_address,  #线下场所地址
            lic_person2=data.biz_sub_appid, #线下场所对应的商家AppID
            lic_copy=data.biz_store_entrance_pic,  #线下场所门头照片
            lic_copy_wx=data.biz_store_entrance_pic_wx,  #微信media_id
            lic_copy_back=data.biz_indoor_pic,  #线下场所内部照片
            lic_copy_back_wx=data.biz_indoor_pic_wx  #微信media_id
        ))
    else:
        # if len(data.contact_id_doc_copy) > 0 or len(data.contact_id_doc_copy_back) > 0 or len(data.business_authorization_letter) > 0:
        res = d_db.insert_business_license(item=m_schema.CreateBusinessLicense(
            business_id=mod_id,
            lic_name=data.biz_store_name,  # 线下场所名称
            lic_person1=data.biz_address_code,  # 线下场所省市编码
            lic_address=data.biz_store_address,  # 线下场所地址
            lic_person2=data.biz_sub_appid,  # 线下场所对应的商家AppID
            lic_copy=data.biz_store_entrance_pic,  # 线下场所门头照片
            lic_copy_wx=data.biz_store_entrance_pic_wx,  # 微信media_id
            lic_copy_back=data.biz_indoor_pic,  # 线下场所内部照片
            lic_copy_back_wx=data.biz_indoor_pic_wx  # 微信media_id
        ))
        sales_biz_store_info = res.id

    # 公众号场景license表ID
    if sales_mp_info > 0:
        d_db.update_business_license(item=m_schema.SBusinessLicense(
            id=sales_mp_info,
            lic_name=data.mp_appid,  # 服务商公众号AppID
            lic_person1=data.mp_sub_appid,  # 商家公众号AppID
            lic_copy_array = data.mp_pics

        ))
    else:
        # if len(data.contact_id_doc_copy) > 0 or len(data.contact_id_doc_copy_back) > 0 or len(data.business_authorization_letter) > 0:
        res = d_db.insert_business_license(item=m_schema.CreateBusinessLicense(
            business_id=mod_id,
            lic_name=data.mp_appid,  # 服务商公众号AppID
            lic_person1=data.mp_sub_appid,  # 商家公众号AppID
            lic_copy_array=data.mp_pics
        ))
        sales_mp_info = res.id

    # 小程序场景license表ID
    if sales_mini_program_info > 0:
        d_db.update_business_license(item=m_schema.SBusinessLicense(
            id=sales_mini_program_info,
            lic_name=data.mini_program_appid,  # 服务商小程序APPID
            lic_person1=data.mini_program_sub_appid,  # 商家小程序APPID
            lic_copy_array=data.mini_program_pics

        ))
    else:
        # if len(data.contact_id_doc_copy) > 0 or len(data.contact_id_doc_copy_back) > 0 or len(data.business_authorization_letter) > 0:
        res = d_db.insert_business_license(item=m_schema.CreateBusinessLicense(
            business_id=mod_id,
            lic_name=data.mini_program_appid,  # 服务商小程序APPID
            lic_person1=data.mini_program_sub_appid,  # 商家小程序APPID
            lic_copy_array=data.mini_program_pics
        ))
        sales_mini_program_info = res.id

    # App场景license表ID
    if sales_app_info > 0:
        d_db.update_business_license(item=m_schema.SBusinessLicense(
            id=sales_app_info,
            lic_name=data.app_appid,  # 服务商小程序APPID
            lic_person1=data.app_sub_appid  # 商家小程序APPID

        ))
    else:
        # if len(data.contact_id_doc_copy) > 0 or len(data.contact_id_doc_copy_back) > 0 or len(data.business_authorization_letter) > 0:
        res = d_db.insert_business_license(item=m_schema.CreateBusinessLicense(
            business_id=mod_id,
            lic_name=data.app_appid,  # 服务商小程序APPID
            lic_person1=data.app_sub_appid  # 商家小程序APPID
        ))
        sales_app_info = res.id

    # 互联网网站场景license表ID
    if sales_web_info > 0:
        d_db.update_business_license(item=m_schema.SBusinessLicense(
            id=sales_web_info,
            lic_name=data.web_domain,  # 互联网网站域名
            lic_person1=data.web_appid,  # 互联网网站对应的商家APPID
            lic_copy=data.web_authorisation,  # 网站授权函
            lic_copy_wx=data.web_authorisation_wx,  # 微信media_id

        ))
    else:
        # if len(data.contact_id_doc_copy) > 0 or len(data.contact_id_doc_copy_back) > 0 or len(data.business_authorization_letter) > 0:
        res = d_db.insert_business_license(item=m_schema.CreateBusinessLicense(
            business_id=mod_id,
            lic_name=data.web_domain,  # 互联网网站域名
            lic_person1=data.web_appid,  # 互联网网站对应的商家APPID
            lic_copy = data.web_authorisation,  # 网站授权函
            lic_copy_wx = data.web_authorisation_wx,  # 微信media_id
        ))
        sales_web_info = res.id

    # 企业微信场景license表ID
    if sales_wework_info > 0:
        d_db.update_business_license(item=m_schema.SBusinessLicense(
            id=sales_wework_info,
            lic_name=data.sub_corp_id,  # 商家企业微信CorpID

        ))
    else:
        # if len(data.contact_id_doc_copy) > 0 or len(data.contact_id_doc_copy_back) > 0 or len(data.business_authorization_letter) > 0:
        res = d_db.insert_business_license(item=m_schema.CreateBusinessLicense(
            business_id=mod_id,
            lic_name=data.sub_corp_id,  # 商家企业微信CorpID
        ))
        sales_wework_info = res.id

    d_db.update_business_content(item=m_schema.SBusinessContent(
        id=data.mod_id,
        business_merchant_shortname=data.merchant_shortname,  # 商户简称
        business_service_phone=data.service_phone,  # 客服电话
        sales_scenes_type=data.sales_scenes_type,  # 经营场景类型
        sales_biz_store_info=sales_biz_store_info,  # 线下场所场景license表ID
        sales_mp_info=sales_mp_info,  # 公众号场景license表ID
        sales_mini_program_info=sales_mini_program_info,  # 小程序场景license表ID
        sales_app_info=sales_app_info,  # App场景license表ID
        sales_web_info = sales_web_info,  # 互联网网站场景license表ID
        sales_wework_info = sales_wework_info  # 企业微信场景license表ID
    ))

    return {"status": 200, "msg": 'success'}

@router.post(f'/save_addank', summary='保存结算银行')
async def save_addank(data: AddBank):
     mod_id = data.mod_id
     d_db.update_business_content(item=m_schema.SBusinessContent(
         id=mod_id,
         bank_account_type=data.bank_account_type,  # 账户类型
         bank_account_name=data.account_name,  # 开户名称
         bank_account_bank=data.account_bank,  # 开户银行
         bank_address_code=data.bank_address_code,  # 开户银行省市编码
         bank_branch_id=data.bank_branch_id,  # 开户银行联行号
         bank_name=data.bank_name,  # 开户银行全称（含支行）
         bank_account_number=data.account_number,  # 银行账号
     ))
     return {"status": 200, "msg": 'success'}

#
# @router.get(f'/submitshoper', summary='提交商户信息')
# async def submitshoper(shid: int):
#     re_val = {"status": 200, "msg": 'success'}
#     shopinfo = d_db.get_business_content(shid)
#     if shopinfo:
#         business_code = shopinfo.business_code
#         #超级管理员信息，示例值: {'contact_name': '张三', 'contact_id_number': '320311770706001','mobile_phone': '13900000000', 'contact_email': 'admin@demo.com'}
#         contact_info = {}
#         contact_info['contact_name'] = shopinfo.contact_name
#         contact_info['mobile_phone'] = shopinfo.contact_mobile_phone
#         contact_info['contact_email'] = shopinfo.contact_email
#         contact_info_license = d_db.get_business_license(shopinfo.contact_license_info)
#         if not contact_info_license:
#             re_val['status'] = 404
#             re_val['msg'] = '超管信息有误，检查后再试'
#             return re_val
#         contact_info['contact_id_number'] = contact_info_license.lic_number
#         #subject_info: 主体资料，示例值:{'subject_type':'SUBJECT_TYPE_ENTERPRISE',
#         # 'business_license_info':{'license_copy':'demo-media-id','license_number':'123456789012345678','merchant_name':'腾讯科技有限公司','legal_person':'张三'},
#         # 'identity_info':{'id_doc_type':'IDENTIFICATION_TYPE_IDCARD','id_card_info'{'id_card_copy':'demo-media-id'}}}
#         subject_info = {}
#         subject_info['subject_type'] = shopinfo.subject_type
#         #-营业执照
#         business_license_info = d_db.get_business_license(shopinfo.subject_business_license_info)
#         if not business_license_info:
#             re_val['status'] = 404
#             re_val['msg'] = '营业执照有误，检查后再试'
#             return re_val
#         business_license_info_dict = {}
#         business_license_info_dict['license_copy'] = business_license_info.lic_copy_wx
#         business_license_info_dict['license_number'] = business_license_info.lic_number
#         business_license_info_dict['merchant_name'] = business_license_info.lic_person1
#         business_license_info_dict['legal_person'] = business_license_info.lic_person2
#         subject_info['business_license_info'] = business_license_info_dict
#         identity_info = d_db.get_business_license(shopinfo.subject_identity_info)
#         if not identity_info:
#             re_val['status'] = 404
#             re_val['msg'] = '营业执照图片信息有误，检查后再试'
#             return re_val
#         identity_info_dict = {}
#         # 经营者/法人身份证件
#         identity_info_dict['id_doc_type'] = identity_info.lic_type_name
#         identity_info_dict['id_card_info'] = {'id_card_copy':identity_info.lic_copy_wx, 'id_card_national':identity_info.lic_copy_back_wx, 'id_card_address':identity_info.lic_address,\
#                                               'id_card_number':identity_info.lic_number, 'id_card_name':identity_info.lic_person1, 'card_period_begin':identity_info.lic_period_begin.strftime("%Y-%m-%d"), \
#                                               'card_period_end':identity_info.lic_period_end.strftime("%Y-%m-%d")}
#         subject_info['identity_info'] = identity_info_dict
#         #business_info: 经营资料，示例值: {'merchant_shortname': '张三餐饮店', 'service_phone': '0758xxxxxx','sales_info': {'sales_scenes_type': ['SALES_SCENES_STORE', 'SALES_SCENES_MP']}}
#         #settlement_info: 结算规则，示例值: {'settlement_id': '719', 'qualification_type': '餐饮'}
#         business_info = {}
#         settlement_info = {'settlement_id':'719', 'qualification_type':'电商平台'}
#         shopinfo.business_sales_scenes_type = "SALES_SCENES_MINI_PROGRAM"
#         if shopinfo.business_sales_scenes_type is None or len(shopinfo.business_sales_scenes_type) < 2:
#             re_val['status'] = 404
#             re_val['msg'] = '经营场景类型信息有误，检查后再试'
#             return re_val
#         business_info['sales_info']={'sales_scenes_type':shopinfo.business_sales_scenes_type.split(',')}
#         business_info['merchant_shortname'] = shopinfo.business_merchant_shortname
#         business_info['service_phone'] = shopinfo.business_service_phone
#         #bank_account_info: 结算银行账户，示例值:{'bank_account_type':'BANK_ACCOUNT_TYPE_CORPORATE','account_name':'xx公司','account_bank':'工商银行','bank_address_code':'110000','account_number':'1234567890'}
#         bank_account_info = {}
#         bank_account_info['bank_account_type'] = shopinfo.bank_account_type
#         bank_account_info['account_name'] = shopinfo.bank_account_name
#         bank_account_info['account_bank'] = shopinfo.bank_account_bank
#         bank_account_info['bank_address_code'] = shopinfo.bank_address_code
#         bank_account_info['account_number'] = shopinfo.bank_account_number
#         logging.info('start to wxpayservice.applyment_submit')
#         logging.info('business_code: ' + str(business_code))
#         logging.info('contact_info: ' + str(contact_info))
#         logging.info('subject_info: ' + str(subject_info))
#         logging.info('business_info: ' + str(business_info))
#         logging.info('settlement_info: ' + str(settlement_info))
#         logging.info('bank_account_info: ' + str(bank_account_info))
#
#         re_val['msg'] = wxpayservice.applyment_submit(business_code, contact_info, subject_info, business_info, settlement_info, bank_account_info)
#         logging.info('wxpayservice.applyment_submit结果: ' + str(re_val['msg']))
#     else:
#         re_val['status'] = 404
#         re_val['msg'] = f"{shid},未知商户信息。"
#
#     return re_val

@router.get(f'/submitshoplowsir', summary='提交二级商户信息')
async def submitshoplowsir(shid: int):
    re_val = {"status": 200, "msg": 'success'}
    shopinfo = d_db.get_business_content(shid)
    if shopinfo:
        #out_request_no, organization_type, finance_institution, id_holder_type, id_doc_type, merchant_shortname, business_license_info, id_card_info, account_info,
        # contact_info, sales_scene_info, finance_institution_info = None, ubo_info_list = None, id_doc_info = None, owner = True, authorize_letter_copy = None,
        # settlement_info = None, qualifications = None, business_addition_pics = None, business_addition_desc = None

        # out_request_no = shopinfo.business_code
        out_request_no = 'APPLYMENT_00000000122'
        # organization_type = shopinfo.subject_type
        organization_type = '2'
        finance_institution = False
        id_holder_type = 'LEGAL'  # 法人
        id_doc_type = 'IDENTIFICATION_TYPE_MAINLAND_IDCARD'  # 中国大陆居民-身份证
        merchant_shortname = shopinfo.business_merchant_shortname  #商户简称

        # -营业执照
        business_license_info_rs = d_db.get_business_license(shopinfo.subject_business_license_info)
        if not business_license_info_rs:
            re_val['status'] = 404
            re_val['msg'] = '营业执照有误，检查后再试'
            return re_val
        business_license_info = {}
        business_license_info['business_license_copy'] = business_license_info_rs.lic_copy_wx
        business_license_info['business_license_number'] = business_license_info_rs.lic_number
        business_license_info['merchant_name'] = business_license_info_rs.lic_person1
        business_license_info['legal_person'] = business_license_info_rs.lic_person2
        business_license_info['business_time'] = "[\"2024-05-26\",\"长期\"]"
        # business_license_info['cert_type'] = "CERTIFICATE_TYPE_2388"   #主体为“个体工商户/企业”时，不填
        business_license_info['company_address'] = "河北省石家庄市正定县正定镇中山东路隆和巷5号"

        # 经营者/法人身份证件
        identity_info_rs = d_db.get_business_license(shopinfo.subject_identity_info)
        if not identity_info_rs:
            re_val['status'] = 404
            re_val['msg'] = '法人身份证件信息有误，检查后再试'
            return re_val
        id_card_info = {}
        id_card_info['id_doc_type'] = identity_info_rs.lic_type_name
        id_card_info['id_card_copy'] = identity_info_rs.lic_copy_wx
        id_card_info['id_card_national'] = identity_info_rs.lic_copy_back_wx
        id_card_info['id_card_address'] = identity_info_rs.lic_address
        id_card_info['id_card_number'] = identity_info_rs.lic_number
        id_card_info['id_card_name'] = identity_info_rs.lic_person1
        id_card_info['id_card_valid_time_begin'] = identity_info_rs.lic_period_begin.strftime("%Y-%m-%d")
        id_card_info['id_card_valid_time'] = identity_info_rs.lic_period_end.strftime("%Y-%m-%d")

        #  结算银行账户
        account_info = {}
        # account_info['bank_account_type'] = shopinfo.bank_account_type
        account_info['bank_account_type'] = '74'  #对公账户
        account_info['account_name'] = shopinfo.bank_account_name
        # account_info['account_bank'] = shopinfo.bank_account_bank
        account_info['account_bank'] = '农业银行'
        # account_info['bank_branch_id'] = "313121006079"  #河北银行股份有限公司新华路支行
        account_info['bank_branch_id'] = "103121032409"  # 中国农业银行股份有限公司正定华阳分理处
        account_info['bank_address_code'] = shopinfo.bank_address_code
        account_info['account_number'] = shopinfo.bank_account_number
        # account_info['bank_branch_id'] = "402713354941"
        account_info['bank_address_code'] = "130100"   #中国,河北省,石家庄市

        #超级管理员信息
        contact_info = {}
        contact_info_license = d_db.get_business_license(shopinfo.contact_license_info)
        if not contact_info_license:
            re_val['status'] = 404
            re_val['msg'] = '超管信息有误，检查后再试'
            return re_val
        contact_info['contact_id_card_number'] = contact_info_license.lic_number
        # 业务办理授权函
        contact_info['business_authorization_letter'] = contact_info_license.lic_copy_other1_wx
        contact_info['contact_email'] = shopinfo.contact_email
        contact_info['contact_id_doc_copy'] = contact_info_license.lic_copy_wx
        contact_info['contact_id_doc_copy_back'] = contact_info_license.lic_copy_back_wx
        contact_info['contact_id_doc_period_begin'] = contact_info_license.lic_period_begin.strftime("%Y-%m-%d")
        contact_info['contact_id_doc_period_end'] = contact_info_license.lic_period_end.strftime("%Y-%m-%d")
        contact_info['contact_id_doc_type'] = "IDENTIFICATION_TYPE_MAINLAND_IDCARD"  # 中国大陆居民-身份证
        contact_info['contact_name'] = shopinfo.contact_name
        # contact_info['contact_type'] = shopinfo.contact_type
        contact_info['contact_type'] = '66'  # 经办人：经商户授权办理微信支付业务的人员
        contact_info['mobile_phone'] = shopinfo.contact_mobile_phone

        #店铺信息
        sales_scene_info = {}
        # sales_scene_info['mini_program_sub_appid'] = 'wxbf29933c8c4b5235'
        # sales_scene_info['store_name'] = '非常市集'
        sales_scene_info['mini_program_sub_appid'] = 'wx4a492527f224c148'
        sales_scene_info['store_name'] = '非常市集'
        # sales_scene_info['store_qr_code'] = shopinfo.contact_type
        sales_scene_info['store_url'] = 'http://www.yxiaozhu.com'

        #out_request_no, organization_type, finance_institution, id_holder_type, id_doc_type, merchant_shortname, business_license_info, id_card_info, account_info, contact_info, sales_scene_info
        logging.info('start to submitshoplowsir')
        logging.info('out_request_no: ' + str(out_request_no))
        logging.info('organization_type: ' + str(organization_type))
        logging.info('finance_institution: ' + str(finance_institution))
        logging.info('id_holder_type: ' + str(id_holder_type))
        logging.info('id_doc_type: ' + str(id_doc_type))
        logging.info('merchant_shortname: ' + str(merchant_shortname))
        logging.info('business_license_info: ' + str(business_license_info))
        logging.info('id_card_info: ' + str(id_card_info))
        logging.info('account_info: ' + str(account_info))
        logging.info('contact_info: ' + str(contact_info))
        logging.info('sales_scene_info: ' + str(sales_scene_info))

        re_val['msg'] = d_admin.applyment_submit_lowsir(out_request_no, organization_type, finance_institution, id_holder_type, id_doc_type, merchant_shortname, business_license_info, id_card_info, account_info, contact_info, sales_scene_info)
        logging.info('d_admin.applyment_submit_lowsir结果: ' + str(re_val['msg']))
    else:
        re_val['status'] = 404
        re_val['msg'] = f"{shid},未知商户信息。"

    return re_val


@router.post(f'/save_shoperpwd', summary='保存商家账户信息')
async def save_shoperpwd(data: ShoperModel):
    re_val = {"status": 200, "msg": 'success'}
    admin_info = d_admin.get_admin_by_businessid(data.modid)
    if admin_info:
        d_admin.update_admin_info(data)
    else:
        d_admin.add_admin_info(data)

    return re_val

@router.get(f'/get_shoperinfo', summary='获取商家账户信息')
async def get_shoperinfo(shopid: int):
    return d_admin.get_admin_by_businessid(shopid)