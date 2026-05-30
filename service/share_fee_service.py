from typing import Optional
from fastapi.exceptions import HTTPException

from common import Dao, global_define, global_function
from model.schema import TUser, TOrder, TGoodSpec, TFlashOrder, TPackage, TOrderSource, TGood, TSupplierIncome, TBigorderInitbag
from dao import d_user_account, d_account, d_user, d_package, d_order, d_groupsir, d_settings, d_partner, d_balance, d_good, d_adbrand, d_found
from model.mall import m_account
import time, datetime, json
import logging

def share_mall_fee_with_other(order_id: int):
    """share mall fee with other"""
    with Dao() as db:
        # 查询数据
        t_order, t_user, t_good = db.query(TOrder, TUser, TGood)\
            .outerjoin(TUser, TUser.id==TOrder.paider_id)\
            .outerjoin(TGood, TOrder.good_id==TGood.id)\
            .filter(TOrder.id == order_id).first()
        if t_order is None:
            raise HTTPException(400, "订单不存在")
        if t_user is None:
            raise HTTPException(400, "用户不存在")
        # if t_spec is None:
        #     raise HTTPException(400, "商品不存在")
        # if t_order.is_assign_income:
        #     raise HTTPException(400, "已经分配过收益")
        t_order: TOrder   # 走批发价商品 t_order.is_wholesale=2
        t_user: TUser    # 批发商身份 t_user.wholesale_id=100
        # t_spec: TGoodSpec
        #t_source: TOrderSource
        t_good: TGood

        #更新秒杀包持有人订单收益记录
        user_income_l = []
        groupsir_income_l = []
        parent_income = 0
        invited_income = 0
        invited_income2 = 0
        top_income = 0
        recommender_income = 0
        recommender_income2 = 0
        supplier_income = 0
        eqlevel_income = 0
        this_tuan_fee = 0
        this_retuan_fee = 0
        supplier_fee = 0
        share_fee = 0
        share_mid_fee = 0
        t_source_list = d_order.get_order_source(t_order.id)
        # 使用积分的订单，视为批发商品订单，不分成
        # if t_order.paid_coin > 0:
        #     t_order.is_wholesale = 2

        # 层级奖
        # parent_id: Optional[int] = None
        # balance_type = global_define.balance_type[1]
        # is_invited = False
        # if t_user.parent_id is not None:
        #     parent_id = t_user.parent_id
        # elif t_user.invited_user_id is not None:
        #     parent_id = t_user.invited_user_id
        #     balance_type = global_define.balance_type[14]
        #     is_invited = True
        #批发商订单不分成  t_order.is_wholesale=2
        # if t_order.parent_uid is not None and t_order.parent_uid > 0 and t_order.is_wholesale != 2:
        # if t_order.parent_uid is not None and t_order.parent_uid > 0:
        #     parent_info = d_account.get_account_info_add(t_order.parent_uid)
        #     this_parent_fee = 0
        #     if t_order.zdyspec:
        #         this_parent_fee = float(json.loads(t_order.zdyspec)['层级']) * 100
        #     else:
        #         this_parent_fee = t_spec.parent_fee
        #     if parent_info and this_parent_fee > 0:
        #         parent_income = this_parent_fee * t_order.number
        #         total_balance = parent_info.balance + parent_income
        #         d_account.update_account_by_id(parent_info.id, {"balance": total_balance})
        #         d_account.add_balance(m_account.BalanceModel(
        #             user_id=parent_info.user_id,
        #             change=parent_income,
        #             balance=total_balance,
        #             type=global_define.balance_type[1],
        #             create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #             good_id=str(t_good.id),
        #             good_title=t_good.title,
        #             good_num=str(t_order.number),
        #             out_trade_no=t_order.out_trade_no
        #         ))

        #当使用销售价格时分推荐奖，使用会员价格时分享奖
        if t_order.is_user_price >= 0:
            if t_order.invited_uid is not None and t_order.invited_uid > 0:
                parent_info = d_account.get_account_info_add(t_order.invited_uid)
                uinfo = d_user.get_user_by_id(t_order.invited_uid)
                this_recommender_fee = 0
                if t_order.zdyspec:
                    try:
                        this_recommender_fee = float(json.loads(t_order.zdyspec)['分享']) * 100
                    except Exception as e:
                        this_recommender_fee = 0
                else:
                    this_recommender_fee = this_recommender_fee
                if parent_info and this_recommender_fee > 0 and uinfo:
                    if uinfo.video_level > 0:
                        share_fee = this_recommender_fee * t_order.number
                        d_balance.invited_user_money(parent_info.user_id, share_fee, global_define.balance_type[28], t_good.id, \
                                                     f"{t_good.id}|{t_good.title}", t_order.number, t_order.out_trade_no)

            # 间推分配收益
            this_jiantui_fee = 0
            if t_order.zdyspec:
                try:
                    this_jiantui_fee = float(json.loads(t_order.zdyspec)['分享推']) * 100
                except Exception as e:
                    this_jiantui_fee = 0
            if t_order.invited_two_uid is not None and t_order.invited_two_uid > 0 and this_jiantui_fee > 0:
                d_balance.invited_user_money(t_order.invited_two_uid, this_jiantui_fee, global_define.balance_type[29], t_good.id, \
                                             f"{t_good.id}|{t_good.title}", t_order.number, t_order.out_trade_no)

        else:
            # 直推级奖 批发商订单不分成  t_order.is_wholesale=2  [2024.5.30批发商订单也分成]
            #if t_order.invited_uid is not None and t_order.invited_uid > 0 and t_order.is_wholesale != 2:
            is_invited_fee = False
            if t_order.invited_uid is not None and t_order.invited_uid > 0:
                parent_info = d_account.get_account_info_add(t_order.invited_uid)
                uinfo = d_user.get_user_by_id(t_order.invited_uid)
                this_recommender_fee = 0
                if t_order.zdyspec:
                    try:
                        this_recommender_fee = float(json.loads(t_order.zdyspec)['直推']) * 100
                    except Exception as e:
                        this_recommender_fee = 0
                else:
                    this_recommender_fee = this_recommender_fee
                if parent_info and this_recommender_fee > 0 and uinfo:
                    if uinfo.video_level > 0:
                        d_balance.invited_user_money(parent_info.user_id, this_recommender_fee, global_define.balance_type[26], t_good.id, \
                                                     f"{t_good.id}|{t_good.title}", t_order.number, t_order.out_trade_no)

            # 间推分配收益
            this_jiantui_fee = 0
            if t_order.zdyspec:
                try:
                    this_jiantui_fee = float(json.loads(t_order.zdyspec)['间推']) * 100
                except Exception as e:
                    this_jiantui_fee = 0
            if t_order.invited_two_uid is not None and t_order.invited_two_uid > 0 and this_jiantui_fee > 0:
                supplier_info = d_account.get_account_info_add(t_order.invited_two_uid)
                uinfo = d_user.get_user_by_id(t_order.invited_two_uid)
                if supplier_info and uinfo:
                    if uinfo.video_level > 0:
                        d_balance.invited_user_money(t_order.invited_two_uid, this_jiantui_fee, global_define.balance_type[27], t_good.id, \
                                                     f"{t_good.id}|{t_good.title}", t_order.number, t_order.out_trade_no)


        # 市代分配收益
        this_sh_agent_fee = 0
        if t_order.zdyspec:
            try:
                this_sh_agent_fee = float(json.loads(t_order.zdyspec)['市代']) * 100
            except Exception as e:
                this_sh_agent_fee = 0
        if t_order.sh_agent_id is not None and t_order.sh_agent_id > 0 and this_sh_agent_fee > 0:
            d_balance.invited_user_money(t_order.sh_agent_id, this_sh_agent_fee, global_define.balance_type[50], t_good.id, \
                                         f"{t_good.id}|{t_good.title}", t_order.number, t_order.out_trade_no)
        #
        # # 商品分享奖励
        # if t_order.share_invited_uid is not None:
        #     if t_order.share_invited_uid > 0:
        #         recommender_info = d_account.get_account_info_add(t_order.share_invited_uid)
        #     else:
        #         recommender_info = None
        #     if t_order.zdyspec:
        #         this_jiantui_fee = float(json.loads(t_order.zdyspec)['分享']) * 100
        #     if recommender_info and this_jiantui_fee > 0:
        #         uinfo = d_user.get_user_by_id(t_order.share_invited_uid)
        #         if uinfo.video_level > 0:
        #             recommender_income = this_jiantui_fee * t_order.number
        #             total_balance = recommender_info.balance + recommender_income
        #             d_account.update_account_by_id(recommender_info.id, {"balance": total_balance})
        #             d_account.add_balance(m_account.BalanceModel(
        #                 user_id=recommender_info.user_id,
        #                 change=recommender_income,
        #                 balance=total_balance,
        #                 type=global_define.balance_type[28],
        #                 create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #                 good_id=str(t_good.id),
        #                 good_title=t_good.title,
        #                 good_num=str(t_order.number),
        #                 out_trade_no=t_order.out_trade_no
        #             ))
        #
        # # 商品间推分享奖励
        # if t_order.share_invited_two_uid is not None:
        #     if t_order.share_invited_two_uid > 0:
        #         recommender_info = d_account.get_account_info_add(t_order.share_invited_two_uid)
        #     else:
        #         recommender_info = None
        #     if t_order.zdyspec:
        #         this_jiantui_fee = float(json.loads(t_order.zdyspec)['分享推']) * 100
        #     if recommender_info and this_jiantui_fee > 0:
        #         uinfo = d_user.get_user_by_id(t_order.share_invited_two_uid)
        #         if uinfo.video_level > 0:
        #             recommender_income = this_jiantui_fee * t_order.number
        #             recommender_income2 = recommender_income
        #             total_balance = recommender_info.balance + recommender_income
        #             d_account.update_account_by_id(recommender_info.id, {"balance": total_balance})
        #             d_account.add_balance(m_account.BalanceModel(
        #                 user_id=recommender_info.user_id,
        #                 change=recommender_income,
        #                 balance=total_balance,
        #                 type=global_define.balance_type[29],
        #                 create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #                 good_id=str(t_good.id),
        #                 good_title=t_good.title,
        #                 good_num=str(t_order.number),
        #                 out_trade_no=t_order.out_trade_no
        #             ))

        #供货收益 介绍人的收益  批发商订单不分成  t_order.is_wholesale=2
        if t_order.supplier_uid is not None and t_order.supplier_uid > 0:
            supplier_info = d_account.get_account_info_add(t_order.supplier_uid)
            if supplier_info:
                if t_order.zdyspec:
                    try:
                        supplier_fee = float(json.loads(t_order.zdyspec)['供货']) * 100
                    except Exception as e:
                        supplier_fee = 0
                supplier_income = supplier_fee * t_order.number
                if supplier_info.balance is None:
                    supplier_info.balance = 0
                total_balance = supplier_info.balance + supplier_income
                d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=t_order.supplier_uid,
                    change=supplier_income,
                    balance=total_balance,
                    type=global_define.balance_type[32],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(t_good.id),
                    good_title=t_good.title,
                    good_num=str(t_order.number),
                    out_trade_no=t_order.out_trade_no
                ))

        #批发商随机分配收益
        # this_random_fee = 0
        # this_xyun_fee = 0
        # if t_order.zdyspec:
        #     this_random_fee = float(json.loads(t_order.zdyspec)['随机分']) * 100
        # else:
        #     this_random_fee = t_spec.random_fee
        # if t_order.random_fee_uid is not None and t_order.random_fee_uid > 0 and this_random_fee > 0:
        #     supplier_info = d_account.get_account_info_add(t_order.random_fee_uid)
        #     if supplier_info:
        #         supplier_income = this_random_fee * t_order.number
        #         if supplier_info.balance is None:
        #             supplier_info.balance = 0
        #         total_balance = supplier_info.balance + supplier_income
        #         d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
        #         d_account.add_balance(m_account.BalanceModel(
        #             user_id=t_order.random_fee_uid,
        #             change=supplier_income,
        #             balance=total_balance,
        #             type=global_define.balance_type[32],
        #             create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #             good_id=str(t_good.id),
        #             good_title=t_good.title,
        #             good_num=str(t_order.number),
        #             out_trade_no=t_order.out_trade_no
        #         ))
        #         # 幸运奖, 给推荐人同样一笔奖励
        #         random_uinfo = d_user.get_user_by_id(t_order.random_invited_uid)
        #         #invitid = random_uinfo.invited_user_id if random_uinfo.invited_user_id is not None else 0
        #         if random_uinfo:
        #             this_xyun_fee = supplier_income
        #             invite_account = d_account.get_account_info_add(t_order.random_invited_uid)
        #             total_balance = invite_account.balance + supplier_income
        #             d_account.update_account_by_id(t_order.random_invited_uid, {"balance": total_balance})
        #             d_account.add_balance(m_account.BalanceModel(
        #                 user_id=t_order.random_invited_uid,
        #                 change=supplier_income,
        #                 balance=total_balance,
        #                 type=global_define.balance_type[36],
        #                 create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #                 good_id=str(t_good.id),
        #                 good_title=t_good.title,
        #                 good_num=str(t_order.number),
        #                 out_trade_no=t_order.out_trade_no
        #             ))
        #

        # 团长分配收益
        this_tuan_fee = 0
        if t_order.zdyspec:
            try:
                this_tuan_fee = float(json.loads(t_order.zdyspec)['推团']) * 100
            except:
                this_tuan_fee = 0
        else:
            this_tuan_fee = this_tuan_fee
        if t_order.tuan_uid is not None and t_order.tuan_uid > 0 and this_tuan_fee > 0:
            supplier_info = d_account.get_account_info_add(t_order.tuan_uid)
            uinfo = d_user.get_user_by_id(t_order.tuan_uid)
            if supplier_info and uinfo:
                if uinfo.video_level > 0:
                    supplier_income = this_tuan_fee * t_order.number
                    if supplier_info.balance is None:
                        supplier_info.balance = 0
                    total_balance = supplier_info.balance + supplier_income
                    d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
                    d_account.add_balance(m_account.BalanceModel(
                        user_id=t_order.tuan_uid,
                        change=supplier_income,
                        balance=total_balance,
                        type=global_define.balance_type[30],
                        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        good_id=str(t_good.id),
                        good_title=t_good.title,
                        good_num=str(t_order.number),
                        out_trade_no=t_order.out_trade_no
                    ))

        # 上级间团分配收益
        this_retuan_fee = 0
        if t_order.zdyspec:
            try:
                this_retuan_fee = float(json.loads(t_order.zdyspec)['间团']) * 100
            except:
                this_retuan_fee = 0
        else:
            this_retuan_fee = this_retuan_fee
        if t_order.retuan_uid is not None and t_order.retuan_uid > 0 and this_retuan_fee > 0:
            supplier_info = d_account.get_account_info_add(t_order.retuan_uid)
            uinfo = d_user.get_user_by_id(t_order.retuan_uid)
            if supplier_info and uinfo:
                if uinfo.video_level > 0:
                    supplier_income = this_retuan_fee * t_order.number
                    # d_balance.invited_user_money(uinfo.id, supplier_income, global_define.balance_type[31], t_order.id,\
                    #                              f"{task_info.id}|{task_info.title}")
                    if supplier_info.balance is None:
                        supplier_info.balance = 0
                    total_balance = supplier_info.balance + supplier_income
                    d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
                    d_account.add_balance(m_account.BalanceModel(
                        user_id=t_order.retuan_uid,
                        change=supplier_income,
                        balance=total_balance,
                        type=global_define.balance_type[31],
                        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        good_id=str(t_good.id),
                        good_title=t_good.title,
                        good_num=str(t_order.number),
                        out_trade_no=t_order.out_trade_no
                    ))


        # 居间分配收益
        this_live_fee = 0
        if t_order.live_mid_uid is not None and t_order.live_mid_uid > 0 and t_order.live_mid_money > 0:
            supplier_info = d_account.get_account_info_add(t_order.live_mid_uid)
            uinfo = d_user.get_user_by_id(t_order.live_mid_uid)
            if supplier_info and uinfo:
                if uinfo.video_level > 0:
                    this_live_fee = t_order.live_mid_money
                    supplier_income = this_live_fee * t_order.number
                    # d_balance.invited_user_money(uinfo.id, supplier_income, global_define.balance_type[31], t_order.id,\
                    #                              f"{task_info.id}|{task_info.title}")
                    if supplier_info.balance is None:
                        supplier_info.balance = 0
                    total_balance = supplier_info.balance + supplier_income
                    d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
                    d_account.add_balance(m_account.BalanceModel(
                        user_id=t_order.live_mid_uid,
                        change=supplier_income,
                        balance=total_balance,
                        type=global_define.balance_type[46],
                        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        good_id=str(t_good.id),
                        good_title=t_good.title,
                        good_num=str(t_order.number),
                        out_trade_no=t_order.out_trade_no
                    ))

        # 省代收益
        # this_shengdai_fee = 0
        # if t_order.zdyspec:
        #     try:
        #         this_shengdai_fee = float(json.loads(t_order.zdyspec)['省代']) * 100
        #     except:
        #         this_shengdai_fee = 0
        # if t_order.shengdai_uid is not None and t_order.shengdai_uid > 0 and this_shengdai_fee > 0:
        #     supplier_info = d_account.get_account_info_add(t_order.shengdai_uid)
        #     if supplier_info:
        #         supplier_income = this_shengdai_fee * t_order.number
        #         if supplier_info.balance is None:
        #             supplier_info.balance = 0
        #         total_balance = supplier_info.balance + supplier_income
        #         d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
        #         d_account.add_balance(m_account.BalanceModel(
        #             user_id=t_order.shengdai_uid,
        #             change=supplier_income,
        #             balance=total_balance,
        #             type=global_define.balance_type[37],
        #             create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #             good_id=str(t_good.id),
        #             good_title=t_good.title,
        #             good_num=str(t_order.number),
        #             out_trade_no=t_order.out_trade_no
        #         ))

        #供货商收回成本
        # if t_spec.supplier_fee is not None and t_good.supplier_id is not None:
        #     supplier_info = d_supplier_account.get_account_info(t_good.supplier_id)
        #     if supplier_info:
        #         supplier_income = t_spec.supplier_fee * t_order.number
        #         if supplier_info.amount is None:
        #             supplier_info.amount = 0
        #         total_balance = supplier_info.amount + supplier_income
        #         d_supplier_account.update_account_by_id(supplier_info.id, {"change": supplier_income,"amount": total_balance})
        #         d_supplier_income.add_income(TSupplierIncome(
        #             supplier_id=t_good.supplier_id,
        #             change=supplier_income,
        #             balance=total_balance,
        #             type=global_define.balance_type[8],
        #             create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #             operator_id=10000
        #             # good_id=str(t_good.id),
        #             # good_title=t_good.title,
        #             # good_num=str(t_order.number)
        #         ))

        #更新订单收益分配状态
        now_time = datetime.datetime.now()
        d_order.assign_income_order(TOrder(
            id=t_order.id,
            complete_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            is_assign_income=1,
            detail=f"[{now_time}#推荐：{invited_income}#间推：{invited_income2}#分享：{recommender_income}#间接分享：{recommender_income2}#团长：{this_tuan_fee}#间团：{this_retuan_fee}#供货：{supplier_fee}#居间：{this_live_fee}#市代：{this_sh_agent_fee}]"
        ))
        # 更新系统用户级别
        if t_user.level_id == 0:
            d_user.update_sysuser_active(t_user.id)
        elif t_user.level_id == 1:
            d_user.update_sysuser_high(t_user.id)
        elif t_user.level_id == 2:
            d_user.update_sysuser_top(t_user.id)
        db.commit()

        # else:
        #     # 更新订单收益分配状态
        #     now_time = datetime.datetime.now()
        #     d_order.assign_income_order2(TOrder(
        #         id=t_order.id,
        #         complete_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #     ))
        #     # 更新系统用户级别
        #     if t_user.level_id == 0:
        #         d_user.update_sysuser_active(t_user.id)
        #     elif t_user.level_id == 1:
        #         d_user.update_sysuser_high(t_user.id)
        #     elif t_user.level_id == 2:
        #         d_user.update_sysuser_top(t_user.id)
        #     db.commit()


def share_mall_fee_with_other_ad(order_id: int):
    """share mall fee with other"""
    with Dao() as db:
        # 查询数据
        t_order, t_user, t_good = db.query(TOrder, TUser, TGood)\
            .outerjoin(TUser, TUser.id==TOrder.paider_id)\
            .outerjoin(TGood, TOrder.good_id==TGood.id)\
            .filter(TOrder.id == order_id).first()
        if t_order is None:
            raise HTTPException(400, "订单不存在")
        if t_user is None:
            raise HTTPException(400, "用户不存在")
        # if t_spec is None:
        #     raise HTTPException(400, "商品不存在")
        # if t_order.is_assign_income:
        #     raise HTTPException(400, "已经分配过收益")
        t_order: TOrder   # 走批发价商品 t_order.is_wholesale=2
        t_user: TUser    # 批发商身份 t_user.wholesale_id=100
        # t_spec: TGoodSpec
        #t_source: TOrderSource
        t_good: TGood

        #更新秒杀包持有人订单收益记录
        user_income_l = []
        groupsir_income_l = []
        parent_income = 0
        invited_income = 0
        invited_income2 = 0
        top_income = 0
        recommender_income = 0
        recommender_income2 = 0
        supplier_income = 0
        eqlevel_income = 0
        this_tuan_fee = 0
        this_retuan_fee = 0
        supplier_fee = 0
        share_fee = 0
        share_mid_fee = 0
        t_source_list = d_order.get_order_source(t_order.id)
        # 使用积分的订单，视为批发商品订单，不分成
        # if t_order.paid_coin > 0:
        #     t_order.is_wholesale = 2

        # 层级奖
        # parent_id: Optional[int] = None
        # balance_type = global_define.balance_type[1]
        # is_invited = False
        # if t_user.parent_id is not None:
        #     parent_id = t_user.parent_id
        # elif t_user.invited_user_id is not None:
        #     parent_id = t_user.invited_user_id
        #     balance_type = global_define.balance_type[14]
        #     is_invited = True
        #批发商订单不分成  t_order.is_wholesale=2
        # if t_order.parent_uid is not None and t_order.parent_uid > 0 and t_order.is_wholesale != 2:
        # if t_order.parent_uid is not None and t_order.parent_uid > 0:
        #     parent_info = d_account.get_account_info_add(t_order.parent_uid)
        #     this_parent_fee = 0
        #     if t_order.zdyspec:
        #         this_parent_fee = float(json.loads(t_order.zdyspec)['层级']) * 100
        #     else:
        #         this_parent_fee = t_spec.parent_fee
        #     if parent_info and this_parent_fee > 0:
        #         parent_income = this_parent_fee * t_order.number
        #         total_balance = parent_info.balance + parent_income
        #         d_account.update_account_by_id(parent_info.id, {"balance": total_balance})
        #         d_account.add_balance(m_account.BalanceModel(
        #             user_id=parent_info.user_id,
        #             change=parent_income,
        #             balance=total_balance,
        #             type=global_define.balance_type[1],
        #             create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #             good_id=str(t_good.id),
        #             good_title=t_good.title,
        #             good_num=str(t_order.number),
        #             out_trade_no=t_order.out_trade_no
        #         ))

        #当使用销售价格时分推荐奖，使用会员价格时分享奖
        # if t_order.is_user_price > 0:
        #     if t_order.invited_uid is not None and t_order.invited_uid > 0:
        #         parent_info = d_account.get_account_info_add(t_order.invited_uid)
        #         uinfo = d_user.get_user_by_id(t_order.invited_uid)
        #         this_recommender_fee = 0
        #         if t_order.zdyspec:
        #             try:
        #                 this_recommender_fee = float(json.loads(t_order.zdyspec)['分享']) * 100
        #             except Exception as e:
        #                 this_recommender_fee = 0
        #         else:
        #             this_recommender_fee = this_recommender_fee
        #         if parent_info and this_recommender_fee > 0 and uinfo:
        #             if uinfo.video_level > 0:
        #                 share_fee = this_recommender_fee * t_order.number
        #                 d_balance.invited_user_money(parent_info.user_id, share_fee, global_define.balance_type[28], t_good.id, \
        #                                              f"{t_good.id}|{t_good.title}", t_order.number, t_order.out_trade_no)
        #
        #     # 间推分配收益
        #     this_jiantui_fee = 0
        #     if t_order.zdyspec:
        #         try:
        #             this_jiantui_fee = float(json.loads(t_order.zdyspec)['分享推']) * 100
        #         except Exception as e:
        #             this_jiantui_fee = 0
        #     if t_order.invited_two_uid is not None and t_order.invited_two_uid > 0 and this_jiantui_fee > 0:
        #         d_balance.invited_user_money(t_order.invited_two_uid, this_jiantui_fee, global_define.balance_type[29], t_good.id, \
        #                                      f"{t_good.id}|{t_good.title}", t_order.number, t_order.out_trade_no)
        #
        # else:
        #     # 直推级奖 批发商订单不分成  t_order.is_wholesale=2  [2024.5.30批发商订单也分成]
        #     #if t_order.invited_uid is not None and t_order.invited_uid > 0 and t_order.is_wholesale != 2:
        #     is_invited_fee = False
        #     if t_order.invited_uid is not None and t_order.invited_uid > 0:
        #         parent_info = d_account.get_account_info_add(t_order.invited_uid)
        #         uinfo = d_user.get_user_by_id(t_order.invited_uid)
        #         this_recommender_fee = 0
        #         if t_order.zdyspec:
        #             try:
        #                 this_recommender_fee = float(json.loads(t_order.zdyspec)['直推']) * 100
        #             except Exception as e:
        #                 this_recommender_fee = 0
        #         else:
        #             this_recommender_fee = this_recommender_fee
        #         if parent_info and this_recommender_fee > 0 and uinfo:
        #             if uinfo.video_level > 0:
        #                 d_balance.invited_user_money(parent_info.user_id, this_recommender_fee, global_define.balance_type[26], t_good.id, \
        #                                              f"{t_good.id}|{t_good.title}", t_order.number, t_order.out_trade_no)
        #
        #     # 间推分配收益
        #     this_jiantui_fee = 0
        #     if t_order.zdyspec:
        #         try:
        #             this_jiantui_fee = float(json.loads(t_order.zdyspec)['间推']) * 100
        #         except Exception as e:
        #             this_jiantui_fee = 0
        #     if t_order.invited_two_uid is not None and t_order.invited_two_uid > 0 and this_jiantui_fee > 0:
        #         supplier_info = d_account.get_account_info_add(t_order.invited_two_uid)
        #         uinfo = d_user.get_user_by_id(t_order.invited_two_uid)
        #         if supplier_info and uinfo:
        #             if uinfo.video_level > 0:
        #                 d_balance.invited_user_money(t_order.invited_two_uid, this_jiantui_fee, global_define.balance_type[27], t_good.id, \
        #                                              f"{t_good.id}|{t_good.title}", t_order.number, t_order.out_trade_no)

        #销售收益
        ad_info = d_adbrand.get_ad_info(t_order.ad_id)
        sell_id = 0
        sell_fee = 0
        if ad_info:
            sell_id = ad_info.user_id
            try:
                sell_fee = float(json.loads(t_order.zdyspec)['销售']) * 100
            except Exception as e:
                pass
            if sell_id > 0 and sell_fee > 0:
                # supplier_info = d_account.get_account_info_add(sell_id)
                d_balance.invited_user_money(sell_id, sell_fee, global_define.balance_type[1], t_good.id,\
                                            f"{t_good.id}|{t_good.title}", t_order.number, t_order.out_trade_no)

        #供货收益 介绍人的收益  批发商订单不分成  t_order.is_wholesale=2
        if t_order.supplier_uid is not None and t_order.supplier_uid > 0:
            supplier_info = d_account.get_account_info_add(t_order.supplier_uid)
            if supplier_info:
                if t_order.zdyspec:
                    try:
                        supplier_fee = float(json.loads(t_order.zdyspec)['供货']) * 100
                    except Exception as e:
                        supplier_fee = 0
                supplier_income = supplier_fee * t_order.number
                if supplier_info.balance is None:
                    supplier_info.balance = 0
                total_balance = supplier_info.balance + supplier_income
                d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=t_order.supplier_uid,
                    change=supplier_income,
                    balance=total_balance,
                    type=global_define.balance_type[32],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(t_good.id),
                    good_title=t_good.title,
                    good_num=str(t_order.number),
                    out_trade_no=t_order.out_trade_no
                ))

        # 团长分配收益
        this_tuan_fee = 0
        if t_order.zdyspec:
            try:
                this_tuan_fee = float(json.loads(t_order.zdyspec)['推团']) * 100
            except:
                this_tuan_fee = 0
        else:
            this_tuan_fee = this_tuan_fee
        if t_order.tuan_uid is not None and t_order.tuan_uid > 0 and this_tuan_fee > 0:
            supplier_info = d_account.get_account_info_add(t_order.tuan_uid)
            uinfo = d_user.get_user_by_id(t_order.tuan_uid)
            if supplier_info and uinfo:
                if uinfo.video_level > 0:
                    supplier_income = this_tuan_fee * t_order.number
                    if supplier_info.balance is None:
                        supplier_info.balance = 0
                    total_balance = supplier_info.balance + supplier_income
                    d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
                    d_account.add_balance(m_account.BalanceModel(
                        user_id=t_order.tuan_uid,
                        change=supplier_income,
                        balance=total_balance,
                        type=global_define.balance_type[30],
                        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        good_id=str(t_good.id),
                        good_title=t_good.title,
                        good_num=str(t_order.number),
                        out_trade_no=t_order.out_trade_no
                    ))

        # 上级间团分配收益
        this_retuan_fee = 0
        if t_order.zdyspec:
            try:
                this_retuan_fee = float(json.loads(t_order.zdyspec)['间团']) * 100
            except:
                this_retuan_fee = 0
        else:
            this_retuan_fee = this_retuan_fee
        if t_order.retuan_uid is not None and t_order.retuan_uid > 0 and this_retuan_fee > 0:
            supplier_info = d_account.get_account_info_add(t_order.retuan_uid)
            uinfo = d_user.get_user_by_id(t_order.retuan_uid)
            if supplier_info and uinfo:
                if uinfo.video_level > 0:
                    supplier_income = this_retuan_fee * t_order.number
                    # d_balance.invited_user_money(uinfo.id, supplier_income, global_define.balance_type[31], t_order.id,\
                    #                              f"{task_info.id}|{task_info.title}")
                    if supplier_info.balance is None:
                        supplier_info.balance = 0
                    total_balance = supplier_info.balance + supplier_income
                    d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
                    d_account.add_balance(m_account.BalanceModel(
                        user_id=t_order.retuan_uid,
                        change=supplier_income,
                        balance=total_balance,
                        type=global_define.balance_type[31],
                        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        good_id=str(t_good.id),
                        good_title=t_good.title,
                        good_num=str(t_order.number),
                        out_trade_no=t_order.out_trade_no
                    ))


        # 居间分配收益
        this_live_fee = 0
        if t_order.live_mid_uid is not None and t_order.live_mid_uid > 0 and t_order.live_mid_money > 0:
            supplier_info = d_account.get_account_info_add(t_order.live_mid_uid)
            uinfo = d_user.get_user_by_id(t_order.live_mid_uid)
            if supplier_info and uinfo:
                if uinfo.video_level > 0:
                    this_live_fee = t_order.live_mid_money
                    supplier_income = this_live_fee * t_order.number
                    # d_balance.invited_user_money(uinfo.id, supplier_income, global_define.balance_type[31], t_order.id,\
                    #                              f"{task_info.id}|{task_info.title}")
                    if supplier_info.balance is None:
                        supplier_info.balance = 0
                    total_balance = supplier_info.balance + supplier_income
                    d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
                    d_account.add_balance(m_account.BalanceModel(
                        user_id=t_order.live_mid_uid,
                        change=supplier_income,
                        balance=total_balance,
                        type=global_define.balance_type[46],
                        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        good_id=str(t_good.id),
                        good_title=t_good.title,
                        good_num=str(t_order.number),
                        out_trade_no=t_order.out_trade_no
                    ))

        # 市代分配收益
        # this_sh_agent_fee = 0
        # if t_order.zdyspec:
        #     try:
        #         this_sh_agent_fee = float(json.loads(t_order.zdyspec)['市代']) * 100
        #     except Exception as e:
        #         this_sh_agent_fee = 0
        # if t_order.sh_agent_id is not None and t_order.sh_agent_id > 0 and this_sh_agent_fee > 0:
        #     d_balance.invited_user_money(t_order.sh_agent_id, this_sh_agent_fee, global_define.balance_type[50], t_good.id, \
        #                                  f"{t_good.id}|{t_good.title}", t_order.number, t_order.out_trade_no)
        #更新订单收益分配状态
        now_time = datetime.datetime.now()
        d_order.assign_income_order(TOrder(
            id=t_order.id,
            complete_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            is_assign_income=1,
            detail=f"[{now_time}#推荐：{invited_income}#间推：{invited_income2}#分享：{recommender_income}#间接分享：{recommender_income2}#团长：{this_tuan_fee}#间团：{this_retuan_fee}#供货：{supplier_fee}#居间：{this_live_fee}]"
        ))
        # 更新系统用户级别
        if t_user.level_id == 0:
            d_user.update_sysuser_active(t_user.id)
        elif t_user.level_id == 1:
            d_user.update_sysuser_high(t_user.id)
        elif t_user.level_id == 2:
            d_user.update_sysuser_top(t_user.id)
        db.commit()

        # else:
        #     # 更新订单收益分配状态
        #     now_time = datetime.datetime.now()
        #     d_order.assign_income_order2(TOrder(
        #         id=t_order.id,
        #         complete_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #     ))
        #     # 更新系统用户级别
        #     if t_user.level_id == 0:
        #         d_user.update_sysuser_active(t_user.id)
        #     elif t_user.level_id == 1:
        #         d_user.update_sysuser_high(t_user.id)
        #     elif t_user.level_id == 2:
        #         d_user.update_sysuser_top(t_user.id)
        #     db.commit()




def share_mall_fee_with_jinny(order_id: int):
    """share mall fee with other"""
    with Dao() as db:
        # 查询数据
        t_order, t_user, t_good = db.query(TOrder, TUser, TGood)\
            .outerjoin(TUser, TUser.id==TOrder.paider_id)\
            .outerjoin(TGood, TOrder.good_id==TGood.id)\
            .filter(TOrder.id == order_id).first()
        if t_order is None:
            raise HTTPException(400, "订单不存在")
        if t_user is None:
            raise HTTPException(400, "用户不存在")
        # if t_spec is None:
        #     raise HTTPException(400, "商品不存在")
        # if t_order.is_assign_income:
        #     raise HTTPException(400, "已经分配过收益")
        t_order: TOrder   # 走批发价商品 t_order.is_wholesale=2
        t_user: TUser    # 批发商身份 t_user.wholesale_id=100
        # t_spec: TGoodSpec
        #t_source: TOrderSource
        t_good: TGood

        #更新秒杀包持有人订单收益记录
        user_income_l = []
        groupsir_income_l = []
        parent_income = 0
        invited_income = 0
        invited_income2 = 0
        top_income = 0
        recommender_income = 0
        supplier_income = 0
        eqlevel_income = 0
        this_random_fee = 0
        this_tuan_fee = 0
        this_retuan_fee = 0
        this_xyun_fee = 0
        this_shengdai_fee = 0

        #使用积分支付的商品不参与分成
        # if t_order.paid_coin > 0:

        # 直推级奖 批发商订单不分成  t_order.is_wholesale=2  [2024.5.30批发商订单也分成]
        #if t_order.invited_uid is not None and t_order.invited_uid > 0 and t_order.is_wholesale != 2:
        is_invited_fee = False
        if t_order.invited_uid is not None and t_order.invited_uid > 0:
            parent_info = d_account.get_account_info_add(t_order.invited_uid)
            this_recommender_fee = 0
            if t_order.zdyspec:
                try:
                    this_recommender_fee = float(json.loads(t_order.zdyspec)['直推']) * 100
                except:
                    pass

            if parent_info and this_recommender_fee > 0:
                invited_income = this_recommender_fee * t_order.number
                total_balance = parent_info.balance + invited_income
                d_account.update_account_by_id(parent_info.id, {"balance": total_balance})
                d_account.add_lock_balance(m_account.LockBalanceModel(
                    user_id=parent_info.user_id,
                    change=invited_income,
                    lock_balance=total_balance,
                    type=global_define.balance_type[1],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    description=str(t_good.id),
                    out_trade_no=t_order.out_trade_no
                ))
            is_invited_fee = True

        #更新订单收益分配状态
        now_time = datetime.datetime.now()
        d_order.assign_income_order(TOrder(
            id=t_order.id,
            complete_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            is_assign_income=1,
            detail=f"[{now_time}#持有：{user_income_l}#层：{parent_income}#点：{top_income}#推：{invited_income}#推2：{invited_income2}#享：{recommender_income}]"
        ))
        # 更新系统用户级别
        # if t_user.level_id == 0:
        #     d_user.update_sysuser_active(t_user.id)
        # elif t_user.level_id == 1:
        #     d_user.update_sysuser_high(t_user.id)
        # elif t_user.level_id == 2:
        #     d_user.update_sysuser_top(t_user.id)
        db.commit()


def share_mall_fee_with_shopbag(order_id: int):
    """share mall fee with other"""
    now_time = datetime.datetime.now()
    with Dao() as db:
        # 查询数据
        t_order, t_user, t_good = db.query(TOrder, TUser, TBigorderInitbag)\
            .outerjoin(TUser, TUser.id==TOrder.paider_id)\
            .outerjoin(TBigorderInitbag, TOrder.good_id==TBigorderInitbag.id)\
            .filter(TOrder.id == order_id).first()
        if t_order is None:
            raise HTTPException(400, "订单不存在")
        if t_user is None:
            raise HTTPException(400, "用户不存在")
        # if t_spec is None:
        #     raise HTTPException(400, "商品不存在")
        # if t_order.is_assign_income:
        #     raise HTTPException(400, "已经分配过收益")
        paider_total = t_order.paid_amount + t_order.paid_coin + t_order.paid_balance + t_order.paid_lock_balance
        if paider_total < t_order.sale_price:
            logging.info(f"{now_time}支付回调失败，支付金额错误,order_id:{order_id},userid:{t_user.id}")
            raise HTTPException(400, "支付金额错误")
        t_order: TOrder   # 走批发价商品 t_order.is_wholesale=2
        t_user: TUser    # 批发商身份 t_user.wholesale_id=100
        # t_spec: TGoodSpec
        #t_source: TOrderSource
        t_good: TBigorderInitbag

        #更新秒杀包持有人订单收益记录
        user_income_l = []
        groupsir_income_l = []
        parent_income = 0
        invited_income = 0
        invited_income2 = 0
        top_income = 0
        recommender_income = 0
        supplier_income = 0
        eqlevel_income = 0
        this_random_fee = 0
        this_tuan_fee = 0
        this_retuan_fee = 0
        this_xyun_fee = 0
        this_shengdai_fee = 0

        #使用积分支付的商品不参与分成
        # if t_order.paid_coin > 0:

        # 直推级奖 批发商订单不分成  t_order.is_wholesale=2  [2024.5.30批发商订单也分成]
        #if t_order.invited_uid is not None and t_order.invited_uid > 0 and t_order.is_wholesale != 2:
        is_invited_fee = False
        if t_order.invited_uid is not None and t_order.invited_uid > 0:
            parent_info = d_account.get_account_info_add(t_order.invited_uid)
            this_recommender_fee = t_good.invited_money

            if parent_info and this_recommender_fee > 0:
                invited_income = this_recommender_fee * t_order.number
                total_balance = parent_info.lock_balance + invited_income
                d_account.update_account_by_id(parent_info.id, {"lock_balance": total_balance})
                d_account.add_lock_balance(m_account.LockBalanceModel(
                    user_id=parent_info.user_id,
                    change=invited_income,
                    lock_balance=total_balance,
                    type=global_define.balance_type[1],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    description=str(t_good.id),
                    out_trade_no=t_order.out_trade_no
                ))
            is_invited_fee = True
        logging.info(f"{now_time}支付回调成功,order_id:{order_id},userid:{t_user.id}")
        #赠予优惠券
        d_account.add_grant_num(t_user.id, t_good.grant_num, t_good.id, 1, t_order.out_trade_no)

        # 加入大公排排序
        # d_bigorder.add_bigorder(t_user.id)

        #公排向上分润
        # d_bigorder.rebuy_distribute(t_user.id, t_good.layer_num, t_good.layer_every, t_good.id, t_order.out_trade_no)

        #归集资金池
        d_found.add_fund_pond(t_order.good_id)

        #更新订单收益分配状态
        d_order.assign_income_order(TOrder(
            id=t_order.id,
            complete_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            is_assign_income=1,
            detail=f"[{now_time}#持有：{user_income_l}#层：{parent_income}#点：{top_income}#推：{invited_income}#推2：{invited_income2}#享：{recommender_income}]"
        ))
        # 更新系统用户级别
        # if t_user.level_id == 0:
        #     d_user.update_sysuser_active(t_user.id)
        # elif t_user.level_id == 1:
        #     d_user.update_sysuser_high(t_user.id)
        # elif t_user.level_id == 2:
        #     d_user.update_sysuser_top(t_user.id)
        db.commit()



#批发商订单，购买及时分成，但不结单
def share_mall_fee_with_this(order_id: int):
    """share mall fee with other"""
    with Dao() as db:
        # 查询数据
        t_order, t_user, t_spec, t_good = db.query(TOrder, TUser, TGoodSpec, TGood)\
            .outerjoin(TUser, TUser.id==TOrder.paider_id)\
            .outerjoin(TGoodSpec, TGoodSpec.id==TOrder.spec_id)\
            .outerjoin(TGood, TOrder.good_id==TGood.id)\
            .filter(TOrder.id == order_id).first()
        if t_order is None:
            raise HTTPException(400, "订单不存在")
        if t_user is None:
            raise HTTPException(400, "用户不存在")
        if t_spec is None:
            raise HTTPException(400, "商品不存在")
        if t_order.is_assign_income:
            raise HTTPException(400, "已经分配过收益")
        t_order: TOrder   # 走批发价商品 t_order.is_wholesale=2
        t_user: TUser    # 批发商身份 t_user.wholesale_id=100
        t_spec: TGoodSpec
        #t_source: TOrderSource
        t_good: TGood

        #更新秒杀包持有人订单收益记录
        user_income_l = []
        groupsir_income_l = []
        parent_income = 0
        invited_income = 0
        invited_income2 = 0
        top_income = 0
        recommender_income = 0
        supplier_income = 0
        eqlevel_income = 0
        this_tuan_fee = 0
        this_retuan_fee = 0
        t_source_list = d_order.get_order_source(t_order.id)
        # 使用积分的订单，视为批发商品订单，不分成
        if t_order.paid_coin > 0:
            t_order.is_wholesale = 2
        for t_source in t_source_list:
            if t_source.source_id is not None:
                get_res = d_package.get_order_package_forid(t_source.source_id)
                if get_res is not None:
                    t_flash_order, t_package = get_res
                    #user_income = t_spec.price * t_source.amount - t_package.flash_sale_price * t_source.amount - t_package.devide_cost * t_source.amount
                    if t_package.devide_cost is None:
                        user_income = 0
                    else:
                        user_income = t_package.devide_cost * t_source.amount
                    # 更新收益
                    account_info = d_account.get_account_info_add(t_flash_order.user_id)
                    total_balance = account_info.balance + user_income
                    d_account.update_account_by_id(account_info.id, {"balance": total_balance})
                    # 更新持有人收益记录
                    #tgood = d_good(t_package.good_id)
                    d_account.add_balance(m_account.BalanceModel(
                        user_id=t_flash_order.user_id,
                        change=user_income,
                        balance=total_balance,
                        type=global_define.balance_type[10],
                        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        good_id=str(t_good.id),
                        good_title=t_good.title,
                        good_num=str(t_source.amount),
                        out_trade_no=t_order.out_trade_no
                    ))
                    user_income_l.append({"uid":t_flash_order.user_id,"ch":user_income})

                    #团长收益  批发商订单不分成  t_order.is_wholesale=2
                    groupsir_user_info = d_groupsir.get_member_for_user(t_flash_order.user_id)
                    if groupsir_user_info and t_order.is_wholesale != 2:
                        groupsir_income = t_spec.price * t_source.amount * d_settings.get_settings().tuan_order_income / 1000
                        groupsir_account_info = d_account.get_account_info_add(groupsir_user_info.user_id)
                        total_balance = groupsir_account_info.balance + groupsir_income
                        d_account.update_account_by_id(groupsir_account_info.id, {"balance": total_balance})
                        d_account.add_balance(m_account.BalanceModel(
                            user_id=groupsir_user_info.user_id,
                            change=groupsir_income,
                            balance=total_balance,
                            type=global_define.balance_type[4],
                            create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                            good_id=str(t_good.id),
                            good_title=t_good.title,
                            good_num=str(t_source.amount),
                            out_trade_no=t_order.out_trade_no
                        ))
                        groupsir_income_l.append({"uid":groupsir_user_info.user_id,"ch":groupsir_income})

        # 层级奖
        # parent_id: Optional[int] = None
        # balance_type = global_define.balance_type[1]
        # is_invited = False
        # if t_user.parent_id is not None:
        #     parent_id = t_user.parent_id
        # elif t_user.invited_user_id is not None:
        #     parent_id = t_user.invited_user_id
        #     balance_type = global_define.balance_type[14]
        #     is_invited = True
        #批发商订单不分成  t_order.is_wholesale=2
        if t_order.parent_uid is not None and t_order.parent_uid > 0 and t_order.is_wholesale != 2:
            parent_info = d_account.get_account_info_add(t_order.parent_uid)
            this_parent_fee = 0
            if t_order.zdyspec:
                try:
                    this_parent_fee = float(json.loads(t_order.zdyspec)['层级']) * 100
                except:
                    this_parent_fee = 0
            else:
                this_parent_fee = t_spec.parent_fee
            if parent_info and this_parent_fee > 0:
                parent_income = this_parent_fee * t_order.number
                total_balance = parent_info.balance + parent_income
                d_account.update_account_by_id(parent_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=parent_info.user_id,
                    change=parent_income,
                    balance=total_balance,
                    type=global_define.balance_type[1],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(t_good.id),
                    good_title=t_good.title,
                    good_num=str(t_order.number),
                    out_trade_no=t_order.out_trade_no
                ))

        # 直推级奖 批发商订单不分成  t_order.is_wholesale=2  [2024.5.30批发商订单也分成]
        #if t_order.invited_uid is not None and t_order.invited_uid > 0 and t_order.is_wholesale != 2:
        is_invited_fee = False
        if t_order.invited_uid is not None and t_order.invited_uid > 0:
            parent_info = d_account.get_account_info_add(t_order.invited_uid)
            this_recommender_fee = 0
            if t_order.zdyspec:
                this_recommender_fee = float(json.loads(t_order.zdyspec)['直推']) * 100
            else:
                this_recommender_fee = t_spec.recommender_fee
            if parent_info and this_recommender_fee > 0:
                invited_income = this_recommender_fee * t_order.number
                total_balance = parent_info.balance + invited_income
                d_account.update_account_by_id(parent_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=parent_info.user_id,
                    change=invited_income,
                    balance=total_balance,
                    type=global_define.balance_type[14],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(t_good.id),
                    good_title=t_good.title,
                    good_num=str(t_order.number),
                    out_trade_no=t_order.out_trade_no
                ))
            is_invited_fee = True

        # 直推分享收益  特别推荐奖，批发价也分成   [2024.5.30批发商订单也分成]
        if t_order.invited_uid is not None and t_order.invited_uid > 0 and not is_invited_fee:
            parent_info = d_account.get_account_info_add(t_order.invited_uid)
            this_recommender2_fee = 0
            if t_order.zdyspec:
                this_recommender2_fee = float(json.loads(t_order.zdyspec)['直推']) * 100
            else:
                this_recommender2_fee = t_spec.recommender2_fee
            if parent_info and this_recommender2_fee > 0:
                invited_income2 = this_recommender2_fee * t_order.number
                total_balance = parent_info.balance + invited_income2
                d_account.update_account_by_id(parent_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=parent_info.user_id,
                    change=invited_income2,
                    balance=total_balance,
                    type=global_define.balance_type[30],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(t_good.id),
                    good_title=t_good.title,
                    good_num=str(t_order.number),
                    out_trade_no=t_order.out_trade_no
                ))

        # 见点奖 批发商订单不分成  t_order.is_wholesale=2
        # top_user_id = d_user.get_top_id(t_user.id)
        # if top_user_id == t_user.id or top_user_id == 0:
        #     top_user_info = None
        # else:
        #     top_user_info = d_account.get_account_info_add(top_user_id)

        this_top_fee = 0
        if t_order.zdyspec:
            try:
                this_top_fee = float(json.loads(t_order.zdyspec)['老板']) * 100
            except:
                this_top_fee = 0
        else:
            this_top_fee = t_spec.top_fee
        # if t_order.top_uid is not None and t_order.top_uid > 0 and this_top_fee > 0 and t_order.is_wholesale != 2:
        if t_order.top_uid is not None and t_order.top_uid > 0 and this_top_fee > 0:
            top_user_info_data = d_user.get_user_by_id(t_order.top_uid)
            top_user_info = d_account.get_account_info_add(t_order.top_uid)
            if top_user_info_data:
                top_income = this_top_fee * t_order.number
                total_balance = top_user_info.balance + top_income
                d_account.update_account_by_id(top_user_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=t_order.top_uid,
                    change=top_income,
                    balance=total_balance,
                    type=global_define.balance_type[2],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(t_good.id),
                    good_title=t_good.title,
                    good_num=str(t_order.number),
                    out_trade_no=t_order.out_trade_no
                ))

        # 平级奖 批发商订单不分成  t_order.is_wholesale=2
        this_eqlevel_fee = 0
        if t_order.zdyspec:
            try:
                this_eqlevel_fee = float(json.loads(t_order.zdyspec)['平级']) * 100
            except:
                this_eqlevel_fee = 0
        else:
            this_eqlevel_fee = t_spec.eqlevel_fee
        # if t_order.eqlevel_uid is not None and t_order.eqlevel_uid > 0 and this_eqlevel_fee > 0 and t_order.is_wholesale != 2:
        if t_order.eqlevel_uid is not None and t_order.eqlevel_uid > 0 and this_eqlevel_fee > 0:
            eqlevel_user_info_data = d_user.get_user_by_id(t_order.eqlevel_uid)
            eqlevel_user_info_account = d_account.get_account_info_add(t_order.eqlevel_uid)
            if eqlevel_user_info_data:
                eqlevel_income = this_eqlevel_fee * t_order.number
                total_balance = eqlevel_user_info_account.balance + eqlevel_income
                d_account.update_account_by_id(eqlevel_user_info_account.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=t_order.eqlevel_uid,
                    change=eqlevel_income,
                    balance=total_balance,
                    type=global_define.balance_type[22],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(t_good.id),
                    good_title=t_good.title,
                    good_num=str(t_order.number),
                    out_trade_no=t_order.out_trade_no
                ))

        # 商品分享奖励  批发商订单不分成  t_order.is_wholesale=2
        if t_order.recommender_id is not None and t_order.is_wholesale != 2:
            if t_order.recommender_id and t_order.recommender_id > 0:
                recommender_info = d_account.get_account_info_add(t_order.recommender_id)
            else:
                recommender_info = None
            if recommender_info and t_spec.share_fee and t_spec.share_fee > 0:
                recommender_income = t_spec.share_fee * t_order.number
                total_balance = recommender_info.balance + recommender_income
                d_account.update_account_by_id(recommender_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=recommender_info.user_id,
                    change=recommender_income,
                    balance=total_balance,
                    type=global_define.balance_type[3],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(t_good.id),
                    good_title=t_good.title,
                    good_num=str(t_order.number),
                    out_trade_no=t_order.out_trade_no
                ))

        #供货收益 介绍人的收益  批发商订单不分成  t_order.is_wholesale=2
        if t_order.supplier_uid is not None and t_order.supplier_uid > 0 and t_spec.supplier_fee > 0 and t_order.is_wholesale != 2:
            supplier_info = d_account.get_account_info_add(t_order.supplier_uid)
            if supplier_info:
                supplier_income = t_spec.supplier_fee * t_order.number
                if supplier_info.balance is None:
                    supplier_info.balance = 0
                total_balance = supplier_info.balance + supplier_income
                d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=t_order.supplier_uid,
                    change=supplier_income,
                    balance=total_balance,
                    type=global_define.balance_type[15],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(t_good.id),
                    good_title=t_good.title,
                    good_num=str(t_order.number),
                    out_trade_no=t_order.out_trade_no
                ))

        #批发商随机分配收益
        this_random_fee = 0
        this_xyun_fee = 0
        if t_order.zdyspec:
            this_random_fee = float(json.loads(t_order.zdyspec)['随机分']) * 100
        else:
            this_random_fee = t_spec.random_fee
        if t_order.random_fee_uid is not None and t_order.random_fee_uid > 0 and this_random_fee > 0:
            supplier_info = d_account.get_account_info_add(t_order.random_fee_uid)
            if supplier_info:
                supplier_income = this_random_fee * t_order.number
                if supplier_info.balance is None:
                    supplier_info.balance = 0
                total_balance = supplier_info.balance + supplier_income
                d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=t_order.random_fee_uid,
                    change=supplier_income,
                    balance=total_balance,
                    type=global_define.balance_type[32],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(t_good.id),
                    good_title=t_good.title,
                    good_num=str(t_order.number),
                    out_trade_no=t_order.out_trade_no
                ))
                # 幸运奖, 给推荐人同样一笔奖励
                random_uinfo = d_user.get_user_by_id(t_order.random_invited_uid)
                #invitid = random_uinfo.invited_user_id if random_uinfo.invited_user_id is not None else 0
                if random_uinfo:
                    this_xyun_fee = supplier_income
                    invite_account = d_account.get_account_info_add(t_order.random_invited_uid)
                    total_balance = invite_account.balance + supplier_income
                    d_account.update_account_by_id(t_order.random_invited_uid, {"balance": total_balance})
                    d_account.add_balance(m_account.BalanceModel(
                        user_id=t_order.random_invited_uid,
                        change=supplier_income,
                        balance=total_balance,
                        type=global_define.balance_type[36],
                        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        good_id=str(t_good.id),
                        good_title=t_good.title,
                        good_num=str(t_order.number),
                        out_trade_no=t_order.out_trade_no
                    ))

        # 间推分配收益
        this_jiantui_fee = 0
        if t_order.zdyspec:
            this_jiantui_fee = float(json.loads(t_order.zdyspec)['间推']) * 100
        if t_order.ininvited_uid is not None and t_order.ininvited_uid > 0 and this_jiantui_fee > 0:
            supplier_info = d_account.get_account_info_add(t_order.ininvited_uid)
            if supplier_info:
                supplier_income = this_jiantui_fee * t_order.number
                if supplier_info.balance is None:
                    supplier_info.balance = 0
                total_balance = supplier_info.balance + supplier_income
                d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=t_order.ininvited_uid,
                    change=supplier_income,
                    balance=total_balance,
                    type=global_define.balance_type[35],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(t_good.id),
                    good_title=t_good.title,
                    good_num=str(t_order.number),
                    out_trade_no=t_order.out_trade_no
                ))

        # 团长分配收益
        this_tuan_fee = 0
        if t_order.zdyspec:
            try:
                this_tuan_fee = float(json.loads(t_order.zdyspec)['团长']) * 100
            except:
                this_tuan_fee = 0
        else:
            this_tuan_fee = t_spec.tuan_fee
        if t_order.tuan_uid is not None and t_order.tuan_uid > 0 and this_tuan_fee > 0:
            supplier_info = d_account.get_account_info_add(t_order.tuan_uid)
            if supplier_info:
                supplier_income = this_tuan_fee * t_order.number
                if supplier_info.balance is None:
                    supplier_info.balance = 0
                total_balance = supplier_info.balance + supplier_income
                d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=t_order.tuan_uid,
                    change=supplier_income,
                    balance=total_balance,
                    type=global_define.balance_type[33],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(t_good.id),
                    good_title=t_good.title,
                    good_num=str(t_order.number),
                    out_trade_no=t_order.out_trade_no
                ))

        # 上级分配收益
        this_retuan_fee = 0
        if t_order.zdyspec:
            try:
                this_retuan_fee = float(json.loads(t_order.zdyspec)['上级团']) * 100
            except:
                this_retuan_fee = 0
        else:
            this_retuan_fee = t_spec.retuan_fee
        if t_order.retuan_uid is not None and t_order.retuan_uid > 0 and this_retuan_fee > 0:
            supplier_info = d_account.get_account_info_add(t_order.retuan_uid)
            if supplier_info:
                supplier_income = this_retuan_fee * t_order.number
                if supplier_info.balance is None:
                    supplier_info.balance = 0
                total_balance = supplier_info.balance + supplier_income
                d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=t_order.retuan_uid,
                    change=supplier_income,
                    balance=total_balance,
                    type=global_define.balance_type[34],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(t_good.id),
                    good_title=t_good.title,
                    good_num=str(t_order.number),
                    out_trade_no=t_order.out_trade_no
                ))

        # 省代收益
        this_shengdai_fee = 0
        if t_order.zdyspec:
            try:
                this_shengdai_fee = float(json.loads(t_order.zdyspec)['省代']) * 100
            except:
                this_shengdai_fee = 0
        if t_order.shengdai_uid is not None and t_order.shengdai_uid > 0 and this_shengdai_fee > 0:
            supplier_info = d_account.get_account_info_add(t_order.shengdai_uid)
            if supplier_info:
                supplier_income = this_shengdai_fee * t_order.number
                if supplier_info.balance is None:
                    supplier_info.balance = 0
                total_balance = supplier_info.balance + supplier_income
                d_account.update_account_by_id(supplier_info.id, {"balance": total_balance})
                d_account.add_balance(m_account.BalanceModel(
                    user_id=t_order.shengdai_uid,
                    change=supplier_income,
                    balance=total_balance,
                    type=global_define.balance_type[37],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id=str(t_good.id),
                    good_title=t_good.title,
                    good_num=str(t_order.number),
                    out_trade_no=t_order.out_trade_no
                ))

        #供货商收回成本
        # if t_spec.supplier_fee is not None and t_good.supplier_id is not None:
        #     supplier_info = d_supplier_account.get_account_info(t_good.supplier_id)
        #     if supplier_info:
        #         supplier_income = t_spec.supplier_fee * t_order.number
        #         if supplier_info.amount is None:
        #             supplier_info.amount = 0
        #         total_balance = supplier_info.amount + supplier_income
        #         d_supplier_account.update_account_by_id(supplier_info.id, {"change": supplier_income,"amount": total_balance})
        #         d_supplier_income.add_income(TSupplierIncome(
        #             supplier_id=t_good.supplier_id,
        #             change=supplier_income,
        #             balance=total_balance,
        #             type=global_define.balance_type[8],
        #             create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #             operator_id=10000
        #             # good_id=str(t_good.id),
        #             # good_title=t_good.title,
        #             # good_num=str(t_order.number)
        #         ))

        #更新订单收益分配状态
        now_time = datetime.datetime.now()
        d_order.assign_income_pifaorder(TOrder(
            id=t_order.id,
            complete_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            is_assign_income=1,
            detail=f"[{now_time}#持有：{user_income_l}#层：{parent_income}#点：{top_income}#推：{invited_income}#推2：{invited_income2}#享：{recommender_income}#供：{supplier_income}#团：{groupsir_income_l}#平：{eqlevel_income}#随：{this_random_fee}#团：{this_tuan_fee}#上团：{this_retuan_fee}#间：{this_jiantui_fee}#幸：{this_xyun_fee}#省：{this_shengdai_fee}]"
        ))
        # 更新系统用户级别
        # if t_user.level_id == 0:
        #     d_user.update_sysuser_active(t_user.id)
        # elif t_user.level_id == 1:
        #     d_user.update_sysuser_high(t_user.id)
        # elif t_user.level_id == 2:
        #     d_user.update_sysuser_top(t_user.id)
        db.commit()


def share_package_fee_with_other(flash_order_id: int):
    """share mall fee with other"""
    with Dao() as db:
        t_flash_order, t_package, t_user = db.query(TFlashOrder, TPackage, TUser).outerjoin(TPackage, TPackage.id==TFlashOrder.package_id).outerjoin(TUser, TUser.id == TFlashOrder.user_id).filter(TFlashOrder.id == flash_order_id).first()
        if t_flash_order is None:
            raise HTTPException(400, "订单不存在")
        if t_package is None:
            raise HTTPException(400, "秒杀包不存在")
        if t_user is None:
            raise HTTPException(400, "用户不存在")
        
        t_package: TPackage
        t_user: TUser

        # 层级奖
        share_fee: int  = t_package.share_fee
        while share_fee is not None and share_fee > 0:
            parent_id = t_user.parent_id
            share_fee = share_fee // 2

            if parent_id is None:
                break

            d_user_account.balance_change(
                user_id=parent_id,
                fee=share_fee,
                category='层级奖',
                description='秒杀包奖励',
                db=db
            )
            t_user = db.query(TUser).filter(TUser.id == parent_id).first()

        db.commit()


def share_package_fee_with_other(flash_order_id: int):
    """share mall fee with other"""
    with Dao() as db:
        t_flash_order, t_package, t_user = db.query(TFlashOrder, TPackage, TUser).outerjoin(TPackage,
                                                                                            TPackage.id == TFlashOrder.package_id).outerjoin(
            TUser, TUser.id == TFlashOrder.user_id).filter(TFlashOrder.id == flash_order_id).first()
        if t_flash_order is None:
            raise HTTPException(400, "订单不存在")
        if t_package is None:
            raise HTTPException(400, "秒杀包不存在")
        if t_user is None:
            raise HTTPException(400, "用户不存在")

        t_package: TPackage
        t_user: TUser

        # 层级奖
        share_fee: int = t_package.share_fee
        while share_fee is not None and share_fee > 0:
            parent_id = t_user.parent_id
            share_fee = share_fee // 2

            if parent_id is None:
                break

            d_user_account.balance_change(
                user_id=parent_id,
                fee=share_fee,
                category='层级奖',
                description='秒杀包奖励',
                db=db
            )
            t_user = db.query(TUser).filter(TUser.id == parent_id).first()

        db.commit()


#批发商订单，购买及时分成，但不结单
def share_mall_fee_with_partner(orders: list):
    """share mall fee with partner"""
    logging.info('start to share_mall_fee_with_partner')
    for t_order in orders:
        zdyspec_str = t_order.zdyspec
        # logging.info(zdyspec_str)
        try:
            zdyspec = json.loads(zdyspec_str)
            this_top_fee = float(zdyspec['金池']) * 100

        except:
            this_top_fee = 0
        this_top_fee = this_top_fee * t_order.number
        logging.info(f"order:{t_order.id},this_top_fee:{this_top_fee}")
        if this_top_fee > 0:
            d_partner.add_fund(global_function.get_current_zhouqi(), t_order.good_id, t_order.id, this_top_fee)