from fastapi import APIRouter
from model.address import Success, UserAddress, AddressRequest
from model.res.common import SuccessResponse
from dao import d_address, d_db, d_user
from model.schema import TAddress
from model import m_schema
from typing import List

router = APIRouter()


@router.get('/daddress')
async def delete_address(user_id:int, address_id: int, valcode: str = ''):
    """
    user_id，当前购物车所属的用户的id；address_id，当前地址信息ID; valcode=omgc@XtSAS7XHAkV5ob1VX
    """
    if valcode != 'omgc@XtSAS7XHAkV5ob1VX':
        return {"code": 404, "message": "error!!!!"}
    user_info = d_user.get_user_by_id(user_id)
    if not user_info:
        return {"code": 404, "message": "error!!!"}
    address_info = d_address.get_address_by_id(address_id)
    if not address_info:
        return {"code": 404, "message": "error!!"}
    if user_info.id != address_info.user_id:
        return {"code": 404, "message": "error!"}

    d_address.delete_address_by_id(address_id)
    return {"code": 200, "message": "success"}


@router.post(f'/update', response_model=dict)
async def update_address(address_id: int, item: AddressRequest) -> dict:
    """根据地址id更新地址信息"""
    d_address.update_address_by_id(address_id, item.__dict__)
    return {'code': 200, 'message': 'success'}


@router.get(f'/get', response_model=List[UserAddress])
async def get_address(user_id: int):
    """根据用户id查询该用户的所有收货地址"""
    t_address_list = d_address.get_address(user_id=user_id)
    return [UserAddress.parse_obj(t.__dict__) for t in t_address_list]


@router.post(f'/set_default', response_model=SuccessResponse, summary='设置默认地址接口')
def set_default_address(user_id: int, address_id: int):
    """将用户地址列表下的某个地址设置为默认地址"""
    f_address: List[m_schema.SAddress] = d_db.filter_address(items={'user_id': user_id}, search_items={}, set_items={})
    for address in f_address:
        if address.id == address_id:
            address.default_ = 1
            d_db.update_address(item=address)
        else:
            address.default_ = 0
            d_db.update_address(item=address)
    return SuccessResponse()


@router.post('/create', response_model=m_schema.SAddress, summary='添加地址（自动设置为默认地址）')
async def add_address(item: m_schema.CreateAddress) -> m_schema.SAddress:
    """创建地址时自动设置为默认地址"""
    s_address: m_schema.SAddress = d_db.insert_address(item=item)
    if set_default_address(user_id=s_address.user_id, address_id=s_address.id):
        s_address.default_ = 1
    return s_address
