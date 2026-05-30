from common import Dao, global_define
from model.schema import TBigorderSet, TBigorderTwo, TUser
from sqlalchemy import or_, and_, func
from typing import List, Optional
from sqlalchemy import text
import datetime, time, sys, math, json, redis
from pydantic import BaseModel, Field
from fastapi.exceptions import HTTPException
from dao import d_user, d_db, d_account
from model.mall import m_account
import logging


RR = redis.Redis(host=global_define.REDIS_HOST, port=global_define.REDIS_PORT, decode_responses=True)

class SearchBalance(BaseModel):
    user_id: Optional[int] = Field(None,title='关联t_user表id')
    type: Optional[str] = Field(None,title='资金类型：1:层级收益,2:见点收益,3:推荐收益,4:团长收益,5:管理变动收益')
    description: Optional[str] = Field(None,title='资金备注，团长收益这里是逗号分隔的订单id')
    create_time: Optional[str] = Field(None,title='时间段：time1,time2')
    is_comein: Optional[int] = Field(None, title='收入(1)/支出(0)')
    # admin_id: Optional[int] = Field(None, title='商家管理id')
    page: int = Field(1, title='当前页码，默认第1页')
    page_size: int = Field(20, title='返回每页数据，默认每页20条数据')

#获取复购排序右侧id，并从列表删除
def get_rpop_layerlist():
    #返回值样式：'1'
    return RR.rpop(global_define.REDIS_LAYER_LIST)

#从左侧插入会员id
def set_lpush_layerlist(userid: int):
    if userid > 0:
        RR.lpush(global_define.REDIS_LAYER_LIST, userid)

#获取复购排队所有列表
def get_lrange_layer_list():
    #返回值样式：['3', '2', '1']
    return RR.lrange(global_define.REDIS_LAYER_LIST, 0, -1)

#某个用户执行复购逻辑
def run_double_buy(user_Id: int):
    # get_id = get_rpop_layerlist()
    if user_Id > 0:
        pass
    else:
        pass

#初次购买礼包把用户加入公排
def add_bigorder(user_id: int = 0):
    uinfo = d_user.get_user_by_id(user_id)
    #bigorder_id < 1 确定用户没有公排序列
    if uinfo and uinfo.bigorder_id < 1:
        max_uinfo = get_bigorder_maxid_uinfo(uinfo.tuan_id)
        if max_uinfo:
            #此tuan_id下有了公排排序
            bigorder_two_id = max_uinfo.bigorder_id + 1
            update_user_orders(user_id, bigorder_two_id)
        else:
            #此tuan_id下第一个公排排序
            update_user_orders(user_id, 1)
    else:
        pass

#过期用户完成任务加入公排
def add_bigorder_express(user_id: int = 0):
    uinfo = d_user.get_user_by_id(user_id)
    #bigorder_id < 1 确定用户没有公排序列
    if uinfo and uinfo.entrust_status == 0:
        max_uinfo = get_bigorder_maxid_uinfo(uinfo.tuan_id)
        if max_uinfo:
            #此tuan_id下有了公排排序
            bigorder_two_id = max_uinfo.bigorder_id + 1
            update_user_orders(user_id, bigorder_two_id)
        else:
            #此tuan_id下第一个公排排序
            update_user_orders(user_id, 1)
    else:
        pass

#获取系统或某团之下已经存在的最大公排Id
def get_bigorder_maxid_uinfo(sir_id:int = 0):
    with Dao() as db:
        return db.query(TUser).where(TUser.tuan_id == sir_id).order_by(TUser.bigorder_id.desc()).first()

def get_bigorder_set(key_name:str):
    with Dao() as db:
        return db.query(TBigorderSet).filter(TBigorderSet.set_name == key_name).first()

#更新用户公排数据，并开启临时托管
def update_user_orders(userid:int, bigorder_id:int, is_never:int = 0):
    '''
      `bigorder_id` int DEFAULT '0' COMMENT '公排id',
      `layer_id` int DEFAULT '0' COMMENT '行号(所在层数)',
      `cur_layer_id` int DEFAULT '0' COMMENT '当前行号从左到右排序号',
      `cur_layer_total` int DEFAULT '0' COMMENT '当前行排序总数量',
      `bigorder_parent_id` int DEFAULT '0' COMMENT '上级对应序号',
      is_never 是否永久加入公排
    '''
    # bigorder_two_next = d_db.get_bigorder_two(bigorder_id)
    never_stat = 1
    if is_never > 0:
        never_stat = 2
    uinfo = d_user.get_user_by_id(userid)
    if uinfo:
        update_data = dict()
        with Dao() as db:
            bigorder_two_next = db.query(TBigorderTwo).where(TBigorderTwo.order_id == bigorder_id).first()
            if uinfo.bigorder_id > 0:
                update_data['entrust_status'] = never_stat
                update_data['entrust_endtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            else:
                update_data['bigorder_id'] = bigorder_two_next.order_id
                update_data['layer_id'] = bigorder_two_next.layer_id
                update_data['cur_layer_id'] = bigorder_two_next.cur_layer_id
                update_data['cur_layer_total'] = bigorder_two_next.cur_layer_total
                update_data['bigorder_parent_id'] = bigorder_two_next.parent_id
                update_data['entrust_status'] = never_stat
                update_data['entrust_startime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            db.query(TUser).where(TUser.id == userid).update(update_data)
            db.commit()

def update_user_neworder(userid:int, bigorder_id:int, never_stat:int = 1):
    '''
      `bigorder_id` int DEFAULT '0' COMMENT '公排id',
      `layer_id` int DEFAULT '0' COMMENT '行号(所在层数)',
      `cur_layer_id` int DEFAULT '0' COMMENT '当前行号从左到右排序号',
      `cur_layer_total` int DEFAULT '0' COMMENT '当前行排序总数量',
      `bigorder_parent_id` int DEFAULT '0' COMMENT '上级对应序号',
      is_never 是否永久加入公排
    '''
    # bigorder_two_next = d_db.get_bigorder_two(bigorder_id)
    uinfo = d_user.get_user_by_id(userid)
    if uinfo:
        update_data = dict()
        with Dao() as db:
            bigorder_two_next = db.query(TBigorderTwo).where(TBigorderTwo.order_id == bigorder_id).first()
            update_data['bigorder_id'] = bigorder_two_next.order_id
            update_data['layer_id'] = bigorder_two_next.layer_id
            update_data['cur_layer_id'] = bigorder_two_next.cur_layer_id
            update_data['cur_layer_total'] = bigorder_two_next.cur_layer_total
            update_data['bigorder_parent_id'] = bigorder_two_next.parent_id
            update_data['entrust_status'] = never_stat
            # update_data['entrust_startime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            db.query(TUser).where(TUser.id == userid).update(update_data)
            db.commit()

def clear_user_order(userid:int):
    '''
      `bigorder_id` int DEFAULT '0' COMMENT '公排id',
      `layer_id` int DEFAULT '0' COMMENT '行号(所在层数)',
      `cur_layer_id` int DEFAULT '0' COMMENT '当前行号从左到右排序号',
      `cur_layer_total` int DEFAULT '0' COMMENT '当前行排序总数量',
      `bigorder_parent_id` int DEFAULT '0' COMMENT '上级对应序号',
      is_never 是否永久加入公排
    '''
    # bigorder_two_next = d_db.get_bigorder_two(bigorder_id)
    uinfo = d_user.get_user_by_id(userid)
    if uinfo:
        update_data = dict()
        with Dao() as db:
            update_data['bigorder_id'] = 0
            update_data['layer_id'] = 0
            update_data['cur_layer_id'] = 0
            update_data['cur_layer_total'] = 0
            update_data['bigorder_parent_id'] = 0
            update_data['entrust_status'] = 0
            update_data['light_status'] = 0

            # update_data['entrust_startime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            db.query(TUser).where(TUser.id == userid).update(update_data)
            db.commit()

#更新用户为永久托管
def update_user_orders_never(userid:int):
    with Dao() as db:
        db.query(TUser).where(TUser.id == userid).update({"entrust_status": 2,"entrust_endtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
        db.commit()

#更新用户为取消托管
def update_user_orders_end(userid:int):
    with Dao() as db:
        db.query(TUser).where(TUser.id == userid).update({"entrust_status": 0,"light_status": 1,"entrust_endtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
        db.commit()

#创建用户分身
def create_user_double(user_id: int):
    if user_id > 0:
        pass
    else:
        pass

def rebuy_distribute_one(bigorder_parent_id:int = 0, every_money:int = 0, good_id:int = 0, good_title:str = '', out_trade_no:str = ''):
    uinfo_b = d_user.get_user_by_bigorder_id(bigorder_parent_id)
    double_money_ls = get_bigorder_set('double_money')  # 复投金额
    double_count_ls = get_bigorder_set('double_count')  # 复投上限
    default_user = 1642
    re_up_bigorder_id = 0
    if uinfo_b:
        logging.info(f"rebuy_distribute_one，分润给用户：{uinfo_b.id}")
        print(f"rebuy_distribute_one，分润给用户：{uinfo_b.id}")
        user_account = d_account.get_account_info_add(uinfo_b.id)  # 用户账户
        if user_account:
            logging.info(f"rebuy_distribute_one，用户资金：{user_account.id}")
            print(f"rebuy_distribute_one，用户资金：{user_account.id}")
            total_balance = user_account.balance + every_money
            d_account.update_account_balance(uinfo_b.id, total_balance)
            logging.info(f"rebuy_distribute_one，大公排分润：{every_money},总额：{total_balance}")
            print(f"rebuy_distribute_one，大公排分润：{every_money},总额：{total_balance}")
            user_banalce_out = m_account.BalanceModel(
                user_id=uinfo_b.id,
                change=+every_money,
                balance=total_balance,
                type=global_define.balance_type[9],
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                good_id=str(good_id),
                good_title=good_title,
                good_num='',
                out_trade_no=out_trade_no
            )
            d_account.add_balance(user_banalce_out)
            # 达到复投金额，加入复投任务
            logging.info(f"rebuy_distribute_one，复投条件double_money_ls.val_int：{double_money_ls.val_int},double_count_ls.val_int：{double_count_ls.val_int}")
            print(f"rebuy_distribute_one，复投条件double_money_ls.val_int：{double_money_ls.val_int},double_count_ls.val_int：{double_count_ls.val_int}")
            if total_balance >= double_money_ls.val_int and uinfo_b.pai_buydui <= double_count_ls.val_int and uinfo_b.entrust_status > 0:
                set_lpush_layerlist(uinfo_b.id)
            #更新上一级公排id
            re_up_bigorder_id = uinfo_b.bigorder_parent_id
            logging.info(f"rebuy_distribute_one，返回上级公排序号：{re_up_bigorder_id}")
            print(f"rebuy_distribute_one，返回上级公排序号：{re_up_bigorder_id}")
    else:
        logging.info(f"rebuy_distribute_one，分润给系统用户：{default_user}")
        print(f"rebuy_distribute_one，分润给系统用户：{default_user}")
        defult_user_account = d_account.get_account_info(default_user)  # 系统账户
        total_balance = defult_user_account.balance + every_money
        d_account.update_account_balance(default_user, total_balance)
        user_banalce_out = m_account.BalanceModel(
            user_id=default_user,
            change=+every_money,
            balance=total_balance,
            type=global_define.balance_type[9],
            create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            good_id=str(good_id),
            good_title=good_title,
            good_num='',
            out_trade_no=out_trade_no
        )
        d_account.add_balance(user_banalce_out)
    return re_up_bigorder_id


#购买礼品公排复购向上层分润
def rebuy_distribute(user_id: int, up_layer: int = 0, every_money: int = 0, good_id:int = 0, out_trade_no:str = '', start_layer:int = 1):
    '''
    up_layer:向上分润层数
    every_money: 每层分润金额
    '''
    logging.info(f"start to 大公排分润，user_id:{user_id},up_layer:{up_layer},every_money:{every_money},good_id:{good_id},out_trade_no:{out_trade_no},start_layer:{start_layer}")
    print(f"start to 大公排分润，user_id:{user_id},up_layer:{up_layer},every_money:{every_money},good_id:{good_id},out_trade_no:{out_trade_no},start_layer:{start_layer}")
    uinfo = d_user.get_user_by_id(user_id)
    num_layer = up_layer
    double_count_ls = get_bigorder_set('double_count')  # 复投上限
    if uinfo:
        #排队次数达到上限，停止复购
        if uinfo.pai_buydui <= double_count_ls.val_int:
            #第一层
            parent_id = 0
            logging.info(f"第一层uinfo.bigorder_parent_id:{uinfo.bigorder_parent_id},num_layer:{num_layer}")
            print(f"第一层uinfo.bigorder_parent_id:{uinfo.bigorder_parent_id},num_layer:{num_layer}")
            if num_layer > 0 and uinfo.bigorder_parent_id > 0:
                #开始层数，且委托中用户entrust_status>0
                binfo = d_user.get_user_by_bigorder_id(uinfo.bigorder_parent_id)
                if 1 >= start_layer and binfo.entrust_status > 1:
                    good_title = f"来源{uinfo.id},来源排序{uinfo.bigorder_id}"
                    logging.info(f"第一层，{good_title}")
                    print(f"第一层，{good_title}")
                    parent_id = rebuy_distribute_one(uinfo.bigorder_parent_id, every_money, good_id, good_title, out_trade_no)
                    num_layer -= 1
                else:
                    # this_info = d_user.get_user_by_bigorder_id(uinfo.bigorder_parent_id)
                    parent_id = binfo.bigorder_parent_id

            #第二层---------------------------------------------------------------
            logging.info(f"第二层num_layer:{num_layer},parent_id:{parent_id}")
            print(f"第二层num_layer:{num_layer},parent_id:{parent_id},start_layer:{start_layer}")
            if num_layer > 0 and parent_id > 0:
                # 开始层数，且委托中用户entrust_status>0
                binfo = d_user.get_user_by_bigorder_id(parent_id)
                if 2 >= start_layer and binfo.entrust_status > 1:
                    good_title = f"来源排序{parent_id}"
                    logging.info(f"第二层，{good_title}")
                    print(f"第二层，{good_title}")
                    parent_id = rebuy_distribute_one(parent_id, every_money, good_id, good_title, out_trade_no)
                    num_layer -= 1
                else:
                    # this_info = d_user.get_user_by_bigorder_id(parent_id)
                    parent_id = binfo.bigorder_parent_id

            #第三层---------------------------------------------------------------
            print(f"第三层um_layer:{num_layer},parent_id:{parent_id},start_layer:{start_layer}")
            if num_layer > 0 and parent_id > 0:
                # 开始层数，且委托中用户entrust_status>0
                binfo = d_user.get_user_by_bigorder_id(parent_id)
                if 3 >= start_layer and binfo.entrust_status > 1:
                    good_title = f"来源排序{parent_id}"
                    logging.info(f"第三层，{good_title}")
                    print(f"第三层，{good_title}")
                    parent_id = rebuy_distribute_one(parent_id, every_money, good_id, good_title, out_trade_no)
                    num_layer -= 1
                else:
                    # this_info = d_user.get_user_by_bigorder_id(parent_id)
                    parent_id = binfo.bigorder_parent_id

            #第四层---------------------------------------------------------------
            print(f"第四层um_layer:{num_layer},parent_id:{parent_id},start_layer:{start_layer}")
            if num_layer > 0 and parent_id > 0:
                # 开始层数，且委托中用户entrust_status>0
                binfo = d_user.get_user_by_bigorder_id(parent_id)
                if 4 >= start_layer and binfo.entrust_status > 1:
                    good_title = f"来源排序{parent_id}"
                    logging.info(f"第四层，{good_title}")
                    print(f"第四层，{good_title}")
                    parent_id = rebuy_distribute_one(parent_id, every_money, good_id, good_title, out_trade_no)
                    num_layer -= 1
                else:
                    # this_info = d_user.get_user_by_bigorder_id(parent_id)
                    parent_id = binfo.bigorder_parent_id

            #第五层---------------------------------------------------------------
            print(f"第五层um_layer:{num_layer},parent_id:{parent_id},start_layer:{start_layer}")
            if num_layer > 0 and parent_id > 0:
                # 开始层数，且委托中用户entrust_status>0
                binfo = d_user.get_user_by_bigorder_id(parent_id)
                if  5 >= start_layer and binfo.entrust_status > 1:
                    good_title = f"来源排序{parent_id}"
                    logging.info(f"第五层，{good_title}")
                    print(f"第五层，{good_title}")
                    parent_id = rebuy_distribute_one(parent_id, every_money, good_id, good_title, out_trade_no)
                    num_layer -= 1
                else:
                    # this_info = d_user.get_user_by_bigorder_id(parent_id)
                    parent_id = binfo.bigorder_parent_id

            #第六层---------------------------------------------------------------
            print(f"第六层um_layer:{num_layer},parent_id:{parent_id}")
            if num_layer > 0 and parent_id > 0:
                # 开始层数，且委托中用户entrust_status>0
                binfo = d_user.get_user_by_bigorder_id(parent_id)
                if 6 >= start_layer and binfo.entrust_status > 1:
                    good_title = f"来源排序{parent_id}"
                    logging.info(f"第六层，{good_title}")
                    print(f"第六层，{good_title}")
                    parent_id = rebuy_distribute_one(parent_id, every_money, good_id, good_title, out_trade_no)
                    num_layer -= 1
                else:
                    # this_info = d_user.get_user_by_bigorder_id(parent_id)
                    parent_id = binfo.bigorder_parent_id

            #第七层---------------------------------------------------------------
            print(f"第七层um_layer:{num_layer},parent_id:{parent_id}")
            if num_layer > 0 and parent_id > 0:
                # 开始层数，且委托中用户entrust_status>0
                binfo = d_user.get_user_by_bigorder_id(parent_id)
                if 7 >= start_layer and binfo.entrust_status > 1:
                    good_title = f"来源排序{parent_id}"
                    logging.info(f"第七层，{good_title}")
                    print(f"第七层，{good_title}")
                    parent_id = rebuy_distribute_one(parent_id, every_money, good_id, good_title, out_trade_no)
                    num_layer -= 1
                else:
                    # this_info = d_user.get_user_by_bigorder_id(parent_id)
                    parent_id = binfo.bigorder_parent_id

            #第八层---------------------------------------------------------------
            print(f"第八层um_layer:{num_layer},parent_id:{parent_id}")
            if num_layer > 0 and parent_id > 0:
                # 开始层数，且委托中用户entrust_status>0
                binfo = d_user.get_user_by_bigorder_id(parent_id)
                if 8 >= start_layer and binfo.entrust_status > 1:
                    good_title = f"来源排序{parent_id}"
                    logging.info(f"第八层，{good_title}")
                    print(f"第八层，{good_title}")
                    parent_id = rebuy_distribute_one(parent_id, every_money, good_id, good_title, out_trade_no)
                    num_layer -= 1
                else:
                    # this_info = d_user.get_user_by_bigorder_id(parent_id)
                    parent_id = binfo.bigorder_parent_id

            #第九层---------------------------------------------------------------
            print(f"第九层um_layer:{num_layer},parent_id:{parent_id}")
            if num_layer > 0 and parent_id > 0:
                # 开始层数，且委托中用户entrust_status>0
                binfo = d_user.get_user_by_bigorder_id(parent_id)
                if 9 >= start_layer and binfo.entrust_status > 1:
                    good_title = f"来源排序{parent_id}"
                    logging.info(f"第九层，{good_title}")
                    print(f"第九层，{good_title}")
                    parent_id = rebuy_distribute_one(parent_id, every_money, good_id, good_title, out_trade_no)
                    num_layer -= 1
                else:
                    # this_info = d_user.get_user_by_bigorder_id(parent_id)
                    parent_id = binfo.bigorder_parent_id

            #第十层---------------------------------------------------------------
            print(f"第十层um_layer:{num_layer},parent_id:{parent_id}")
            if num_layer > 0 and parent_id > 0:
                # 开始层数，且委托中用户entrust_status>0
                binfo = d_user.get_user_by_bigorder_id(parent_id)
                if 10 >= start_layer and binfo.entrust_status > 1:
                    good_title = f"来源排序{parent_id}"
                    logging.info(f"第十层，{good_title}")
                    print(f"第十层，{good_title}")
                    parent_id = rebuy_distribute_one(parent_id, every_money, good_id, good_title, out_trade_no)
                    num_layer -= 1
                else:
                    # this_info = d_user.get_user_by_bigorder_id(parent_id)
                    parent_id = binfo.bigorder_parent_id

            #第十一层---------------------------------------------------------------
            print(f"第十一层um_layer:{num_layer},parent_id:{parent_id}")
            if num_layer > 0 and parent_id > 0:
                # 开始层数，且委托中用户entrust_status>0
                binfo = d_user.get_user_by_bigorder_id(parent_id)
                if 11 >= start_layer and binfo.entrust_status > 1:
                    good_title = f"来源排序{parent_id}"
                    logging.info(f"第十一层，{good_title}")
                    print(f"第十一层，{good_title}")
                    parent_id = rebuy_distribute_one(parent_id, every_money, good_id, good_title, out_trade_no)
                    num_layer -= 1
                else:
                    # this_info = d_user.get_user_by_bigorder_id(parent_id)
                    parent_id = binfo.bigorder_parent_id

            #第十二层---------------------------------------------------------------
            print(f"第十二层um_layer:{num_layer},parent_id:{parent_id}")
            if num_layer > 0 and parent_id > 0:
                # 开始层数，且委托中用户entrust_status>0
                binfo = d_user.get_user_by_bigorder_id(parent_id)
                if 12 >= start_layer and binfo.entrust_status > 1:
                    good_title = f"来源排序{parent_id}"
                    logging.info(f"第十二层，{good_title}")
                    print(f"第十二层，{good_title}")
                    parent_id = rebuy_distribute_one(parent_id, every_money, good_id, good_title, out_trade_no)
                    num_layer -= 1
                else:
                    # this_info = d_user.get_user_by_bigorder_id(parent_id)
                    parent_id = binfo.bigorder_parent_id

            #第十三层---------------------------------------------------------------
            print(f"第十三层um_layer:{num_layer},parent_id:{parent_id}")
            if num_layer > 0 and parent_id > 0:
                # 开始层数，且委托中用户entrust_status>0
                binfo = d_user.get_user_by_bigorder_id(parent_id)
                if 13 >= start_layer and binfo.entrust_status > 1:
                    good_title = f"来源排序{parent_id}"
                    logging.info(f"第十三层，{good_title}")
                    print(f"第十三层，{good_title}")
                    parent_id = rebuy_distribute_one(parent_id, every_money, good_id, good_title, out_trade_no)
                    num_layer -= 1
                else:
                    # this_info = d_user.get_user_by_bigorder_id(parent_id)
                    parent_id = binfo.bigorder_parent_id

            #第十四层---------------------------------------------------------------
            print(f"第十四层um_layer:{num_layer},parent_id:{parent_id}")
            if num_layer > 0 and parent_id > 0:
                # 开始层数，且委托中用户entrust_status>0
                binfo = d_user.get_user_by_bigorder_id(parent_id)
                if 14 >= start_layer and binfo.entrust_status > 1:
                    good_title = f"来源排序{parent_id}"
                    logging.info(f"第十四层，{good_title}")
                    print(f"第十四层，{good_title}")
                    parent_id = rebuy_distribute_one(parent_id, every_money, good_id, good_title, out_trade_no)
                    num_layer -= 1
                else:
                    # this_info = d_user.get_user_by_bigorder_id(parent_id)
                    parent_id = binfo.bigorder_parent_id

            #第十五层---------------------------------------------------------------
            print(f"第十五层um_layer:{num_layer},parent_id:{parent_id}")
            if num_layer > 0 and parent_id > 0:
                # 开始层数，且委托中用户entrust_status>0
                binfo = d_user.get_user_by_bigorder_id(parent_id)
                if 15 >= start_layer and binfo.entrust_status > 1:
                    good_title = f"来源排序{parent_id}"
                    logging.info(f"第十五层，{good_title}")
                    print(f"第十五层，{good_title}")
                    parent_id = rebuy_distribute_one(parent_id, every_money, good_id, good_title, out_trade_no)
                    num_layer -= 1
                else:
                    # this_info = d_user.get_user_by_bigorder_id(parent_id)
                    parent_id = binfo.bigorder_parent_id

#更新用户礼包购买数量
def update_bagorder(user_id:int, num:int = 1):
    with Dao() as db:
        db.query(TUser).where(TUser.id == user_id).update({"bagorder_num" : num})
        db.commit()

#获取公排失效用户id列表
def get_fail_user_for_order():
    re_ids = []
    with Dao() as db:
        search_rs = db.query(TUser.id).filter(TUser.entrust_status == 0).filter(TUser.bigorder_id > 0).all()
        for r in search_rs:
            re_ids.append(r["id"])
    return re_ids

#获取公排有效用户id列表
def get_sucess_user_for_order():
    re_ids = []
    with Dao() as db:
        search_rs = db.query(TUser.id).filter(TUser.entrust_status > 0).order_by(TUser.bigorder_id.asc()).all()
        for r in search_rs:
            re_ids.append(r["id"])
    return re_ids

#获取公排
def get_bigordertwo(order_id:int):
    with Dao() as db:
        return db.query(TBigorderTwo).where(TBigorderTwo.order_id == order_id).first()

#------------------------------------------------任务区域-=====================================================================
#到期未完成任务取消托管
def scan_fail_bigorders():
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"start:{start_time}")
    items = dict()
    search_items = dict()
    set_items = dict()
    order_items = dict()
    items['entrust_status'] = 1
    data_count = d_db.filter_count_user(items, search_items, set_items)
    page = 40
    page_count = math.ceil(data_count / 40) + 1
    num = 0
    for i in range(1, page_count):
        data = d_db.filter_user(items, search_items, set_items, order_items, i, page)

        #| 5 | double_tscount   |      10 |         | 拉新人数要求
        #| 6 | double_tstime    |      24 |         | 拉新时间要求(小时)
        double_tscount_ls = get_bigorder_set('double_tscount')
        double_tstime_ls = get_bigorder_set('double_tstime')
        now_time = datetime.datetime.now()
        express_time = now_time - datetime.timedelta(hours=double_tstime_ls.val_int)
        print(f"expree_time:{express_time}")
        for dd in data:
            print(f"处理开始:{dd.id}")
            # new_count = d_user.get_lower_user_count(dd.id)
            new_count = d_user.get_bagorder_user_count(dd.id)
            #拉新人数大于系统要求人数
            if new_count >= double_tscount_ls.val_int:
                print(f"永久托管")
                update_user_orders_never(dd.id)
            else:  #少于人数，取消托管
                # 如果开始时间晚于结束时间，执行结束托管
                if express_time >= dd.entrust_startime:
                    print(f"取消托管")
                    update_user_orders_end(dd.id)
            print(f"处理结束:{dd.id}")
            num = num + 1
            time.sleep(0.1)
        print(f"分页,第：{i}业")
        time.sleep(0.1)
    print(f"end,共处理：{num}条，一共：{data_count}条")



#按序列完成复购任务
def san_rebuy_list():
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"start:{start_time}")
    user_id = get_rpop_layerlist()
    if user_id:
        try:
            user_id = int(user_id)
        except:
            user_id = 0
        print(f"user_id:{user_id}")
        uinfo = d_user.get_user_by_id(user_id)
        if uinfo:
            user_account = d_account.get_account_info(user_id)
            double_money_ls = get_bigorder_set('double_money')  # 复投金额
            double_count_ls = get_bigorder_set('double_count')  # 复投上限
            double_dblayer_ls = get_bigorder_set('double_dblayer')  #复购层数
            double_dbinvited_ls = get_bigorder_set('double_dbinvited')  #复购分红金额，每层分多少钱
            double_dbquan_ls = get_bigorder_set('double_dbquan')  #购物券数
            print(f"double_money_ls:{double_money_ls.val_int},double_count_ls:{double_count_ls.val_int},double_dblayer_ls:{double_dblayer_ls.val_int},\
            double_dbinvited_ls:{double_dbinvited_ls.val_int},double_dbquan_ls:{double_dbquan_ls.val_int},user_account:{user_account.balance},\
            uinfo.pai_buydui:{uinfo.pai_buydui}")
            #账户余额足够，没有超限复购次数，则执行复购扣钱、分润
            if user_account.balance >= double_money_ls.val_int and uinfo.pai_buydui <= double_count_ls.val_int:
                #扣减账户金额
                print(f"扣减账户金额")
                total_balance = user_account.balance - double_money_ls.val_int
                pai_buydui_cont = uinfo.pai_buydui + 1
                good_title = f"复购，pai_buydui:{pai_buydui_cont}"
                d_account.update_account_balance(uinfo.id, total_balance)
                user_banalce_out = m_account.BalanceModel(
                    user_id=uinfo.id,
                    change=-double_money_ls.val_int,
                    balance=total_balance,
                    type=global_define.balance_type[11],
                    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    good_id='',
                    good_title=good_title,
                    good_num='',
                    out_trade_no=''
                )
                d_account.add_balance(user_banalce_out)
                #增加复购次数
                print(f"增加复购次数")
                d_user.update_user_pai_buydui(uinfo.id, pai_buydui_cont)
                #执行推荐奖
                # if uinfo.invited_user_id > 0:
                #     parent_info = d_account.get_account_info_add(uinfo.invited_user_id)
                #     if parent_info:
                #         total_balance = parent_info.lock_balance + double_dbinvited_ls.val_int
                #         d_account.update_account_by_id(parent_info.id, {"lock_balance": total_balance})
                #         d_account.add_balance(m_account.BalanceModel(
                #             user_id=parent_info.user_id,
                #             change=double_dbinvited_ls.val_int,
                #             balance=total_balance,
                #             type=global_define.balance_type[12],
                #             create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                #             good_id='',
                #             good_title='',
                #             good_num='',
                #             out_trade_no=''
                #         ))
                #执行赠予购物券
                print(f"执行赠予购物券")
                d_account.add_grant_num(uinfo.id, double_dbquan_ls.val_int)
                # 公排向上分润
                print(f"公排向上分润")
                # start_lay = 3 + pai_buydui_cont
                start_lay = 1
                rebuy_distribute(user_id=uinfo.id, up_layer=double_dblayer_ls.val_int, every_money=double_dbinvited_ls.val_int, good_id=0, out_trade_no='', start_layer=start_lay)
    print(f"end")

#重排大公排，剔除空余排序会员
def scan_anddel_bigorders():
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"重新排序大公排用户start:{start_time}")
    # 重新排序大公排用户
    sucess_ls = get_sucess_user_for_order()
    print(f"处理公排有效用户：{sucess_ls}")
    order_id = 1
    for i in sucess_ls:
        u_info = d_user.get_user_by_id(i)
        # order_ls = get_bigordertwo(order_id)
        #更新用户：update_user_orders(userid,bigorder_id,is_never)
        update_user_neworder(i, order_id, u_info.entrust_status)

        print(f"{i},原公排:{u_info.bigorder_id},变更至:{order_id}")
        order_id += 1
        time.sleep(0.2)

    #清除排序但失效用户
    fail_ls = get_fail_user_for_order()
    print(f"处理公排失效用户：{fail_ls}")
    for i in fail_ls:
        u_info = d_user.get_user_by_id(i)
        # 更新用户：clear_user_order(userid)
        clear_user_order(i)
        print(f"{i},原公排:{u_info.bigorder_id},删除公排")
        time.sleep(0.2)
    print(f"===================================================================================")
    print(f"处理完毕")

