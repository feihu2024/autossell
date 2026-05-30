import datetime, time
import random
import ssl
import json
import urllib.error
import io, qrcode
import requests
import numpy as np
import logging
import uuid
from pathlib import Path
from config import DIRS

from dao import d_user, d_db, d_account, d_groupsir, d_good, d_address, d_order, d_query, d_bigorder, d_found
import urllib.request as urllib2
from urllib.parse import urlencode
from model.res.auth import LoginRes, UserRequest, UserRequestPhone
from model.schema import TUser, TUserAccount
from model import m_schema
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Body, Depends, Header, Request, UploadFile, File
from service.auth_service import token_encode
from service import express_service, wx_service
from model.mall import m_order, m_account
from PIL import Image, ImageDraw, ImageFont
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from common import global_define, global_function
from model import schema
from dao.task import d_task
from config import SECRET
from fastapi.responses import JSONResponse
from service import qiniu_service

async def verify_token(welcomesession: str = Header(...)):
    #if welcomesession != "fake-super-secret-token":
    if not d_user.is_login(welcomesession):
        raise HTTPException(status_code=400, detail="login invalid")

router = APIRouter()

class GoodspecPostpic(BaseModel):
    user_id: Optional[int] = Field(None, title='推广人id')
    path: Optional[str] = Field(None, title='推广地址 /page/....')
    spec_id:  Optional[int] = Field(None, title='规格id，用于获取那个规格的海报图片')
    style: Optional[str] = Field(None, title='样式，为生成各种样式推广海报预留的参数')

class Posterpic(BaseModel):
    user_id: Optional[int] = Field(None, title='推广人id')
    poster_id: Optional[int] = Field(None, title='选中海报图的id')
    poster_url: Optional[str] = Field(None, title='选中的海报地址')
    path: Optional[str] = Field(None, title='推广地址 /page/....')

class UpdateUser(BaseModel):
    id: Optional[int] = Field(None, title='用户id')
    nickname: Optional[str] = Field(None, title='用户昵称')
    avatar: Optional[str] = Field(None, title='头像url')
    phone: Optional[str] = Field(None, title='手机电话号码')
    valcode: Optional[str] = Field(None, title='post提交code')
    ercode: Optional[str] = Field(None, title='个人二维码')

class RegistUser(BaseModel):
    nickname: Optional[str] = Field(None, title='用户昵称')
    phone: Optional[str] = Field(None, title='手机电话号码')
    code: Optional[str] = Field(None, title='手机验证码')
    passwd: Optional[str] = Field(None, title='登录密码')
    valcode: Optional[str] = Field(None, title='邀请码code')


class UpdatePassUser(BaseModel):
    phone: Optional[str] = Field(None, title='手机电话号码')
    old_passwd: Optional[str] = Field(None, title='旧密码')
    new_passwd: Optional[str] = Field(None, title='新密码')
    new_passwd2: Optional[str] = Field(None, title='重复新密码')

class UpdatePayPass(BaseModel):
    phone: Optional[str] = Field(None, title='手机电话号码')
    code: Optional[str] = Field(None, title='手机验证码')
    pay_passwd: Optional[str] = Field(None, title='支付密码')
    pay_passwd2: Optional[str] = Field(None, title='重复支付密码')

@router.get(f'/logintest', summary='获取测试token')
async def logintest():
    """
    返回：welcomesession携带到请求体head中，作为后端接口请求的token
    """
    return d_user.userpass_login_for_token('usertest','kc1n6MVB')

# @router.post("/userpass_login", summary='账号密码登录')
# def userpass_login(data: UserRequest):
#     """
#     账号密码方式验证登录，获取授权token，头部参数：welcomesession
#     """
#     re_val = {"user_id":"","nickname":"","token":"","avatar":""}
#     user = d_user.get_user_by_phone(data.phone)
#     if not user:
#         return re_val
#     token = d_user.userpass_login_for_token_byphone(data.phone, data.password)
#     if token:
#         #raise HTTPException(status_code=200, detail={'token': token, 'massage': 'Success'}, headers={"data": '123'})
#         re_val["user_id"] = user.id
#         re_val["nickname"] = user.nickname
#         re_val["token"] = token
#         re_val["avatar"] = user.avatar
#         #更新用户级别
#         d_user.jny_parter_up(user.id)
#     # res = LoginRes(token=token, user_id=t_user.id, nickname=t_user.nickname, avatar=t_user.avatar)
#     return re_val
#
# @router.post("/userphone_login", summary='短信验证登录')
# def userphone_login(data: UserRequestPhone):
#     """
#     手机号码方式验证登录，获取授权token
#     """
#     re_val = {"user_id": "", "nickname": "", "token": "", "avatar": ""}
#     user = d_user.get_user_by_phone(data.phone)
#     if not user:
#         return re_val
#     user_phone_code: List[m_schema.SUserPhoneCode] = d_db.filter_user_phone_code(items={'code': data.code, 'phone': data.phone}, search_items={},set_items={}, page=1, page_size=1)
#     if user_phone_code:
#         phone_code = user_phone_code[0].code
#         send_time = user_phone_code[0].send_time
#         seconds = user_phone_code[0].expired_time
#         time_now = datetime.datetime.now()
#         over_time = send_time + datetime.timedelta(seconds=seconds)
#         if time_now > over_time:
#             raise HTTPException(status_code=201, detail='验证码过期')
#         if phone_code != data.code:
#             raise HTTPException(status_code=202, detail='验证码错误')
#
#         token = d_user.userphone_login_for_token(data.phone)
#         if token:
#             # raise HTTPException(status_code=200, detail={'token': token, 'massage': 'Success'}, headers={"data": '123'})
#             re_val["user_id"] = user.id
#             re_val["nickname"] = user.nickname
#             re_val["token"] = token
#             re_val["avatar"] = user.avatar
#             # 更新用户级别
#             d_user.jny_parter_up(user.id)
#
#     return re_val

#
# @router.post("/user_regist", summary='账号注册')
# def user_regist(data: RegistUser):
#     """
#     手机号的验证码，和邀请码需要正确才能注册
#     (测试邀请码：2345)
#     """
#     old_user_info = d_user.get_user_by_phone(data.phone)
#     if old_user_info:
#         return {'code': 404, 'detail': '手机号已经存在'}
#     user_phone_code: List[m_schema.SUserPhoneCode] = d_db.filter_user_phone_code(items={'code': data.code, 'phone': data.phone}, search_items={}, set_items={}, page=1, page_size=1)
#     if not user_phone_code:
#         return {'code': 404, 'detail': '验证码错误'}
#     user = d_user.get_user_by_code(data.valcode)
#     if not user:
#         return {'code': 404, 'detail': '邀请码错误'}
#     parend_id = user.id
#     if user.parent_id:
#         parend_id = user.parent_id
#     insert_user = TUser(
#         nickname=data.nickname,
#         password=data.passwd,
#         phone=data.phone,
#         invited_user_id=user.id,
#         invited_code=global_function.get_randoms(10),
#         parent_id=parend_id
#     )
#     user_info = d_user.insert_user(insert_user)
#     if user_info:
#         d_account.create_account(TUserAccount(
#             user_id=user_info.id,
#             balance=0,
#             lock_balance=0,
#             coin=0,
#             create_time=datetime.datetime.now()
#         ))
#
#     return {'code': 200, 'detail': 'success'}
#
#
# @router.post("/update_passwd", dependencies=[Depends(verify_token)], summary='修改密码')
# def user_regist(request: Request,data: UpdatePassUser):
#     """
#     重置登录密码，数字/字母结合6位以上混合字串
#     """
#     if global_function.is_simple_password(data.new_passwd):
#         return {'code': 404, 'detail': '密码至少6位以上，数字/字母...结合'}
#     if data.new_passwd != data.new_passwd2:
#         return {'code': 404, 'detail': '两次设置新密码不一致'}
#     welcomesession = request.headers.get('welcomesession')
#     user_id = d_user.get_login_id(welcomesession)
#     user_info = d_user.get_user_by_phone(data.phone)
#     if user_info.id != user_id:
#         return {'code': 404, 'detail': '非法操作'}
#     # user_phone_code: List[m_schema.SUserPhoneCode] = d_db.filter_user_phone_code(items={'code': data.code, 'phone': data.phone}, search_items={}, set_items={}, page=1, page_size=1)
#     # if not user_phone_code:
#     #     return {'code': 404, 'detail': '验证码错误'}
#     # user = d_user.get_user_by_code(data.valcode)
#     d_user.update_user_passwd(user_info.id, data.new_passwd)
#     return {'code': 200, 'detail': 'success'}


@router.post("/update_paypasswd", summary='修改支付密码')
def update_paypasswd(request: Request,data: UpdatePayPass):
    """
    修改支付密码，需要短信验证，且当前登录用户
    """
    if global_function.is_simple_password(data.pay_passwd):
        return {'code': 404, 'detail': '密码至少6位以上，数字/字母...结合'}
    if data.pay_passwd != data.pay_passwd2:
        return {'code': 404, 'detail': '两次设置新密码不一致'}
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    user_info = d_user.get_user_by_phone(data.phone)
    if user_info.id != user_id:
        return {'code': 404, 'detail': '非法操作'}
    # user_phone_code: List[m_schema.SUserPhoneCode] = d_db.filter_user_phone_code(items={'code': data.code, 'phone': data.phone}, search_items={}, set_items={}, page=1, page_size=1)
    # if not user_phone_code:
    #     return {'code': 404, 'detail': '验证码错误'}
    # user = d_user.get_user_by_code(data.valcode)
    d_user.update_user_paypwd(user_info.id, data.pay_passwd)
    return {'code': 200, 'detail': 'success'}


@router.get("/update_wx_openid", dependencies=[Depends(verify_token)], summary='更新微信openid，否则不能支持微信支付')
def update_wx_openid(request: Request, code: str):
    """
    微信登录，参数为code，例如 `/web/.../update_wx_openid?code=xxxxxx`
    更新微信openid，否则不能支持微信支付
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    wx_res = wx_service.wx_login(code)
    if 'openid' in wx_res:
        d_user.update_user_openid(user_id, wx_res["openid"], "no")
    return wx_res


@router.get("/wx_login", response_model=LoginRes, summary='微信登录接口')
def wx_login(code: str, user_id:int = 0) -> LoginRes:
    """
    微信登录，参数为code，例如 `/mall/wx_login?code=xxxxxx&user_id=1`
    Login by wx code
    user_id,是推荐人用户的id
    """
    wx_res = wx_service.wx_login(code)
    t_user = d_user.get_user_by_openid(wx_res.openid)
    if t_user is None:
        if user_id > 0:
            tui_user_info = d_user.get_user_by_id(user_id)
            tuan_id = 0
            if tui_user_info:
                if tui_user_info.is_tuan > 0:
                    tuan_id = tui_user_info.id
                else:
                    tuan_id = tui_user_info.tuan_id
            t_user = TUser(open_id=wx_res.openid, union_id=wx_res.unionid,parent_id=user_id,invited_user_id=user_id, tuan_id=tuan_id)
            #raise HTTPException(status_code=404, detail='error')
            t_user = d_user.insert_user(t_user)
            #更新入团日志
            d_task.add_groupuser_log(t_user.id, tuan_id, 0, global_define.groupsir_type[0])
            #更新团成员
            #d_groupsir.add_groupsir(t_user.id, user_id, '新用户入团')
            #更新赠予积分
            # account_info = d_account.get_account_info_add(t_user.id)
            # coin_num = account_info.coin + global_define.platform_prize['prize3']
            # d_account.update_account_by_id(account_info.id, {"coin":coin_num})
            #发送通知
            # d_db.insert_notice(item=m_schema.CreateNotice(
            #     user_ids=str(t_user.id),
            #     type='系统通知',
            #     title='新用户注册',
            #     description=global_define.new_user_notice,
            #     status=0
            # ))
            #给推荐人赠送积分并发送通知
            # acount_info = d_account.get_account_info(user_id)
            # if acount_info:
            #     total_coin = acount_info.coin + global_define.recommend_coin
            #     d_account.update_account_by_id(acount_info.id, {"coin": total_coin})
            #     coin_model = m_account.CoinModel(
            #         user_id=user_id,
            #         change=global_define.recommend_coin,
            #         coin=total_coin,
            #         type=global_define.balance_type[29],
            #         create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            #         description=global_define.balance_type[29]
            #     )
            #     d_account.insert_coin(coin_model)
        else:
            #t_user = TUser(open_id=wx_res.openid, union_id=wx_res.unionid,parent_id=-1)
            t_user = TUser(open_id=wx_res.openid, union_id=wx_res.unionid)
            t_user = d_user.insert_user(t_user)
            #更新赠予积分
            # account_info = d_account.get_account_info_add(t_user.id)
            # coin_num = account_info.coin + global_define.platform_prize['prize3']
            # d_account.update_account_by_id(account_info.id, {"coin":coin_num})
            #发送通知
            # d_db.insert_notice(item=m_schema.CreateNotice(
            #     user_ids=str(t_user.id),
            #     type='系统通知',
            #     title='新用户注册',
            #     description=global_define.new_user_notice,
            #     status=0
            # ))

    # 更新系统用户级别
    if t_user.level_id == 0:
        d_user.update_sysuser_active(t_user.id)
    elif t_user.level_id == 1:
        d_user.update_sysuser_high(t_user.id)
    elif t_user.level_id == 2:
        d_user.update_sysuser_top(t_user.id)

    # 更新推广用户级别
    # d_user.update_user_top(t_user.id)

    token = d_user.userid_login_for_token(user_id=t_user.id)
    res = LoginRes(token=token['token_val'], user_id=t_user.id, nickname=t_user.nickname, avatar=t_user.avatar)
    return res


# @router.get(f'/check', response_model=dict, summary="是否实名")
# async def user_check(user_id: int):
#     user = d_db.get_user(user_id=user_id)
#     if user is not None:
#         if user.is_agree == 1:
#             return {'code': 1, 'detail': '该用户已实名', 'data': {'username': user.username, 'idcard': user.id_card}}
#         else:
#             return {'code': 0, 'detail': '该用户未实名'}
#     else:
#         return {'code': 2, 'detail': '该用户不存在'}
#
#
# @router.post('/check_idcard', dependencies=[Depends(verify_token)], response_model=dict, summary='用户实名认证')
# async def user_check_idcard(user_id: int, name: str, idcard: str):
#     host = 'https://idcert.market.alicloudapi.com'
#     path = '/idcard'
#     appcode = 'ac375fe220064a038b864231ba5b820d'  # 开通服务后 买家中心-查看AppCode
#     query = urlencode({'idCard': idcard, 'name': name})
#     url = host + path + '?' + query
#     logging.info(f"user_check_idcard，idCard: {idcard}，name: {name}")
#     #idcard唯一性验证
#     get_card = d_user.get_user_forcard(idcard)
#     if get_card:
#         raise HTTPException(status_code=400, detail="认证信息已存在")
#     request = urllib2.Request(url)
#     request.add_header('Authorization', 'APPCODE ' + appcode)
#     ctx = ssl.create_default_context()
#     ctx.check_hostname = False
#     ctx.verify_mode = ssl.CERT_NONE
#     try:
#         response = urllib2.urlopen(request, context=ctx)
#         content = json.loads(response.read().decode(encoding='utf-8'))
#     except Exception as e:
#         logging.info(f"user_check_idcard，Exception: {e}")
#
#     if content['status'] == '01':
#         d_db.update_user(item=m_schema.SUser(id=user_id, username=name, name=name, id_card=idcard, is_agree=1))
#         return {'code': 200, 'message': 'success'}
#     else:
#         logging.info(f"user_check_idcard，HTTPException: {content['msg']}")
#         raise HTTPException(status_code=400, detail=content['msg'])

#
# @router.get(f'/send_phone_code', dependencies=[Depends(verify_token)], summary="发送短信验证码")
# async def send_phone_code(request: Request, phone: str):
#     """
#     手机号码验证
#     """
#     # employee_id: 代表商家负责人id
#     # store_owner_id: 代表店铺负责人id
#     # worker_id: 代表普通员工id
#     welcomesession = request.headers.get('welcomesession')
#     user_id = d_user.get_login_id(welcomesession)
#     user_id: Optional[int] = None
#     employee_id: Optional[int] = None
#     store_owner_id: Optional[int] = None
#     worker_id: Optional[int] = None
#     code = str(random.randint(100000, 999999))
#     content = express_service.query_duanxin(phone, code)
#     content = json.loads(content)
#     if content['status'] == 'OK':
#         if user_id is not None:
#             phone_code: List[m_schema.SUserPhoneCode] = d_db.filter_user_phone_code(items={'user_id': user_id},
#                                                                                     search_items={}, set_items={},
#                                                                                     page=1,
#                                                                                     page_size=1)
#             if phone_code:
#                 phone_code[0].code = code
#                 phone_code[0].send_time = datetime.datetime.now()
#                 d_db.update_user_phone_code(phone_code[0])
#             else:
#                 d_db.insert_user_phone_code(
#                     item=m_schema.CreateUserPhoneCode(user_id=user_id, phone=phone, code=code, expired_time=5 * 60,
#                                                       send_time=datetime.datetime.now()))
#         elif employee_id is not None:
#             phone_code: List[m_schema.SUserPhoneCode] = d_db.filter_user_phone_code(items={'employee_id': employee_id},
#                                                                                     search_items={}, set_items={},
#                                                                                     page=1, page_size=1)
#             if phone_code:
#                 phone_code[0].code = code
#                 phone_code[0].send_time = datetime.datetime.now()
#                 d_db.update_user_phone_code(phone_code[0])
#             else:
#                 d_db.insert_user_phone_code(
#                     item=m_schema.CreateUserPhoneCode(employee_id=employee_id, phone=phone, code=code,
#                                                       expired_time=5 * 60,
#                                                       send_time=datetime.datetime.now()))
#
#         elif store_owner_id is not None:
#             phone_code: List[m_schema.SUserPhoneCode] = d_db.filter_user_phone_code(
#                 items={'store_owner_id': store_owner_id},
#                 search_items={}, set_items={},
#                 page=1, page_size=1)
#             if phone_code:
#                 phone_code[0].code = code
#                 phone_code[0].send_time = datetime.datetime.now()
#                 d_db.update_user_phone_code(phone_code[0])
#             else:
#                 d_db.insert_user_phone_code(
#                     item=m_schema.CreateUserPhoneCode(store_owner_id=store_owner_id, phone=phone, code=code,
#                                                       expired_time=5 * 60,
#                                                       send_time=datetime.datetime.now()))
#
#         elif worker_id is not None:
#             phone_code: List[m_schema.SUserPhoneCode] = d_db.filter_user_phone_code(items={'worker_id': worker_id},
#                                                                                     search_items={}, set_items={},
#                                                                                     page=1, page_size=1)
#             if phone_code:
#                 phone_code[0].code = code
#                 phone_code[0].send_time = datetime.datetime.now()
#                 d_db.update_user_phone_code(phone_code[0])
#             else:
#                 d_db.insert_user_phone_code(
#                     item=m_schema.CreateUserPhoneCode(worker_id=worker_id, phone=phone, code=code, expired_time=5 * 60,
#                                                       send_time=datetime.datetime.now()))
#         else:
#             d_db.insert_user_phone_code(
#                 item=m_schema.CreateUserPhoneCode(phone=phone, code=code, expired_time=5 * 60,
#                                                   send_time=datetime.datetime.now()))
#
#         return {'code': 200, 'message': 'success'}
#     else:
#         return {'code': 204, 'message': 'fail'}



#
# @router.get(f'/verify_phone_code', response_model=dict, summary='校验短信验证码')
# async def verify_phone_code(code: str, phone: Optional[str] = None, user_id: Optional[int] = None,
#                             employee_id: Optional[int] = None, store_owner_id: Optional[int] = None,
#                             worker_id: Optional[int] = None):
#     if user_id is not None and employee_id is not None:
#         return {'code': 204, 'detail': '参数过多'}
#
#     user_phone_code: List[m_schema.SUserPhoneCode] = d_db.filter_user_phone_code(items={'code': code, 'phone': phone},
#                                                                                  search_items={},
#                                                                                  set_items={}, page=1, page_size=1)
#     if user_id is not None:
#         user_phone_code: List[m_schema.SUserPhoneCode] = d_db.filter_user_phone_code(items={'user_id': user_id},
#                                                                                      search_items={},
#                                                                                      set_items={}, page=1, page_size=1)
#     if employee_id is not None:
#         user_phone_code: List[m_schema.SUserPhoneCode] = d_db.filter_user_phone_code(items={'employee_id': employee_id},
#                                                                                      search_items={},
#                                                                                      set_items={}, page=1, page_size=1)
#     if store_owner_id is not None:
#         user_phone_code: List[m_schema.SUserPhoneCode] = d_db.filter_user_phone_code(
#             items={'store_owner_id': store_owner_id},
#             search_items={},
#             set_items={}, page=1, page_size=1)
#     if worker_id is not None:
#         user_phone_code: List[m_schema.SUserPhoneCode] = d_db.filter_user_phone_code(items={'worker_id': worker_id},
#                                                                                      search_items={},
#                                                                                      set_items={}, page=1, page_size=1)
#
#     if user_phone_code:
#         phone_code = user_phone_code[0].code
#         send_time = user_phone_code[0].send_time
#         seconds = user_phone_code[0].expired_time
#         time_now = datetime.datetime.now()
#         over_time = send_time + datetime.timedelta(seconds=seconds)
#         if time_now > over_time:
#             raise HTTPException(status_code=201, detail='验证码过期')
#         if phone_code != code:
#             raise HTTPException(status_code=202, detail='验证码错误')
#         if over_time > time_now and phone_code == code:
#             return {'detail': 'success', 'data': {}}
#     else:
#         raise HTTPException(status_code=203, detail='用户不存在')
#
#
@router.get(f'/get_wx_phone', dependencies=[Depends(verify_token)], summary='获取微信手机号')
async def get_wx_phone(code: str):
    phone_info = wx_service.mall_wx_sdk.get_phone_number(code=code)
    phone_info = phone_info.phone_info

    return {"phoneNumber":phone_info.phoneNumber,"purePhoneNumber":phone_info.purePhoneNumber,"countryCode":phone_info.countryCode}

# @router.get(f'/get_user_list', response_model=list, summary='获取用户列表')
# async def get_user_list(get_page: int = 1):
#     user = d_db.get_users_list(page=get_page)
#     return user

# @router.get(f'/phone/get_userinfo', summary='通过手机号获取用户基础信息')
# async def get_userinfo_phone(phone: str = ''):
#     res_fetch = d_user.get_user_by_phone(phone)
#     #print('------------------------------------')
#     #print(res_fetch)
#     return_fetch = {
#         "user_id":res_fetch.id,
#         "user_name": res_fetch.username,
#         "nickname": res_fetch.nickname,
#         "avatar": res_fetch.avatar
#     }
#     return return_fetch

@router.post(f'/get_user_post_pic', dependencies=[Depends(verify_token)], summary='获取用户推广产品二维码,带参?user_id=n')
async def get_user_post_pic(data:GoodspecPostpic):
    """
    获取商品的推广二维码，使用规格上面配置的海报图和产品主图生成图像
    返回png格式的图像二进制码
    """
    if data.spec_id is None:
        raise HTTPException(status_code=304, detail='规格参数错误')
    data_spec = d_good.get_good_spec_by_id(data.spec_id)
    if not data_spec:
        raise HTTPException(status_code=304, detail='未找到规格数据')
    data_good = d_good.get_good_data(data_spec.good_id)
    if not data_good:
        raise HTTPException(status_code=304, detail='未找到商品数据')

    #haibao = './pic_package/haibao_online.jpg'
    #haibao = './pic_package/haibao_online3.jpg'
    #haibao = './pic_package/haibao_online5.jpg'
    haibao = './pic_package/haibao_online.png'
    chanpin = './pic_package/chanpin.jpg'
    #erweima = './pic_package/erweima.jpg'
    logo = './pic_package/logo_online.png'
    path = "?".join((data.path, f"superiors_user_id={data.user_id}&id={data.spec_id}"))
    code_pic = wx_service.mall_wx_sdk.get_getwxacode(300, path)
    # logging.info(f"图片URL：{path}")
    is_spec_post = False
    if data_spec.post is not None:
        haibao = './' + data_spec.post.split('com/')[1]
        try:
            haibao_pil = Image.open(haibao).convert('RGBA')
            is_spec_post = True
        except:
            #haibao = './pic_package/haibao_online.jpg'
            haibao = './pic_package/haibao_online.png'
            haibao_pil = Image.open(haibao).convert('RGBA')
    elif data_good.image_url is not None:
        haibao_pil = Image.open(haibao).convert('RGBA')


    stream = io.BytesIO(code_pic)
    erweima_pil = Image.open(stream).convert("RGBA")
    haibao_pil.paste(erweima_pil, (794, 1388, erweima_pil.width + 794, erweima_pil.height + 1388))

    if not is_spec_post:
        chanpin = './' + data_good.image_url.split('com/')[1]
        try:
            chanpin_pil = Image.open(chanpin).convert('RGBA')
        except:
            logging.info(f"get_user_post_pic，bad path: {chanpin}")
            chanpin = './pic_package/chanpin.jpg'
            chanpin_pil = Image.open(chanpin).convert('RGBA')
            if is_spec_post:
                is_spec_post = False
        #erweima_pil = Image.open(erweima).convert('RGBA')
        #logo_pil = Image.open(logo).convert('RGBA').resize((208,201))

        chanpin_pil = chanpin_pil.resize((1195, 1195))
        haibao_pil.paste(chanpin_pil, (0, 0, chanpin_pil.width, chanpin_pil.height))
        #haibao_pil.paste(logo_pil, (10, 10, logo_pil.width + 10, logo_pil.height + 10))

        draw = ImageDraw.Draw(haibao_pil)
        font_path = './pic_package/msyhbd.ttc'
        font = ImageFont.truetype(font=font_path, size=50, encoding='utf-8')
        if data_good.title is None:
            data_good.title = ""
        draw.text(xy=(70, 1265), text=f"{data_good.title[0:20]}", fill=(0, 0, 0), font=font)
        font = ImageFont.truetype(font=font_path, size=70, encoding='utf-8')
        font2 = ImageFont.truetype(font=font_path, size=72, encoding='utf-8')
        if data_spec.price is None:
            data_spec.price = 0
        if data_spec.price_line is None:
            data_spec.price_line = 0
        draw.text(xy=(60, 1390), text='￥' + str('%.2f' % (data_spec.price_line / 100)), fill=(0, 0, 0), font=font)
        #draw.text(xy=(60, 1516), text='￥' + str('%.2f' % (data_spec.wholesale_price/100)), font=font2, fill='red')  # fill=(160, 160, 160),
        draw.text(xy=(60, 1516), text='￥' + str('%.2f' % (data_spec.price / 100)), font=font2, fill='red')
        #draw.line([(370, 1495), (640, 1495)], fill="gray", width=4)

    img_byte = io.BytesIO()
    haibao_pil.convert('RGB').save(img_byte, format='jpeg', quality=60)
    haibao_pil.close()
    erweima_pil.close()
    if not is_spec_post:
        chanpin_pil.close()
    #logo_pil.close()
    return StreamingResponse(content=io.BytesIO(img_byte.getvalue()), media_type="image/jpeg")

    # bg = './code_default2.jpg'
    # path = "?".join((data.path, f"superiors_user_id={data.user_id}&id={data.spec_id}"))
    # #image_bg = Image.new("RGBA", (800, 1000), "#00ff00")
    # image_bg = Image.open(bg).convert('RGBA')
    # image_array = []
    # if data.spec_id is not None:
    #     data_spec = d_good.get_good_spec_by_id(data.spec_id)
    #     if data_spec is not None:
    #         if data_spec.post is not None:
    #             file_path = './assets' + data_spec.post.split('/assets')[1]
    #             image_bg = Image.open(file_path)
    # code_pic = wx_service.mall_wx_sdk.get_getwxacode(280, path)
    # stream = io.BytesIO(code_pic)
    # image_stream = Image.open(stream).convert("RGBA")
    #
    # #重置背景图片大小
    # # image_bg.resize((600,800))
    # image_bg_size = image_bg.size
    # image_bg.paste(image_stream, (image_bg_size[0] - 322, image_bg_size[1] - 360), image_stream)
    # img_byte = io.BytesIO()
    # image_bg.save(img_byte, format='png')
    # return StreamingResponse(content=io.BytesIO(img_byte.getvalue()), media_type="image/png")

# @router.post(f'/get_code_pic', summary='获取用户推广小程序二维码,带参?user_id=n')
# async def get_code_pic(data:GoodspecPostpic):
#     """
#     返回png格式的图像二进制码
#     """
#     path = "?".join((data.path, f"superiors_user_id={data.user_id}"))
#     code_pic = wx_service.mall_wx_sdk.get_getwxacode(300, path)
#     # stream = io.BytesIO(code_pic)
#     # erweima_pil = Image.open(stream).convert("RGBA")
#     # img_byte = io.BytesIO()
#     # haibao_pil.convert('RGB').save(img_byte, format='jpeg', quality=60)
#     return StreamingResponse(content=io.BytesIO(code_pic), media_type="image/jpeg")


@router.get(f'/get_code_pic', dependencies=[Depends(verify_token)], summary='获取用户推广二维码,带参?user_id=n')
async def get_code_pic(request: Request):
    """
    图像二进制码地址：https://yxiaozhu.com/web/user/wx_login?user_id=1
    微信登录推荐注册,返回二维码jpg图片二进制数据流
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if not user_id:
        raise HTTPException(status_code=403, detail='用户不存在')
    # pay_bd_count = d_order.get_baodan_order_count(user_id)
    # if pay_bd_count < 1:
    #     raise HTTPException(status_code=403, detail='请购买报单商品授权后再试！')
    user_info = d_user.get_user_by_id(user_id)
    if user_info:
        tpath = f"https://yxiaozhu.com/web/user/wx_login?userId=%s" % user_info.id
        qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=4)
        qr.add_data(tpath)
        qr.make(fit=True)
        img = qr.make_image()

        img_byte = io.BytesIO()
        img.convert("RGB").save(img_byte, format='jpeg', quality=60)

        # code_pic = wx_service.mall_wx_sdk.get_getwxacode(300, path)
        # stream = io.BytesIO(code_pic)
        # erweima_pil = Image.open(stream).convert("RGBA")
        # img_byte = io.BytesIO()
        # haibao_pil.convert('RGB').save(img_byte, format='jpeg', quality=60)
        return StreamingResponse(content=img_byte, media_type="image/jpeg")
    else:
        return {}

@router.get(f'/get_posters', dependencies=[Depends(verify_token)], summary='获取海报图列表')
async def get_posters():
    return d_address.list_tposter_front()

@router.post(f'/get_posters_share', dependencies=[Depends(verify_token)], summary='获取合成海报图用于用户自己的推广')
async def get_posters_share(data:Posterpic):
    """
    生成用户某个推广页面的推广海报图。
    返回jpg格式的图像二进制码, poster_id 与 poster_url需要一致
    path,是小程序的推广地址,即：注册地址/xxx/xxx
    """
    if not data.poster_id or not data.user_id or not data.path or not data.poster_url:
        raise HTTPException(status_code=304, detail='data error!!')
    poster_info = d_address.get_poster_by_id(data.poster_id)
    if not poster_info:
        raise HTTPException(status_code=304, detail='poster_id error!!')
    if poster_info.poster_url != data.poster_url:
        raise HTTPException(status_code=304, detail='前后端path不一致!!')

    haibao = './pic_package/xhaibao_default.jpg'
    # path = "?".join((data.path, f"superiors_user_id={data.user_id}"))
    path = "?".join(('pages/index/index', f"userId={data.user_id}"))
    #haibao_pil = Image.open(haibao).convert('RGBA')
    # if data.poster_url is not None:
    #     haibao = './' + data.poster_url.split('com/')[1]

    try:
        if data.poster_url is not None:
            # 发送GET请求
            response = requests.get(data.poster_url)
            h_stream = io.BytesIO(response.content)
            haibao_pil = Image.open(h_stream).convert("RGBA")
        else:
            haibao_pil = Image.open(haibao).convert('RGBA')
    except:
        logging.info(f"get_posters_share，bad path: {haibao}")
        haibao = './pic_package/xhaibao_default.jpg'
        haibao_pil = Image.open(haibao).convert('RGBA')
    #erweima_pil = Image.open(erweima).convert('RGBA')
    #logo_pil = Image.open(logo).convert('RGBA').resize((208,201))
    code_pic = wx_service.mall_wx_sdk.get_getwxacode(300, path)
    stream = io.BytesIO(code_pic)
    erweima_pil = Image.open(stream).convert("RGBA")
    haibao_pil = haibao_pil.resize((1275, 2270))
    haibao_pil.paste(erweima_pil, (846, 1898, erweima_pil.width + 846, erweima_pil.height + 1898))

    img_byte = io.BytesIO()
    haibao_pil.convert('RGB').save(img_byte, format='jpeg', quality=60)
    haibao_pil.close()
    erweima_pil.close()
    #logo_pil.close()
    return StreamingResponse(content=io.BytesIO(img_byte.getvalue()), media_type="image/jpeg")

@router.get(f'/get_user_info', dependencies=[Depends(verify_token)],summary='获取用户基本信息')
async def get_user_info(request: Request):
    '''
    entrust_status   委托状态0未接受1临时托管中2永久托管;
    light_status    熄灯状态0正常1熄灯;
    entrust_startime   开启托管时间;
    entrust_endtime   结束托管时间;
    bagorder_num  礼包购买数;
    prop_one_blance  初级资金池分润预测值
    prop_two_blance  高级资金池分润预测值
    prop_three_blance  顶级资金池分润预测值

    '''
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    prop_one_blance = 0
    prop_two_blance = 0
    prop_three_blance = 0
    if not user_id:
        raise HTTPException(status_code=403, detail='用户不存在')
    if user_id <= 0:
        raise HTTPException(status_code=403, detail='未找到用户')

    user_info = d_user.get_user_by_id(user_id)
    if not user_info:
        raise HTTPException(status_code=203, detail='未找到用户')

    # if user_info:
    #     # 更新系统用户级别
    #     if user_info.level_id == 0:
    #         d_user.update_sysuser_active(user_id)
    #     elif user_info.level_id == 1:
    #         d_user.update_sysuser_high(user_id)zhifu
    #     elif user_info.level_id == 2:
    #         d_user.update_sysuser_top(user_id)
    #     # 更新推广用户级别
    #     d_user.update_user_top(user_id)

    if user_info.level_id == 0:
        user_info.withdraw = global_define.setting_withdraw['fans']
    elif user_info.level_id == 1:
        user_info.withdraw = global_define.setting_withdraw['member']
    elif user_info.level_id == 2:
        user_info.withdraw = global_define.setting_withdraw['boss']
    else:
        user_info.withdraw = global_define.setting_withdraw['bigboss']

    #获取资金账户信息
    balance_info = d_account.get_account_info(user_id)
    if balance_info:
        prop_one_blance = balance_info.forecast_one
        prop_two_blance = balance_info.forecast_two
        prop_three_blance = balance_info.forecast_three

    return {"id":user_info.id,"username":user_info.username,"email":user_info.email,"nickname":user_info.nickname,"phone":user_info.phone,"level_id":user_info.level_id,"register_time":user_info.register_time,\
            "avatar":user_info.avatar,"invited_user_id":user_info.invited_user_id,"invited_code":user_info.invited_code,"open_id":user_info.open_id,"union_id":user_info.union_id,"tuan_id":user_info.tuan_id,\
            "entrust_status":user_info.entrust_status,"light_status":user_info.light_status,"entrust_startime":user_info.entrust_startime,"entrust_endtime":user_info.entrust_endtime,\
            "bagorder_num":user_info.bagorder_num,"weight_num":user_info.weight_num,"fund_weight_num":user_info.fund_weight_num,"prop_one_blance":prop_one_blance,"prop_two_blance":prop_two_blance,\
            "prop_three_blance":prop_three_blance,"video_level":user_info.video_level,"ercode":user_info.ercode}


@router.get(f'/other/get_user_info', dependencies=[Depends(verify_token)],summary='获取id获取基本信息')
async def other_get_user_info(request: Request, userid:int = 0):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    u_info = d_user.get_user_by_id(userid)
    re_data = {}
    if u_info:
        re_data['nickname'] = u_info.nickname
        re_data['username'] = u_info.username
        re_data['name'] = u_info.name
        re_data['avatar'] = u_info.avatar
        # re_data['phone'] = u_info.phone
    return re_data
#
# @router.get(f'/get_user_info_by_phone',summary='通过手机号获取用户基本信息')
# async def get_user_info_by_phone(phone: str):
#     if str is None or str == '':
#         raise HTTPException(status_code=203, detail='用户不存在')
#     return d_user.get_user_by_phone(phone)
#
# @router.post(f'/get_wx_token', summary='获取微信token')
# async def get_wx_token():
#     return wx_service.mall_wx_sdk.get_access_token()
#
# @router.post(f'/get_wx_link', summary='获取微信短连接')
# async def get_wx_link(page_url:str , page_title:str = None, is_permanent=False):
#     return wx_service.mall_wx_sdk.get_getwxshorturl(page_url, page_title, is_permanent)


@router.get(f'/get_invited_user', dependencies=[Depends(verify_token)], summary='分页获取直推（团队）用户列表')
async def get_invited_user(request: Request, page:int = 1):
    """
    分页获取推荐用户列表
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    return d_user.get_invited_user_to_page(user_id, page)


@router.get(f'/get_user_stat', dependencies=[Depends(verify_token)], summary='获取用户统计和配置信息')
async def get_user_stat(request: Request):
    '''
    max_entrust_len, 临时托管期限（小时）;
    invited_count，推荐人数；
    invited_really_count,  推荐有效人数；
    '''
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    u_info = d_user.get_user_by_id(user_id)
    re_val = {"max_entrust_len":0, "invited_count":0, "invited_really_count":0}
    if u_info:
        re_val["max_entrust_len"] = global_define.max_entrust_len
        re_val["invited_count"] = d_user.get_lower_user_count(user_id)
        re_val["invited_really_count"] = d_user.get_bagorder_user_count(user_id)

    return re_val

#
# @router.get(f'/get_invited_user_achieve', dependencies=[Depends(verify_token)], summary='分页获取推荐用户列表和业绩数据')
# async def get_invited_user_achieve(request: Request, page:int = 1):
#     """
#     分页获取推荐用户列表和业绩数据
#     invited_user_list,当前页推荐用户列表
#     invited_user_data，当前页用户业绩，invited_achieve我的业绩，invited_invited_achieve团队业绩,abouns分红次数
#     """
#     welcomesession = request.headers.get('welcomesession')
#     user_id = d_user.get_login_id(welcomesession)
#     user_info = d_user.get_user_by_id(user_id)
#     invited_user_data = []
#     invited_user_list = []
#     invited_user_list_out = []
#     if user_info:
#         invited_user_list = d_user.get_invited_user_to_page(user_id, page)
#         invited_user_ids = d_user.get_invited_user_ids(user_id)
#         invited_invited_user_ids = d_user.get_invited_user_for_list(invited_user_ids)
#         invited_user_data.append({"id":user_info.id, "nickname":user_info.nickname, "phone":user_info.phone, \
#                                   "avatar":user_info.avatar, "invited_achieve":d_order.get_user_bdorders_paidsum(invited_user_ids), \
#                                   "invited_invited_achieve":d_order.get_user_bdorders_paidsum(invited_invited_user_ids), \
#                                   "abouns":d_account.get_room_fenhong_count(user_id)})
#         if invited_user_list:
#             for i in invited_user_list:
#                 invited_user_list_out.append({"id": i.id, "nickname": i.nickname, "phone": i.phone, \
#                                           "avatar": i.avatar, "level_id":i.level_id,"is_partner":i.is_partner,"parent_id":i.parent_id,"invited_user_id":i.invited_user_id})
#                 invited_user_ids = d_user.get_invited_user_ids(i.id)
#                 invited_invited_user_ids = d_user.get_invited_user_for_list(invited_user_ids)
#                 invited_user_data.append({"id": i.id, "nickname": i.nickname, "phone": i.phone, \
#                                           "avatar": i.avatar, "invited_achieve": d_order.get_user_bdorders_paidsum(invited_user_ids), \
#                                           "invited_invited_achieve": d_order.get_user_bdorders_paidsum(invited_invited_user_ids), \
#                                           "abouns":d_account.get_room_fenhong_count(i.id)})
#
#     return {'code':200, 'invited_user_list':invited_user_list_out, 'invited_user_data':invited_user_data}



@router.get(f'/get_invited_sir', dependencies=[Depends(verify_token)], summary='获取团队直推用户列表')
async def get_invited_sir(request: Request):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    re_val = {}
    re_list = d_user.get_invited_user(user_id)
    re_val['total'] = len(re_list)
    re_val['data'] = re_list
    return re_val

@router.get(f'/get/invited/two', dependencies=[Depends(verify_token)], summary='获取团队直推团队两层列表')
async def get_invited_two(request: Request):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    re_val = {}
    re_list = d_user.get_invited_user(user_id)
    user_id_two = d_user.get_invited_user_for_list([user_id])
    user_id_two_list = d_user.get_invited_user_two(user_id_two)
    re_val['total'] = len(re_list)
    re_val['data1'] = re_list
    re_val['data2'] = user_id_two_list
    return re_val

@router.get(f'/get_tuan_sir', dependencies=[Depends(verify_token)], summary='获取团队全部用户列表')
async def get_tuan_sir(request: Request):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    u_info = d_user.get_user_by_id(user_id)
    re_val = {}
    if u_info:
       if u_info.is_tuan > 0:
           re_val = d_user.get_groupsir_user(user_id)
       else:
           re_val = d_user.get_invited_user(user_id)
    return re_val

@router.get(f'/get/tuan', dependencies=[Depends(verify_token)], summary='获取下级团长列表')
async def get_tuan(request: Request):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    u_info = d_user.get_user_by_id(user_id)
    re_val = {}
    if u_info:
       if u_info.is_tuan > 0:
           re_val = d_user.get_groupsir_lower(user_id)

    return re_val

@router.get(f'/get/tuan/user', dependencies=[Depends(verify_token)], summary='获取下级成员列表')
async def get_tuan(request: Request):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    u_info = d_user.get_user_by_id(user_id)
    re_val = {}
    if u_info:
       if u_info.is_tuan > 0:
           re_val = d_user.get_groupsir_lower_user(user_id)

    return re_val


# @router.get(f'/get_tuan_lower', summary='获取下级团队列表')
# async def get_tuan_lower(request: Request):
#     welcomesession = request.headers.get('welcomesession')
#     user_id = d_user.get_login_id(welcomesession)
#     u_info = d_user.get_user_by_id(user_id)
#     re_val = {}
#     if u_info:
#        if u_info.is_tuan > 0:
#            re_val = d_user.get_groupsir_lower(user_id)
#     return re_val

@router.get(f'/get_tuan_stat', dependencies=[Depends(verify_token)], summary='获取团队统计信息')
async def get_tuan_stat(request: Request):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    u_info = d_user.get_user_by_id(user_id)
    re_val = {"yes_hpoto":0, "pass_photo":0, "sale_count":0, "sale_tuan_count":0}
    if u_info:
       if u_info.is_tuan > 0: #团队信息
           re_val_ids = d_user.get_tuan_ids(user_id)
           re_val["yes_hpoto"] = d_task.get_taskclock_count(re_val_ids)
           re_val["pass_photo"] = d_task.get_taskclock_count(re_val_ids, 1)
           re_val["sale_count"] = d_order.get_user_orders_count([user_id])
           re_val["sale_tuan_count"] = d_order.get_user_orders_count(re_val_ids)
       else:  #个人信息
           pass
    return re_val

# @router.post(f'/get_invparent_user', summary='获取直推下级团队成员列表')
# async def get_parent_user(user_id:int):
#     inv_list =  d_user.get_invited_user(user_id)
#     invusers = []
#     for i in inv_list:
#         invusers.append(i.id)
#     return d_user.get_invparent_user(invusers)

@router.post(f'/updatemyinfo', dependencies=[Depends(verify_token)], summary='更新用户基本信息(wx_login之后，必须更新手机号)')
async def updatemyinfo(request: Request, user_data: UpdateUser):
    """
    更新用户，昵称、头像url，手机号，valcode：tNP1Lp4wubp07Lx
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if user_data.valcode is None or user_data.valcode != 'tNP1Lp4wubp07Lx':
        raise HTTPException(status_code=403, detail='code error!')
    user_info = d_user.get_user_by_id(user_id)
    if not user_info:
        raise HTTPException(status_code=403, detail='user error!')
    # update_data.id = user_data.id
    if user_data.phone is not None:
        if d_user.get_user_by_phone(user_data.phone) is not None:
            raise HTTPException(status_code=403, detail='手机已存在!')
        if user_info.phone is not None:
            if len(user_data.phone) > 10:
                raise HTTPException(status_code=403, detail='手机已绑定!')

    # update_data.phone = user_data.phone
    d_user.update_user_base_info(user_id, user_data.nickname, user_data.avatar, user_data.phone, user_data.ercode)
    return {'code': 200, 'detail': 'success'}




# @router.get(f'/wholesalelist',summary='获取直推批发商列表')
# async def get_wholesale(user_id: int):
#     if user_id is None or user_id == '':
#         raise HTTPException(status_code=203, detail='用户不存在')
#     return d_user.get_wholesale_list(user_id)
#
# @router.get(f'/get_wholesale_role', summary='获取批发商角色')
# async def get_wholesale_role():
#     return global_define.wholesale_role
#
# #@router.post(f'/get_user_test', response_model=m_order.UserGoodsInfo, summary='test')
# @router.post(f'/get_user_test', summary='test')
# async def get_user_test(user:m_schema.CreateUser):
#     re_val={'status':200}
#     re_val['data'] = d_user.update_sysuser_active(1)
#     test = ''
#     return re_val
#
# @router.get(f'/prize_user_coin', summary='赠予用户注册积分')
# async def prize_user_coin(user_id: int):
#     # 更新赠予积分
#     acount_info = d_account.get_account_info(user_id)
#     if acount_info:
#         raise HTTPException(status_code=403, detail='非新注册用户！')
#     account_info = d_account.get_account_info_add(user_id)
#     coin_num = account_info.coin + global_define.platform_prize['prize4']
#     d_account.update_account_by_id(account_info.id, {"coin":coin_num})
#     coin_model = m_account.CoinModel(
#         user_id=user_id,
#         change=global_define.platform_prize['prize4'],
#         coin=coin_num,
#         type=global_define.balance_type[28],
#         create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
#         description=global_define.balance_type[28]
#     )
#     d_account.insert_coin(coin_model)
#     # 发送通知
#     d_db.insert_notice(item=m_schema.CreateNotice(
#         user_ids=str(user_id),
#         type='系统通知',
#         title=global_define.balance_type[28],
#         description=global_define.new_user_coin_notice,
#         status=0
#     ))
#
# @router.post(f'/get_user_test', summary='test')
# async def get_user_test(user:m_schema.CreateUser):
#     re_val={'status':200}
#     re_val['data'] = d_user.update_sysuser_active(1)
#     test = ''
#     return re_val
#
# @router.get('/getpartner')
# async def getpartner(parent_id: int):
#     """
#     获取合伙人列表
#     """
#     query_data = d_query.FilterQueryData.parse_obj({
#         "table": "fund_partner",
#         "joins": [
#             {
#                 "table": "user",
#                 "on_left": "user_id",
#                 "on_right": "id"
#             }
#         ],
#         "filters": [{
#             "field": "fund_partner.parent_id",
#             "value": parent_id
#         }]
#     })
#     res = d_query.filter_items(query_data)
#     return {"code": 0, "data": res['data'], 'total': res['total']}
#
# @router.get('/getpartnernow')
# async def getpartnernow(parent_id: int):
#     """
#     获取当前留下的合伙人列表
#     """
#     # query_data = d_query.FilterQueryData.parse_obj({
#     #     "table": "user",
#     #     "filters": [{
#     #         "field": "user.partner_id",
#     #         "value": parent_id
#     #     }]
#     # })
#     # res = d_query.filter_items(query_data)
#     # return {"code": 0, "data": res['data'], 'total': res['total']}
#     return d_user.get_partner_at_users(parent_id)
#
# @router.get('/getmothpartner')
# async def getmothpartner(parent_id: int, month: int):
#     """
#     获取某一周期合伙人推荐的历史合伙人
#     """
#     query_data = d_query.FilterQueryData.parse_obj({
#         "table": "user",
#         "joins": [
#             {
#                 "table": "fund_partner",
#                 "on_left": "user_id",
#                 "on_right": "id"
#             }
#         ],
#         "filters": [
#             {
#                 "field": "fund_partner.parent_id",
#                 "value": parent_id
#             },
#             {
#                 "field": "fund_partner.zhouqi",
#                 "value": month
#             }]
#     })
#     res = d_query.filter_items(query_data)
#     return {"code": 0, "data": res['data'], 'total': res['total']}



@router.get('/qiniu/geturl', dependencies=[Depends(verify_token)], summary="小程序端获取七牛访问url")
async def qiniu_geturl(httpurl: str):
    """
    七牛资源下载
    :httpurl: 如：http://www.xxxxx.com/5f59dace081de.jpg
    :return: http://www.xxxxx.com/5f59dace081de.jpg?e=1719126477&token=Mply7-4INH5tRfYBrYc8MTT-l2_0xhwUhXI4R7_i:BgAmqkA7x8MxR9mUULxq0-_RDzQ=
    """
    return qiniu_service.get_download_url(httpurl)

@router.post('/qiniu/upload_file', dependencies=[Depends(verify_token)], summary="七牛上传小程序端头像")
async def qiniu_upload_file(file: UploadFile = File(...)):
    """
    返回值结构：{"hash":"Ft3_zcPtzqR9B-aZ1q5RaLxfLXze","key":"15cc3ae2-e818-11ef-9e46-00163e410368.jpg"}
    """
    file_type = 'file'
    file_date = f'{datetime.date.today()}'
    file_name = f'{uuid.uuid1()}{Path(file.filename).suffix}'
    file_dir = Path(DIRS.assets_dir) / file_type / file_date
    file_dir.mkdir(parents=True, exist_ok=True)
    file_path = file_dir / file_name

    context = await file.read()
    #5M
    if len(context) > 1 * 1024 * 1024:
        raise HTTPException(400, "已超文件最大限制")

    with open(str(file_path), 'wb') as f:
        f.write(context)
    qiniu_res = qiniu_service.qiniu_upload(file_path, file_name)
    # file_res = FileRes(
    #     file_type=file_type,
    #     file_date=file_date,
    #     file_name=file_name
    # )
    return qiniu_res

@router.get(f'/apply_entrust', dependencies=[Depends(verify_token)], summary='用于用户小程序端申请加入公排')
async def updatemyinfo(request: Request):
    """
    需要完成指定任务，申请才有效
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    #获取用户订单数量
    order_num = d_order.get_tuan_pifaorder_count([user_id])
    double_tscount_ls = d_bigorder.get_bigorder_set('double_tscount')
    if order_num < double_tscount_ls.val_int:
        raise HTTPException(400, "条件不足，申请失败！")
    # 加入大公排排序
    d_bigorder.add_bigorder_express(user_id)
    return {'code': 200, 'message': 'success'}

@router.get(f'/service/get_code', dependencies=[Depends(verify_token)], summary='获取客服二维码配置项')
async def get_bigorder_set():
    return d_db.get_bigorder_set(10)

@router.get(f'/fund/user_list', dependencies=[Depends(verify_token)], summary='获取资金池合法分润用户列表')
async def get_fund_user_list(fund_id:int):
    fund_ls = d_found.get_fund_by_id(fund_id)
    if not fund_ls:
        raise HTTPException(400, "未知数据！")
    if fund_ls.users:
        user_list = fund_ls.users.split(',')
        user_list = user_list[0:4]
        return d_user.get_user_for_list_roomgold(user_list)
    else:
        return {}