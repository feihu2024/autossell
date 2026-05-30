import datetime
from dao import d_store
from fastapi import APIRouter
from dao import d_db
from model import m_schema
from model.m_schema import *
from router.mall import user
from router import r_schema
from pydantic import Field, BaseModel
from typing import Optional, List

router = APIRouter()


class AStoreCount(BaseModel):
    total: Optional[int] = Field(title='商家总数')
    current: Optional[int] = Field(title='当日新增商家')
    cancel: Optional[int] = Field(title='停用商家数')
    review: Optional[int] = Field(title='审核中商家')


class AStoreMsgAdd(BaseModel):
    s_Store: Optional[m_schema.SStore] = Field(title='店铺信息')
    s_StoreOwner: Optional[m_schema.SStoreOwner] = Field(title='店铺负责人信息')


class AStoreMsg(AStoreMsgAdd):
    s_StoreState: Optional[m_schema.SStoreState] = Field(title='店铺状态信息')
    s_StoreAmount: Optional[m_schema.SStoreAmount] = Field(title='店铺资金信息')
    s_User: Optional[m_schema.SUser] = Field(title='店铺推荐人')


class AStoreMsgList(BaseModel):
    data: Optional[List[AStoreMsg]]
    total: Optional[int]


class AStoreLicense(BaseModel):
    SStoreOwner: Optional[m_schema.SStoreOwner] = Field(title='店铺负责人信息')
    SStoreLicense: Optional[m_schema.FilterResStoreLicense] = Field(title='店铺资质信息')


@router.get(f'/store_count/get', response_model=AStoreCount, summary='获取店铺统计数据')
async def store_count() -> AStoreCount:
    total: int = d_store.store_count()
    current: int = d_store.current_store_count()
    cancel: int = d_store.cancel_store_count(status_id=4)
    review: int = d_store.review_store_count(status_id=1)

    return AStoreCount(total=total, current=current, cancel=cancel, review=review)


@router.post(f'/store_list/get', response_model=AStoreMsgList, summary='获迪店铺列表')
async def get_store_list(
        id: Optional[int] = None,
        name: Optional[str] = None,
        owner: Optional[str] = None,
        owner_id: Optional[int] = None,
        phone: Optional[str] = None,
        status: Optional[int] = None,
        area: Optional[str] = None,
        supplier_id: Optional[str] = None,
        register_start: Optional[str] = None,
        register_end: Optional[str] = None,
        expired_start: Optional[str] = None,
        expired_end: Optional[str] = None,
        expired: Optional[str] = None,
        page: Optional[int] = 1,
        page_size: Optional[int] = 20
):
    f_store_return: dict = await d_store.query_store(id, name, owner, owner_id, phone, status, area, supplier_id,
                                                     register_start, register_end, expired_start, expired_end,
                                                     expired, page, page_size)

    total_size: int = f_store_return['total']
    store_msg_list: AStoreMsgList = AStoreMsgList(data=[], total=total_size)
    for t_store in f_store_return['data']:
        a_store_msg: AStoreMsg = AStoreMsg()
        for i in range(len(t_store)):
            t_model = t_store[i]
            if t_model is None:
                continue
            obj_name: str = type(t_model).__name__
            s_model_name: str = 'S' + obj_name[1:]
            cls = globals()[s_model_name]
            attr: str = cls.__name__
            attr: str = attr[0].lower() + '_' + attr[1:]
            setattr(a_store_msg, attr, cls.parse_obj(t_model.__dict__))

        if a_store_msg.s_Store is not None:
            a_store_msg.s_StoreAmount = await d_store.get_amount_by_store_id(store_id=a_store_msg.s_Store.id)

        store_msg_list.data.append(a_store_msg)

    return store_msg_list


@router.post(f'/store_members/get', response_model=m_schema.FilterResOrder, summary='获取店铺会员列表')
async def get_members(store_id: int, user_id: Optional[str] = None, username: Optional[str] = None,
                      consume_start: Optional[str] = None, consume_end: Optional[str] = None,
                      phone: Optional[str] = None, page: Optional[int] = 1, page_size: Optional[int] = 20):
    if consume_start and consume_end:
        paid_time_interval = consume_start + ',' + consume_end
        f_orders: m_schema.FilterResOrder = await r_schema.filter_order(store_id=str(store_id), paider_id=user_id,
                                                                        paid_time=paid_time_interval,
                                                                        s_paider_name=username, paider_phone=phone,
                                                                        page=page, page_size=page_size)

    else:
        f_orders: m_schema.FilterResOrder = await r_schema.filter_order(store_id=str(store_id), paider_id=user_id,
                                                                        s_paider_name=username, paider_phone=phone,
                                                                        page=page, page_size=page_size)

    return f_orders


@router.get(f'/store_license/get', response_model=AStoreLicense, summary='获取店铺资质')
async def get_store_license(store_id: int):
    s_store: m_schema.SStore = await r_schema.get_store(store_id=store_id)
    s_store_owner: m_schema.SStoreOwner = await r_schema.get_store_owner(store_owner_id=s_store.owner_id)
    f_licenses: m_schema.FilterResStoreLicense = await r_schema.filter_store_license(store_id=str(store_id))

    return AStoreLicense(SStoreOwner=s_store_owner, SStoreLicense=f_licenses)


@router.post(f'/store/register_next', response_model=m_schema.SStore, summary='注册店铺-下一步')
async def register_store(item: m_schema.CreateStore):
    store: m_schema.SStore = d_db.insert_store(item=item)
    return store


@router.post(f'/store/register_sure', response_model=List[m_schema.SStoreLicense], summary='注册店铺-确定')
async def register_sure(items: List[m_schema.CreateStoreLicense]):
    licenses = []
    for item in items:
        item.create_time = datetime.now()
        licenses.append(d_db.insert_store_license(item=item))
    return licenses


@router.get(f'/store/set_default', response_model=dict, summary='设置默认店铺')
async def set_default_store(store_id: int):
    store: m_schema.SStore = d_db.get_store(store_id=store_id)
    stores: List[m_schema.SStore] = d_db.filter_store(items={'supplier_id': store.supplier_id}, search_items={},
                                                      set_items={}, page=1, page_size=100)
    for store in stores:
        if store.id == store_id:
            store.is_default = 1
            d_db.update_store(item=store)
        else:
            store.is_default = 0
            d_db.update_store(item=store)

    return {'code': 200, 'detail': 'success'}


@router.post(f'/store/append', response_model=dict, summary='店铺补充资料')
async def store_message_append(items: AStoreMsgAdd):
    if items.s_Store:
        items.s_Store.status = 1
        d_db.update_store(item=items.s_Store)
    if items.s_StoreOwner:
        d_db.update_store_owner(item=items.s_StoreOwner)
    return {'code': 200, 'detail': 'success'}


@router.post(f'/store_owner/create', response_model=dict, summary='创建/绑定负责人')
async def store_owner_create(code: str, item: m_schema.CreateStoreOwner):
    res: dict = await user.verify_phone_code(code=code, phone=item.phone)
    if res['detail'] == 'success':
        store_owner_list = d_db.filter_store_owner(items={'phone': item.phone}, search_items={}, set_items={}, page=1,
                                                   page_size=1)
        if store_owner_list:
            return {'detail': 'success', 'data': {'store_owner_id': store_owner_list[0].id}}
        else:
            owner: m_schema.SStoreOwner = d_db.insert_store_owner(item=item)
            return {'detail': 'success', 'data': {'store_owner_id': owner.id}}
    else:
        return {'detail': '短信验证失败', 'data': {}}
