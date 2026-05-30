import datetime
from dao import d_db, d_supplier
from fastapi import APIRouter, Depends, Header, Request
from model.mall import m_supplier
from model import m_schema, schema
from model.m_schema import *
from router.mall import user
from typing import Optional, List
from router import r_schema
from model.res import auth
from service.auth_service import token_encode
from router.admin.user import verify_token
from pydantic import BaseModel, Field

router = APIRouter(dependencies=[Depends(verify_token)])

@router.post(f'/supplier/getlist', response_model=m_supplier.ASupplierMsgList, summary='获取供应商列表')
async def get_supplier_list(
        id: Optional[int] = None,
        name: Optional[str] = None,
        owner: Optional[str] = None,
        phone: Optional[str] = None,
        status: Optional[int] = None,
        area: Optional[str] = None,
        register_start: Optional[str] = None,
        register_end: Optional[str] = None,
        expired_start: Optional[str] = None,
        expired_end: Optional[str] = None,
        expired: Optional[str] = None,
        page: Optional[int] = 1,
        page_size: Optional[int] = 20
):
    f_supplier_return: dict = await d_supplier.query_supplier(id, name, owner, phone, status, area,
                                                              register_start, register_end, expired_start, expired_end,
                                                              expired, page, page_size)

    total_size: int = f_supplier_return['total']
    supplier_msg_list: m_supplier.ASupplierMsgList = m_supplier.ASupplierMsgList(data=[], total=total_size)
    for t_supplier in f_supplier_return['data']:
        a_supplier_msg: m_supplier.ASupplierMsg = m_supplier.ASupplierMsg()
        for i in range(len(t_supplier)):
            t_model = t_supplier[i]
            if t_model is None:
                continue
            obj_name: str = type(t_model).__name__
            s_model_name: str = 'S' + obj_name[1:]
            cls = globals()[s_model_name]
            setattr(a_supplier_msg, s_model_name, cls.parse_obj(t_model.__dict__))

        if a_supplier_msg.SSupplier is not None:
            a_supplier_msg.SSupplierAmount = await d_supplier. \
                get_amount_by_supplier_id(supplier_id=a_supplier_msg.SSupplier.id)

            a_supplier_msg.SStoreCount = await d_supplier. \
                get_store_count(supplier_id=a_supplier_msg.SSupplier.id)

        supplier_msg_list.data.append(a_supplier_msg)

    return supplier_msg_list

#
# @router.get(f'/supplier_members/get', response_model=m_schema.FilterResOrder, summary='获取商家会员列表')
# async def get_members(supplier_id: int, user_id: Optional[str] = None, username: Optional[str] = None,
#                       consume_start: Optional[str] = None, consume_end: Optional[str] = None,
#                       phone: Optional[str] = None, page: Optional[int] = 1, page_size: Optional[int] = 20):
#     supplier_members: dict = await d_supplier.query_supplier_members(supplier_id=str(supplier_id), user_id=user_id,
#                                                                      consume_start=consume_start,
#                                                                      consume_end=consume_end,
#                                                                      username=username, phone=phone)
#     s_order_list: List[m_schema.SOrder] = supplier_members['data']
#     return m_schema.FilterResOrder(data=s_order_list[(page - 1) * page_size:page * page_size],
#                                    total=supplier_members['total'])
#
#
# @router.get(f'/supplier_amount_record/get', response_model=m_supplier.ARecordMsgList, summary='获取商家资金列表')
# async def get_amount_records(supplier_id: int, page: Optional[int] = 1,
#                              page_size: Optional[int] = 10) -> m_supplier.ARecordMsgList:
#     amount_record_dict: dict = await d_supplier.get_amount_record_list(supplier_id, page, page_size)
#
#     total_size: int = amount_record_dict['total']
#     record_msg_list: m_supplier.ARecordMsgList = m_supplier.ARecordMsgList(data=[], total=total_size)
#     for t_record in amount_record_dict['data']:
#         a_record_msg: m_supplier.ARecordMsg = m_supplier.ARecordMsg()
#         for i in range(len(t_record)):
#             t_model = t_record[i]
#             if t_model is None:
#                 continue
#             obj_name: str = type(t_model).__name__
#             s_model_name: str = 'S' + obj_name[1:]
#             cls = globals()[s_model_name]
#             setattr(a_record_msg, s_model_name, cls.parse_obj(t_model.__dict__))
#
#         record_msg_list.data.append(a_record_msg)
#
#     return record_msg_list

#
@router.get(f'/supplier_license/get', response_model=m_supplier.ASupplierLicense, summary='获供应商资质')
async def get_supplier_license(supplier_id: int):
    t_supplier_owner: schema.TStoreOwner = await d_supplier.query_supplier_owner(supplier_id=supplier_id)
    f_licenses: m_schema.FilterResSupplierLicense = await r_schema.filter_supplier_license(supplier_id=str(supplier_id))

    return m_supplier.ASupplierLicense(
        SSupplierOwner=m_schema.SSupplierOwner.parse_obj(t_supplier_owner.__dict__) if t_supplier_owner else None,
        SSupplierLicense=f_licenses)


@router.get(f'/supplier/register_info', response_model=m_supplier.RSupplierMsg, summary='获取供应商全部注册信息')
async def supplier_register(employee_id: int):
    supplier_owner: Optional[m_schema.SSupplierOwner] = d_db.get_supplier_owner(supplier_owner_id=employee_id)
    supplier_list: List[m_schema.SSupplier] = d_db.filter_supplier(items={'owner_id': employee_id}, search_items={},
                                                                   set_items={}, page=1, page_size=1)
    supplier: m_schema.SSupplier = supplier_list[0] if supplier_list else None
    supplier_state: m_schema.SSupplierState = d_db.get_supplier_state(supplier_state_id=supplier.status)
    supplier_license: List[m_schema.SSupplierLicense] = d_db.filter_supplier_license(
        items={'supplier_id': supplier.id}, search_items={}, set_items={}, page=1,
        page_size=10) if supplier else None
    return m_supplier.RSupplierMsg(TSupplier=supplier, TSupplierOwner=supplier_owner, TSupplierLicense=supplier_license,
                                   TSupplierState=supplier_state)


class CreateSupplierInfo(BaseModel):
    phone: Optional[str] = Field(title='电话')
    password: Optional[str] = Field(title='密码（哈希值）')
    recommender_id: Optional[int] = Field(title='推荐人信息')

@router.post(f'/supplier/register_next', response_model=dict, summary='供应商注册-初始化注册账户')
# async def supplier_register_next(code: str, employee_id: int, phone: str, recommender_id: int, password: str):
async def supplier_register_next(data: CreateSupplierInfo):
    '''
    创建登录账户和供应商主题信息id，以手机号为准，注册过则更新
    phone:注册供应商联系电话
    recommender_id：推荐人id
    password:供应商登录密码
    '''
    # res: dict = await user.verify_phone_code(employee_id=employee_id, code=code)
    # if res['detail'] == 'success':
    #     d_db.update_supplier_owner(item=m_schema.SSupplierOwner(id=employee_id, password=password, phone=phone))
    #     supplier_list: List[m_schema.SSupplier] = d_db.filter_supplier(items={'owner_id': employee_id}, search_items={},
    #                                                                    set_items={}, page=1, page_size=1)
    #     if supplier_list:
    #         s_supplier: m_schema.SSupplier = m_schema.SSupplier(id=supplier_list[0].id, owner_id=employee_id,
    #                                                             recommender_id=recommender_id)
    #         d_db.update_supplier(s_supplier)
    #     else:
    #         s_supplier: m_schema.SSupplier = d_db.insert_supplier(
    #             item=m_schema.CreateSupplier(owner_id=employee_id, recommender_id=recommender_id))
    #
    #     return {'code': 200, 'detail': 'success',
    #             'data': {'supplier_id': s_supplier.id, 'employee_id': s_supplier.owner_id}}
    # else:
    #     return {'code': 204, 'detail': '短信验证失败'}

    supplier_list: List[m_schema.SSupplier] = d_db.filter_supplier(items={'phone': data.phone}, search_items={},
                                                                   set_items={}, page=1, page_size=1)
    s_supplier = None
    if supplier_list:
        s_supplier: m_schema.SSupplier = m_schema.SSupplier(id=supplier_list[0].id, recommender_id=data.recommender_id)
        d_db.update_supplier_owner(item=m_schema.SSupplierOwner(id=s_supplier.id, password=data.password, phone=data.phone))
        # d_db.update_supplier(s_supplier)
    else:
        s_supplier_owner: m_schema.SSupplierOwner = d_db.insert_supplier_owner(item=m_schema.CreateSupplierOwner(phone=data.phone, password=data.password))
        s_supplier: m_schema.SSupplier = d_db.insert_supplier(
            item=m_schema.CreateSupplier(owner_id=s_supplier_owner.id, recommender_id=data.recommender_id))

    return {'code': 200, 'detail': 'success',
            'data': {'supplier_id': s_supplier.id, 'employee_id': s_supplier.owner_id}}


@router.post(f'/supplier/register_sure', response_model=dict, summary='供应商注册-确定(也可以用于修改)')
async def supplier_make_sure(supplier: m_supplier.RSupplierMsgAdd):
    d_db.update_supplier(item=supplier.TSupplier)
    d_db.update_supplier_owner(item=supplier.TSupplierOwner)
    # license_list: List[m_schema.SSupplierLicense] = d_db.filter_supplier_license(
    #     items={'supplier_id': supplier.TSupplier.id},
    #     search_items={}, set_items={}, page=1,
    #     page_size=1)
    # if license_list:
    #     s_license: m_schema.SSupplierLicense = license_list[0]
    #     s_license.license = supplier.TSupplierLicense
    #     d_db.update_supplier_license(item=s_license)
    # else:
    #     for c_license in supplier.TSupplierLicense:
    #         c_license.supplier_id = supplier.TSupplier.id
    #         c_license.create_time = datetime.datetime.now()
    #         d_db.insert_supplier_license(item=c_license)
    return {'code': 200, 'detail': 'success'}
#
#
# @router.post(f'/supplier/wx_login', response_model=auth.SupplierLoginRes, summary='商家小程序登录')
# async def supplier_employee_login(code: str) -> auth.SupplierLoginRes:
#     """
#     微信登录，参数为code
#     Login by wx code
#     """
#     supplier_res = wx_service.supplier_login(code)
#     t_employee: schema.TSupplierOwner = d_supplier.get_employee_by_openid(supplier_res.openid)
#     if t_employee is None:
#         t_employee: schema.TSupplierOwner = schema.TSupplierOwner(open_id=supplier_res.openid,
#                                                                   union_id=supplier_res.unionid)
#         t_employee = d_supplier.insert_employee(employee=t_employee)
#     token = token_encode(user_id=t_employee.id)
#     res = auth.SupplierLoginRes(token=token, employee_id=t_employee.id, level_id=t_employee.level_id)
#     return res
#
#
# @router.post(f'/supplier/append', response_model=dict, summary='商家补充资料')
# async def supplier_message_append(items: m_supplier.RSupplierMsgAdd):
#     if items.TSupplier:
#         supplier = items.TSupplier
#         supplier.status = 1
#         d_db.update_supplier(item=supplier)
#     if items.TSupplierOwner:
#         d_db.update_supplier_owner(item=items.TSupplierOwner)
#     if items.TSupplierLicense:
#         for t_license in items.TSupplierLicense:
#             d_db.update_supplier_license(item=t_license)
#     return {'code': 200, 'detail': 'success'}
#
# @router.get(f'/supplier/get_info', summary="获取商家或供应商信息")
# async def supplier_get_info(supplier_id:int):
#     res = d_db.get_supplier(supplier_id)
#     if not res:
#         return {'status': 200, 'detail': '未找到数据'}
#     '''
# |  1 | 待审核    |
# |  2 | 已激活    |
# |  3 | 已驳回    |
# |  4 | 已注销    |
#     '''
#     if res.status != 2:
#         return {'status': 200, 'detail': '此供应商状态未激活'}
#     return res
