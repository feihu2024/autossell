from common import Dao
from model.schema import TTask, TTaskuser, TTasktopic, TTaskclockup, TUser
from dao import d_db, d_query
from model import m_schema
from model.task import m_task
import datetime,time,sys,math,json
from common import global_define

def model2dict(item) -> dict:
    return {key: val for key, val in item.dict().items() if val is not None}

def get_taskuser_for_filename(fname:str, sign:int = 0, task_id:int = 0):
    with Dao() as db:
        if sign == 0:
            if task_id == 0:
                return db.query(TTaskuser).filter(TTaskuser.filename == fname).filter(TTaskuser.status == 0).first()
            else:
                return db.query(TTaskuser).filter(TTaskuser.filename == fname).filter(TTaskuser.status == 0).filter(TTaskuser.task_id == task_id).first()
        else:
            if task_id == 0:
                return db.query(TTaskuser).filter(TTaskuser.filename == fname).first()
            else:
                return db.query(TTaskuser).filter(TTaskuser.filename == fname).filter(TTaskuser.task_id == task_id).first()

def get_task_for_id(task_id:int):
    with Dao() as db:
        return db.query(TTask).filter(TTask.id == task_id).first()

def get_taskuser_for_id(idd:int):
    with Dao() as db:
        return db.query(TTaskuser).filter(TTaskuser.id == idd).first()

def get_taskuser_for_id_taskid(idd:int, taskid):
    with Dao() as db:
        return db.query(TTaskuser).filter(TTaskuser.id == idd).filter(TTaskuser.task_id == taskid).first()

#获取所属任务数量
def get_taskuser_count_for_taskid(taskid:int, is_del:int = 0):
    with Dao() as db:
        if is_del == 0:
            return db.query(TTaskuser).filter(TTaskuser.task_id == taskid).count()
        else:
            return db.query(TTaskuser).filter(TTaskuser.task_id == taskid).where(TTaskuser.status == 0).count()

#获取所属任务，未领数量
def get_taskuser_count_for_taskid_has(taskid:int):
    with Dao() as db:
        return db.query(TTaskuser).filter(TTaskuser.task_id == taskid).filter(TTaskuser.user_id == 0).count()

#获取所属用户数量
def get_taskuser_count_for_userid(userid:int):
    with Dao() as db:
        return db.query(TTaskuser).filter(TTaskuser.user_id == userid).count()

#获取所属用户某个任务的数量
def get_taskuser_count_for_userid_taskid(taskid:int, userid:int):
    with Dao() as db:
        return db.query(TTaskuser).filter(TTaskuser.task_id == taskid).filter(TTaskuser.status == 0).filter(TTaskuser.user_id == userid).count()

#获取所属用户的打卡统计数据
def get_taskclock_count_touser(user_id:int, task_id:int = 0,topic_id:int = 0, taskuser_id = 0, status:int = -1):
    with Dao() as db:
        query = db.query(TTaskclockup).filter(TTaskclockup.user_id == user_id).filter(TTaskclockup.ctype == 0)
        if status > -1:
            query = query.filter(TTaskclockup.status == status)
        if task_id > 0:
            query = query.filter(TTaskclockup.task_id == task_id)
        if topic_id > 0:
            query = query.filter(TTaskclockup.topic_id == topic_id)
        if taskuser_id > 0:
            query = query.filter(TTaskclockup.tuser_id == taskuser_id)
        return query.count()

#获取所属团队的打卡统计数据
def get_taskclock_count(user_ids:int, status:int = -1):
    with Dao() as db:
        query = db.query(TTaskclockup).filter(TTaskclockup.user_id.in_(user_ids)).filter(TTaskclockup.ctype == 0)
        if status > -1:
            query = query.filter(TTaskclockup.status == status)
        return query.count()

def insert_taskuser_for_filename(fname:str, task_id:int):
    res = d_db.insert_taskuser(item=m_schema.CreateTaskuser(
            task_id=task_id,
            filename=fname
        ))
    return res

def insert_taskuser_for_filename(fname:str, task_id:int):
    res = d_db.insert_taskuser(item=m_schema.CreateTaskuser(
            task_id=task_id,
            filename=fname
        ))
    return res

def update_taskuser_task_url(sc_id:int, task_url:str, topic_id:int = 0):
    with Dao() as db:
        if topic_id == 0:
            db.query(TTaskuser).where(TTaskuser.id == sc_id).update(
                {"task_url": task_url})
        else:
            db.query(TTaskuser).where(TTaskuser.id == sc_id).update(
                {"task_url": task_url, "topic_id":topic_id})
        db.commit()

#更新任务上传数量
def update_task_upload(task_id:int, is_add:int = 1, num:int = 1):
    with Dao() as db:
        task = db.query(TTask).where(TTask.id == task_id).first()
        upload_num = 1
        if task.upload is not None:
            if is_add == 1:
                upload_num = task.upload + num
            else:
                upload_num = task.upload - num
        db.query(TTask).where(TTask.id == task_id).update(
            {"upload": upload_num})
        db.commit()

def update_topic_num(topic_id:int, is_add:int = 1, num:int = 1):
    with Dao() as db:
        topic = db.query(TTasktopic).where(TTasktopic.id == topic_id).first()
        topic_num = 1
        if topic.ts_num is not None:
            if is_add == 1:
                topic_num = topic.ts_num + num
            else:
                topic_num = topic.ts_num - num
        db.query(TTasktopic).where(TTasktopic.id == topic_id).update(
            {"ts_num": topic_num})
        db.commit()

def select_topic_count(topic_id:int):
    with Dao() as db:
        return db.query(TTaskuser).where(TTaskuser.topic_id == topic_id).where(TTaskuser.status == 0).count()

#更新打卡上传数量
def update_taskuser_upload(taskuser_id:int, is_add:int = 1, num:int = 1):
    with Dao() as db:
        task = db.query(TTaskuser).where(TTaskuser.id == taskuser_id).first()
        upload_num = 1
        if task.upload is not None:
            if is_add == 1:
                upload_num = task.upload + num
            else:
                upload_num = task.upload - num
        db.query(TTaskuser).where(TTaskuser.id == taskuser_id).update(
            {"upload": upload_num})
        db.commit()

def get_taskuser(task_id:int = -1, taskuser_id:int = -1, user_rose:int = -1, parent_id:int = -1,  link_stat:int = -1, pic_stat:int = -1, page:int = 1, page_size:int = 10, user_id:int = -1):
    filter = []
    if taskuser_id > 0:
        filter.append({"field": "taskuser.id","value": taskuser_id})
    if user_rose > 0:
        filter.append({"field": "User.level_id","value": user_rose})
    if parent_id > 0:
        filter.append({"field": "User.tuan_id","value": parent_id})
    if link_stat > 0:
        filter.append({"field": "taskuser.link_stat","value": link_stat})
    if pic_stat > 0:
        filter.append({"field": "taskuser.pic_stat","value": pic_stat})
    if task_id > 0:
        filter.append({"field": "taskuser.task_id","value": task_id})
    if user_id >= 0:
        filter.append({"field": "taskuser.user_id","value": user_id})
    filter.append({"field": "taskuser.status","op": ">","value": -1})
    query_data = d_query.FilterQueryData.parse_obj({
        "table": "taskuser",
        "joins": [
            {
                "table": "user",
                "on_left": "user_id",
                "on_right": "id"
            }
        ],
        # "selects": ["good", "min(good_spec.id)"],
        # "selects": ["good", "min(good_spec.id)"],
        # "group_by": ["good.id"],
        "filters": filter,
        "order_by": [{"field": "taskuser.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    # res = d_query.group_filter(query_data)
    # items = list(map(fill_spec_field, res['data']))
    res = d_query.filter_items(query_data)
    #return {"code": 0, "data": res['data'], 'total': res['total']}
    return res

def update_taskuser_pic_stats(task_id:int = -1, taskuser_id:int = -1, user_rose:int = -1, parent_id:int = -1,  link_stat:int = -1, pic_stat:int = -1, page:int = 1, page_size:int = 10, user_id:int = -1):
    re_val = []
    #0未打卡,1未审核,2已审核
    #每行：{"taskuser_id":0,"task_id":0,"user_id":0,"daka_num":0,"audit_num":0,"audit":0}  daka_num,打卡总数;audit_num,审核数量;audit,给予状态
    with Dao() as db:
        task_res = db.query(TTaskuser, TUser).outerjoin(TUser, TTaskuser.user_id == TUser.id)
        if taskuser_id > 0:
            task_res = task_res.filter(TTaskuser.id == taskuser_id)
        if user_rose > 0:
            task_res = task_res.filter(TUser.level_id == user_rose)
        if parent_id > 0:
            task_res = task_res.filter(TUser.tuan_id == parent_id)
        if link_stat > 0:
            task_res = task_res.filter(TTaskuser.link_stat == link_stat)
        if pic_stat > 0:
            task_res = task_res.filter(TTaskuser.pic_stat == pic_stat)
        if task_id > 0:
            task_res = task_res.filter(TTaskuser.task_id == task_id)
        if user_id >= 0:
            task_res = task_res.filter(TTaskuser.user_id == user_id)
        re_data = task_res.offset(page * page_size - page_size).limit(page_size).all()
        if re_data:
            for item in re_data:
                task_user, t_user = item
                if task_user and t_user:
                    user_lockup = find_taskclockup(task_user.id, t_user.id)
                    pic_stat = 0
                    link_stat = 0
                    if user_lockup:
                        audit_num = 0
                        daka_num = 0
                        link_audit_num = 0
                        link_daka_num = 0
                        #0未打卡,1未审核,2已审核
                        for item2 in user_lockup:
                            if item2.status in (1,2):
                                if item2.ctype == 1:
                                    link_audit_num += 1
                                    link_daka_num += 1
                                else:
                                    audit_num += 1
                                    daka_num += 1
                            else:
                                if item2.ctype == 1:
                                    link_daka_num += 1
                                else:
                                    daka_num += 1

                        this_val = {"taskuser_id": task_user.id, "task_id": task_user.task_id, "user_id": t_user.id,
                                           "daka_num": daka_num, "link_daka_num": link_daka_num, "audit_num": audit_num, "pic_audit": 0, "link_audit": 0}

                        if daka_num > 0:
                            if audit_num == daka_num: #已审核
                                pic_stat = 2
                                #update_taskuser_link_stat
                                update_taskuser_pic_stat(task_user.id, pic_stat)
                                this_val['pic_audit'] = pic_stat
                            else: #未审核
                                pic_stat = 1
                                update_taskuser_pic_stat(task_user.id, pic_stat)
                                this_val['pic_audit'] = pic_stat
                        else:
                            update_taskuser_pic_stat(task_user.id, pic_stat)

                        if link_daka_num > 0:
                            if link_audit_num == link_daka_num: #已审核
                                link_stat = 2
                                #update_taskuser_link_stat
                                update_taskuser_link_stat(task_user.id, link_stat)
                                this_val['link_audit'] = link_stat
                            else: #未审核
                                link_stat = 1
                                update_taskuser_link_stat(task_user.id, link_stat)
                                this_val['link_audit'] = link_stat
                        else:
                            update_taskuser_link_stat(task_user.id, link_stat)


                        re_val.append(this_val)

                    else:  #未打卡
                        update_taskuser_pic_stat(task_user.id, pic_stat)
                        update_taskuser_link_stat(task_user.id, link_stat)
                        re_val.append({"taskuser_id":task_user.id,"task_id":task_user.task_id,"user_id":t_user.id,"daka_num":0,"link_daka_num":0,"audit_num":0, "pic_audit": 0, "link_audit": 0})
    return re_val

def find_taskclockup(taskuser_id:int = -1, user_id:int = -1):
    with Dao() as db:
        return db.query(TTaskclockup).filter(TTaskclockup.tuser_id == taskuser_id).filter(TTaskclockup.user_id == user_id).all()

def update_taskuser_pic_stat(taskuser_id:int = -1,pic_stat:int = 0):
    with Dao() as db:
        db.query(TTaskuser).where(TTaskuser.id == taskuser_id).update(
            {"pic_stat": pic_stat})
        db.commit()

def update_taskuser_link_stat(taskuser_id:int = -1,link_stat:int = 0):
    with Dao() as db:
        db.query(TTaskuser).where(TTaskuser.id == taskuser_id).update(
            {"link_stat": link_stat})
        db.commit()

def taskclockup_audit(lp_id:int, audit:int = 0, stat_count:int = 0):
    with Dao() as db:
        db.query(TTaskclockup).where(TTaskclockup.id == lp_id).update(
            {"status": audit,"stat_count":stat_count})
        db.commit()

def update_taskuser_reason(sc_id:int, link_stat:int = 0, nopass:str = "", nopass_txt:str = ""):
    with Dao() as db:
        db.query(TTaskuser).where(TTaskuser.id == sc_id).update(
            {"link_stat": link_stat, "nopass": nopass, "nopass_txt": nopass_txt})
        db.commit()

def update_topic_name(tp_id:int, topic_name:str = ""):
    with Dao() as db:
        db.query(TTasktopic).where(TTasktopic.id == tp_id).update(
            {"topic_name": topic_name})
        db.commit()

def update_topic_comment(tp_id:int, topic_comment:str = ""):
    with Dao() as db:
        db.query(TTasktopic).where(TTasktopic.id == tp_id).update(
            {"topic_comment": topic_comment})
        db.commit()

def get_topic_for_id_taskid(idd:int, taskid):
    with Dao() as db:
        return db.query(TTasktopic).filter(TTasktopic.id == idd).filter(TTasktopic.task_id == taskid).first()

def del_topic(tp_id:int):
    with Dao() as db:
        db.query(TTasktopic).where(TTasktopic.id == tp_id).update({"status": -1})
        db.query(TTaskuser).where(TTaskuser.topic_id == tp_id).update({"status": -1})
        db.commit()

def del_taskuser(ts_id:int):
    with Dao() as db:
        db.query(TTaskuser).where(TTaskuser.id == ts_id).update({"status": -1})
        db.commit()

def update_task(item: m_task.STask):
    data = model2dict(item)
    data.pop('id')
    with Dao() as db:
        db.query(TTask).where(TTask.id == item.id).update(data)
        db.commit()

#修改状态
def update_task_stat(task_id:int, stat:int = 0):
    with Dao() as db:
        db.query(TTask).where(TTask.id == task_id).update({"stat": stat})
        db.commit()

#用户打卡
def insert_clockup(data: m_task.UserTaskclockup):
    res = d_db.insert_taskclockup(item=m_schema.CreateTaskclockup(
        task_id = data.task_id,
        tuser_id = data.sucai_id,
        topic_id = data.topic_id,
        user_id = data.user_id,
        ctype = data.ctype,
        content = data.content,
        verfy_name = data.verfy_name,
        status = 0,
        stat_count = data.stat_count,
        user_acc = data.user_acc
    ))
    return res

#修改用户打卡
def update_clockup(data: m_task.UserTaskclockup):
    res = d_db.update_taskclockup(item=m_schema.STaskclockup(
        id=data.id,
        content=data.content,
        stat_count=data.stat_count,
        user_acc=data.user_acc
    ))
    return res
    # with Dao() as db:
    #     db.query(TTasktopic).where(TTasktopic.id == data.id).update({"content": str(data.content)})
    #     db.commit()

#更新用户打卡数量
def user_get_taskuser_count(taskuser_id:int):
    with Dao() as db:
        task = db.query(TTaskuser).where(TTaskuser.id == taskuser_id).first()
        upload_num = 1
        if task.upload is not None:
            upload_num = task.upload + 1
        db.query(TTaskuser).where(TTaskuser.id == taskuser_id).update(
            {"upload": upload_num})
        db.commit()

#用户领取素材
def user_get_taskuser(data:m_task.GetTaskuser):
    with Dao() as db:
        taskuser = db.query(TTaskuser).where(TTaskuser.task_id == data.task_id).where(TTaskuser.user_id == 0).where(TTaskuser.status == 0).first()
        db.query(TTaskuser).where(TTaskuser.id == taskuser.id).update(
            {"user_time":datetime.datetime.now(), "user_id": data.user_id, "phone": data.phone, "address": data.address})
        db.commit()

#更用户领取素材数量
def update_task_userget(task_id:int):
    with Dao() as db:
        task = db.query(TTask).where(TTask.id == task_id).first()
        received = 1
        if task.received is not None:
            received = task.received + 1
        db.query(TTask).where(TTask.id == task_id).update(
            {"received": received})
        db.commit()

#导出已领取素材列表
def get_taskuser_export(task_id:int):
    with Dao() as db:
        query = db.query(TTaskuser).where(TTaskuser.task_id == task_id).where(TTaskuser.user_id > 0).where(TTaskuser.status == 0)
        taskcount = query.count()
        tasklist = query.all()
        return {'total':taskcount, 'data':tasklist}

def get_taskclockup_export(task_id:int):
    with Dao() as db:
        query = db.query(TTaskclockup).where(TTaskclockup.task_id == task_id).where(TTaskclockup.status >= 0).where(TTaskclockup.ctype == 0)
        taskcount = query.count()
        tasklist = query.all()
        return {'total':taskcount, 'data':tasklist}

#获取用户某个任务的打卡信息
def get_taskclockup(user_id:int, task_id:int = 0, sucai_id:int = 0):
    with Dao() as db:
        query = db.query(TTaskclockup).where(TTaskclockup.user_id == user_id).where(TTaskclockup.ctype == 0)
        if task_id > 0:
            query = query.where(TTaskclockup.task_id == task_id)
        if sucai_id > 0:
            query = query.where(TTaskclockup.tuser_id == sucai_id)
        taskcount = query.count()
        tasklist = query.all()
        return {'total':taskcount, 'data':tasklist}

#获取某用户的参与任务Id，List
def get_taskid_foruser(user_id:int):
    with Dao() as db:
        tasklist = db.query(TTaskuser).group_by(TTaskuser.task_id).filter(TTaskuser.user_id == user_id).all()
        re_val = list()
        for i in tasklist:
            re_val.append(i.task_id)
        return re_val

#获取某用户的List任务
def get_task_forid(task_ids:list, is_in:int = 1):
    with Dao() as db:
        if is_in == 1:
            return db.query(TTask).filter(TTask.id.in_(task_ids)).order_by(TTask.id.desc()).all()
        else:
            return db.query(TTask).filter(TTask.id.notin_(task_ids)).order_by(TTask.id.desc()).all()

#获取所有未结束 的 自动任务
def get_task_stat_auto():
    with Dao() as db:
        return db.query(TTask).filter(TTask.stat.in_([0,1,2])).filter(TTask.is_auto == 0).all()

#自动处理到时任务
def run_task_auto_stat():
    task_list = get_task_stat_auto()
    now_time = datetime.datetime.now()
    for i in task_list:
        front = "异常"
        if i.expired_time is not None and i.clock_time is not None and i.run_time is not None:
            front = "正常"
            if now_time >= i.expired_time:  #结束时间
                update_task_stat(i.id, 3)
            elif now_time >= i.clock_time:  #打卡时间
                update_task_stat(i.id, 2)
            elif now_time >= i.run_time:  #进行中时间
                update_task_stat(i.id, 1)
        print(f"-{front}-{i.id}|{i.title}|结束:{i.expired_time}|打卡:{i.clock_time}|进行:{i.run_time} \r\n")

#过期素材未下载，自动收回
def run_taskuser_auto_retract():
    expres_time = datetime.datetime.now() + datetime.timedelta(days=0,hours=0,minutes=0,seconds=global_define.taskuser_expires)
    update_ids = []
    with Dao() as db:
        # get_count = db.query(TTaskuser).where(TTaskuser.status == 0).where(TTaskuser.down == 0).where(TTaskuser.user_id > 0).where(TTaskuser.user_time > expres_time).count()
        # db.query(TTaskuser).where(TTaskuser.status == 0).where(TTaskuser.down == 0).where(TTaskuser.user_id > 0).where(TTaskuser.user_time > expres_time).update({"user_id": 0})
        # db.commit()
        get_list = db.query(TTaskuser).where(TTaskuser.status == 0).where(TTaskuser.down == 0).where(TTaskuser.user_id > 0).where(TTaskuser.user_time > expres_time).all()
        get_count = 0
        for li in get_list:
            this_recovery = li.recovery + 1
            db.query(TTaskuser).where(TTaskuser.id == li.id).update({"user_id": 0,"recovery":this_recovery})
            update_ids.append(li.id)
            get_count += 1
        db.commit()
        update_ids_str = ','.join(map(lambda x:str(x),update_ids))
    print(f"-{expres_time}|收回:{get_count}条|{update_ids_str} \r\n")

def get_task_stat(task_id:int):
    #总数、链接上传数、链接审核数、打卡条数、打卡审核数、合格数、未审核数
    re_val = {"total":0, "link":0, "link_audit":0, "daka":0, "daka_audit":0, "audit":0, "no_audit":0}
    task_info = get_task_for_id(task_id)
    if task_info:
        with Dao() as db:
            re_val["total"] = db.query(TTaskclockup).where(TTaskclockup.task_id == task_id).count()
            #re_val["total"] = task_info.upload
            re_val["link"] = db.query(TTaskclockup).where(TTaskclockup.task_id == task_id).where(TTaskclockup.ctype == 1).count()
            re_val["link_audit"] = db.query(TTaskclockup).where(TTaskclockup.task_id == task_id).where(TTaskclockup.ctype == 1).where(TTaskclockup.status.in_([1,2])).count()
            re_val["daka"] = db.query(TTaskclockup).where(TTaskclockup.task_id == task_id).where(TTaskclockup.ctype == 0).count()
            re_val["daka_audit"] = db.query(TTaskclockup).where(TTaskclockup.task_id == task_id).where(TTaskclockup.ctype == 0).where(TTaskclockup.status.in_([1, 2])).count()
            #re_val["audit"] = re_val["link_audit"] + re_val["daka_audit"]
            #re_val["no_audit"] = re_val["total"] - re_val["audit"]
            re_val["audit"] = db.query(TTaskclockup).where(TTaskclockup.task_id == task_id).where(TTaskclockup.ctype == 0).where(TTaskclockup.status == 1).count()
            re_val["no_audit"] = db.query(TTaskclockup).where(TTaskclockup.task_id == task_id).where(TTaskclockup.ctype == 0).where(TTaskclockup.status == 2).count()

    return re_val

def get_task_statcount(task_id:int, taskuser_id:int, user_id:int):
    #任务打卡平台流量统计
    re_val = []
    task_info = get_task_for_id(task_id)
    if task_info:
        if task_info.verfy:
            #抖音,小红书,视频号
            verfy_list = task_info.verfy.split(',')
            with Dao() as db:
                for i in verfy_list:
                    get_info = db.query(TTaskclockup).where(TTaskclockup.task_id == task_id).where(TTaskclockup.tuser_id == taskuser_id).where(TTaskclockup.user_id == user_id).where(TTaskclockup.ctype == 0).where(TTaskclockup.verfy_name == i).first()
                    get_num = 0
                    stat = '未审核'
                    if get_info:
                        get_num = get_info.stat_count
                        get_user_acc = get_info.user_acc
                        if get_info.status == 1:
                            stat = "合格"
                        elif get_info.status == 2:
                            stat = "不合格"
                        re_val.append(f"{i}-{get_num} | {stat} | {get_user_acc}")
    return re_val

def update_is_groupsir(user_id:int, rose_id:int = 0, username:str = '',  phone:str = '', email:str = ''):
    with Dao() as db:
        db.query(TUser).where(TUser.id == user_id).update(
            {"is_tuan": rose_id, "username": username, "email":email, "phone":phone})
        db.commit()

def update_is_groupuser(user_id:int, group_id:int = 0):
    with Dao() as db:
        db.query(TUser).where(TUser.id == user_id).update({"is_tuan": group_id})
        db.commit()

#转移团成员
def add_change_groupuser(user_id:int, group_id:int = 0):
    with Dao() as db:
        db.query(TUser).where(TUser.id == user_id).update(
            {"tuan_id": group_id})
        db.commit()

#团队日志
def add_groupuser_log(user_id:int, groupsir_id:int = 0, admin_id:int = 0, logtype:str = "未知"):
    res = d_db.insert_groupsirlog(item=m_schema.CreateGroupsirlog(
        user_id=user_id,
        groupsir_id=groupsir_id,
        admin_id=admin_id,
        logtype=logtype
    ))
    return res

def taskuser_download_count_add(taskid:int):
    re_num = 0
    with Dao() as db:
        ts_info = db.query(TTaskuser).filter(TTaskuser.id == taskid).first()
        re_num = 0
        if ts_info.down is not None:
            re_num = ts_info.down + 1
        db.query(TTaskuser).where(TTaskuser.id == taskid).update(
            {"down": re_num})
        db.commit()
    return re_num

#回收素材日志
def add_tsrecovery_log(user_id:int, task_id:int = 0, ts_id:int = 0, phone:str = "", address:str = "", logtype:str = "自动回收"):
    res = d_db.insert_tsrecoverylog(item=m_schema.CreateTsrecoverylog(
        user_id=user_id,
        ts_id=ts_id,
        task_id=task_id,
        phone=phone,
        address=address,
        logtype=logtype
    ))
    return res

def update_shengdai(user_id:int, level_shengdai:int = 0):
    with Dao() as db:
        db.query(TUser).where(TUser.id == user_id).update({"level_shengdai": level_shengdai})
        db.commit()


def init_bigorder_two():
    struct_num = 2  # 会员下属结构 2结构
    # struct_num = 3  #会员下属结构 3结构
    start_id = 1  # 起始id
    start_layer_id = 2  # 起始层
    line_nums = [(1, 1)]  # 行与数量[(1,1),(2,2),(3,4),(4,8),(5,16),(6,32)]
    # [(1, 1), (2, 3), (3, 9), (4, 27), (5, 81), (6, 243)]
    cur_line_nums_global = [1]
    cur_layer_id = 1
    max_layer_id = 100
    cur_layer_len = 1
    for i in range(start_layer_id, max_layer_id):
        cur_layer_len = cur_layer_len * struct_num if cur_layer_len == 1 else cur_layer_len
        line_nums.append((i, cur_layer_len))
        cur_layer_len = cur_layer_len * struct_num
        # print(i)
        # time.sleep(1)

    # print(line_nums)

    for j,i in line_nums:
        if j == 1:
            cur_line_nums = [1]
        else:
            #cur_line_nums = [x for x in range(start_id, start_id * struct_num - 1)]  #3结构
            cur_line_nums = [x for x in range(start_id, start_id * struct_num)]  #2结构
        print(cur_line_nums)
        for k in cur_line_nums:
            index_num = int(int(cur_line_nums.index(k)/struct_num))
            #print(f"index_num:{index_num}")
            #print(f"cur_line_nums_global:{cur_line_nums_global}")
            # out_str = f"{k}属于{cur_line_nums_global[index_num]},行号{j},当前行排序{cur_line_nums.index(k)+1},总数{len(cur_line_nums)}"
            # print(out_str)
            res = d_db.insert_bigorder_two(item=m_schema.CreateBigorderTwo(
                layer_id=j,
                cur_layer_id=cur_line_nums.index(k)+1,
                cur_layer_total=len(cur_line_nums),
                parent_id=cur_line_nums_global[index_num],
                order_id=k
            ))
            time.sleep(0.2)
        cur_line_nums_global = cur_line_nums
        start_id = max(cur_line_nums) + 1
        #print(cur_line_nums)
        time.sleep(0.1)
