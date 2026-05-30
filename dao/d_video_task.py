from common import Dao, global_define
from model.schema import *
from model.m_schema import *
from sqlalchemy import or_, and_, func
from typing import List, Optional
from sqlalchemy import text
import datetime, time, sys, math, json, redis
from pydantic import BaseModel, Field
from fastapi.exceptions import HTTPException
from dao import d_user, d_db, d_account, d_good, d_order, d_bigorder, d_balance

import logging


class SearchVideoTask(BaseModel):
    user_id: Optional[int] = Field(None,title='关联t_user表id')
    # description: Optional[str] = Field(None,title='资金备注，团长收益这里是逗号分隔的订单id')
    # create_time: Optional[str] = Field(None,title='时间段：time1,time2')
    good_id: Optional[int] = Field(None, title='礼包筛选')
    video_level: Optional[int] = Field(None, title='视频分发身份0达人,1店长,2服务商,3分公司')
    is_act: Optional[int] = Field(None, title='是否被激活,0未激活,1已激活')
    page: int = Field(1, title='当前页码，默认第1页')
    page_size: int = Field(20, title='返回每页数据，默认每页20条数据')

class ActModel(BaseModel):
    user_id: Optional[int] = Field(0,title='激活用户id')
    act_code: Optional[str] = Field(None, title='激活码')
    address_id: Optional[int] = Field(0, title='地址id')

class PicModel(BaseModel):
    task_id: Optional[int] = Field(None,title='任务id')
    receive_id: Optional[int] = Field(None, title='领取任务id')
    up_pic: Optional[str] = Field(None, title='任务上传截图')

class AuditModel(BaseModel):
    video_id: Optional[int] = Field(None, title='视频任务id')
    receive_id: Optional[int] = Field(None, title='领取视频任务id')
    audit: Optional[int] = Field(None, title='0未审核,1通过审核,2未通过')
    # audit_time '审核时间',
    audit_adm: Optional[int] = Field(None, title='审核管理人id')
    audit_info: Optional[str] = Field(None, title='审核备注100个汉字以内')

def get_video_task(video_task_id: int) -> Optional[SVideoTask]:
    with Dao() as db:
        t = db.query(TVideoTask).where(TVideoTask.id == video_task_id).first()
        if t:
            return SVideoTask.parse_obj(t.__dict__)
        else:
            return None

#激活视频码用户日志列表
def get_vrecharge_log_for_user(items: SearchVideoTask):
    with Dao() as db:
        res = db.query(TVideoRechargeLog).filter(TVideoTask.user_id == items.user_id)
        if items.good_id:
            res = res.filter(TVideoRechargeLog.good_id == items.good_id)

        res = res.order_by(TVideoRechargeLog.id.desc())
        total = res.count()
        search_list = res.offset(items.page * items.page_size - items.page_size).limit(items.page_size).all()
        return {"total":total, "data": search_list}

#激活视频码码主日志列表
def get_vrecharge_log_for_owner(items: SearchVideoTask):
    with Dao() as db:
        res = db.query(TVideoRechargeLog).filter(TVideoRechargeLog.owner_id == items.user_id).filter(TVideoRecharge.video_level == items.video_level)
        if items.good_id:
            res = res.filter(TVideoRechargeLog.good_id == items.good_id)

        res = res.order_by(TVideoRechargeLog.id.desc())
        total = res.count()
        search_list = res.offset(items.page * items.page_size - items.page_size).limit(items.page_size).all()
        return {"total":total, "data": search_list}

#获取码主充值码列表
def get_vrecharge_for_owner(items: SearchVideoTask):
    with Dao() as db:
        res = db.query(TVideoRecharge).filter(TVideoRecharge.owner_id == items.user_id).filter(TVideoRecharge.video_level == items.video_level)
        if items.good_id:
            res = res.filter(TVideoRecharge.good_id == items.good_id)

        res = res.order_by(TVideoRecharge.id.desc())
        total = res.count()
        search_list = res.offset(items.page * items.page_size - items.page_size).limit(items.page_size).all()
        return {"total":total, "data": search_list}

#获取用户激活充值码列表
def get_vrecharge_for_user(items: SearchVideoTask):
    with Dao() as db:
        res = db.query(TVideoRecharge).filter(TVideoRecharge.user_id == items.user_id)
        if items.good_id:
            res = res.filter(TVideoRecharge.good_id == items.good_id)
        if items.video_level:
            res = res.filter(TVideoRecharge.video_level == items.video_level)
        if items.is_act > 0:
            res = res.filter(TVideoRecharge.is_act == items.is_act)

        res = res.order_by(TVideoRecharge.id.desc())
        total = res.count()
        search_list = res.offset(items.page * items.page_size - items.page_size).limit(items.page_size).all()
        return {"total":total, "data": search_list}

# def insert_video_recharge_log(items: CreateVideoRechargeLog):
#     add_instance = TVideoRechargeLog(
#         user_id=items.user_id,
#         user_nick = items.user_nick,
#         phone = items.phone,
#         change = items.change,
#         balance = items.balance,
#         type = items.type,
#         description = items.description,
#         create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
#         operator_id = items.operator_id,
#         out_trade_no = items.out_trade_no,
#         good_id = items.good_id,
#         good_title = items.good_title,
#         good_num = items.good_num,
#         recharge_id = items.recharge_id,
#         owner_id = items.owner_id,
#         owner_nick = items.owner_nick,
#         owner_phone = items.owner_phone
#     )
#     with Dao() as db:
#         db.add(add_instance)
#         db.commit()

#给用户增加指定视频礼包的条数
def buy_pro_for_user(order_id:int):
    oinfo = d_order.get_order_data(order_id)
    if oinfo:
        user_id = oinfo.paider_id
        uinfo = d_user.get_user_by_id(user_id)
        uaccount = d_account.get_account_info_add(user_id)
        ginfo = d_good.get_good_data(oinfo.good_id)
        total_nvideo = uaccount.nvideo + ginfo.video_num
        with Dao() as db:
            db.query(TUserAccount).filter(TUserAccount.user_id == user_id).update({"nvideo": total_nvideo})
            db.commit()
        #写入日志
        add_log = CreateVideoRechargeLog(user_id=user_id,
                                        user_nick = uinfo.nickname,
                                        phone = uinfo.phone,
                                        change = ginfo.video_num,
                                        balance = total_nvideo,
                                        type = global_define.balance_type[18],
                                        description = global_define.balance_type[18],
                                        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                        operator_id = 0,
                                        out_trade_no = oinfo.out_trade_no,
                                        good_id = ginfo.id,
                                        good_title = f"{ginfo.name},{ginfo.title}",
                                        good_num = oinfo.number,
                                        recharge_id = oinfo.id,
                                        owner_id = 0,
                                        owner_nick = "",
                                        owner_phone = "")
        d_db.insert_video_recharge_log(add_log)

def act_recharge_for_user(user_id:int, good_id:int, recharge_id:int):
    uinfo = d_user.get_user_by_id(user_id)
    uaccount = d_account.get_account_info_add(user_id)
    ginfo = d_good.get_good_data(good_id)
    total_nvideo = uaccount.nvideo + ginfo.video_num
    urecharge = get_recharge_by_id(recharge_id)
    with Dao() as db:
        db.query(TUserAccount).filter(TUserAccount.user_id == user_id).update({"nvideo": total_nvideo})
        db.commit()
    #写入日志
    add_log = CreateVideoRechargeLog(user_id=user_id,
                                    user_nick = uinfo.nickname,
                                    phone = uinfo.phone,
                                    change = ginfo.video_num,
                                    balance = total_nvideo,
                                    type = global_define.balance_type[18],
                                    description = global_define.balance_type[18],
                                    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                    operator_id = 0,
                                    out_trade_no = 'act',
                                    good_id = ginfo.id,
                                    good_title = f"{ginfo.name},{ginfo.title}",
                                    good_num = 1,
                                    recharge_id = urecharge.id,
                                    owner_id = urecharge.user_id,
                                    owner_nick = urecharge.user_name,
                                    owner_phone = urecharge.user_phone)
    d_db.insert_video_recharge_log(add_log)
    #更新用户视频级别
    d_user.update_user_video_level(user_id, ginfo.video_level)
    #
    # zdyspec = str(ginfo.zdyspec)
    # zhitui = d_order.get_findall_second_num(zdyspec, '直推') * 100
    # jiantui = d_order.get_findall_second_num(zdyspec, '间推') * 100
    # tui_tuan = d_order.get_findall_second_num(zdyspec, '推团') * 100
    # tui_midd_tuan = d_order.get_findall_second_num(zdyspec, '间团') * 100
    # user_invit_info = None
    # if uinfo.invited_user_id is None:
    #     uinfo.invited_user_id = 0
    # if uinfo.invited_user_id > 0:
    #     user_invit_info = d_user.get_user_by_id(uinfo.invited_user_id)
    # # 推荐奖
    # if zhitui > 0 and user_invit_info:
    #     d_balance.invited_user_money(user_invit_info.id, zhitui, global_define.balance_type[40], good_id, f"{good_id}|{ginfo.title}")
    #     # 间推奖
    #     user_midd_info = None
    #     if user_invit_info.invited_user_id is None:
    #         user_invit_info.invited_user_id = 0
    #     if user_invit_info.invited_user_id > 0:
    #         user_midd_info = d_user.get_user_by_id(user_invit_info.invited_user_id)
    #     if jiantui > 0 and user_midd_info:
    #         d_balance.invited_user_money(user_midd_info.id, jiantui, global_define.balance_type[41], good_id, f"{good_id}|{ginfo.title}")
    # # 推荐团长奖
    # tuan_info = None
    # if uinfo.tuan_id > 0:
    #     tuan_info = d_user.get_user_by_id(uinfo.tuan_id)
    # if tui_tuan > 0 and tuan_info:
    #     d_balance.invited_user_money(tuan_info.id, tui_tuan, global_define.balance_type[42], good_id, f"{good_id}|{ginfo.title}")
    #     # 间推团长奖
    #     if tui_midd_tuan > 0 and tuan_info.tuan_id > 0:
    #         tuan_midd_info = d_user.get_user_by_id(tuan_info.tuan_id)
    #         d_balance.invited_user_money(tuan_midd_info.id, tui_midd_tuan, global_define.balance_type[43], good_id,f"{good_id}|{ginfo.title}")
    # #居间收益
    # if ginfo.live_mid_uid > 0 and ginfo.live_mid_money > 0:
    #     live_info = d_user.get_user_by_id(ginfo.live_mid_uid)
    #     d_balance.invited_user_money(live_info.id, ginfo.live_mid_money, global_define.balance_type[48], good_id,f"{good_id}|{ginfo.title}")


def get_recharge_by_id(recharge_id: int):
    with Dao() as db:
        return db.query(TVideoRecharge).where(TVideoRecharge.id == recharge_id).first()

def get_recharge_by_code_one(code: str):
    code = code.strip()
    with Dao() as db:
        return db.query(TVideoRecharge).where(TVideoRecharge.act_code == code).first()

def task_recharge_add(task_id: int, addnum:int = 1):
    with Dao() as db:
        db.query(TVideoTask).where(TVideoTask.id == task_id).update({"received": addnum})
        db.commit()

def get_vtask_by_id(vtask_id: int):
    with Dao() as db:
        return db.query(TVideoTask).where(TVideoTask.id == vtask_id).first()

def get_receive_by_id(receive_id: int):
    with Dao() as db:
        return db.query(TVideoTaskReceive).where(TVideoTaskReceive.id == receive_id).first()

def get_recharge_by_code(act_code: str):
    with Dao() as db:
        return db.query(TVideoRecharge, TGood).join(TGood, TGood.id == TVideoRecharge.good_id, isouter=True).filter(TVideoRecharge.act_code == act_code).first()

def act_recharge_code(user_id:int, act_code:str, address_id:int):
    uinfo = d_user.get_user_by_id(user_id)
    urecharge = get_recharge_by_code_one(act_code)
    #1领取成功, 2激活码错误, 3激活码失效, 4数据错误
    re_info = 1
    if uinfo and urecharge:
        if urecharge.act_code == act_code:
            if urecharge.is_act == 0:
                act_recharge_for_user(user_id, urecharge.good_id, urecharge.id)
                with Dao() as db:
                    db.query(TVideoRecharge).filter(TVideoRecharge.id == urecharge.id).update({"act_user_id": user_id, \
                                                                                              "act_user_phone": uinfo.phone, \
                                                                                              "act_user_name": uinfo.nickname, \
                                                                                              "act_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), \
                                                                                              "is_act": 1})
                    db.commit()
                d_order.add_order_and_balance(urecharge.good_id, urecharge.user_id, address_id, user_id)
            else:
                re_info = 3
        else:
            re_info = 2
    else:
        re_info = 4
    return re_info

def get_vrecharge_brach_list(page:int=1, page_size:int=20):
    with Dao() as db:
        res = db.query(TVideoRecharge).group_by(TVideoRecharge.batch_code).order_by(TVideoRecharge.id.desc())
        total = res.count()
        search_list = res.offset(page * page_size - page_size).limit(page_size).all()
        return {"total":total, "data": search_list}

#获取某级别领取视频码的统计数据: 达人  店长   服务商
def get_vrecharge_stat_data(video_level:int=0, user_id:int = -1):
    re_val = {"total":0, "used": 0}
    with Dao() as db:
        re_val["total"] = db.query(TVideoRecharge).filter(TVideoRecharge.video_level == video_level).filter(TVideoRecharge.user_id == user_id).count()
        re_val["used"] = db.query(TVideoRecharge).filter(TVideoRecharge.video_level == video_level).filter(TVideoRecharge.user_id == user_id).filter(TVideoRecharge.is_act == 1).count()

    return re_val

def update_audit(data:AuditModel):
    with Dao() as db:
        db.query(TVideoTask).filter(TVideoTask.id == data.video_id).update({"audit": data.audit, \
                                                                           "audit_time":  time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()), \
                                                                           "audit_adm": data.audit_adm, \
                                                                           "audit_info": data.audit_info})
        db.commit()

def update_receive_audit(data:AuditModel):
    with Dao() as db:
        db.query(TVideoTaskReceive).filter(TVideoTaskReceive.id == data.receive_id).update({"audit_status": data.audit, \
                                                                           "audit_time":  time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()), \
                                                                           "audit_adm": data.audit_adm, \
                                                                           "audit_info": data.audit_info})
        db.commit()

def update_receive_audit_and_money(data:AuditModel):
    with Dao() as db:
        db.query(TVideoTaskReceive).filter(TVideoTaskReceive.id == data.receive_id).update({"audit_status": data.audit, \
                                                                           "audit_time":  time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()), \
                                                                           "audit_adm": data.audit_adm, \
                                                                           "audit_info": data.audit_info, "money_status": 1})
        db.commit()

def del_material(maid:int):
    with Dao() as db:
        db.query(TVideoTaskMaterial).filter(TVideoTaskMaterial.id == maid).update({"is_del": 1, "update_time":  time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())})
        db.commit()

def update_uppic(data:PicModel):
    receive_info = get_receive_by_id(data.receive_id)
    if receive_info:
        with Dao() as db:
            if receive_info.audit_status == 0:
                db.query(TVideoTaskReceive).filter(TVideoTaskReceive.id == data.receive_id).update({"up_pic": data.up_pic, \
                                                                                                    "audit_status": 1, \
                                                                                                    "update_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
            else:
                db.query(TVideoTaskReceive).filter(TVideoTaskReceive.id == data.receive_id).update({"up_pic": data.up_pic, \
                                                                                   "update_time":  time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())})
            db.commit()



def get_receive_next(receive_id:int):
    with Dao() as db:
        return db.query(TVideoTaskReceive).filter(TVideoTaskReceive.id > receive_id).filter(TVideoTaskReceive.audit_status == 1).order_by(TVideoTaskReceive.id.asc()).first()

def get_mater_count_to_today(user_id:int, task_id:int):
    today = datetime.datetime.now()
    # yesterday = today - datetime.timedelta(days=1)
    # 昨天的0点
    # yesterday_start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    # 昨天的24点，即今天的0点
    # yesterday_end = yesterday.replace(hour=24, minute=0, second=0, microsecond=0)
    #今天最早时间
    today_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
    num = 0
    with Dao() as db:
        num = db.query(TVideoTaskReceive).filter(TVideoTaskReceive.user_id == user_id).filter(TVideoTaskReceive.task_id == task_id).filter(TVideoTaskReceive.register_time > today_start).count()
    return num

class MateDownLoadModel(BaseModel):
    mate_id: Optional[int] = Field(None, title='更新素材id')
    task_id: Optional[int] = Field(None,title='参与任务id')
    user_id: Optional[int] = Field(None, title='领取用户id')

def update_get_task_material(data:MateDownLoadModel):
    with Dao() as db:
        db.query(TVideoTaskMaterial).filter(TVideoTaskMaterial.id == data.mate_id).update({"task_id": data.task_id, \
                                                                                           "user_id": data.user_id, \
                                                                                           "is_download": 1, \
                                                                                           "down_time": time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()), \
                                                                                           "update_time":  time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())})
        db.commit()

def get_video_task_down_list(bag_id:int, m_type:int, page_size:int = 1):
    re_val = {"data": 0, "total": 0}
    with Dao() as db:
        query = db.query(TVideoTaskMaterial).filter(TVideoTaskMaterial.m_type == m_type)\
                                            .filter(TVideoTaskMaterial.bag_id == bag_id)\
                                            .filter(TVideoTaskMaterial.is_del == 0) \
                                            .filter(TVideoTaskMaterial.is_download == 0)
        query = query.limit(page_size)
        re_val["total"] = query.count()
        re_val["data"] = query.all()

    return re_val

def update_task_stat():
    now_time = datetime.datetime.now()
    re_val = {'start':0, 'end':0}
    with Dao() as db:
        re_val['start'] = db.query(TVideoTask).filter(TVideoTask.run_time <= now_time).filter(TVideoTask.stat == 0).count()
        re_val['end'] = db.query(TVideoTask).filter(TVideoTask.expired_time <= now_time).filter(TVideoTask.stat.in_([0,1])).count()
        if re_val['start'] > 0:
            db.query(TVideoTask).filter(TVideoTask.run_time <= now_time).filter(TVideoTask.stat == 0).update({"stat": 1, "update_time":  time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())})
            db.commit()
        if re_val['end'] > 0:
            db.query(TVideoTask).filter(TVideoTask.expired_time <= now_time).filter(TVideoTask.stat.in_([0,1])).update({"stat": 2, "update_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
            db.commit()
    return re_val

def del_video_article(delid:int):
    with Dao() as db:
        db.query(TVideoArticle).filter(TVideoArticle.id == delid).update({"is_del": 1})
        db.commit()

def del_video_article_list(delid:int):
    with Dao() as db:
        db.query(TVideoArticleList).filter(TVideoArticleList.id == delid).update({"is_del": 1})
        db.commit()

def get_video_article(video_id: int):
    with Dao() as db:
        return db.query(TVideoArticle).where(TVideoArticle.id == video_id).first()

def get_video_arc_list(cid:int = 0, page:int = 1, searchtitle:str = None, searchlabel:str = None, searchany:str = None):
    video_arc = d_bigorder.get_bigorder_set('video_arc')
    result_rs = {}
    #视频
    if video_arc.val_int > 0:
        with Dao() as db:
            # search_rs = db.query(TVideoArticle).filter(TVideoArticle.pic_id == 1).filter(TVideoArticle.is_del == 0)
            search_rs = db.query(TVideoArticle).filter(TVideoArticle.is_del == 0)
            if cid > 0:
                search_rs = search_rs.filter(TVideoArticle.type_id == cid)
            if searchtitle is not None:
                search_rs = search_rs.filter(TVideoArticle.title.like(f'%{searchtitle}%'))
            if searchlabel is not None:
                search_rs = search_rs.filter(TVideoArticle.share_label.like(f'%{searchlabel}%'))
            if searchany is not None:
                search_rs = search_rs.filter(TVideoArticle.share_label.like(f'%{searchany}%')).filter(TVideoArticle.title.like(f'%{searchany}%')).filter(TVideoArticle.title_tit.like(f'%{searchany}%'))
            result_rs['toal'] = search_rs.count()
            result_rs['data'] = search_rs.order_by(TVideoArticle.order_id.desc()).order_by(TVideoArticle.video_level.asc()).order_by(TVideoArticle.id.desc()).offset(page * 20 - 20).limit(20).all()
            return result_rs
    #等于0，图片
    else:
        with Dao() as db:
            # search_rs = db.query(TVideoArticle).filter(TVideoArticle.pic_id == 0).filter(TVideoArticle.is_del == 0)
            search_rs = db.query(TVideoArticle).filter(TVideoArticle.is_del == 0)
            if cid > 0:
                search_rs = search_rs.filter(TVideoArticle.type_id == cid)
            if searchtitle is not None:
                search_rs = search_rs.filter(TVideoArticle.title.like(f'%{searchtitle}%'))
            if searchlabel is not None:
                search_rs = search_rs.filter(TVideoArticle.share_label.like(f'%{searchlabel}%'))
            if searchany is not None:
                search_rs = search_rs.filter(TVideoArticle.share_label.like(f'%{searchany}%')).filter(TVideoArticle.title.like(f'%{searchany}%')).filter(TVideoArticle.title_tit.like(f'%{searchany}%'))
            result_rs['toal'] = search_rs.count()
            result_rs['data'] = search_rs.order_by(TVideoArticle.order_id.desc()).order_by(TVideoArticle.video_level.asc()).order_by(TVideoArticle.id.desc()).offset(page * 20 - 20).limit(20).all()
            return result_rs


def get_video_article_class():
    with Dao() as db:
        res = db.query(TVideoArticleType)
        res = res.order_by(TVideoArticleType.id.asc())
        total = res.count()
        search_list = res.all()
        return {"total":total, "data": search_list}

def add_video_label(video_id:int, video_label:str):
    label_info = get_video_article(video_id)
    update_label = f"{label_info['share_label']},{video_label}"
    if label_info:
        with Dao() as db:
            db.query(TVideoArticle).filter(TVideoArticle.id == video_id).update({"share_label": update_label})
            db.commit()