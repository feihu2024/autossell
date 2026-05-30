#!/usr/bin/env python
# encoding: utf-8
import datetime
from typing import List, Optional

from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException

from common import Dao
from dao import d_db
from model import schema
from model.schema import TOrder
from service.mall import s_order, s_flash_order
from service.wx_service import wxpay
import hashlib
import logging
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.post('/notify/pay')
async def notify(request: Request):
    logging.info('start to notify  pay')
    result = wxpay.callback(request.headers, await request.body())
    if result and result.get('event_type') == 'TRANSACTION.SUCCESS':
        logging.info('start to TRANSACTION.SUCCESS')
        resource = result.get('resource')

        # appid = resource.get('appid')
        # mchid = resource.get('mchid')
        out_trade_no = resource.get('out_trade_no')
        amount = resource.get('amount').get('total')
        s_order.pay_success(amount=amount, out_trade_no=out_trade_no)

        # transaction_id = resource.get('transaction_id')
        # trade_type = resource.get('trade_type')
        # trade_state = resource.get('trade_state')
        # trade_state_desc = resource.get('trade_state_desc')
        # bank_type = resource.get('bank_type')
        # attach = resource.get('attach')
        # success_time = resource.get('success_time')
        # payer = resource.get('payer')
        # amount = resource.get('amount').get('total')
        # TODO: 根据返回参数进行必要的业务处理，处理完后返回200或204
        logging.info(str(result))
        return {'code': 'SUCCESS', 'message': '成功'}
    else:
        logging.info('error to notify  pay')
        logging.info(str(result))
        raise HTTPException(status_code=500, detail={"code": 'FAILED', "message": "失败"})


@router.post('/notify/paybag')
async def notify_paybag(request: Request):
    logging.info('start to notify  pay')
    result = wxpay.callback(request.headers, await request.body())
    if result and result.get('event_type') == 'TRANSACTION.SUCCESS':
        logging.info('start to TRANSACTION.SUCCESS')
        resource = result.get('resource')

        # appid = resource.get('appid')
        # mchid = resource.get('mchid')
        out_trade_no = resource.get('out_trade_no')
        amount = resource.get('amount').get('total')
        s_order.pay_success_bag(amount=amount, out_trade_no=out_trade_no)

        # transaction_id = resource.get('transaction_id')
        # trade_type = resource.get('trade_type')
        # trade_state = resource.get('trade_state')
        # trade_state_desc = resource.get('trade_state_desc')
        # bank_type = resource.get('bank_type')
        # attach = resource.get('attach')
        # success_time = resource.get('success_time')
        # payer = resource.get('payer')
        # amount = resource.get('amount').get('total')
        # TODO: 根据返回参数进行必要的业务处理，处理完后返回200或204
        logging.info(str(result))
        return {'code': 'SUCCESS', 'message': '成功'}
    else:
        logging.info('error to notify  pay')
        logging.info(str(result))
        raise HTTPException(status_code=500, detail={"code": 'FAILED', "message": "失败"})

#
# @router.post('/notify/flash_pay')
# async def notify(request: Request):
#     result = wxpay.callback(request.headers, await request.body())
#     if result and result.get('event_type') == 'TRANSACTION.SUCCESS':
#         resource = result.get('resource')
#
#         # appid = resource.get('appid')
#         # mchid = resource.get('mchid')
#         out_trade_no = resource.get('out_trade_no')
#         amount = resource.get('amount').get('total')
#         s_flash_order.pay_success(amount=amount, out_trade_no=out_trade_no)
#
#         # transaction_id = resource.get('transaction_id')
#         # trade_type = resource.get('trade_type')
#         # trade_state = resource.get('trade_state')
#         # trade_state_desc = resource.get('trade_state_desc')
#         # bank_type = resource.get('bank_type')
#         # attach = resource.get('attach')
#         # success_time = resource.get('success_time')
#         # payer = resource.get('payer')
#         # amount = resource.get('amount').get('total')
#         # TODO: 根据返回参数进行必要的业务处理，处理完后返回200或204
#         return {'code': 'SUCCESS', 'message': '成功'}
#     else:
#         raise HTTPException(status_code=500, detail={"code": 'FAILED', "message": "失败"})

@router.get('/notify/interaction', response_class=PlainTextResponse)
async def interaction(request: Request):
    #signature: str, timestamp: str, nonce: str, echostr: str
    #logging.info(request.url.path)
    #logging.info(str(request.path_params))
    print(request.url.path)
    print(str(request.path_params))
    #return request.path_params['echostr']

    wxtoken = 'umMLj5YD5stK1TVZSFwQGUtOjwIL'
    signature = request.query_params.get("signature")
    timestamp = request.query_params.get("timestamp")
    nonce = request.query_params.get("nonce")
    echostr = request.query_params.get("echostr")

    #return f"wxtoken: {wxtoken}, signature:{signature}, timestamp:{timestamp}, nonce:{nonce}, echostr:{echostr} "
    if not signature or not timestamp or not nonce:
         return "no"
    joinlist = [wxtoken, timestamp, nonce]
    joinlist.sort()
    joinstr = ''.join(joinlist)
    joinstr = hashlib.sha1(joinstr.encode("utf8")).hexdigest()
    if joinstr == signature:
        return echostr
        #return True
        # return HttpResponse(echostr)
    else:
        #return False
        return 'no'
        # return HttpResponse("no")

# @router.post('/interaction')
# async def interaction(request: Request):
#     pass