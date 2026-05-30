import datetime, time, random, json, io
from fastapi import APIRouter, HTTPException, Body

from common import global_define, Dao
from model import schema
from model import m_schema
from typing import List, Optional
from dao import d_db, d_shuser

router = APIRouter()

@router.post(f'/user_consum', summary='顾客消费')
async def user_consum(data: d_shuser.consumModel):
    re_val={'status':200,'msg':'消费已扣款'}
    if data.balance is None or data.shop_id is None or data.pinpai_id is None or data.manager_id is None or data.user_id is None:
        re_val['msg'] = '数据错误'
        return re_val
    if data.cons_type == '0': #储值消费
        userinfo = d_db.get_sh_user(data.user_id)
        if not userinfo:
            re_val['msg'] = '没找到顾客信息'
            return re_val
        if data.balance > (userinfo.balance + userinfo.givebalance):
            re_val['msg'] = f"顾客金额不足，无法满足消费"
            return re_val
        recominfo = None
        # 有推荐人
        if userinfo.recommenda > 0:
            recominfo = d_db.get_sh_user(userinfo.recommenda)
        # 随机找推荐人
        if not recominfo:
            ids: List[m_schema.SShUser]  = d_db.filter_sh_user(items={'pinpai_id': data.pinpai_id}, search_items={},set_items={}, order_items={'id':'desc'}, page=1, page_size=1000)
            random_id = random.randint(1,len(ids)) - 1
            recominfo = ids[random_id]
        recomlevel = d_db.get_sh_userlevel(recominfo.user_level)
        if not recomlevel:
            re_val['msg'] = f"没找到推荐人{recominfo.id}级别信息"
            return re_val
        #计算推荐人所得
        # recommoney = round(data.balance * recomlevel.propo / 100)
        recommoney = data.balance * recomlevel.propo / 100
        data.shareuser_id = recominfo.id
        data.shareuser_balance = recommoney
        d_shuser.update_recommend(data)
        #更新顾客消费金额
        if not d_shuser.update_clientuser(data):
            re_val['msg'] = f"顾客金额不足，无法满足消费"
            return re_val
    else:  #第三方消费
        ids: List[m_schema.SShUser] = d_db.filter_sh_user(items={'pinpai_id': data.pinpai_id}, search_items={},
                                                          set_items={}, order_items={'id': 'desc'}, page=1,
                                                          page_size=1000)
        random_id = random.randint(1, len(ids)) - 1
        recominfo = ids[random_id]
        recomlevel = d_db.get_sh_userlevel(recominfo.user_level)
        if not recomlevel:
            re_val['msg'] = f"没找到推荐人{recominfo.id}级别信息"
            return re_val
        recommoney = data.balance * recomlevel.propo / 100
        data.shareuser_id = recominfo.id
        data.shareuser_balance = recommoney
        d_shuser.update_recommend(data)
        d_shuser.update_clientuser_other(data)

    return re_val

@router.post(f'/set_deflevel', summary='设置默认级别')
async def set_deflevel(data: d_shuser.defalutLevelModel):
    re_val = {'status': 200, 'msg': '设置成功'}
    if data.status is None:
        data.status = 0
    if data.status == 1:
        d_shuser.update_deflevel(data.pinpai_id, data.le_id)
    else:
        re_val['msg'] = f"设置成功."
    return re_val


@router.get(f'/get_user_test', summary='test')
async def get_user_test(user:str):
    re_val={'status':200,'user':user}
    test = ''
    return re_val

