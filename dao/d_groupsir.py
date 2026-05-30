import datetime,time
from common import Dao
from model import schema, m_schema
from router import r_schema
from typing import List, Optional
from pydantic import BaseModel, Field
from dao import d_user


class SearchGroupsir(BaseModel):
    group_id: Optional[int] = Field(None, title='团员id，当设置此值时表示只查询返回个人信息，而不是列表')
    user_id: Optional[int] = Field(None,title='关联t_user表id')
    parent_id: Optional[int] = Field(None,title='0:表示团长，非0表示下级成员')
    register_time: Optional[str] = Field(None, title='成团时间和入团,是一个时间段如： 2023.1.1,2023.5.1')
    status: Optional[int] = Field(None, title='0: 启用   1: 暂停  -1：出团或解散')
    is_empower: Optional[int] = Field(None, title='0: 未授权   1:已授权（可以使用所有商品秒杀包）')
    notes: Optional[str] = Field(None, title='团员备注')
    page: int = Field(1, title='当前页码，默认第1页')
    page_size: int = Field(20, title='返回每页数据，默认每页20条数据')


def insert_gorupsir(Titem: schema.TGroupsir):
    re = 'add sucess'
    with Dao() as db:
        if db.query(schema.TUser).where(schema.TUser.id==Titem.user_id).first():
            if not db.query(schema.TGroupsir).where(schema.TGroupsir.user_id == Titem.user_id).first():
                db.add(Titem)
                db.commit()
            else:
                re = f"用户已成团，请到团长处管理。"
        else:
            re = f"用户不存在{Titem.user_id}"
    return re

def update_groupsir_status(user_id:int = 0, status:int = 0):
    with Dao() as db:
        db.query(schema.TGroupsir).where(schema.TGroupsir.user_id == user_id).update({"status": status})
        db.commit()

def update_groupsir_empower(user_id:int = 0, status:int = 0):
    re = 'update sucess'
    groupsir_info = get_groupsir_for_user(user_id)
    if groupsir_info:
        with Dao() as db:
            db.query(schema.TGroupsir).where(schema.TGroupsir.user_id == user_id).update({"is_empower": status})
            db.commit()
    else:
        re = f"非法团长{user_id}，授权失败"
    return re

def search_groupsir(items: SearchGroupsir):
    with Dao() as db:
        res = db.query(schema.TGroupsir, schema.TUser).outerjoin(schema.TUser, schema.TGroupsir.user_id == schema.TUser.id)
        if items.user_id:
            res = res.filter(schema.TGroupsir.user_id == items.user_id)
        if items.parent_id is not None:
            res = res.filter(schema.TGroupsir.parent_id == items.parent_id)
        if items.register_time:
            times = items.register_time.split(',')
            res = res.filter(schema.TGroupsir.register_time > times[0])
            res = res.filter(schema.TGroupsir.register_time < times[1])
        if items.status is not None:
            res = res.filter(schema.TGroupsir.status == items.status)
        else:
            res = res.filter(schema.TGroupsir.status > -1)
        if items.is_empower is not None:
            res = res.filter(schema.TGroupsir.is_empower == items.is_empower)
        if items.notes:
            res = res.filter(schema.TGroupsir.notes.like(f'%{items.notes}%'))
        res = res.order_by(schema.TGroupsir.id.desc())
        total = res.count()
        search_list = res.offset(items.page * items.page_size - items.page_size).limit(items.page_size).all()
        return {"total":total, "data": search_list}

def get_groupsir(group_id:int =0):
    with Dao() as db:
        return db.query(schema.TGroupsir, schema.TUser).outerjoin(schema.TUser, schema.TGroupsir.user_id == schema.TUser.id).filter(schema.TGroupsir.id == group_id).first()

def get_groupsir_for_user(user_id:int = 0):
    with Dao() as db:
        return db.query(schema.TGroupsir).filter(schema.TGroupsir.user_id == user_id).filter(schema.TGroupsir.parent_id == 0).filter(schema.TGroupsir.status == 0).first()
def get_member_for_user(user_id:int = 0):
    with Dao() as db:
        return db.query(schema.TGroupsir).filter(schema.TGroupsir.user_id == user_id).first()

def add_groupsir(g_user_id:int = 0, g_parent_id:int = 0, g_notes: str = ''):
    parent_info = get_groupsir_for_user(g_parent_id)
    #确定团长存在且启用
    if parent_info:
        #确定是新团员
        if not get_member_for_user(g_user_id):
            insert_tgroupsir = schema.TGroupsir(
                user_id=g_user_id,
                parent_id=g_parent_id,
                notes=g_notes
            )
            insert_gorupsir(insert_tgroupsir)

def get_all_groupsir():
    with Dao() as db:
        return db.query(schema.TGroupsir.user_id).filter(schema.TGroupsir.parent_id == 0).all()

def get_members_count(userid:int):
    with Dao() as db:
        # res = db.query(schema.TGroupsir, schema.TUser).outerjoin(schema.TUser, schema.TGroupsir.user_id == schema.TUser.id)
        # res = res.filter(schema.TGroupsir.user_id == userid)
        return db.query(schema.TUser).filter(schema.TUser.tuan_id == userid).filter(schema.TUser.is_tuan == 0).count()
def get_gsir_count(userid:int):
    with Dao() as db:
        return db.query(schema.TUser).filter(schema.TUser.tuan_id == userid).filter(schema.TUser.is_tuan == 1).count()

def update_groupsir_create_addmembers(user_id:int = 0):
    user_ids = [user_id]
    user_search = [user_id]
    for i in range(10):
        if len(user_search) > 0:
            user_ids = d_user.get_invited_user_for_list(user_search)
            user_search = d_user.get_invited_user_for_list_notuan(user_search)
            update_groupsir_create_addmembers_run(user_ids, user_id)

def update_groupsir_create_addmembers_test(user_id:int = 0):
    user_ids = [user_id]
    user_search = [user_id]
    re_data = [{'id1':[],'id2':[],'id3':[],'id4':[],'id5':[],'id6':[],'id7':[],'id8':[],'id9':[],'id10':[],'user_ids_total':0},
               {'id1':[],'id2':[],'id3':[],'id4':[],'id5':[],'id6':[],'id7':[],'id8':[],'id9':[],'id10':[],'user_search_total':0}]
    for i in range(10):
        index_num = i + 1
        sub_name = f"id{index_num}"
        if len(user_search) > 0:
            user_ids = d_user.get_invited_user_for_list(user_search)
            user_search = d_user.get_invited_user_for_list_notuan(user_search)
            #update_groupsir_create_addmembers_run(user_ids, user_id)
            re_data[0][sub_name].append(user_ids)
            re_data[0]['user_ids_total'] = re_data[0]['user_ids_total'] + len(user_ids)
            re_data[1][sub_name].append(user_search)
            re_data[1]['user_search_total'] = re_data[1]['user_search_total'] + len(user_search)
    return re_data

def update_groupsir_create_addmembers_run(user_ids:list, tuan_id:int):
    with Dao() as db:
        db.query(schema.TUser).where(schema.TUser.id.in_(user_ids)).update({"tuan_id": tuan_id})
        db.commit()
