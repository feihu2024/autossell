from fastapi import APIRouter

import model
import model.res.user
# from service import wx_service

router = APIRouter()

#
# @router.get(f'/get_wx_phone', response_model=model.res.user.PhoneNumber, summary='获取微信手机号')
# async def get_wx_phone(code: str):
#     phone_info = wx_service.supplier_wx_sdk.get_phone_number(code=code)
#     phone_info = phone_info.phone_info
#
#     return model.res.user.PhoneNumber(
#         phoneNumber=phone_info.phoneNumber,
#         purePhoneNumber=phone_info.purePhoneNumber,
#         countryCode=phone_info.countryCode
#     )
