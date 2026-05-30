from datetime import datetime
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.orm import Query

from common import Dao
from common.db import SessionLocal
from dao import d_good, d_db, d_admin
from model import m_schema
from model import schema
from model.mall import m_good
from model.schema import TGoodSpec, TGood
from router import r_schema
from model.res import common
from sqlalchemy.ext.declarative import declarative_base
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field
from model.m_schema import *
import re
from router.admin.user import verify_token

from service import create_service


Base = declarative_base()
metadata = Base.metadata

router = APIRouter(dependencies=[Depends(verify_token)])

class UpdatePriority(BaseModel):
    good_id: int = Field(title='t_good产品id')
    priority_num: int = Field(title='优先级，数字越大排序越靠前')
#
# @router.post(f'/good_details/create', response_model=common.SuccessResponse, summary='添加商品详情接口')
# async def create_good_detail(item: m_good.CreateRealGoodDetail) -> common.SuccessResponse:
#     """
#         1.图片第一张作为商品的主图
#         2.规格数据结构：  [结构Json] @@ [数据表Json]
#         例如：[{"title":"规格","val":[{"v":"鸡蛋"}]}]@@[{"规格":"1瓶装","库存":"0","克重":"0","成本":"0","售价":"199","会员价":"0","直推":"0","分享":"0","随机分":"0","图片":"https://xxxx.com/assets/image/2024-08-30/3fdfea1a-667f-11ef-8b83-00163e37f3cb.jpg"}},
#         3。当用户选择某个规格，订单提交规格的一个Jsong结构数据：
#         {"规格":"1瓶装","库存":"0","克重":"0","成本":"0","售价":"199","会员价":"0","直推":"0","分享":"0","随机分":"0","图片":"https://xxxx.com/assets/image/2024-08-30/3fdfea1a-667f-11ef-8b83-00163e37f3cb.jpg"}
#     """
#     item.good.image_url = item.images[0] if item.images else None
#     # 后期这块可能要设置商品推荐人默认为商家推荐人
#     # if item.introducer is not None:
#     #     item.good.introducer_id = item.introducer.id
#     s_good: m_schema.SGood = await r_schema.create_good(item.good)
#
#     if s_good is not None:
#
#         for image in item.images:
#             await r_schema.create_good_image(m_schema.CreateGoodImage(good_id=s_good.id, image=image))
#
#         for delivery_rule in item.delivery_rules:
#             delivery_rule.good_id = s_good.id
#             await r_schema.create_delivery_rule(delivery_rule)
#
#         # for spec in item.specs:
#         #     spec.good_id = s_good.id
#         #     await r_schema.create_good_spec(spec)
#
#         for text in item.texts:
#             text.good_id = s_good.id
#             await r_schema.create_good_text(text)
#
#         return common.SuccessResponse(code=200, message='success', data={'good_id': s_good.id})


@router.post('/good/create', summary='添加商品详情接口')
async def create_good(data: dict) -> dict:
    """
        1.图片第一张作为商品的主图
        2.规格数据结构：  [结构Json] @@ [数据表Json]
        例如：[{"title":"规格","val":[{"v":"鸡蛋"}]}]@@[{"规格":"1瓶装","库存":"0","克重":"0","成本":"0","售价":"199","会员价":"0","直推":"0","分享":"0","随机分":"0","积分":"0","图片":"https://xxxx.com/assets/image/2024-08-30/3fdfea1a-667f-11ef-8b83-00163e37f3cb.jpg"}},
        3。当用户选择某个规格，订单提交规格的一个Jsong结构数据：
        {"规格":"1瓶装","库存":"0","克重":"0","成本":"0","售价":"199","会员价":"0","直推":"0","分享":"0","随机分":"0","积分":"0","图片":"https://xxxx.com/assets/image/2024-08-30/3fdfea1a-667f-11ef-8b83-00163e37f3cb.jpg"}
        4.`model_id` int DEFAULT NULL COMMENT '所属团长id'
        5. `coinable_number` int DEFAULT NULL COMMENT '优惠券可用额度'
    """
    if len(data['good_image']) == 0:
        raise HTTPException(status_code=400, detail='商品图片不能为空')
    if data['good'].get('image_url') is None:
        raise HTTPException(status_code=400, detail='商品主图不能为空')

    #data['good']['image_url'] = data['good_image'][0]['image']

    return create_service.create(data)


def update_good_items(table, items, good_id: int, db: SessionLocal):
    """
        更新表中的数据
    """
    # 查询老数据
    old_ids = db.query(table.id).filter(table.good_id == good_id).all()
    old_ids = [item.id for item in old_ids]

    # 根据id查看新老数据交集
    new_ids = [item.id for item in items if id is not None]
    intersection_ids = set(old_ids).intersection(set(new_ids))

    # 应该删除的数据
    delete_ids = set(old_ids).difference(intersection_ids)
    for delete_id in delete_ids:
        # if not isinstance(table, schema.TGoodSpec):
        if table != schema.TGoodSpec:
            db.query(table).filter(table.id == delete_id).delete()

    # 应该添加的数据
    for item in items:
        if item.id is None:
            # 没有id的数据，直接添加
            item.good_id = good_id
            item_dict = item.dict()
            item_dict.pop('id')
            item = table(**item_dict)
            db.add(item)
        else:
            # 有id的数据，更新
            db.query(table).filter(table.id == item.id).update(item.dict())
    db.flush()


def update_good_spec_items(table, items, db: SessionLocal):
    """
        更新表中的数据
    """
    if len(items) == 0:
        return

    for item in items:
        if item.good_spec_id is None:
            raise HTTPException(status_code=400, detail=f'{table.__tablename__}数据中good_spec_id为空,但是其不能为空')


    for item in items:
        if item.id is None:
            # 没有id的数据，直接添加
            item_dict = item.dict()
            item_dict.pop('id')
            item = table(**item_dict)
            db.add(item)
        else:
            # 有id的数据，更新
            db.query(table).filter(table.id == item.id).update(item.dict())



def update_good_item(table, item, good_id: int, db: SessionLocal):
    """
        更新表中的数据
    """
    item.good_id = good_id
    item_dict = item.dict()
    if 'id' not in item_dict:
        error_info = f'更新数据的{table.__tablename__}没有id'
        logging.error(error_info)
        raise HTTPException(status_code=400, detail=error_info)

    item_dict.pop('id')
    if item.id is None:
        old_item = db.query(table).filter(table.good_id == good_id).first()
        if old_item is None:
            # 没有数据，直接添加
            db.add(table(**item_dict))
        else:
            raise HTTPException(status_code=400, detail=f'前后端数据不一致，商品id为{good_id}的商品已经存在{table.__tablename__}数据,但是更新数据的{table.__tablename__}没有id或为空')
    else:
        # 有数据，更新
        db.query(table).filter(table.id == item.id).update(item_dict)

    db.flush()


@router.post(f'/good_details/update', summary='更新商品详情 包邮模板 图片等')
async def update_good_detail(item: m_good.UpdateGoodDetail):
    """
        1.图片第一张作为商品的主图
        2.规格数据结构：  [结构Json] @@ [数据表Json]
        例如：[{"title":"规格","val":[{"v":"鸡蛋"}]}]@@[{"规格":"1瓶装","库存":"0","克重":"0","成本":"0","售价":"199","会员价":"0","直推":"0","分享":"0","随机分":"0","图片":"https://xxxx.com/assets/image/2024-08-30/3fdfea1a-667f-11ef-8b83-00163e37f3cb.jpg"}},
        3。当用户选择某个规格，订单提交规格的一个Jsong结构数据：
        {"规格":"1瓶装","库存":"0","克重":"0","成本":"0","售价":"199","会员价":"0","直推":"0","分享":"0","随机分":"0","图片":"https://xxxx.com/assets/image/2024-08-30/3fdfea1a-667f-11ef-8b83-00163e37f3cb.jpg"}
    """
    with Dao() as db:
        # 更新商品
        if not item.good_image:
            raise HTTPException(status_code=400, detail='商品图片不能为空')
            #item.good.image_url = item.good_image[0].image
        db.query(TGood).filter(TGood.id == item.good.id).update(item.good.dict())

        # 更新邮寄规则
        update_good_items(table=schema.TDeliveryRule, items=item.delivery_rule, good_id=item.good.id, db=db)

        # 更新商品图片
        update_good_items(table=schema.TGoodImage, items=item.good_image, good_id=item.good.id, db=db)

        # 更新商品购买规则
        # if item.good_rule:
        #     update_good_item(table=schema.TGoodRule, item=item.good_rule, good_id=item.good.id, db=db)

        # 更新商品规格
        # update_good_items(table=schema.TGoodSpec, items=item.good_spec, good_id=item.good.id, db=db)

        # 更新套餐信息
        # update_good_spec_items(table=schema.TGoodSpecCombo, items=item.good_spec_combo, db=db)

        # 更新规格图文详情
        # update_good_spec_items(table=schema.TGoodSpecDetail, items=item.good_spec_detail, db=db)

        # 更新图文详情
        if item.good_text:
            update_good_item(table=schema.TGoodText, item=item.good_text, good_id=item.good.id, db=db)

        db.commit()

    return common.SuccessResponse(code=200)


# @router.post(f'/good_details/delete', summary='删除商品详情 包邮模板 规格 图片等')
# async def delete_good_detail(good_id: int):
#     """
#        删除商品详情接口，同样调用了 r_schema 文件内的方法
#     """
#     await r_schema.delete_good(good_id)
#
#     # 查询商品id对应的图片id 并删除图片
#     fg_good: m_schema.FilterResGoodImage = await r_schema.filter_good_image(good_id=str(good_id))
#     images: List[m_schema.SGoodImage] = fg_good.data
#     for img in images:
#         await r_schema.delete_good_image(good_image_id=img.id)
#
#     # 查询商品id对应的介绍人id 并删除介绍人
#     f_good: m_schema.FilterResGood = await r_schema.filter_good(id=str(good_id))
#     good_list: List[m_schema.SGood] = f_good.data
#     for good in good_list:
#         await r_schema.delete_good_introducer(good_introducer_id=good.introducer_id)
#
#     # 查询商品id对应的规格id  并删除规格
#     f_spec: m_schema.FilterResGoodSpec = await r_schema.filter_good_spec(good_id=str(good_id))
#     specs: List[m_schema.SGoodSpec] = f_spec.data
#     for spec in specs:
#         await r_schema.delete_good_spec(good_spec_id=spec.id)
#
#     # 查询商品id对应的图文id  并删除图文
#     f_text: m_schema.FilterResGoodText = await r_schema.filter_good_text(good_id=str(good_id))
#     texts: List[m_schema.SGoodText] = f_text.data
#     for text in texts:
#         await r_schema.delete_good_text(good_text_id=text.id)
#
#     return 'success'
#
#
# @router.post(f'/good_details/add', response_model=common.SuccessResponse, summary='添加使用规则、使用人数、套餐区')
# async def create_card_good_detail(item: m_good.AddGoodDetail) -> common.SuccessResponse:
#     await r_schema.create_good_rule(item.rules)
#
#     for package in item.packages:
#         await r_schema.create_good_package(package)
#
#     # for person in item.persons:
#     #    await r_schema.create_good_person(person)
#
#     return common.SuccessResponse(code=200, message='success')
#
#
# @router.get(f'/schema/category_lower/filter', response_model=m_good.ResCategory, summary='全部商品类别')
# async def get_good_category():
#     category_list: List[m_schema.SCategory] = d_db.filter_category(items={}, search_items={}, set_items={})
#     c_list = []
#     for category in category_list:
#         c_list.append(m_good.GoodCategory(id=category.id, title=category.name))
#     return m_good.ResCategory(data=c_list, total=c_list.__len__())
#
#
# @router.get(f'/good_list/on_sell', response_model=m_good.AGoodList, summary='获取上架商品列表')
# async def on_sell_good_list(page: int = 1, page_size: int = 20):
#     return await d_good.get_good_detail(status=1, good_id=None, good_name=None, good_type=None, coinable=None,
#                                         expired=None, page=page, page_size=page_size)
#
#
# @router.get(f'/good_list/off_sell', response_model=m_good.AGoodList, summary='获取下架商品列表')
# async def off_sell_good_list(page: int = 1, page_size: int = 20):
#     return await d_good.get_good_detail(status=0, good_id=None, good_name=None, good_type=None, coinable=None,
#                                         expired=None, page=page, page_size=page_size)
#
#
# @router.get(f'/good_list/expired', response_model=m_good.AGoodList, summary='获取临期商品列表')
# async def expired_good_list(page: int = 1, page_size: int = 20):
#     return await d_good.get_good_detail(expired=1, good_id=None, good_name=None, good_type=None, coinable=None,
#                                         status=None, page=page, page_size=page_size)
#
#
# @router.get(f'/good_list/real', response_model=m_good.AGoodList, summary='获取实体商品数据')
# async def real_good_data(page: int = 1, page_size: int = 20):
#     return await d_good.get_good_detail(good_type=1, good_id=None, good_name=None, coinable=None, status=None,
#                                         expired=None, page=page, page_size=page_size)
#
#
# @router.get(f'/good_list/card', response_model=m_good.AGoodList, summary='获取卡券商品数据')
# async def real_good_data(page: int = 1, page_size: int = 20):
#     return await d_good.get_good_detail(good_type=0, good_id=None, good_name=None, coinable=None, status=None,
#                                         expired=None, page=page, page_size=page_size)
#
#
@router.get(f'/good_list/search', response_model=m_good.AGoodList, summary='商品列表搜索')
async def search_good_list(good_id: Optional[int] = None, good_name: Optional[str] = None, status: Optional[int] = None,
                           good_type: Optional[int] = None, coinable: Optional[str] = None,
                           expired: Optional[int] = None, is_video: Optional[int] = None, page: int = 1, page_size: int = 20):
    """
        1. good_id:    商品id
        2. good_name:  商品名称，模糊搜索，如'美丽'可以搜出漾美丽保湿喷雾
        3. status:     0表示下架   1表示上架
        4. good_type:  0表示卡券   1表示实体
        5. coinable:   0表示不可用积分   1表示可用积分
        6. expired:    1表示临期商品   其他数据无效
    """
    return await d_good.get_good_detail(good_id, good_name, status, good_type, coinable, expired, is_video, page, page_size)

#
# @router.get(f'/good_list/get', response_model=m_good.AGoodList, summary='商品列表搜索')
# async def get_good_list(good_id: Optional[int] = None, good_name: Optional[str] = None, status: Optional[int] = None,
#                         good_type: Optional[int] = None, coinable: Optional[str] = None,
#                         expired: Optional[int] = None, page: int = 1, page_size: int = 20):
#     return await d_good.get_good_detail(good_id, good_name, status, good_type, coinable, expired, page, page_size)
#
# @router.get('/good_spec/filter')
# async def filter_good_spec(id: Optional[int] = None, keyword: Optional[str] = None, page: int = 1, page_size: int = 10):
#     with Dao() as db:
#         query: Query = db.query(TGoodSpec, TGood).join(TGood, TGood.id==TGoodSpec.good_id)
#         if id:
#             query = query.filter(TGoodSpec.good_id == id)
#         if keyword:
#             query = query.filter(TGood.title.like(f'%{keyword}%'))
#         total = query.count()
#         query = query.offset((page - 1) * page_size).limit(page_size)
#         return {"data": query.all(), "total": total}
#
@router.get(f'/good_details/get', summary='获取商品详情')
async def good_details_get(good_id:int):
    res = d_good.get_good_info(good_id)
    return res

# @router.post('/create', summary='创建商品')
# async def create_good(data: dict) -> dict:
#     if len(data['good_image']) == 0:
#         raise HTTPException(status_code=400, detail='商品图片不能为空')
#     if data['good'].get('image_url') is None:
#         raise HTTPException(status_code=400, detail='商品主图不能为空')
#
#     #data['good']['image_url'] = data['good_image'][0]['image']
#
#     return create_service.create(data)

@router.post('/update_priority', summary='修改商品优先级')
async def update_priority(data: UpdatePriority):
    if data.good_id is None or data.priority_num is None:
        raise HTTPException(status_code=400, detail='参数错误')
    d_good.update_good_priority(data.good_id, data.priority_num)
    return {"status":200, "message":'success'}

@router.post(f'/good_category/create', response_model=SGoodCategory, summary='创建商品分类')
async def create_good_category(item: CreateGoodCategory) -> SGoodCategory:
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

    return d_db.insert_good_category(item)

@router.post(f'/good_category/update', response_model=str, summary='修改分类')
async def update_good_category(item: SGoodCategory) -> str:
    d_db.update_good_category(item)
    return "success"

@router.get(f'/good_category/get', response_model=SGoodCategory, summary='获取商品分类详情')
async def get_good_category(good_category_id: int) -> SGoodCategory:
    return d_db.get_good_category(good_category_id)

@router.get(f'/good_category/filter', response_model=FilterResGoodCategory, summary='获取分类列表')
async def filter_good_category(
        id: Optional[str] = None,
        title: Optional[str] = None,
        general_id: Optional[str] = None,
        l_id: Optional[str] = None,
        l_title: Optional[str] = None,
        l_general_id: Optional[str] = None,
        s_title: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 20) -> FilterResGoodCategory:
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

    if general_id is not None:
        values = general_id.split(',')
        if len(values) == 1:
            val = values[0]
            items['general_id'] = int(val)
        else:
            val = values[0]
            if val != '':
                items['general_id_start'] = int(val)

            val = values[1]
            if val != '':
                items['general_id_end'] = int(val)

    if s_title is not None:
        search_items['title'] = '%' + s_title + '%'

    if l_id is not None:
        values = l_id.split(',')
        values = [int(val) for val in values]
        set_items['id'] = values

    if l_title is not None:
        values = l_title.split(',')
        values = [val for val in values]
        set_items['title'] = values

    if l_general_id is not None:
        values = l_general_id.split(',')
        values = [int(val) for val in values]
        set_items['general_id'] = values

    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_good_category(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_good_category(items, search_items, set_items)

    return FilterResGoodCategory(data=data, total=c)