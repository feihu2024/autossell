from typing import List, Optional
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from pydantic import BaseModel, Field
from model import m_schema, schema
from router import r_schema
from fastapi.exceptions import HTTPException
from dao import d_address, d_db
from datetime import datetime
from .user import verify_token
import re

# router = APIRouter()
router = APIRouter(dependencies=[Depends(verify_token)])


class ABanner(BaseModel):
    banner: Optional[m_schema.SBanner]
    good: Optional[m_schema.SGood]
    TGoodSpec: Optional[m_schema.SGoodSpec]

class DBanner(BaseModel):
    banner_id: Optional[int] = Field(title='banner表id')
    valcode: Optional[str] = Field(title='验证码')

class MPoster(BaseModel):
    poster_url: Optional[str] = Field(title='海报文件地址')
    status: Optional[str] = Field(title='状态：空为正常，del为删除')
    description: Optional[str] = Field(title='描述(做多50个中文字符)')
    create_time: Optional[datetime] = Field(title='创建时间')

@router.post(f'/banner_list', response_model=List[ABanner], summary='获取banner或其他广告列表')
async def get_banners(type_id: int = 0):
    """
    type_id默认值0，表示banner列表
    """
    banner_list = []
    f_banner: m_schema.FilterResBanner = await r_schema.filter_banner(type_id=str(type_id))
    banners: List[m_schema.SBanner] = f_banner.data
    for banner in banners:
        if banner is not None:
            good: m_schema.SGood = await r_schema.get_good(good_id=banner.good_id)
            f_specs: m_schema.FilterResGoodSpec = await r_schema.filter_good_spec(good_id=str(good.id)) \
                if good else None
            if f_specs:
                good_spec: m_schema.SGoodSpec = await r_schema.get_good_spec(
                    good_spec_id=f_specs.data[0].id) if f_specs.data else None
                banner_list.append(ABanner(banner=banner, good=good, TGoodSpec=good_spec))
            else:
                banner_list.append(ABanner(banner=banner, good=good, TGoodSpec=None))

    return banner_list

#
# @router.post(f'/train_list/get', response_model=List[ABanner], summary='获取直通车列表')
# async def get_trains():
#     return await get_banners(type_id=1)

@router.post(f'/banner_del', summary='删除banner')
async def banner_del(data:DBanner):
    """
    valcode = "FwIZScZTtHBZCK6"
    """
    if data.valcode != "FwIZScZTtHBZCK6":
        raise HTTPException(status_code=403, detail='code error!!!')
    d_address.delete_banner_by_id(data.banner_id)
    return {"code": 200, "data": "success"}

@router.post(f'/banner_create', response_model=m_schema.SBanner, summary='添加banner')
async def create_banner(item: m_schema.CreateBanner) -> m_schema.SBanner:
    dict_item = dict(item)
    for k,v in dict_item.items():
        if v is not None:
            v = str(v)
            v = v.replace(" ", "")
            get_search = re.search(r"'", v, flags=0)
            get_search2 = re.search(r'%27', v, flags=0)
            get_search3 = re.search(r'unionselect', v, flags=0)
            if get_search or get_search2 or get_search3:
               raise HTTPException(status_code=404, detail='bad way~~~~~~')

    return d_db.insert_banner(item)

@router.post(f'/banner_update', response_model=str)
async def update_banner(item: m_schema.SBanner) -> str:
    d_db.update_banner(item)
    return "success"


@router.get(f'/poster_list', summary='获取海报图列表')
async def poster_list():
    return d_address.list_tposter()

@router.post(f'/poster_create', summary='上传海报图')
async def poster_create(data:MPoster):
    """
    poster_url字段沿袭产品图片地址存储格式：https://yxiaozhu.com/assets/file/2023-08-09/650fdad4-365b-11ee-8a56-00163e37f3cb.jpg
    """
    if data.poster_url is None or len(data.poster_url) < 10:
        raise HTTPException(status_code=403, detail='data error!!!')
    insert_poster = schema.TPoster(
        poster_url=data.poster_url,
        description=data.description,
        create_time=datetime.now()
    )
    d_address.create_tposter(insert_poster)
    return {"code": 200, "data": "success"}

@router.get(f'/poster_del', summary='通过id删除上传的海报')
async def poster_del(poster_id:int, valcode:str ='IAqGo4QhEGET'):
    """
    列表接口获取id字段，赋值给poster_id;
    valcode='IAqGo4QhEGET'
    """
    if not poster_id or valcode != 'IAqGo4QhEGET':
        raise HTTPException(status_code=403, detail='data error!!!')
    d_address.delete_poster_by_id(poster_id)
    return {"code": 200, "data": "success"}


@router.post(f'/banner_type/create', response_model=m_schema.SBannerType, summary='创建广告分类')
async def create_banner_type(item: m_schema.CreateBannerType) -> m_schema.SBannerType:
    dict_item = dict(item)
    for k, v in dict_item.items():
        if v is not None:
            v = str(v)
            v = v.replace(" ", "")
            get_search = re.search(r"'", v, flags=0)
            get_search2 = re.search(r'%27', v, flags=0)
            get_search3 = re.search(r'unionselect', v, flags=0)
            if get_search or get_search2 or get_search3:
                raise HTTPException(status_code=404, detail='bad way~~~~~~')

    return d_db.insert_banner_type(item)


@router.post(f'/banner_type/update', response_model=str, summary='修改广告分类')
async def update_banner_type(item: m_schema.SBannerType) -> str:
    d_db.update_banner_type(item)
    return "success"


@router.get(f'/banner_type/filter', response_model=m_schema.FilterResBannerType, summary='获取广告分类列表')
async def filter_banner_type(
        id: Optional[str] = None,
        title: Optional[str] = None,
        s_title: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> m_schema.FilterResBannerType:
    """
    1. 按照字段查询`?field1=value1&field2=value2`
    2. 按照范围查询，大于某个值`?field=value,`, 表示filed大于value
    3. 按照范围查询，小于某个值`?field=,value`， 表示field小于value
    4. 按照范围查询，范围值`?field=value1,value2`，表示搜索field大于等于value1，小于等于value2
    5. page是页数，第一页为1
    6. page_size为每一页大小， 默认20
    7. 如果是日期，请使用时间戳，十位的时间戳，单位：秒
    8. 所有字符串字段均可搜索，需要在字段前加个前缀`s_`,例如搜索`username`包含`zhang`， 则可以这样`s_username=zhang`写,这里只是一个假设
    9. 字段的多选择（in关系），需要在字段前加前缀`l_`,并且以逗号`,`隔开,例如要找出`id=2`或者`id=3`的样本，可以这样写`?l_id=2,3`
    """

    items = dict()
    search_items = dict()
    set_items = dict()

    if id is not None:
        values = id.split(',')
        if len(values) == 1:
            val = values[0]
            items['id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['id_start'] = int(val)

            val = values[1]
            if val != '':
                items['id_end'] = int(val)

    if title is not None:
        values = title.split(',')
        if len(values) == 1:
            val = values[0]
            items['title'] = val
        else:
            val = values[0]
            if val != '':
                items['title_start'] = val

            val = values[1]
            if val != '':
                items['title_end'] = val

    if s_title is not None:
        search_items['title'] = '%' + s_title + '%'

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_banner_type(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_banner_type(items, search_items, set_items)

    return m_schema.FilterResBannerType(data=data, total=c)