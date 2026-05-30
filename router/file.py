from fastapi import APIRouter, UploadFile, File, Depends, Header, HTTPException, Request
from fastapi.responses import FileResponse
import datetime, json
import uuid
from pathlib import Path

from config import DIRS
from model.res.file import FileRes, FileResTowx
from fastapi.exceptions import HTTPException
import io
import traceback
from PIL import Image, ImageDraw, ImageFont
from common import global_define
from pydantic import BaseModel, Field
from typing import List, Optional
from service.wx_service import wxpayservice
from service import qiniu_service
from dao.task import d_task
from router.admin.user import verify_token



router = APIRouter(dependencies=[Depends(verify_token)])

class MapModel(BaseModel):
    data_url: Optional[str] = Field(None, title='腾讯Javascript API库的URL，如：https://map.qq.com/api/gljs?v=1.exp')

@router.get('/qiniu_token', summary="获取七牛上传Token")
async def qiniu_token(filename: str, type: str = 'product'):
    """
    参数：
    filename，上传文件名，如果abcdef.jpg
    type，上传类型，默认值“product”表示产品图片上传，“cover”表示封面图，"main“表示产品主图
    返回值：
    code：  200表示正常，304表示filename上传重复,404表示发生错误
    """
    re_val = {"code": 200, "id": 1, "fname": filename, "token": "123456"}
    task_id = 100
    if type == "sucai":
        get_sucai = d_task.get_taskuser_for_filename(filename, 0, task_id)
        if get_sucai:
            re_val['code'] = 304
            re_val['id'] = 0
            re_val['token'] = ''
        else:
            save_data = d_task.insert_taskuser_for_filename(filename, task_id)
            token = qiniu_service.get_upload_token(filename)
            re_val["token"] = token
            re_val['id'] = save_data.id
    else:
        token = qiniu_service.get_upload_token(filename)
        re_val["token"] = token
        re_val['id'] = 0

    return re_val



@router.get('/qiniu_httpurl', summary="获取七牛访问url")
async def qiniu_httpurl(httpurl: str):
    """
    七牛资源下载
    :httpurl: 如：http://www.xxxxx.com/5f59dace081de.jpg
    :return: http://www.xxxxx.com/5f59dace081de.jpg?e=1719126477&token=Mply7-4INH5tRfYBrYc8MTT-l2_0xhwUhXI4R7_i:BgAmqkA7x8MxR9mUULxq0-_RDzQ=
    """
    return qiniu_service.get_download_url(httpurl)


@router.post('/upload_file', summary="七牛上传，专用于富文本编辑")
async def upload_file(file: UploadFile = File(...)):
    """
    返回值结构：{"hash":"Ft3_zcPtzqR9B-aZ1q5RaLxfLXze","key":"15cc3ae2-e818-11ef-9e46-00163e410368.jpg"}
    """
    file_type = 'file'
    file_date = f'{datetime.date.today()}'
    file_name = f'{uuid.uuid1()}{Path(file.filename).suffix}'
    file_dir = Path(DIRS.assets_dir) / file_type / file_date
    file_dir.mkdir(parents=True, exist_ok=True)
    file_path = file_dir / file_name

    context = await file.read()
    #5M
    if len(context) > 1 * 1024 * 1024:
        raise HTTPException(400, "已超文件最大限制")

    with open(str(file_path), 'wb') as f:
        f.write(context)
    qiniu_res = qiniu_service.qiniu_upload(file_path, file_name)
    # file_res = FileRes(
    #     file_type=file_type,
    #     file_date=file_date,
    #     file_name=file_name
    # )
    return qiniu_res


#
# @router.post('/upload_video', response_model=FileRes)
# async def upload_video(file: UploadFile = File(...)) -> FileRes:
#     """视频上传，小于5M"""
#     file_type = 'file'
#     file_date = f'{datetime.date.today()}'
#     file_name = f'{uuid.uuid1()}{Path(file.filename).suffix}'
#     file_dir = Path(DIRS.assets_dir) / file_type / file_date
#     file_dir.mkdir(parents=True, exist_ok=True)
#     file_path = file_dir / file_name
#
#     context = await file.read()
#     #5M
#     if len(context) > 5 * 1024 * 1024:
#         raise HTTPException(400, "已超文件最大限制")
#
#     with open(str(file_path), 'wb') as f:
#         f.write(context)
#
#     file_res = FileRes(
#         file_type=file_type,
#         file_date=file_date,
#         file_name=file_name
#     )
#     return file_res
#
# @router.post('/upload_cover_file', response_model=FileRes)
# async def upload_cover_file(file: UploadFile = File(...)) -> FileRes:
#     file_type = 'image'
#     file_date = f'{datetime.date.today()}'
#     file_name = f'{uuid.uuid1()}{Path(file.filename).suffix}'
#     file_dir = Path(DIRS.assets_dir) / file_type / file_date
#     file_dir.mkdir(parents=True, exist_ok=True)
#     file_path = file_dir / file_name
#
#     context = await file.read()
#     #2M
#     if len(context) > 2 * 1024 * 1024:
#         raise HTTPException(400, "已超文件最大限制")
#
#     try:
#         stream = io.BytesIO(context)
#         # image_pil = Image.open(stream).convert('RGB').resize((400, 400))
#         image_pil = Image.open(stream).convert('RGB')
#         image_pil.save(str(file_path), format='jpeg', quality=100)
#     except OSError:
#         traceback.print_exc()
#         raise HTTPException(400, "文件错误")
#
#     # with open(str(file_path), 'wb') as f:
#     #     f.write(context)
#
#     file_res = FileRes(
#         file_type=file_type,
#         file_date=file_date,
#         file_name=file_name
#     )
#     return file_res
#
@router.get('/{file_type}/{file_date}/{file_name}', response_class=FileResponse)
async def get_asset(file_type: str, file_date, file_name) -> str:
    return str(Path(DIRS.assets_dir).absolute() / file_type / file_date / file_name)
#
#
# @router.post(f'/get_map_jsapi', summary='获取带key的腾讯地图api库地址')
# async def get_map_jsapi(data: MapModel):
#     if data.data_url is None:
#         return "https://"
#     if data.data_url.find("?") > 0:
#         return f"{data.data_url}&key={global_define.jsapi_key}"
#     else:
#         return f"{data.data_url}?key={global_define.jsapi_key}"
#
# @router.post('/upload_file_towx', response_model=FileResTowx)
# async def upload_file_towx(file: UploadFile = File(...)) -> FileResTowx:
#     file_type = 'file'
#     file_date = f'{datetime.date.today()}'
#     file_name = f'{uuid.uuid1()}{Path(file.filename).suffix}'
#     file_dir = Path(DIRS.assets_dir) / file_type / file_date
#     file_dir.mkdir(parents=True, exist_ok=True)
#     file_path = file_dir / file_name
#
#     context = await file.read()
#     #5M
#     if len(context) > 1 * 1024 * 1024:
#         raise HTTPException(400, "已超文件最大限制")
#
#     with open(str(file_path), 'wb') as f:
#         f.write(context)
#
#     #上传微信服务期
#     wx_res = wxpayservice.image_upload(str(file_path))
#     mediaid = ''
#     if len(wx_res) > 1:
#         try:
#             mediaid = json.loads(wx_res[1])['media_id']
#         except:
#             pass
#
#     file_res = FileResTowx(
#         file_type=file_type,
#         file_date=file_date,
#         file_name=file_name,
#         media_code=str(wx_res[0]),
#         media_id=mediaid,
#         media_msg=str(wx_res)
#     )
#     return file_res