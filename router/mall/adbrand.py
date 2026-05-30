from dao import d_db, d_query, d_user, d_bigorder, d_adbrand, d_good
from model.m_schema import *
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Request
from .user import verify_token

# router = APIRouter()
router = APIRouter(dependencies=[Depends(verify_token)])


@router.get(f"/get/list/all", summary="获取当前用户创建的广告列表")
async def get_list(request: Request, page:int=1):
    """
        t_coin
    """
    page = page
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "user_ad",
        "joins": [
            {
                "table": "user_adbrand",
                "on_left": "adbrand_id",
                "on_right": "id"
            }
        ],
        "selects": ["user_ad"],
        "filters": [
            {
                "field": "user_ad.user_id",
                "value": user_id
            },
            {
                "field": "user_ad.is_del",
                "value": 0
            }
        ],
        "order_by": [{"field": "user_ad.is_del", "order": "asc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res

@router.get(f"/get/barnd/default", summary="获取默认模板表")
async def get_list_brand_default(request: Request, page:int=1):
    """
        t_coin
    """
    page = page
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "user_adbrand",
        "selects": ["user_adbrand"],
        "filters": [
            {
                "field": "user_adbrand.is_default",
                "value": 1
            },
            {
                "field": "user_adbrand.is_del",
                "value": 0
            }
        ],
        "order_by": [{"field": "user_adbrand.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res

#绑定项目
@router.post(f'/add/ad', summary="绑定项目")
async def add_user_ad(request: Request, item: d_adbrand.AddAd):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if item.model_id is None:
        return '未知项目模板！'
    uinfo = d_user.get_user_by_id(user_id)
    if not uinfo:
        return '未授权用户！'
    if uinfo.nickname is None or uinfo.phone is None:
        return '请完善用户信息！'
    if not uinfo.nickname or not uinfo.phone:
        return '请完善用户信息！！'
    model_info = d_adbrand.get_brand_info(item.model_id)
    if not model_info:
        return '项目模板选择错误！'
    if model_info.is_del > 0:
        return '项目模板选择错误！!'
    add_num = d_adbrand.get_ad_count(user_id, item.model_id)
    if add_num >= 1:
        return '此模板创建广告超限！'
    item.user_name = uinfo.nickname
    item.user_phone = uinfo.phone
    item.qr_code_user = uinfo.ercode
    d_adbrand.add_user_ad(item)
    return 'success'

@router.post(f'/update/ad', summary="更新广告信息")
async def update_user_ad(request: Request, item: d_adbrand.AddAd):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if item.ad_id is None:
        return '未知广告内容！'
    ad_info = d_adbrand.get_ad_info(item.ad_id)
    if ad_info:
        if ad_info.user_id != user_id:
            return '非法操作！'
        d_adbrand.update_ad(item)
        return 'success'
    else:
        return '未找到广告内容!'


@router.post(f'/del/ad', summary="删除用户广告")
async def del_user_ad(request: Request, item: d_adbrand.AddAd):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if item.ad_id is None:
        return '未知广告内容！'
    ad_info = d_adbrand.get_ad_info(item.ad_id)
    if ad_info:
        if ad_info.user_id != user_id:
            return '非法操作！'
        d_adbrand.del_ad(item)
        return 'success'
    else:
        return '未找到广告内容!'

@router.get('/get/ad/brand', summary='获取广告页用户配置和项目模板数据')
async def get_ad_brand_list(request: Request, ad_id:int = 0):
    """
    ad_id，创建广告的id
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if ad_id > 0:
        return_item = d_adbrand.get_adbrand_info(user_id, ad_id)
        if return_item:
            level_three = d_bigorder.get_bigorder_set('ad_video')
            if level_three.val_int > 0:
                return_item.TUserAdbrand.video = ''
        return return_item
    else:
        return '未知广告'

@router.get('/get/ad/model', summary='获取项目模板详情')
async def get_ad_brand_model(request: Request, model_id:int = 0):
    """
    model_id，项目模板id
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if model_id > 0:
        return d_adbrand.get_brand_info(model_id)

@router.get('/get/goods/list', summary='获取广告页商品列表')
async def get_goods_list(request: Request, good_id:str = ''):
    """
    good_id，商品id，如：112,113,114,115
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    goods = []
    for t in good_id.split(','):
        try:
            nn = int(t)
            if nn > 0:
                goods.append(nn)
        except:
            pass
    if len(goods) > 0:
        return d_good.get_good_for_ids(goods)
    else:
        return '未找到商品！'

@router.post('/update/ad/userinfo', summary='更新广告用户详情')
async def update_ad_brand_userinfo(request: Request, data:d_adbrand.AddAdUinfo):
    """
    user_id:    '用户id'
    user_name:      '用户昵称'
    user_phone:     '用户电话'
    qr_code_user:      '用户微信'
    qr_code_enterprise:      企业微信'
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if data.update_id is None:
        d_adbrand.add_adbrand_ad_uinfo(data)
    else:
        ad_info = d_adbrand.get_adbrand_ad_uinfo(data.update_id)
        if ad_info:
            if ad_info.user_id == user_id:
                d_adbrand.update_adbrand_ad_uinfo(data)
            else:
                return '您无权修改！'
        else:
            return '未找到数据！'
    return 'success'

@router.get('/get/ad/user/info', summary='获取广告用户详情')
async def get_ad_user_info(request: Request):
    """
    ad_id，创建广告的id
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    return d_adbrand.get_adbrand_ad_uinfo_for_userid(user_id)

@router.get('/get/ad/brand/menu', summary='获取广告扩展菜单列表')
async def get_ad_brand_menu(request: Request, adbrand_id:int, page:int=1):
    """
    adbrand_id，创建广告的id
    page  页码
    """
    page_size: int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "user_adbrand_menu",
        "selects": ["user_adbrand_menu"],
        "filters": [
            {
                "field": "user_adbrand_menu.adbrand_id",
                "value": adbrand_id
            },
            {
                "field": "user_adbrand_menu.is_del",
                "value": 0
            },
            {
                "field": "user_adbrand_menu.is_hide",
                "value": 0
            }
        ],
        "order_by": [{"field": "user_adbrand_menu.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res

@router.get('/get/ad/brand/menu/file', summary='获取广告扩展菜单的文件列表')
async def get_ad_brand_menu_file(request: Request, adbrand_id:int, menu_id:int, page:int=1):
    """
    adbrand_id，创建广告的id;
    menu_id,  文件列表对象id
    """
    page_size: int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "user_adbrand_file",
        "selects": ["user_adbrand_file"],
        "filters": [
            {
                "field": "user_adbrand_file.adbrand_id",
                "value": adbrand_id
            },
            {
                "field": "user_adbrand_file.menu_id",
                "value": menu_id
            },
            {
                "field": "user_adbrand_file.is_del",
                "value": 0
            }
        ],
        "order_by": [{"field": "user_adbrand_file.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res
