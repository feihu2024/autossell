from fastapi import APIRouter, HTTPException, Body
from sqlalchemy.engine import Row
from sqlalchemy import or_, func
from model.task import m_task
from dao.task import d_task
import datetime
import uuid
from config import DIRS, DOMAIN
from pathlib import Path
from dao import d_order, d_db, d_user
from model import m_schema
from common import global_define
from openpyxl import Workbook
from openpyxl.drawing.image import Image
import requests, os

router = APIRouter()

@router.post('/save_sucai', summary="素材回传七牛地址")
async def save_sucai(data: m_task.SaveSucai):
    """
    返回值：
    code：  200表示保存成功，304表示未找到task_id 或 sucai_id
    """
    re_val = {"code":200, "msg":"保存成功"}
    res = d_task.get_taskuser_for_id_taskid(data.sucai_id, data.task_id)
    if res:
        d_task.update_taskuser_task_url(data.sucai_id, data.task_url, data.topic_id)
        d_task.update_task_upload(data.task_id)
        d_task.update_topic_num(data.topic_id)
    else:
        re_val["code"] = 304
        re_val["msg"] = "未找到素材或任务。"
    return re_val


@router.get('/get_taskuser')
async def get_taskuser(task_id:int = -1, taskuser_id:int = -1, user_rose:int = -1, parent_id:int = -1,  link_stat:int = -1, pic_stat:int = -1, page:int = 1, page_size:int = 20, user_id:int = -1):
    """
    获取素材和用户列表,
    task_id, 任务id
    taskuser_id, 素材ID
    user_rose, 用户角色id
    parent_id, 上一级用户id
    link_stat, 链接状态
    pic_stat, 素材打卡状态,截图审核状态,0未打卡,1未审核,2已审核
    page:当前页码，默认1.
    page_size：每页做多条数，默认20
    user_id, 用户id
    """
    re_val = {"code": 0, "data": "", "total":0}
    if task_id < 1:
        re_val['data'] = "未知任务"
        return re_val
    res = d_task.get_taskuser(task_id, taskuser_id, user_rose, parent_id, link_stat, pic_stat, page, page_size, user_id)
    re_val['data'] = res['data']
    re_val['total'] = res['total']
    return re_val

@router.get('/get_taskuser_notake')
async def get_taskuser_notake(task_id:int = -1, page:int = 1, page_size:int = 10):
    """
    获取素材和用户列表,
    task_id, 任务id
    page:当前页码，默认1.
    page_size：每页做多条数，默认20
    """
    re_val = {"code": 0, "data": "", "total":0}
    if task_id < 1:
        re_val['data'] = "未知任务"
        return re_val
    res = d_task.get_taskuser(task_id, -1, -1, -1, -1, -1, page, page_size, 0)
    re_val['data'] = res['data']
    re_val['total'] = res['total']
    return re_val

@router.get('/flush_taskuser')
async def flush_taskuser(task_id:int = -1, taskuser_id:int = -1, user_rose:int = -1, parent_id:int = -1,  link_stat:int = -1, pic_stat:int = -1, page:int = 1, page_size:int = 20, user_id:int = -1):
    """
    刷新素材和用户的 打卡状态列表,
    task_id, 任务id
    taskuser_id, 素材ID
    user_rose, 用户角色id
    parent_id, 上一级用户id
    link_stat, 链接状态
    pic_stat, 素材打卡状态,截图审核状态,0未打卡,1未审核,2已审核
    page:当前页码，默认1.
    page_size：每页做多条数，默认20
    user_id, 用户id
    """
    re_val = {"code": 0, "data": "", "total":0}
    if task_id < 1:
        re_val['data'] = "未知任务"
        return re_val
    re_val['data'] = d_task.update_taskuser_pic_stats(task_id, taskuser_id, user_rose, parent_id, link_stat, pic_stat, page, page_size, user_id)
    return re_val

@router.post('/taskaudit_reason')
async def taskclockup_audit(data: m_task.SaveReason):
    """
    用户任务素材审核原因
    """
    res = d_task.get_taskuser_for_id_taskid(data.sucai_id, data.task_id)
    if not res:
        raise HTTPException(status_code=400, detail="非法数据")
    d_task.update_taskuser_reason(data.sucai_id, data.link_stat, data.nopass, data.nopass_txt)
    return {"code":200}

@router.get('/del_topic', summary="删除话题，将删除其下所有素材")
async def del_topic(topic_id:int):
    d_task.del_topic(topic_id)
    return {"code":200}

@router.get('/del_material', summary="删除素材")
async def del_material(ts_id:int):
    ts_info = d_task.get_taskuser_for_id(ts_id)
    if not ts_info:
        raise HTTPException(status_code=400, detail="非法数据")
    d_task.del_taskuser(ts_id)
    #话题减少1
    if ts_info.topic_id is not None:
        d_task.update_topic_num(ts_info.topic_id,0)
    #任务减少1
    if ts_info.task_id > 0:
        d_task.update_task_upload(ts_info.task_id,0)
    return {"code":200}

@router.post('/task_update')
async def task_update(data: m_task.STask):
    """
    修改任务数据
    """
    res = d_task.get_task_for_id(data.id)
    if not res:
        raise HTTPException(status_code=400, detail="未知任务")
    d_task.update_task(data)
    return {"code":200}

@router.get('/task_update_stat')
async def task_update_stat(task_id:int, stat:int = 0):
    """
    修改任务数据状态
    task_id,任务id
    stat,状态值：0未开启,1进行中,2打开中,3已结束
    """
    res = d_task.get_task_for_id(task_id)
    if not res:
        raise HTTPException(status_code=400, detail="未知任务")
    if res.is_auto == 0:
        raise HTTPException(status_code=400, detail="非手动处理任务")
    d_task.update_task_stat(task_id, stat)
    return {"code":200}


@router.post('/get_sucai', summary="用户领取素材")
async def get_sucai(data: m_task.GetTaskuser):
    """
    返回值：
    code：  200表示保存成功，304表示未找到task_id 或 sucai_id
    """
    re_val = {"code":200, "msg":"领取成功"}
    if data.user_id in global_define.ts_blacklist:
        re_val["msg"] = "限制用户，请与管理员联系。"
        re_val["code"] = 304
    else:
        task = d_task.get_task_for_id(data.task_id)
        if task:
            max_num = d_task.get_taskuser_count_for_userid_taskid(data.task_id, data.user_id)
            has_num = d_task.get_taskuser_count_for_taskid_has(data.task_id)
            if max_num >= task.big or has_num < 1:
                re_val["code"] = 304
                re_val["msg"] = "领取已达到上限或素材库存不足。"
            else:
                d_task.user_get_taskuser(data)
                d_task.update_task_userget(data.task_id)
        else:
            re_val["code"] = 304
            re_val["msg"] = "未找到任务。"
    return re_val

@router.get(f'/export_user', summary='导出任务素材列表')
async def export_user(taskid:int):
    """
    导出任务素材列表
    """
    task_info = d_task.get_task_for_id(taskid)
    data = d_task.get_taskuser_export(taskid)
    data_d = data['data']
    data_t = data['total']
    down_url = ""
    if data_t > 0:
        file_type = 'file'
        file_date = f'{datetime.date.today()}'
        file_name = f'{uuid.uuid1()}export.csv'
        file_dir = Path(DIRS.assets_dir) / file_type / file_date
        file_dir.mkdir(parents=True, exist_ok=True)
        file_path = file_dir / file_name
        content = f"任务id,素材id,用户id,用户名,团长id,团长名,上级团长,上级团长名,推荐人id,打卡总数,打卡合格数,{task_info.verfy} \r\n"
        for i in data_d:
            d = i
            default_val = {'uname':'未知', 'tuan_id':'0', 'tuan_name':'未知', 'pare_tuan_id':'0', 'pare_tuan_name':'未知','recom_id':'0', 'daka_total':'0', 'daka_ok':'0'}
            userinfo = d_user.get_user_by_id(d.user_id)
            if userinfo:
                if userinfo.username is None:
                    userinfo.username = ''
                if userinfo.nickname is None:
                    userinfo.nickname = ''
                default_val['uname'] = userinfo.username + '/' + userinfo.nickname
                default_val['tuan_id'] = str(userinfo.tuan_id)
                default_val['recom_id'] = str(userinfo.invited_user_id)
                if userinfo.tuan_id > 0:
                    tuaninfo = d_user.get_user_by_id(userinfo.tuan_id)
                    if tuaninfo:
                        if tuaninfo.username is None:
                            tuaninfo.username = ''
                        if tuaninfo.nickname is None:
                            tuaninfo.nickname = ''
                        default_val['tuan_name'] = tuaninfo.username + '/' + tuaninfo.nickname

            get_daka = d_task.get_taskclockup(d.user_id, d.task_id, d.id)
            default_val['daka_total'] = str(get_daka['total'])
            is_youxiao = 0
            for su in get_daka['data']:
                if su.status == 1:
                    is_youxiao += 1
            default_val['daka_ok'] = str(is_youxiao)
            #default_val['daka_ok'] = get_daka['total']
            stat_count_info = d_task.get_task_statcount(taskid, d.id, d.user_id)
            content += ','.join((str(taskid), str(d.id), str(d.user_id), default_val['uname'], default_val['tuan_id'], default_val['tuan_name'], default_val['pare_tuan_id'], default_val['pare_tuan_name'], default_val['recom_id'], default_val['daka_total'], default_val['daka_ok']))
            for ii in task_info.verfy.split(','):
                this_info = '0'
                for tt in stat_count_info:
                    if tt.find(ii) >= 0:
                        this_info = tt
                content = content + ',' + this_info
            content += '\r\n'
        # content += d_order.create_export_content(data_d)
        with open(str(file_path), 'a') as f:
            f.write(content)

    down_url = DOMAIN + '/' + str(file_path)
    d_order.insert_exportfile(m_schema.CreateExportFile(
        user_id=0,
        export_url=down_url,
        type=global_define.setting_orders_export['sucai_user_list']
    ))
    return down_url

def save_img(url):
    file_name = ""
    try:
        res = requests.get(url)
        file_name = url.split('/')[-1]
        file_name = f"/tmp/{file_name.split('?')[0]}"
        if os.path.exists(file_name):
            return file_name
        with open(file_name, 'wb') as f:
             for data in res.iter_content(128):
                f.write(data)
    except:
        pass
    return file_name

def insert_img(sh, line, column, file_name):
    sh.row_dimensions[line].height=140
    sh.column_dimensions[column].width = 40
    img = Image(file_name)
    img.width, img.height=140, 140
    sh.add_image(img, f"{column}{line}")

@router.get(f'/export_user_toexcel', summary='导出EXCEL任务素材列表')
async def export_user_toexcel(taskid:int):
    """
    导出EXCEL任务素材列表
    """
    task_info = d_task.get_task_for_id(taskid)
    data = d_task.get_taskclockup_export(taskid)
    data_d = data['data']
    data_t = data['total']
    down_url = ""
    if data_t > 0:
        file_type = 'file'
        file_date = f'{datetime.date.today()}'
        file_name = f'{uuid.uuid1()}export.xlsx'
        file_dir = Path(DIRS.assets_dir) / file_type / file_date
        file_dir.mkdir(parents=True, exist_ok=True)
        file_path = file_dir / file_name
        down_url = DOMAIN + '/' + str(file_path)
        wb = Workbook()
        sh = wb.active
        row_num = 1
        # 日期	平台	昵称	帐号	浏览量   主页截图  	浏览量页面
        sh['A1'] = '日期'
        sh['B1'] = '平台'
        sh['C1'] = '昵称'
        sh['D1'] = '帐号'
        sh['E1'] = '浏览量'
        # sh['F1'] = '主页截图'
        # sh['G1'] = '浏览量页面'
        sh['F1'] = '用户id'
        sh['G1'] = '电话'
        sh['H1'] = '直推上级id'
        sh['I1'] = '团长id'
        sh['J1'] = '上级团长id'
        sh['K1'] = '主页截图'
        sh['L1'] = '浏览量页面'
        sh.column_dimensions['F'].width = 40
        sh.column_dimensions['G'].width = 40
        # content = f"任务id,素材id,用户id,用户名,团长id,团长名,上级团长,上级团长名,推荐人id,打卡总数,打卡合格数,{task_info.verfy} \r\n"
        for i in data_d:
            d = i
            row_num += 1
            sh.row_dimensions[row_num].height = 140
            # default_val = {'uname':'未知', 'tuan_id':'0', 'tuan_name':'未知', 'pare_tuan_id':'0', 'pare_tuan_name':'未知','recom_id':'0', 'daka_total':'0', 'daka_ok':'0'}
            userinfo = d_user.get_user_by_id(d.user_id)
            if userinfo:
                C = [f"A{row_num}", f"B{row_num}", f"C{row_num}", f"D{row_num}", f"E{row_num}", f"F{row_num}",f"G{row_num}",f"H{row_num}",f"I{row_num}",f"J{row_num}",f"K{row_num}",f"L{row_num}",f"M{row_num}",f"N{row_num}",f"O{row_num}"]
                sh[C[0]] = d.register_time
                sh[C[1]] = '' if d.verfy_name is None else d.verfy_name
                sh[C[2]] = '' if userinfo.username is None else userinfo.username+ '/' + '' if userinfo.nickname is None else userinfo.nickname
                sh[C[3]] = '' if d.user_acc is None else d.user_acc
                sh[C[4]] = '' if d.stat_count is None else d.stat_count
                sh[C[5]] = userinfo.id
                sh[C[6]] = '' if userinfo.phone is None else userinfo.phone
                sh[C[7]] = '' if userinfo.invited_user_id is None else userinfo.invited_user_id
                sh[C[8]] = '' if userinfo.tuan_id is None else userinfo.tuan_id
                sh[C[9]] = ''
                # sh[C[10]] = '主页截图'
                # sh[C[11]] = '浏览量页面'
                # sh.add_image(img, 'K1')
                dakas = d.content.split(',')
                if len(dakas) == 1:
                    fname = save_img(dakas[0])
                    if fname:
                        insert_img(sh, row_num, 'K', fname)
                    sh[C[10]] = ''
                elif len(dakas) == 2:
                    fname = save_img(dakas[0])
                    if fname:
                        insert_img(sh, row_num, 'K', fname)
                    fname = save_img(dakas[1])
                    if fname:
                        insert_img(sh, row_num, 'L', fname)
                elif len(dakas) == 3:
                    fname = save_img(dakas[0])
                    if fname:
                        insert_img(sh, row_num, 'K', fname)
                    fname = save_img(dakas[1])
                    if fname:
                        insert_img(sh, row_num, 'L', fname)
                    fname = save_img(dakas[2])
                    if fname:
                        insert_img(sh, row_num, 'M', fname)
                elif len(dakas) == 4:
                    fname = save_img(dakas[0])
                    if fname:
                        insert_img(sh, row_num, 'K', fname)
                    fname = save_img(dakas[1])
                    if fname:
                        insert_img(sh, row_num, 'L', fname)
                    fname = save_img(dakas[2])
                    if fname:
                        insert_img(sh, row_num, 'M', fname)
                    fname = save_img(dakas[3])
                    if fname:
                        insert_img(sh, row_num, 'N', fname)
                else:
                    sh[C[10]] = ''
                    sh[C[11]] = ''
        wb.save(file_path)

        d_order.insert_exportfile(m_schema.CreateExportFile(
            user_id=0,
            export_url=down_url,
            type=global_define.setting_orders_export['sucai_user_list_xlsx']
        ))
    return down_url

@router.get('/get_topic_count')
async def get_topic_count(topic_id:int):
    """
    获取话题下的素材数量
    """
    re_val = {"code":200, "data":0}
    re_val['data'] = d_task.select_topic_count(topic_id)
    return re_val

@router.get('/get_task_count')
async def get_task_count(task_id:int):
    """
    获取任务下的素材数量
    """
    re_val = {"code":200, "data":0}
    re_val['data'] = d_task.get_taskuser_count_for_taskid(task_id, 1)
    return re_val

# @router.get('/taskuser_dwonload')
# async def taskuser_dwonload(ts_id:int):
#     """
#     素材下载次数累计
#     """
#     re_val = {"code":200, "data":0}
#     re_val['data'] = d_task.taskuser_download_count_add(ts_id)
#     return re_val