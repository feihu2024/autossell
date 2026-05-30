import datetime
import json
import logging
import time
import uuid
import random
from typing import Optional, List, Text

from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field
from wechatpayv3 import WeChatPayType, SignType

from common import Dao, global_define
from config import DOMAIN, WX
from dao import d_db, d_order, d_package, d_account, d_user, d_good, d_address, d_query, d_bagpass
from model import m_schema, schema
from model.mall import m_order, m_account
from router import r_schema
from model.schema import TUser, TUserAccount
from service import express_service, share_fee_service
from service.mall import s_order
from service.wx_service import wxpay
from .user import verify_token
from model.address import Success, UserAddress, AddressRequest
from model.res.common import SuccessResponse

router = APIRouter(dependencies=[Depends(verify_token)])


class AOrderCart(BaseModel):
    user_id: int = Field(title='用户id')
    good_id: int = Field(title='产品id')
    good_spec_id: int = Field(title='规格id')
    amount: int = Field(title='购买数量')
    good_option_id: int = Field(title='商品选项id')
    good_option_name: Optional[str] = Field(title='选项名称')
    zdyspec: Optional[str] = Field(title='选择自定义规格')


class AGood(BaseModel):
    good_id: int = Field(title='商品ID')
    # spec_id: int = Field(title='规格ID')
    use_balance: int = Field(title='是否使用余额')
    use_coin: int = Field(title='是否使用优惠券')
    amount: int = Field(title='购买数量')
    recommender_id: Optional[int] = Field(title='推荐人ID')
    good_option_id:Optional[int] = Field(title='商品选项id', default=0)
    good_option_name: Optional[str] = Field(title='选项名称')
    user_detail: Optional[str] = Field(title='用户订单备注')
    zdyspec: Optional[str] = Field(title='选择自定义规格')
    zdyspec_good: Optional[str] = Field(title='选择商品后(减去指定库存)，商品的规格json，用于更新商品规格')
    zdyspec_good_index:Optional[str] = Field(title='选择规格和数量，编号从1开始，如规格1数量1/规格2数量1/规格3数量2表达为：{1:1, 2:1, 3:2}')

class AOrder(BaseModel):
    user_id: int = Field(title='用户ID')
    address_id: Optional[int] = Field(title='地址id')
    data: List[AGood]
    # data: AGood
    total_price: Optional[int] = Field(title='计算后的总价，需要前后端计算一致')
    # cart_id: Optional[str] = Field(None, title='购物车id，1,2,3')

class AVideo(BaseModel):
    # user_id: int = Field(title='用户ID')
    # address_id: Optional[int] = Field(title='地址id')
    data: List[AGood]
    # data: AGood
    total_price: Optional[int] = Field(title='计算后的总价，需要前后端计算一致')
    # cart_id: Optional[str] = Field(None, title='购物车id，1,2,3')

class ABag(BaseModel):
    user_id: int = Field(title='用户ID')
    address_id: Optional[int] = Field(title='地址id')
    # data: List[AInitbag]
    bag_id: int = Field(title='首单礼包ID')
    # spec_id: int = Field(title='规格ID')
    use_balance: int = Field(title='是否使用余额')
    use_coin: int = Field(title='是否使用优惠券')
    amount: int = Field(title='购买数量')
    recommender_id: Optional[int] = Field(title='推荐人ID')
    user_detail: Optional[str] = Field(title='用户订单备注')
    total_price: Optional[int] = Field(title='计算后的总价，需要前后端计算一致')

class AOrderAd(BaseModel):
    user_id: int = Field(title='用户ID')
    address_id: Optional[int] = Field(title='地址id')
    ad_id: int = Field(title='广告页ID')
    data: List[AGood]
    # data: AGood
    total_price: Optional[int] = Field(title='计算后的总价，需要前后端计算一致')
    # cart_id: Optional[str] = Field(None, title='购物车id，1,2,3')

class UpdateCartModel(BaseModel):
    user_id: int = Field(title='用户ID')
    cart_id: Optional[int] = Field(title='购物车id')
    cart_num: Optional[int] = Field(title='修改数量')
    update_state: Optional[str] = Field(title='修改数量增加(add)或减少(dec)')

#
# @router.post(f'/cart')
# def order_cart(item: AOrderCart):
#     cart_item = m_schema.CreateCart.parse_obj({**item.dict(), "create_time": datetime.datetime.now()})
#     return d_db.insert_cart(item=cart_item)


@router.post(f'/create', summary='创建商品订单并唤起支付')
def create_order(request: Request,data: AOrder):
    """创建订单并唤起支付"""
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        # 取X-Forwarded-For头部的第一个IP地址（客户端真实IP）
        client_ip = x_forwarded_for.split(",")[0]
    else:
        client_ip = request.client.host
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')
    data.user_id = user_id
    logging.info('start to order')
    logging.info(str(data.dict()))
    orders = []
    fee_to_pay = 0
    base_data = data
    user = None
    user_account = None

    with Dao() as db:
        user_info = db.query(TUser, TUserAccount).outerjoin(TUserAccount, TUser.id == TUserAccount.user_id).filter(
            TUser.id == data.user_id).first()
        if user_info is None:
            raise HTTPException(status_code=201, detail='没有找到该用户的信息')
        user: TUser = user_info['TUser']

        user_account: Optional[TUserAccount] = user_info['TUserAccount']
        if user_account is None:
            user_account = TUserAccount()
            user_account.user_id = data.user_id
            user_account.coin = 0
            user_account.balance = 0
            user_account.lock_balance = 0
            db.add(user_account)
            db.commit()
            db.refresh(user_account)
            db.refresh(user)

    total_coin = user_account.coin
    total_locked_balance = user_account.lock_balance
    total_balance = user_account.balance

    good_ids = []
    good_titles=[]
    good_nums = []
    good_total_balance = 0

    out_trade_no = f"{int(time.time())}{user_account.user_id:08d}{uuid.uuid4().hex[-4:]}"
    # comein_users = d_user.get_comein_users(data.user_id)

    address = None
    if data.address_id:
        address = d_db.get_address(data.address_id)
    for item in data.data:
        # spec = d_db.get_good_spec(item.spec_id)
        good = d_db.get_good(item.good_id)
        #检测库存
        # if spec.stock < item.amount:
        #     raise HTTPException(status_code=400, detail=f'商品{spec.good_id}库存不足')

        # 监测用户是否购买过报单商品
        # if good.type == 1:
        #     buynum = d_order.get_baodan_order_count(user_id)
        #     if buynum >= 1:
        #         raise HTTPException(status_code=400, detail=f'您已经购买过报单商品，请勿越权操作。')

        #检测过期时间
        if good.expired_time is not None:
            if good.expired_time <= datetime.datetime.now():
                raise HTTPException(status_code=400, detail=f'商品{item.good_id}已过期')

        #包邮计费
        #delivery_rule = d_db.filter_delivery_rule(items={'good_id': good.id})
        # delivery_rule = d_good.get_delivery(good.id)
        delivery_fee = 0
        # for de in delivery_rule:
        #     de.province.strip()
        #     address.province.strip()
        #     if address.province == de.province:
        #         delivery_fee = de.delivery_fee

        #邮费
        try:
            delivery_fee = float(json.loads(item.zdyspec)['邮费']) * 100
        except:
            pass

        #不可达地区
        # if delivery_fee is None:
        #     raise HTTPException(status_code=400, detail=f'快递-{address.province}-该地区无货')

        # 区分订单是：普通商品 0、成为批发商商品 1、走批发价商品 2
        #is_wholesale = good.is_wholesale
        # if good.is_wholesale is None:
        #     is_wholesale = 0
        # else:
        #     is_wholesale = good.is_wholesale

        # if user.wholesale_id in (100, 200, 300):
        #     if item.zdyspec:
        #         spec_price = float(json.loads(item.zdyspec)['会员价']) * 100
        #         is_wholesale = 2
        #         if spec_price <= 0:
        #             spec_price = float(json.loads(item.zdyspec)['售价']) * 100
        #             is_wholesale = 0
        #     else:
        #         spec_price = spec.wholesale_price
        #         is_wholesale = 2
        # else:
        #     if item.zdyspec:
        #         spec_price = float(json.loads(item.zdyspec)['售价']) * 100
        #     else:
        #         spec_price = spec.price
        # fee = spec_price * item.amount
        # if delivery_fee:
        #     fee += delivery_fee
        user_price = -1
        try:
            user_price = float(json.loads(item.zdyspec)['会员价']) * 100
        except:
            pass
        spec_price = 0
        try:
            spec_price = float(json.loads(item.zdyspec)['售价']) * 100
        except:
            pass
        fee = spec_price * item.amount
        if user.video_level >= 0 and user_price >= 0:
            fee = user_price * item.amount + delivery_fee

        logging.info(f"支付总价：{fee}")
        good_total_balance += fee
        good_ids.append(good.id)
        good_titles.append(good.title)
        good_nums.append(item.amount)
        #确定供货介绍人
        # if good.introducer_id is not None:
        #     comein_users['supplier_uid'] = good.introducer_id
        #  good.supplier_id

        real_coin_cost = 0
        if good.coinable_number is None:
            good.coinable_number = 0
        if item.use_coin and good.coinable_number > 0 and user_price <= 0:
            real_coin_cost = min(good.coinable_number * item.amount, total_coin)
            total_coin = total_coin - real_coin_cost
        else:
            item.use_coin = 0
        fee = fee - real_coin_cost
        assert fee >= 0
        logging.info(f"用券后支付总价：{fee}")
        #
        # real_locked_balance_cost = 0
        # if item.use_balance:
        #     real_locked_balance_cost = min(fee, total_locked_balance)
        #     total_locked_balance = total_locked_balance - real_locked_balance_cost
        # else:
        #     item.use_balance = 0
        # fee = fee - real_locked_balance_cost
        # assert fee >= 0

        real_balance_cost = 0
        if item.use_balance:
            real_balance_cost = min(fee, total_balance)
            total_balance = total_balance - real_balance_cost
        fee = fee - real_balance_cost
        assert fee >= 0
        logging.info(f"用锁定额后支付总价：{fee}")

        #获取团长 上级团长信息
        tuan_uid = 0
        retuan_uid = 0
        if user.is_tuan > 0:
            tuan_uid = user.id
            if user.tuan_id is not None:
                retuan_uid = user.tuan_id
        else:
            if user.tuan_id is not None:
                tuan_uid = user.tuan_id
                retuan_info = d_user.get_user_by_id(tuan_uid)
                if retuan_info:
                    if retuan_info.tuan_id is not None:
                        retuan_uid = retuan_info.tuan_id

        # 推荐人id  推荐人的推荐人id
        invited_uid = 0
        middle_invited_id = 0
        if user.invited_user_id is None:
            user.invited_user_id = 0
        invited_uid = user.invited_user_id
        invited_info = d_user.get_user_by_id(user.invited_user_id)
        if invited_info:
            if invited_info.invited_user_id is None:
                invited_info.invited_user_id = 0
            middle_invited_id = invited_info.invited_user_id
        #获取批发商随机分润id和推荐人id
        # random_fee_id = 0
        # wholesae_info = d_user.get_wholesale_user()
        # if wholesae_info:
        #     random_fee_id = wholesae_info.id
        #     random_invited_id = wholesae_info.invited_user_id if wholesae_info.invited_user_id is not None else 0

        #分享人，间接分享人
        middle_recommender_id = 0
        recommender_info = d_user.get_user_by_id(item.recommender_id)
        if recommender_info:
            if recommender_info.invited_user_id is None:
                recommender_info.invited_user_id = 0
            middle_recommender_id = recommender_info.invited_user_id

        # 市代理人
        sh_agent_user = d_user.get_sh_agent(user.id)

        order = dict(
            good_id=good.id,
            paider_id=user.id,
            sale_price=spec_price,
            create_time=datetime.datetime.now(),
            status_id=0,
            number=item.amount,
            consignee_name=address.consignee if address else None,
            consignee_province=address.province if address else None,
            consignee_city=address.city if address else None,
            consignee_area=address.area if address else None,
            consignee_street=address.street if address else None,
            consignee_description=address.description if address else None,
            consignee_phone=address.phone if address else None,
            paid_coin=real_coin_cost,
            paid_lock_balance=0,
            paid_balance=real_balance_cost,
            paid_amount=fee,
            out_trade_no=out_trade_no,
            recommender_id=item.recommender_id,
            # parent_uid = comein_users['parent_uid'],
            # top_uid=comein_users['top_uid'],
            invited_uid=invited_uid,
            invited_two_uid=middle_invited_id,
            supplier_id=good.supplier_id,
            supplier_uid=good.introducer_id,
            use_balance=item.use_balance,
            use_coin=item.use_coin,
            delivery_fee=delivery_fee,
            # eqlevel_uid=comein_users['eqlevel_uid'],
            good_option_id=item.good_option_id,
            good_option_name=item.good_option_name,
            user_detail = item.user_detail,
            # random_fee_uid = random_fee_id,
            zdyspec = item.zdyspec,
            zdyspec_good=item.zdyspec_good,
            zdyspec_good_index=item.zdyspec_good_index,
            tuan_uid = tuan_uid,
            retuan_uid = retuan_uid,
            # random_invited_uid = random_invited_id,
            # ininvited_uid = ininvited_uid,
            # admin_id=good.admin_id,
            share_invited_uid=item.recommender_id,
            share_invited_two_uid=middle_recommender_id,
            is_user_price=user_price,
            live_mid_uid=good.live_mid_uid,
            live_mid_money=good.live_mid_money,
            sh_agent_id=sh_agent_user
        )
        orders.append(order)
        fee_to_pay += fee
    fee_to_pay = round(fee_to_pay)
    if data.total_price != fee_to_pay:
        logging.error(f'前端金额为: {data.total_price}分，后端计算金额为:{fee_to_pay}分，金额不一致')
        raise HTTPException(status_code=400, detail='前后端价格不一致')

    t_orders = [schema.TOrder(**order) for order in orders]

    with Dao() as db:
        db.add_all(t_orders)
        # 更新订单来源
        db.flush()
        #d_order.update_order_source(t_orders)
        db.commit()
        #更新金额、购物券
        # d_account.update_account_by_id(user_account.id,{'balance':total_balance, 'coin': total_coin})
        # if total_balance < user_account.balance:
        #     ninus_balance = user_account.balance - total_balance
        #     d_account.add_balance(m_account.BalanceModel(
        #         user_id=user_id,
        #         change=-ninus_balance,
        #         balance=total_balance,
        #         type=global_define.balance_type[5],
        #         create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #         good_id=','.join(good_ids),
        #         good_title=','.join(good_titles),
        #         good_num='',
        #         out_trade_no=out_trade_no
        #     ))
        #
        # if total_coin < user_account.coin:
        #     ninus_balance = user_account.coin - total_coin
        #     description_str = ','.join(good_ids) + ','.join(good_titles)
        #     d_account.insert_coin(m_account.CoinModel(
        #         user_id=user_id,
        #         change=-ninus_balance,
        #         coin=total_coin,
        #         type=global_define.balance_type[13],
        #         create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #         description=description_str,
        #         out_trade_no=out_trade_no
        #     ))



    body = {'code': 200, 'detail': '不需要支付', 'out_trade_no':out_trade_no}
    if fee_to_pay:
        logging.info('start to wxpay')
        if not user.open_id:
            raise HTTPException(status_code=400, detail='请完善您的微信授权信息')
        res = wxpay.pay(
            out_trade_no=out_trade_no,
            amount={'total': int(fee_to_pay), 'currency': 'CNY'},
            description='购买商品',
            payer={'openid': user.open_id},
            notify_url=f"{DOMAIN}/wx/notify/pay",
            pay_type=WeChatPayType.JSAPI
        )

        if res[0] == 200:
            logging.info(res[1])
            if isinstance(res[1], Text):
                data = json.loads(res[1])
            body = {
                "appId": WX.appId,
                "timeStamp": str(int(time.time())),
                "nonceStr": uuid.uuid4().hex[:32],
                "package": f"prepay_id={data['prepay_id']}",
                "signType": "RSA"
                # "out_trade_no": out_trade_no
            }
            body['paySign'] = wxpay.sign(
                data=[body['appId'], body['timeStamp'], body['nonceStr'], body['package']],
                sign_type=SignType.RSA_SHA256)
        else:
            logging.error(res[1])
            raise HTTPException(status_code=400, detail=res[1]['message'])

    else:
        logging.info('no need to pay')
        s_order.pay_success(amount=fee_to_pay, out_trade_no=out_trade_no)
    #
    # #清空购物车
    # if base_data.cart_id is not None:
    #     del_item = base_data.cart_id.split(",")
    #     if len(del_item) > 0:
    #         d_order.del_cart(del_item)

    # orders = [schema.TOrder(**order) for order in orders]
    # with Dao() as db:
    #     db.add_all(orders)
    #    db.commit()
    return body

@router.post(f'/create/ad/order', summary='创建广告页商品订单并唤起支付')
def create_ad_order(request: Request,data: AOrderAd):
    """创建订单并唤起支付"""
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        # 取X-Forwarded-For头部的第一个IP地址（客户端真实IP）
        client_ip = x_forwarded_for.split(",")[0]
    else:
        client_ip = request.client.host
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')
    if not data.ad_id:
        raise HTTPException(status_code=400, detail='非法下单！')
    data.user_id = user_id
    logging.info('start to order')
    logging.info(str(data.dict()))
    orders = []
    fee_to_pay = 0
    base_data = data
    user = None
    user_account = None

    with Dao() as db:
        user_info = db.query(TUser, TUserAccount).outerjoin(TUserAccount, TUser.id == TUserAccount.user_id).filter(TUser.id == data.user_id).first()
        if user_info is None:
            raise HTTPException(status_code=201, detail='没有找到该用户的信息')
        user: TUser = user_info['TUser']

        user_account: Optional[TUserAccount] = user_info['TUserAccount']
        if user_account is None:
            user_account = TUserAccount()
            user_account.user_id = data.user_id
            user_account.coin = 0
            user_account.balance = 0
            user_account.lock_balance = 0
            db.add(user_account)
            db.commit()
            db.refresh(user_account)
            db.refresh(user)

    total_coin = user_account.coin
    total_locked_balance = user_account.lock_balance
    total_balance = user_account.balance

    good_ids = []
    good_titles=[]
    good_nums = []
    good_total_balance = 0

    out_trade_no = f"{int(time.time())}{user_account.user_id:08d}{uuid.uuid4().hex[-4:]}"
    # comein_users = d_user.get_comein_users(data.user_id)

    address = 0
    if data.address_id:
        address = d_db.get_address(data.address_id)
    for item in data.data:
        # spec = d_db.get_good_spec(item.spec_id)
        good = d_db.get_good(item.good_id)
        #检测库存
        # if spec.stock < item.amount:
        #     raise HTTPException(status_code=400, detail=f'商品{spec.good_id}库存不足')

        # 监测用户是否购买过报单商品
        # if good.type == 1:
        #     buynum = d_order.get_baodan_order_count(user_id)
        #     if buynum >= 1:
        #         raise HTTPException(status_code=400, detail=f'您已经购买过报单商品，请勿越权操作。')

        #检测过期时间
        if good.expired_time is not None:
            if good.expired_time <= datetime.datetime.now():
                raise HTTPException(status_code=400, detail=f'商品{item.good_id}已过期')

        #包邮计费
        #delivery_rule = d_db.filter_delivery_rule(items={'good_id': good.id})
        # delivery_rule = d_good.get_delivery(good.id)
        delivery_fee = 0
        # for de in delivery_rule:
        #     de.province.strip()
        #     address.province.strip()
        #     if address.province == de.province:
        #         delivery_fee = de.delivery_fee

        # 邮费
        try:
            delivery_fee = float(json.loads(item.zdyspec)['邮费']) * 100
        except:
            pass

        #不可达地区
        # if delivery_fee is None:
        #     raise HTTPException(status_code=400, detail=f'快递-{address.province}-该地区无货')

        # 区分订单是：普通商品 0、成为批发商商品 1、走批发价商品 2
        #is_wholesale = good.is_wholesale
        # if good.is_wholesale is None:
        #     is_wholesale = 0
        # else:
        #     is_wholesale = good.is_wholesale

        # if user.wholesale_id in (100, 200, 300):
        #     if item.zdyspec:
        #         spec_price = float(json.loads(item.zdyspec)['会员价']) * 100
        #         is_wholesale = 2
        #         if spec_price <= 0:
        #             spec_price = float(json.loads(item.zdyspec)['售价']) * 100
        #             is_wholesale = 0
        #     else:
        #         spec_price = spec.wholesale_price
        #         is_wholesale = 2
        # else:
        #     if item.zdyspec:
        #         spec_price = float(json.loads(item.zdyspec)['售价']) * 100
        #     else:
        #         spec_price = spec.price
        # fee = spec_price * item.amount
        # if delivery_fee:
        #     fee += delivery_fee
        user_price = -1
        try:
            user_price = float(json.loads(item.zdyspec)['会员价']) * 100
        except:
            pass
        spec_price = 0
        try:
            spec_price = float(json.loads(item.zdyspec)['售价']) * 100
        except:
            pass
        fee = spec_price * item.amount
        if user_price >= 0:
            fee = user_price * item.amount + delivery_fee

        logging.info(f"支付总价：{fee}")
        good_total_balance += fee
        good_ids.append(good.id)
        good_titles.append(good.title)
        good_nums.append(item.amount)
        #确定供货介绍人
        # if good.introducer_id is not None:
        #     comein_users['supplier_uid'] = good.introducer_id
        #  good.supplier_id

        real_coin_cost = 0
        if good.coinable_number is None:
            good.coinable_number = 0
        if item.use_coin and good.coinable_number > 0 and user_price <= 0:
            real_coin_cost = min(good.coinable_number * item.amount, total_coin)
            total_coin = total_coin - real_coin_cost
        else:
            item.use_coin = 0
        fee = fee - real_coin_cost
        assert fee >= 0
        logging.info(f"用券后支付总价：{fee}")
        #
        # real_locked_balance_cost = 0
        # if item.use_balance:
        #     real_locked_balance_cost = min(fee, total_locked_balance)
        #     total_locked_balance = total_locked_balance - real_locked_balance_cost
        # else:
        #     item.use_balance = 0
        # fee = fee - real_locked_balance_cost
        # assert fee >= 0

        real_balance_cost = 0
        if item.use_balance:
            real_balance_cost = min(fee, total_balance)
            total_balance = total_balance - real_balance_cost
        fee = fee - real_balance_cost
        assert fee >= 0
        logging.info(f"用锁定额后支付总价：{fee}")

        #获取团长 上级团长信息
        tuan_uid = 0
        retuan_uid = 0
        if user.is_tuan > 0:
            tuan_uid = user.id
            if user.tuan_id is not None:
                retuan_uid = user.tuan_id
        else:
            if user.tuan_id is not None:
                tuan_uid = user.tuan_id
                retuan_info = d_user.get_user_by_id(tuan_uid)
                if retuan_info:
                    if retuan_info.tuan_id is not None:
                        retuan_uid = retuan_info.tuan_id

        # 推荐人id  推荐人的推荐人id
        invited_uid = 0
        middle_invited_id = 0
        if user.invited_user_id is None:
            user.invited_user_id = 0
        invited_uid = user.invited_user_id
        invited_info = d_user.get_user_by_id(user.invited_user_id)
        if invited_info:
            if invited_info.invited_user_id is None:
                invited_info.invited_user_id = 0
            middle_invited_id = invited_info.invited_user_id
        #获取批发商随机分润id和推荐人id
        # random_fee_id = 0
        # wholesae_info = d_user.get_wholesale_user()
        # if wholesae_info:
        #     random_fee_id = wholesae_info.id
        #     random_invited_id = wholesae_info.invited_user_id if wholesae_info.invited_user_id is not None else 0

        #分享人，间接分享人
        middle_recommender_id = 0
        recommender_info = d_user.get_user_by_id(item.recommender_id)
        if recommender_info:
            if recommender_info.invited_user_id is None:
                recommender_info.invited_user_id = 0
            middle_recommender_id = recommender_info.invited_user_id

        #市代理人
        sh_agent_user = d_user.get_sh_agent(user.id)

        order = dict(
            good_id=good.id,
            paider_id=user.id,
            sale_price=spec_price,
            create_time=datetime.datetime.now(),
            status_id=0,
            number=item.amount,
            consignee_name=address.consignee if address else None,
            consignee_province=address.province if address else None,
            consignee_city=address.city if address else None,
            consignee_area=address.area if address else None,
            consignee_street=address.street if address else None,
            consignee_description=address.description if address else None,
            consignee_phone=address.phone if address else None,
            paid_coin=real_coin_cost,
            paid_lock_balance=0,
            paid_balance=real_balance_cost,
            paid_amount=fee,
            out_trade_no=out_trade_no,
            recommender_id=item.recommender_id,
            # parent_uid = comein_users['parent_uid'],
            # top_uid=comein_users['top_uid'],
            invited_uid=invited_uid,
            invited_two_uid=middle_invited_id,
            supplier_id=good.supplier_id,
            supplier_uid=good.introducer_id,
            use_balance=item.use_balance,
            use_coin=item.use_coin,
            delivery_fee=delivery_fee,
            # eqlevel_uid=comein_users['eqlevel_uid'],
            good_option_id=item.good_option_id,
            good_option_name=item.good_option_name,
            user_detail = item.user_detail,
            # random_fee_uid = random_fee_id,
            zdyspec = item.zdyspec,
            zdyspec_good=item.zdyspec_good,
            zdyspec_good_index=item.zdyspec_good_index,
            tuan_uid = tuan_uid,
            retuan_uid = retuan_uid,
            # random_invited_uid = random_invited_id,
            # ininvited_uid = ininvited_uid,
            # admin_id=good.admin_id,
            share_invited_uid=item.recommender_id,
            share_invited_two_uid=middle_recommender_id,
            is_user_price=user_price,
            live_mid_uid=good.live_mid_uid,
            live_mid_money=good.live_mid_money,
            ad_id=data.ad_id,
            sh_agent_id=sh_agent_user
        )
        orders.append(order)
        fee_to_pay += fee
    fee_to_pay = round(fee_to_pay)
    if data.total_price != fee_to_pay:
        logging.error(f'前端金额为: {data.total_price}分，后端计算金额为:{fee_to_pay}分，金额不一致')
        raise HTTPException(status_code=400, detail='前后端价格不一致')

    t_orders = [schema.TOrder(**order) for order in orders]

    with Dao() as db:
        db.add_all(t_orders)
        # 更新订单来源
        db.flush()
        #d_order.update_order_source(t_orders)
        db.commit()
        #更新金额、购物券
        # d_account.update_account_by_id(user_account.id,{'balance':total_balance, 'coin': total_coin})
        # if total_balance < user_account.balance:
        #     ninus_balance = user_account.balance - total_balance
        #     d_account.add_balance(m_account.BalanceModel(
        #         user_id=user_id,
        #         change=-ninus_balance,
        #         balance=total_balance,
        #         type=global_define.balance_type[5],
        #         create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #         good_id=','.join(good_ids),
        #         good_title=','.join(good_titles),
        #         good_num='',
        #         out_trade_no=out_trade_no
        #     ))
        #
        # if total_coin < user_account.coin:
        #     ninus_balance = user_account.coin - total_coin
        #     description_str = ','.join(good_ids) + ','.join(good_titles)
        #     d_account.insert_coin(m_account.CoinModel(
        #         user_id=user_id,
        #         change=-ninus_balance,
        #         coin=total_coin,
        #         type=global_define.balance_type[13],
        #         create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #         description=description_str,
        #         out_trade_no=out_trade_no
        #     ))



    body = {'code': 200, 'detail': '不需要支付', 'out_trade_no':out_trade_no}
    if fee_to_pay:
        logging.info('start to wxpay')
        if not user.open_id:
            raise HTTPException(status_code=400, detail='请完善您的微信授权信息')
        res = wxpay.pay(
            out_trade_no=out_trade_no,
            amount={'total': int(fee_to_pay), 'currency': 'CNY'},
            description='购买商品',
            payer={'openid': user.open_id},
            notify_url=f"{DOMAIN}/wx/notify/pay",
            pay_type=WeChatPayType.JSAPI
        )

        if res[0] == 200:
            logging.info(res[1])
            if isinstance(res[1], Text):
                data = json.loads(res[1])
            body = {
                "appId": WX.appId,
                "timeStamp": str(int(time.time())),
                "nonceStr": uuid.uuid4().hex[:32],
                "package": f"prepay_id={data['prepay_id']}",
                "signType": "RSA"
                # "out_trade_no": out_trade_no
            }
            body['paySign'] = wxpay.sign(
                data=[body['appId'], body['timeStamp'], body['nonceStr'], body['package']],
                sign_type=SignType.RSA_SHA256)
        else:
            logging.error(res[1])
            raise HTTPException(status_code=400, detail=res[1]['message'])

    else:
        logging.info('no need to pay')
        s_order.pay_success(amount=fee_to_pay, out_trade_no=out_trade_no)
    #
    # #清空购物车
    # if base_data.cart_id is not None:
    #     del_item = base_data.cart_id.split(",")
    #     if len(del_item) > 0:
    #         d_order.del_cart(del_item)

    # orders = [schema.TOrder(**order) for order in orders]
    # with Dao() as db:
    #     db.add_all(orders)
    #    db.commit()
    return body


@router.post(f'/createbag', summary='创建礼包订单并唤起支付')
def create_order_bag(request: Request,data: ABag):
    """创建初始礼包订单并唤起支付"""
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        # 取X-Forwarded-For头部的第一个IP地址（客户端真实IP）
        client_ip = x_forwarded_for.split(",")[0]
    else:
        client_ip = request.client.host
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')
    data.user_id = user_id
    logging.info('start to order')
    logging.info(str(data.dict()))
    orders = []
    fee_to_pay = 0
    base_data = data
    user = None
    user_account = None

    with Dao() as db:
        user_info = db.query(TUser, TUserAccount).outerjoin(TUserAccount, TUser.id == TUserAccount.user_id).filter(
            TUser.id == data.user_id).first()
        if user_info is None:
            raise HTTPException(status_code=201, detail='没有找到该用户的信息')
        user: TUser = user_info['TUser']

        user_account: Optional[TUserAccount] = user_info['TUserAccount']
        if user_account is None:
            user_account = TUserAccount()
            user_account.user_id = data.user_id
            user_account.coin = 0
            user_account.balance = 0
            user_account.lock_balance = 0
            db.add(user_account)
            db.commit()
            db.refresh(user_account)
            db.refresh(user)

    total_coin = user_account.coin
    total_locked_balance = user_account.lock_balance
    total_balance = user_account.balance

    good_total_balance = 0

    out_trade_no = f"{int(time.time())}{user_account.user_id:08d}{uuid.uuid4().hex[-4:]}"
    # comein_users = d_user.get_comein_users(data.user_id)

    address = None
    if data.address_id:
        address = d_db.get_address(data.address_id)



    # for item in data.data:
    good = d_db.get_bigorder_initbag(data.bag_id)
    #检测库存
    # if spec.stock < item.amount:
    #     raise HTTPException(status_code=400, detail=f'商品{spec.good_id}库存不足')

    #检测过期时间
    # if good.expired_time is not None:
    #     if good.expired_time <= datetime.datetime.now():
    #         raise HTTPException(status_code=400, detail=f'商品{item.good_id}已过期')

    #包邮计费
    #delivery_rule = d_db.filter_delivery_rule(items={'good_id': good.id})
    # delivery_rule = d_good.get_delivery(good.id)
    # delivery_fee = None
    # for de in delivery_rule:
    #     de.province.strip()
    #     address.province.strip()
    #     if address.province == de.province:
    #         delivery_fee = de.delivery_fee

    #监测用户是否购买过报单商品
    # if good.type == 1:
    buynum = d_order.get_baodan_order_count(user_id)
    if buynum >= 1:
        raise HTTPException(status_code=400, detail=f'您已经购买过报单商品，请勿越权操作。')

    spec_price = good.price_total
    fee = spec_price * data.amount

    good_total_balance += fee
    #确定供货介绍人
    # if good.introducer_id is not None:
    #     comein_users['supplier_uid'] = good.introducer_id

    # real_coin_cost = 0
    # if data.use_coin and good.coinable:
    #     if good.coinable_number is None:
    #         good.coinable_number = 0
    #     real_coin_cost = min(good.coinable_number * item.amount, total_coin)
    #     total_coin = total_coin - real_coin_cost
    # else:
    #     item.use_coin = 0
    # fee = fee - real_coin_cost
    # assert fee >= 0
    #
    # real_locked_balance_cost = 0
    # if item.use_balance:
    #     real_locked_balance_cost = min(fee, total_locked_balance)
    #     total_locked_balance = total_locked_balance - real_locked_balance_cost
    # else:
    #     item.use_balance = 0
    # fee = fee - real_locked_balance_cost
    # assert fee >= 0

    real_balance_cost = 0
    if data.use_balance:
        real_balance_cost = min(fee, total_balance)
        total_balance = total_balance - real_balance_cost
    fee = fee - real_balance_cost
    assert fee >= 0

    #获取团长 上级团长信息
    # tuan_uid = 0
    # retuan_uid = 0
    # if user.tuan_id is not None:
    #     tuan_uid = user.tuan_id
    #     retuan_info = d_user.get_user_by_id(tuan_uid)
    #     if retuan_info:
    #         if retuan_info.tuan_id is not None:
    #             retuan_uid = retuan_info.tuan_id

    #获取批发商随机分润id和推荐人id
    # random_fee_id = 0
    # random_invited_id = 0
    # wholesae_info = d_user.get_wholesale_user()
    # if wholesae_info:
    #     random_fee_id = wholesae_info.id
    #     random_invited_id = wholesae_info.invited_user_id if wholesae_info.invited_user_id is not None else 0

    # 推荐人id  推荐人的推荐人id
    invited_uid = user.invited_user_id

    order = dict(
        good_id=good.id,
        paider_id=user.id,
        sale_price=spec_price,
        create_time=datetime.datetime.now(),
        status_id=0,
        number=data.amount,
        consignee_name=address.consignee if address else None,
        consignee_province=address.province if address else None,
        consignee_city=address.city if address else None,
        consignee_area=address.area if address else None,
        consignee_street=address.street if address else None,
        consignee_description=address.description if address else None,
        consignee_phone=address.phone if address else None,
        paid_coin=0,
        paid_lock_balance=0,
        paid_balance=real_balance_cost,
        paid_amount=fee,
        out_trade_no=out_trade_no,
        recommender_id=data.recommender_id,
        # parent_uid = comein_users['parent_uid'],
        # top_uid=comein_users['top_uid'],
        invited_uid=invited_uid,
        use_balance=data.use_balance,
        use_coin=data.use_coin,
        user_detail = data.user_detail,
        # random_fee_uid = random_fee_id,
        isfirst=1
    )
    orders.append(order)
    fee_to_pay += fee


    fee_to_pay = round(fee_to_pay)
    if data.total_price != fee_to_pay:
        logging.error(f'前端金额为: {data.total_price}分，后端计算金额为:{fee_to_pay}分，金额不一致')
        raise HTTPException(status_code=400, detail='前后端价格不一致')

    t_orders = [schema.TOrder(**order) for order in orders]

    with Dao() as db:
        db.add_all(t_orders)
        # 更新订单来源
        db.flush()
        #d_order.update_order_source(t_orders)
        db.commit()

    body = {'code': 200, 'detail': '不需要支付', 'out_trade_no':out_trade_no}
    if fee_to_pay:
        logging.info('start to wxpay')
        if not user.open_id:
            raise HTTPException(status_code=400, detail='请完善您的微信授权信息')
        res = wxpay.pay(
            out_trade_no=out_trade_no,
            amount={'total': int(fee_to_pay), 'currency': 'CNY'},
            description='购买礼包商品',
            payer={'openid': user.open_id},
            notify_url=f"{DOMAIN}/wx/notify/paybag",
            pay_type=WeChatPayType.JSAPI
        )

        if res[0] == 200:
            logging.info(res[1])
            if isinstance(res[1], Text):
                data = json.loads(res[1])
            body = {
                "appId": WX.appId,
                "timeStamp": str(int(time.time())),
                "nonceStr": uuid.uuid4().hex[:32],
                "package": f"prepay_id={data['prepay_id']}",
                "signType": "RSA"
                # "out_trade_no": out_trade_no
            }
            body['paySign'] = wxpay.sign(
                data=[body['appId'], body['timeStamp'], body['nonceStr'], body['package']],
                sign_type=SignType.RSA_SHA256)
        else:
            logging.error(res[1])
            raise HTTPException(status_code=400, detail=res[1]['message'])

    else:
        logging.info('no need to pay')
        s_order.pay_success_bag(amount=fee_to_pay, out_trade_no=out_trade_no)
    #
    # #清空购物车
    # if base_data.cart_id is not None:
    #     del_item = base_data.cart_id.split(",")
    #     if len(del_item) > 0:
    #         d_order.del_cart(del_item)

    # orders = [schema.TOrder(**order) for order in orders]
    # with Dao() as db:
    #     db.add_all(orders)
    #    db.commit()
    return body


@router.post(f'/createvideo', summary='创建购买视频条数订单并唤起支付')
def createvideo_order(request: Request,data: AVideo):
    """创建订单并唤起支付"""
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        # 取X-Forwarded-For头部的第一个IP地址（客户端真实IP）
        client_ip = x_forwarded_for.split(",")[0]
    else:
        client_ip = request.client.host
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')
    data.user_id = user_id
    logging.info('start to order')
    logging.info(str(data.dict()))
    orders = []
    fee_to_pay = 0
    base_data = data
    user = None
    user_account = None

    with Dao() as db:
        user_info = db.query(TUser, TUserAccount).outerjoin(TUserAccount, TUser.id == TUserAccount.user_id).filter(
            TUser.id == data.user_id).first()
        if user_info is None:
            raise HTTPException(status_code=201, detail='没有找到该用户的信息')
        user: TUser = user_info['TUser']

        user_account: Optional[TUserAccount] = user_info['TUserAccount']
        if user_account is None:
            user_account = TUserAccount()
            user_account.user_id = data.user_id
            user_account.coin = 0
            user_account.balance = 0
            user_account.lock_balance = 0
            db.add(user_account)
            db.commit()
            db.refresh(user_account)
            db.refresh(user)

    total_coin = user_account.coin
    total_locked_balance = user_account.lock_balance
    total_balance = user_account.balance

    good_ids = []
    good_titles=[]
    good_nums = []
    good_total_balance = 0

    out_trade_no = f"{int(time.time())}{user_account.user_id:08d}{uuid.uuid4().hex[-4:]}"
    # comein_users = d_user.get_comein_users(data.user_id)

    address = None
    if data.address_id:
        address = d_db.get_address(data.address_id)
    for item in data.data:
        # spec = d_db.get_good_spec(item.spec_id)
        good = d_db.get_good(item.good_id)
        #检测库存
        # if spec.stock < item.amount:
        #     raise HTTPException(status_code=400, detail=f'商品{spec.good_id}库存不足')

        # 监测用户是否购买过报单商品
        # if good.type == 1:
        #     buynum = d_order.get_baodan_order_count(user_id)
        #     if buynum >= 1:
        #         raise HTTPException(status_code=400, detail=f'您已经购买过报单商品，请勿越权操作。')

        #检测过期时间
        if good.expired_time is not None:
            if good.expired_time <= datetime.datetime.now():
                raise HTTPException(status_code=400, detail=f'商品{item.good_id}已过期')

        #包邮计费
        delivery_rule = d_good.get_delivery(good.id)
        delivery_fee = None
        for de in delivery_rule:
            de.province.strip()
            address.province.strip()
            if address.province == de.province:
                delivery_fee = de.delivery_fee

        #不可达地区
        # if delivery_fee is None:
        #     raise HTTPException(status_code=400, detail=f'快递-{address.province}-该地区无货')

        # 区分订单是：普通商品 0、成为批发商商品 1、走批发价商品 2
        #is_wholesale = good.is_wholesale
        # if good.is_wholesale is None:
        #     is_wholesale = 0
        # else:
        #     is_wholesale = good.is_wholesale

        # if user.wholesale_id in (100, 200, 300):
        #     if item.zdyspec:
        #         spec_price = float(json.loads(item.zdyspec)['会员价']) * 100
        #         is_wholesale = 2
        #         if spec_price <= 0:
        #             spec_price = float(json.loads(item.zdyspec)['售价']) * 100
        #             is_wholesale = 0
        #     else:
        #         spec_price = spec.wholesale_price
        #         is_wholesale = 2
        # else:
        #     if item.zdyspec:
        #         spec_price = float(json.loads(item.zdyspec)['售价']) * 100
        #     else:
        #         spec_price = spec.price
        # fee = spec_price * item.amount
        # if delivery_fee:
        #     fee += delivery_fee
        user_price = -1
        try:
            user_price = float(json.loads(item.zdyspec)['会员价']) * 100
        except:
            pass
        spec_price = 0
        try:
            spec_price = float(json.loads(item.zdyspec)['售价']) * 100
        except:
            pass
        fee = spec_price * item.amount
        if user.video_level >= 0 and user_price >= 0:
            fee = user_price * item.amount

        logging.info(f"支付总价：{fee}")
        good_total_balance += fee
        good_ids.append(good.id)
        good_titles.append(good.title)
        good_nums.append(item.amount)
        # 确定供货介绍人
        # if good.introducer_id is not None:
        #     comein_users['supplier_uid'] = good.introducer_id
        #  good.supplier_id

        real_coin_cost = 0
        if good.coinable_number is None:
            good.coinable_number = 0
        if item.use_coin and good.coinable_number > 0 and user_price == 0:
            real_coin_cost = min(good.coinable_number * item.amount, total_coin)
            total_coin = total_coin - real_coin_cost
        else:
            item.use_coin = 0
        fee = fee - real_coin_cost
        assert fee >= 0
        logging.info(f"用券后支付总价：{fee}")
        #
        # real_locked_balance_cost = 0
        # if item.use_balance:
        #     real_locked_balance_cost = min(fee, total_locked_balance)
        #     total_locked_balance = total_locked_balance - real_locked_balance_cost
        # else:
        #     item.use_balance = 0
        # fee = fee - real_locked_balance_cost
        # assert fee >= 0

        real_balance_cost = 0
        if item.use_balance:
            real_balance_cost = min(fee, total_balance)
            total_balance = total_balance - real_balance_cost
        fee = fee - real_balance_cost
        assert fee >= 0
        logging.info(f"用锁定额后支付总价：{fee}")

        # 获取团长 上级团长信息
        tuan_uid = 0
        retuan_uid = 0
        if user.is_tuan > 0:
            tuan_uid = user.id
            if user.tuan_id is not None:
                retuan_uid = user.tuan_id
        else:
            if user.tuan_id is not None:
                tuan_uid = user.tuan_id
                retuan_info = d_user.get_user_by_id(tuan_uid)
                if retuan_info:
                    if retuan_info.tuan_id is not None:
                        retuan_uid = retuan_info.tuan_id

        # 推荐人id  推荐人的推荐人id
        invited_uid = 0
        middle_invited_id = 0
        if user.invited_user_id is None:
            user.invited_user_id = 0
        invited_uid = user.invited_user_id
        invited_info = d_user.get_user_by_id(user.invited_user_id)
        if invited_info:
            if invited_info.invited_user_id is None:
                invited_info.invited_user_id = 0
            middle_invited_id = invited_info.invited_user_id
        # 获取批发商随机分润id和推荐人id
        # random_fee_id = 0
        # wholesae_info = d_user.get_wholesale_user()
        # if wholesae_info:
        #     random_fee_id = wholesae_info.id
        #     random_invited_id = wholesae_info.invited_user_id if wholesae_info.invited_user_id is not None else 0

        # 分享人，间接分享人
        middle_recommender_id = 0
        recommender_info = d_user.get_user_by_id(item.recommender_id)
        if recommender_info:
            if recommender_info.invited_user_id is None:
                recommender_info.invited_user_id = 0
            middle_recommender_id = recommender_info.invited_user_id

        order = dict(
            good_id=good.id,
            paider_id=user.id,
            sale_price=spec_price,
            create_time=datetime.datetime.now(),
            status_id=0,
            number=item.amount,
            consignee_name=address.consignee if address else None,
            consignee_province=address.province if address else None,
            consignee_city=address.city if address else None,
            consignee_area=address.area if address else None,
            consignee_street=address.street if address else None,
            consignee_description=address.description if address else None,
            consignee_phone=address.phone if address else None,
            paid_coin=real_coin_cost,
            paid_lock_balance=0,
            paid_balance=real_balance_cost,
            paid_amount=fee,
            out_trade_no=out_trade_no,
            recommender_id=item.recommender_id,
            # parent_uid = comein_users['parent_uid'],
            # top_uid=comein_users['top_uid'],
            invited_uid=invited_uid,
            invited_two_uid=middle_invited_id,
            supplier_id=good.supplier_id,
            supplier_uid=good.introducer_id,
            use_balance=item.use_balance,
            use_coin=item.use_coin,
            delivery_fee=delivery_fee,
            # eqlevel_uid=comein_users['eqlevel_uid'],
            good_option_id=item.good_option_id,
            good_option_name=item.good_option_name,
            user_detail=item.user_detail,
            # random_fee_uid = random_fee_id,
            zdyspec=item.zdyspec,
            zdyspec_good=item.zdyspec_good,
            zdyspec_good_index=item.zdyspec_good_index,
            tuan_uid=tuan_uid,
            retuan_uid=retuan_uid,
            # random_invited_uid = random_invited_id,
            # ininvited_uid = ininvited_uid,
            # admin_id=good.admin_id,
            share_invited_uid=item.recommender_id,
            share_invited_two_uid=middle_recommender_id,
            is_video=1,
            is_user_price=user_price,
            live_mid_uid=good.live_mid_uid,
            live_mid_money=good.live_mid_money
        )
        orders.append(order)
        fee_to_pay += fee
    fee_to_pay = round(fee_to_pay)
    if data.total_price != fee_to_pay:
        logging.error(f'前端金额为: {data.total_price}分，后端计算金额为:{fee_to_pay}分，金额不一致')
        raise HTTPException(status_code=400, detail='前后端价格不一致')

    t_orders = [schema.TOrder(**order) for order in orders]

    with Dao() as db:
        db.add_all(t_orders)
        # 更新订单来源
        db.flush()
        #d_order.update_order_source(t_orders)
        db.commit()
        #更新金额、购物券
        # d_account.update_account_by_id(user_account.id,{'balance':total_balance, 'coin': total_coin})
        # if total_balance < user_account.balance:
        #     ninus_balance = user_account.balance - total_balance
        #     d_account.add_balance(m_account.BalanceModel(
        #         user_id=user_id,
        #         change=-ninus_balance,
        #         balance=total_balance,
        #         type=global_define.balance_type[5],
        #         create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #         good_id=','.join(good_ids),
        #         good_title=','.join(good_titles),
        #         good_num='',
        #         out_trade_no=out_trade_no
        #     ))
        #
        # if total_coin < user_account.coin:
        #     ninus_balance = user_account.coin - total_coin
        #     description_str = ','.join(good_ids) + ','.join(good_titles)
        #     d_account.insert_coin(m_account.CoinModel(
        #         user_id=user_id,
        #         change=-ninus_balance,
        #         coin=total_coin,
        #         type=global_define.balance_type[13],
        #         create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #         description=description_str,
        #         out_trade_no=out_trade_no
        #     ))

    body = {'code': 200, 'detail': '不需要支付', 'out_trade_no':out_trade_no}
    if fee_to_pay:
        logging.info('start to wxpay')
        if not user.open_id:
            raise HTTPException(status_code=400, detail='请完善您的微信授权信息')
        res = wxpay.pay(
            out_trade_no=out_trade_no,
            amount={'total': int(fee_to_pay), 'currency': 'CNY'},
            description='购买商品',
            payer={'openid': user.open_id},
            notify_url=f"{DOMAIN}/wx/notify/pay",
            pay_type=WeChatPayType.JSAPI
        )

        if res[0] == 200:
            logging.info(res[1])
            if isinstance(res[1], Text):
                data = json.loads(res[1])
            body = {
                "appId": WX.appId,
                "timeStamp": str(int(time.time())),
                "nonceStr": uuid.uuid4().hex[:32],
                "package": f"prepay_id={data['prepay_id']}",
                "signType": "RSA"
                # "out_trade_no": out_trade_no
            }
            body['paySign'] = wxpay.sign(
                data=[body['appId'], body['timeStamp'], body['nonceStr'], body['package']],
                sign_type=SignType.RSA_SHA256)
        else:
            logging.error(res[1])
            raise HTTPException(status_code=400, detail=res[1]['message'])

    else:
        logging.info('no need to pay')
        s_order.pay_success(amount=fee_to_pay, out_trade_no=out_trade_no)
    #
    # #清空购物车
    # if base_data.cart_id is not None:
    #     del_item = base_data.cart_id.split(",")
    #     if len(del_item) > 0:
    #         d_order.del_cart(del_item)

    # orders = [schema.TOrder(**order) for order in orders]
    # with Dao() as db:
    #     db.add_all(orders)
    #    db.commit()
    return body



# @router.get(f'/get_bdorder_num', summary='获取用户报单订单数量')
# def get_bdorder_num(request: Request):
#     """当前用户数据"""
#     welcomesession = request.headers.get('welcomesession')
#     user_id = d_user.get_login_id(welcomesession)
#     buynum = d_order.get_baodan_order_count(user_id)
#     return buynum

#
# @router.post(f'/update')
# def update_order(item: m_schema.SOrder):
#     """更新订单"""
#     d_db.update_order(item)
#     return {'code': 200, 'detail': 'success'}


@router.get(f'/express', summary='获取商品订单物流信息')
async def get_express(request: Request, order_id: int):
    """获取物流信息"""
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')
    order = d_db.get_order(order_id)
    if order.paider_id != user_id:
        raise HTTPException(status_code=400, detail='非法操作')

    if order is None:
        raise HTTPException(status_code=400, detail='订单不存在')

    if order.status_id == 1:
        raise HTTPException(status_code=400, detail='订单未发货')

    if order.delivery_track_code is None:
        raise HTTPException(status_code=400, detail='没有物流单号')

    return express_service.query_express2(order.delivery_track_code)
#
# @router.get(f'/express_package')
# async def get_express_package(expiress_id: int):
#     """获取物流信息"""
#     expiress_order = d_package.get_package_express(expiress_id)
#     if expiress_order is None:
#         raise HTTPException(status_code=400, detail='订单不存在')
#
#     if expiress_order.status == 1:
#         raise HTTPException(status_code=400, detail='订单未发货')
#
#     if expiress_order.express_num is None:
#         raise HTTPException(status_code=400, detail='没有物流单号')
#
#     return express_service.query_express2(expiress_order.express_num)
#
#
# @router.get(f'/code')
# async def get_order_code(user_id: int, order_id: int):
#     """获取订单二维码"""
#     order = d_db.get_order(order_id)
#     if order is None:
#         raise HTTPException(status_code=400, detail='订单不存在')
#
#     code = f'{random.randint(0, 999999):06}'
#     expired_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
#     d_db.update_order(m_schema.SOrder(id=order_id, code=code, code_expired_time=expired_time))
#     return {'code': code}

#
# @router.get(f'/verify_code')
# async def get_order_code(order_id: int, code: str):
#     """校验订单二维码"""
#     with Dao() as db:
#         order = db.query(schema.TOrder).filter(schema.TOrder.id == order_id).filter(schema.TOrder.code == code).filter(
#             schema.TOrder.code_expired_time > datetime.datetime.now()).first()
#         if order is None:
#             raise HTTPException(status_code=400, detail='二维码已过期或者无效')
#         db.query(schema.TOrder).where(schema.TOrder.id == order_id).update({"status_id": 8})
#         db.commit()
#     return {"code": 0, "detail": "success"}


class ARefundOrder(BaseModel):
    order_id: int
    refund_type: int
    refund_reason: str

#
# @router.post(f'/refund')
# async def refund_order(data: ARefundOrder):
#     """申请退款"""
#     order = d_db.get_order(data.order_id)
#     if order is None:
#         raise HTTPException(status_code=400, detail='订单不存在')
#
#     with Dao() as db:
#         db.query(schema.TOrder).where(schema.TOrder.id == data.order_id).update({"status_id": 3})
#         refund_order = db.query(schema.TOrderReturn).where(schema.TOrderReturn.order_id == data.order_id).first()
#         if refund_order is None:
#             db.add(schema.TOrderReturn(order_id=data.order_id, return_type=data.refund_type,
#                                        return_reason=data.refund_reason))
#         else:
#             refund_order.return_type = data.refund_type
#             refund_order.return_reason = data.refund_reason
#         db.commit()
#     return {"code": 0, "detail": "success"}


@router.get(f'/wait_send', summary='商品待发货订单')
async def wait_send(request: Request, page:int = 1):
    """
    当前登录用户待发货订单，且满足 is_display='1', status_id='1'
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')

    # page:当前页码，默认1.
    # page_size：每页做多条数，默认10
    page_size = 10
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "order",
        "joins": [
            {
                "table": "good",
                "on_left": "good_id",
                "on_right": "id"
            }
        ],
        "filters": [
            {
                "field": "order.status_id",
                "value": 1
            },
            {
                "field": "order.paider_id",
                "value": user_id
            },
            {
            "field": "order.is_display",
            "value": 1
            },
            {
            "field": "order.isfirst",
            "value": 0
            }
        ],
        # "order_by": [{"field": "good.priority", "order": "desc"},{"field": "good.id", "order": "desc"}],
        "order_by": [{"field": "order.id", "order": "desc"}],
        "page":page,
        "page_size":page_size
    })
    res = d_query.filter_items(query_data)
    return res
    # items = list(map(fill_spec_field, res['data']))
    # if user_id:
    #     t_user = d_user.get_user_by_id(user_id)
    #     if t_user:
    #         # 更新系统用户级别
    #         if t_user.level_id == 0:
    #             d_user.update_sysuser_active(t_user.id)
    #         elif t_user.level_id == 1:
    #             d_user.update_sysuser_high(t_user.id)
    #         elif t_user.level_id == 2:
    #             d_user.update_sysuser_top(t_user.id)
    #         # 更新推广用户级别
    #         d_user.update_user_top(user_id)
    #
    # return {"code": 0, "data": items, "total": res['total']}
    # return await r_schema.filter_order(paider_id=str(user_id), status_id='1', is_display='1', page=page)


@router.get(f'/wait_send_two', summary='商品待发货订单(包括礼包订单)')
async def wait_send_two(request: Request, page:int = 1):
    """
    当前登录用户待发货订单，且满足 is_display='1', status_id='1'
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')

    # page:当前页码，默认1.
    # page_size：每页做多条数，默认10
    page_size = 10
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "order",
        "selects": ["order"],
        "filters": [
            {
                "field": "order.status_id",
                "value": 1
            },
            {
                "field": "order.paider_id",
                "value": user_id
            },
            {
            "field": "order.is_display",
            "value": 1
            }
        ],
        # "order_by": [{"field": "good.priority", "order": "desc"},{"field": "good.id", "order": "desc"}],
        "order_by": [{"field": "order.id", "order": "desc"}],
        "page":page,
        "page_size":page_size
    })
    res = d_query.filter_items(query_data)
    return res

@router.get(f'/wait_receive', summary='商品待收货订单')
async def wait_receive(request: Request, page:int = 1):
    """
    当前登录用户待收货订单，且满足 is_display='1', status_id='2'
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')
    page_size = 10
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "order",
        "joins": [
            {
                "table": "good",
                "on_left": "good_id",
                "on_right": "id"
            }
        ],
        "filters": [
            {
                "field": "order.status_id",
                "value": 2
            },
            {
                "field": "order.paider_id",
                "value": user_id
            },
            {
                "field": "order.is_display",
                "value": 1
            },
            {
            "field": "order.isfirst",
            "value": 0
            }
        ],
        # "order_by": [{"field": "good.priority", "order": "desc"},{"field": "good.id", "order": "desc"}],
        "order_by": [{"field": "order.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res
    # return await r_schema.filter_order(paider_id=str(user_id), status_id='2', is_display='1', page=page)


@router.get(f'/wait_receive_two', summary='商品待收货订单(包括礼包订单)')
async def wait_receive_two(request: Request, page:int = 1):
    """
    当前登录用户待收货订单，且满足 is_display='1', status_id='2'
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')
    page_size = 10
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "order",
        "selects": ["order"],
        "filters": [
            {
                "field": "order.status_id",
                "value": 2
            },
            {
                "field": "order.paider_id",
                "value": user_id
            },
            {
                "field": "order.is_display",
                "value": 1
            }
        ],
        # "order_by": [{"field": "good.priority", "order": "desc"},{"field": "good.id", "order": "desc"}],
        "order_by": [{"field": "order.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res


@router.get(f'/get_payorder', summary='通过out_trade_no查询商品订单')
async def get_payorder(request: Request, out_trade_no:str):
    """
    查询支付订单,一次可能支付多个订单
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')

    return await r_schema.filter_order(paider_id=str(user_id), out_trade_no=out_trade_no, is_display='1')


#
# @router.get(f'/return', response_model=m_schema.FilterResOrder, summary='退换订单')
# async def get_return_order(user_id: int):
#     return await r_schema.filter_order(user_id=str(user_id), l_status_id='3,4,5,6', is_display='1')



@router.get(f'/finish', summary='已完成商品订单')
async def get_finish_order(request: Request, page:int = 1):
    """
    当前登录用户已完成订单，且满足 is_display='1', status_id='3'
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')
    page_size = 10
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "order",
        "joins": [
            {
                "table": "good",
                "on_left": "good_id",
                "on_right": "id"
            }
        ],
        "filters": [
            {
                "field": "order.status_id",
                "value": 3
            },
            {
                "field": "order.paider_id",
                "value": user_id
            },
            {
                "field": "order.is_display",
                "value": 1
            },
            {
            "field": "order.isfirst",
            "value": 0
            }
        ],
        # "order_by": [{"field": "good.priority", "order": "desc"},{"field": "good.id", "order": "desc"}],
        "order_by": [{"field": "order.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res
    # return await r_schema.filter_order(paider_id=str(user_id), status_id='3', is_display='1', page=page)


@router.get(f'/finish_two', summary='已完成商品订单(包括礼包订单)')
async def get_finish_two_order(request: Request, page:int = 1):
    """
    当前登录用户已完成订单，且满足 is_display='1', status_id='3'
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')
    page_size = 10
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "order",
        "selects": ["order"],
        "filters": [
            {
                "field": "order.status_id",
                "value": 3
            },
            {
                "field": "order.paider_id",
                "value": user_id
            },
            {
                "field": "order.is_display",
                "value": 1
            }
        ],
        # "order_by": [{"field": "good.priority", "order": "desc"},{"field": "good.id", "order": "desc"}],
        "order_by": [{"field": "order.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res

@router.get(f'/all', summary='全部订单')
async def get_all_order(request: Request, page:int = 1):
    """
    当前登录用户所有订单，且满足 is_display='1'
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')
    page_size = 10
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "order",
        "joins": [
            {
                "table": "good",
                "on_left": "good_id",
                "on_right": "id"
            }
        ],
        "filters": [
            # {
            #     "field": "order.status_id",
            #     "value": 1
            # },
            {
                "field": "order.paider_id",
                "value": user_id
            },
            {
                "field": "order.is_display",
                "value": 1
            },
            {
            "field": "order.isfirst",
            "value": 0
            }
        ],
        # "order_by": [{"field": "good.priority", "order": "desc"},{"field": "good.id", "order": "desc"}],
        "order_by": [{"field": "order.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res

    # return await r_schema.filter_order(paider_id=str(user_id), is_display='1', page=page)




@router.get(f'/all', summary='全部订单')
async def get_all_order(request: Request, page:int = 1):
    """
    当前登录用户所有订单，且满足 is_display='1'
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')
    page_size = 10
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "order",
        "joins": [
            {
                "table": "good",
                "on_left": "good_id",
                "on_right": "id"
            }
        ],
        "filters": [
            # {
            #     "field": "order.status_id",
            #     "value": 1
            # },
            {
                "field": "order.paider_id",
                "value": user_id
            },
            {
                "field": "order.is_display",
                "value": 1
            },
            {
            "field": "order.isfirst",
            "value": 0
            }
        ],
        # "order_by": [{"field": "good.priority", "order": "desc"},{"field": "good.id", "order": "desc"}],
        "order_by": [{"field": "order.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res


@router.get(f'/all_two', summary='全部订单(包括礼包订单)')
async def get_all_two(request: Request, page:int = 1):
    """
    当前登录用户所有订单，且满足 is_display='1'
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')
    page_size = 10
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "order",
        "joins": [
            {
                "table": "good",
                "on_left": "good_id",
                "on_right": "id"
            }
        ],
        "filters": [
            # {
            #     "field": "order.status_id",
            #     "value": 1
            # },
            {
                "field": "order.paider_id",
                "value": user_id
            },
            {
                "field": "order.is_display",
                "value": 1
            }
        ],
        # "order_by": [{"field": "good.priority", "order": "desc"},{"field": "good.id", "order": "desc"}],
        "order_by": [{"field": "order.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res



@router.get(f'/get_baglist', summary='获取礼包订单')
async def get_baglist(request: Request, page:int = 1):
    """
    当前登录用户所有获取礼包订单
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')
    page_size = 10
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "order",
        "joins": [
            {
                "table": "bigorder_initbag",
                "on_left": "good_id",
                "on_right": "id"
            }
        ],
        "filters": [
            # {
            #     "field": "order.status_id",
            #     "value": 1
            # },
            {
                "field": "order.paider_id",
                "value": user_id
            },
            {
            "field": "order.isfirst",
            "value": 1
            }
        ],
        # "order_by": [{"field": "good.priority", "order": "desc"},{"field": "good.id", "order": "desc"}],
        "order_by": [{"field": "order.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res


@router.get(f'/confirm', response_model=str, summary='确认商品订单收货')
async def fake_confirm_order(request: Request, order_id: int):
    """
    需满足status_id = 2 待收货状态
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    order = d_db.get_order(order_id=order_id)
    if user_id != order.paider_id:
        raise HTTPException(status_code=400, detail='order error')
    if order is None:
        raise HTTPException(status_code=400, detail='订单不存在')
    if order.status_id != 2:
        raise HTTPException(status_code=400, detail='订单状态有误')
    item: m_schema.SOrder = m_schema.SOrder(id=order_id, status_id=3)
    # share_fee_service.share_mall_fee_with_other(order_id)
    return await r_schema.update_order(item)

@router.get(f'/real_detail', response_model=m_order.RealOrderDetail, summary='商品订单详情')
async def get_real_detail(request: Request, order_id: int):
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    order: m_schema.SOrder = d_db.get_order(order_id=order_id)
    if user_id != order.paider_id:
        raise HTTPException(status_code=400, detail='order error')
    good: m_schema.SGood = d_db.get_good(good_id=order.good_id)
    # spec: m_schema.SGoodSpec = d_db.get_good_spec(good_spec_id=order.spec_id)
    channel: m_schema.SPayChannel = d_db.get_pay_channel(pay_channel_id=order.paid_channel_id)
    total_price: int = order.sale_price * order.number
    return m_order.RealOrderDetail(order=order, good=good, spec=None, channel=channel, total_price=total_price)

@router.get(f'/wx/detail', summary='订单详情')
async def get_wx_detail(request: Request, trade_no: str):
    '''
    检索参数，out_trade_no，订单的生成序列号
    '''
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    # order: m_schema.SOrder = d_db.get_order(out_trade_no=trade_no)
    # user: m_schema.SUser = d_db.get_user(good_id=order.paider_id)
    return d_order.get_out_trade_order(trade_no)

#
# @router.get(f'/fake_delete', response_model=str, summary='订单假删除')
# async def fake_delete_order(order_id: int):
#     item: m_schema.SOrder = m_schema.SOrder(id=order_id, is_display=0)
#     return await r_schema.update_order(item)
#

# @router.get(f'/confirm_express', summary='确认收货')
# async def confirm_express(expiress_id: int):
#     expiress_order = d_package.get_package_express(expiress_id)
#     if expiress_order is None:
#         raise HTTPException(status_code=400, detail='订单不存在')
#     if expiress_order.status in (4, 6):
#         raise HTTPException(status_code=400, detail='订单已收货')
#     d_package.update_flash_order_express(expiress_id, 4)
#     #share_fee_service.share_mall_fee_with_other(order_id)
#     return {'statusCode':200}

#
# @router.get(f'/card_detail', response_model=m_order.CardOrderDetail, summary='卡券订单详情')
# async def get_real_detail(order_id: int):
#     order: m_schema.SOrder = d_db.get_order(order_id=order_id)
#     store: m_schema.SStore = d_db.get_store(store_id=order.store_id)
#     good: m_schema.SGood = d_db.get_good(good_id=order.good_id)
#     good_packages: List[m_schema.SGoodPackage] = d_db.filter_good_package(items={'good_id': good.id}, search_items={},
#                                                                           set_items={})
#     supplier = d_db.get_supplier(good.supplier_id)
#     good_rule: List[m_schema.SGoodRule] = d_db.filter_good_rule(items={'good_id': good.id}, search_items={},
#                                                                 set_items={})
#     spec: m_schema.SGoodSpec = d_db.get_good_spec(good_spec_id=order.spec_id)
#     order_state: m_schema.SOrderState = d_db.get_order_state(order_state_id=order.status_id)
#     channel: m_schema.SPayChannel = d_db.get_pay_channel(pay_channel_id=order.paid_channel_id)
#     total_price: int = order.sale_price * order.number
#
#     good_spec_combos = d_db.filter_good_spec_combo(items={'good_spec_id': order.spec_id})
#     return m_order.CardOrderDetail(order=order, good=good, TStore=store, TGoodRule=good_rule,
#                                    TGoodPackage=good_packages, spec=spec,
#                                    channel=channel,
#                                    order_state=order_state,
#                                    total_price=total_price,
#                                    TSupplier=supplier,
#                                    TGoodSpecCombo=good_spec_combos
#                                    )

#
# @router.post(f'/order_stats')
# async def return_flash_order(user_id: int):
#     """
#     POST请求，get参数user_id携带查询用户的id
#     返回：
#         "status_id ": 1, 状态值
#         "num": 2,  此状态数量
#         "state": "未发货" , 此状态值的文本意义
#     }
#     """
#     status_list = {-1: "删除", 0: "未付款", 1: "未发货", 2: "已发货", 3: "退货协商中", 4: "等待退货物流", 5: "商品退回中",
#                    6: "退货已签收", 7: "已签收", 8: "已完结", 9: "未使用", 10: "已使用"}
#     if user_id <= 0:
#         raise HTTPException(400, "非法用户")
#     res = d_order.get_order_stats(user_id)
#     for k in status_list:
#         has = False
#         for r in res:
#             if r["status_id"] == k:
#                 has = True
#         if not has:
#             res.append({"status_id": k, "num": 0, "state": status_list.get(k)})
#     return res
#
# @router.post(f'/update_cart')
# async def update_cart(data: UpdateCartModel):
#     """
#     cart_num参数，如果为0，或加减计算后小于等于0，则删除购物车中此条订单。
#     如：减少一件商品的提参：{"user_id":1,"cart_id":1,"cart_num":1,"update_state":"dec"}
#     """
#     if data.user_id is None or data.cart_id is None or data.cart_num is None:
#         raise HTTPException(status_code=400, detail='参数错误')
#     res = d_order.update_cart_amount(data.user_id, data.cart_id, data.cart_num, data.update_state)
#     if res:
#         return {"status":200, "detail": "sucess"}
#     else:
#         return {"status": 400, "detail": "未找到数据"}

def update_default(user_id:int, address_id:int):
    f_address: List[m_schema.SAddress] = d_db.filter_address(items={'user_id': user_id}, search_items={}, set_items={})
    for address in f_address:
        if address.id == address_id:
            address.default_val = 1
            d_db.update_address(item=address)
        else:
            address.default_val = 0
            d_db.update_address(item=address)

@router.get('/address/daddress', summary='删除邮寄地址')
async def delete_address(request: Request, address_id: int, valcode: str = ''):
    """
    address_id，当前地址信息ID; valcode=omgc@XtSAS7XHAkV5ob1VX
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if valcode != 'omgc@XtSAS7XHAkV5ob1VX':
        return {"code": 404, "message": "error!!!!"}
    user_info = d_user.get_user_by_id(user_id)
    if not user_info:
        return {"code": 404, "message": "error!!!"}
    address_info = d_address.get_address_by_id(address_id)
    if not address_info:
        return {"code": 404, "message": "error!!"}
    if user_info.id != address_info.user_id:
        return {"code": 404, "message": "user error!"}

    d_address.delete_address_by_id(address_id)
    return {"code": 200, "message": "success"}


@router.post(f'/address/update', response_model=dict, summary='更新邮寄地址')
async def update_address(request: Request, address_id: int, item: AddressRequest) -> dict:
    """根据地址id更新地址信息"""
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    item.user_id = user_id
    address_info = d_address.get_address_by_id(address_id)
    if not address_info:
        return {"code": 404, "message": "error!!"}
    if user_id != address_info.user_id:
        return {"code": 404, "message": "user error!"}
    d_address.update_address_by_id(address_id, item.__dict__)
    return {'code': 200, 'message': 'success'}


@router.get(f'/address/get', response_model=List[UserAddress], summary='获取用户邮寄地址列表')
async def get_address(request: Request):
    """根据用户id查询该用户的所有收货地址"""
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    t_address_list = d_address.get_address(user_id=user_id)
    return [UserAddress.parse_obj(t.__dict__) for t in t_address_list]


@router.post(f'/address/set_default', response_model=SuccessResponse, summary='设置默认地址接口')
async def set_default_address(request: Request, address_id: int):
    """将用户地址列表下的某个地址设置为默认地址"""
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    update_default(user_id, address_id)
    return SuccessResponse()



@router.post('/address/create', response_model=m_schema.SAddress, summary='添加地址（自动设置为默认地址）')
async def add_address(request: Request, item: m_schema.CreateAddress) -> m_schema.SAddress:
    """创建地址时自动设置为默认地址"""
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    item.user_id = user_id
    s_address: m_schema.SAddress = d_db.insert_address(item=item)
    if item.default_val > 0:
        update_default(user_id, s_address.id)
    return s_address

# @router.post('/order/getsetup', summary='获取公众号配置')
# async def getsetup(request: Request):
#     """获取微信配置"""
#     return {"APP_ID":WX.appId, "DOMAIN": DOMAIN}

@router.get(f'/bag_pas/active', summary="卡密激活")
async def create_bag_active(request: Request, code: str):
    '''
    pc_code: Optional[str] = Field(title='卡密码，十六进制编码')
    user_id: Optional[int] = Field(title='激活会员id')
    '''
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    pas_info = d_bagpass.find_pc_for_num(code)
    if not  pas_info:
        raise HTTPException(status_code=404, detail='参数错误')
    if pas_info.stat != 0:
        raise HTTPException(status_code=404, detail='卡密码,有误！')
    u_info = d_user.get_user_by_id(user_id)
    if not u_info:
        raise HTTPException(status_code=404, detail='未知用户')
    #更新
    d_bagpass.bagpass_active(code, user_id)
    return {'code': 200, 'message': 'success'}


@router.get(f'/bag_pas/filter', summary="查询卡密列表")
async def filter_bag_pas(pass_num: Optional[str] = None):
    if not pass_num:
        raise HTTPException(status_code=404, detail='未知参数')
    return d_order.get_bagpass_for_pass(pass_num)


@router.get(f'/video/baglist', summary='获取当前用户视频条数礼包订单列表')
async def video_get_baglist(request: Request, page:int = 1):
    """
    当前登录用户所有订单，且满足 is_display='1'
    """
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if not user_id:
        raise HTTPException(status_code=400, detail='please login')
    page_size = 20
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "order",
        # "joins": [
        #     {
        #         "table": "good",
        #         "on_left": "good_id",
        #         "on_right": "id"
        #     }
        # ],
        "selects": ["order"],
        "filters": [
            # {
            #     "field": "order.status_id",
            #     "value": 1
            # },
            {
                "field": "order.paider_id",
                "value": user_id
            },
            {
                "field": "order.is_video",
                "value": 1
            }
            # {
            # "field": "order.isfirst",
            # "value": 0
            # }
        ],
        # "order_by": [{"field": "good.priority", "order": "desc"},{"field": "good.id", "order": "desc"}],
        "order_by": [{"field": "order.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res
