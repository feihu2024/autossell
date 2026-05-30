from fastapi import APIRouter, HTTPException, Body, Depends, Request
from sqlalchemy.engine import Row
from sqlalchemy import or_, func
from dao import d_account
from model.m_schema import *

from common import Dao
from dao import d_query, d_db, d_user, d_comment, d_order
from model import schema
from model.mall_res import GoodResponse
from service import jxhh_service
import datetime
import re
from typing import Optional
from .user import verify_token

router = APIRouter(dependencies=[Depends(verify_token)])

def fill_spec_field(item: Row) -> dict:
    good_spec_id = item['min_good_spec_id']
    good_spec = d_db.get_good_spec(good_spec_id=good_spec_id)
    new_item = dict()
    new_item['TGoodSpec'] = good_spec.dict() if good_spec else None
    new_item['TGood'] = item['TGood']
    return new_item

@router.get('/bdgood_list', summary='获取上架团长商品列表')
async def bdgood_list(page:int = 1, page_size:int = 10, sir_id:int = 0):
    """
    参数为用户id，用来获取该用户的推荐物品(好物推荐),
    page:当前页码，默认1.
    page_size：每页做多条数，默认10
    status=1,上架商品
    type=0, 普通商品
    sir_id,团长id
    """
    if sir_id > 0:
        query_data = d_query.FilterGroupQueryData.parse_obj({
            "table": "good",
            "joins": [
                {
                    "table": "good_spec",
                    "on_left": "id",
                    "on_right": "good_id"
                }
            ],
            "selects": ["good", "min(good_spec.id)"],
            # "group_by": ["good.id"],
            "filters": [
                {
                    "field": "good.status",
                    "value": 1
                },
                {
                    "field": "good.type",
                    "value": 0
                },
                {
                "field": "good.model_id",
                "value":sir_id
                }
                # {
                # "field": "good_spec.is_default",
                # "op": ">",
                # "value":1
                # },
                # {
                # "field": "good.is_wholesale",
                # "value":0
                # }
            ],
            "order_by": [{"field": "good.priority", "order": "desc"},{"field": "good.id", "order": "desc"}],
            "page":page,
            "page_size":page_size
        })
        # res = d_query.group_filter(query_data)
        res = d_query.filter_items(query_data)
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
        return {"code": 0, "data": res['data'], 'total': res['total']}
    else:
        return {"code": 0, "data": {}, "total": 0}
    # return jxhh_service.recommend(page=1, limit=40)


@router.get('/generalgood_list', summary='获取上架普通商品列表')
async def generalgood_list(page:int = 1, page_size:int = 10):
    """
    参数为用户id，用来获取该用户的推荐物品(好物推荐),
    page:当前页码，默认1.
    page_size：每页做多条数，默认10
    status=1,上架商品
    type=0, 报单商品
    """
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "good",
        "selects": ["good"],
        "filters": [
            {
                "field": "good.status",
                "value": 1
            },
            {
                "field": "good.type",
                "value": 0
            },
            {
                "field": "good.is_video",
                "value": 0
            }
        ],
        "order_by": [{"field": "good.priority", "order": "desc"},{"field": "good.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res


@router.get('/firstbag_list', summary='获取团长首单礼包列表')
async def firstbag_list(page:int = 1, page_size:int = 10, sir_id:int = 0):
    """
    参数为用户id，用来获取该用户的推荐物品(好物推荐),
    page:当前页码，默认1.
    page_size：每页做多条数，默认10
    sir_id=0, 团长id，默认为系统礼包
    """
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "bigorder_initbag",
        # "joins": [
        #     {
        #         "table": "good_spec",
        #         "on_left": "id",
        #         "on_right": "good_id"
        #     }
        # ],
        "selects": ["bigorder_initbag"],
        # "selects": ["good", "min(good_spec.id)"],
        # "group_by": ["good.id"],
        "filters": [
            {
                "field": "bigorder_initbag.tuan_id",
                "value": sir_id
            }
            # {
            # "field": "good.expired_time",
            # "op": ">",
            # "value":datetime.datetime.now()
            # },
            # {
            # "field": "good_spec.is_default",
            # "value":1
            # },
            # {
            # "field": "good.is_wholesale",
            # "value":0
            # }
        ],
        "order_by": [{"field": "bigorder_initbag.price_total", "order": "desc"},{"field": "bigorder_initbag.id", "order": "desc"}],
        "page":page,
        "page_size":page_size
    })
    res = d_query.group_filter(query_data)
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

    return {"code": 0, "data": res['data'], "total": res['total']}



@router.get('/video_pro/list', summary='获取视频礼包商品列表')
async def video_pro_list(page:int = 1, page_size:int = 10):
    """
    参数为用户id，用来获取该用户的推荐物品(好物推荐),
    page:当前页码，默认1.
    page_size：每页做多条数，默认10
    status=1,上架商品
    type=0, 报单商品
    """
    query_data = d_query.FilterGroupQueryData.parse_obj({
        "table": "good",
        "selects": ["good"],
        "filters": [
            {
                "field": "good.status",
                "value": 1
            },
            {
                "field": "good.is_video",
                "value": 1
            }
        ],
        "order_by": [{"field": "good.priority", "order": "desc"},{"field": "good.id", "order": "desc"}],
        "page": page,
        "page_size": page_size
    })
    res = d_query.filter_items(query_data)
    return res

#
# @router.get('/myselfgood')
# async def myselfgood(user_id: int, page:int = 1, page_size:int = 10):
#     """
#     获取自营商品
#     参数为用户id，用来获取该用户的推荐物品(好物推荐),
#     page:当前页码，默认1.
#     page_size：每页做多条数，默认10
#     """
#     query_data = d_query.FilterGroupQueryData.parse_obj({
#         "table": "good",
#         "joins": [
#             {
#                 "table": "good_spec",
#                 "on_left": "id",
#                 "on_right": "good_id"
#             }
#         ],
#         # "selects": ["good", "min(good_spec.id)"],
#         "selects": ["good", "min(good_spec.id)"],
#         "group_by": ["good.id"],
#         "filters": [
#             {
#                 "field": "good.status",
#                 "value": 1
#             },
#             {
#                 "field": "good_spec.status",
#                 "value": 1
#             },
#             {
#             "field": "good.expired_time",
#             "op": ">",
#             "value":datetime.datetime.now()
#             },
#             {
#             "field": "good_spec.is_default",
#             "value":1
#             },
#             {
#             "field": "good.is_wholesale",
#             "value":0
#             },
#             {
#             "field": "good.sale_type",
#             "value":0
#             }
#         ],
#         "order_by": [{"field": "good.priority", "order": "desc"},{"field": "good.id", "order": "desc"}],
#         "page":page,
#         "page_size":page_size
#     })
#     res = d_query.group_filter(query_data)
#     items = list(map(fill_spec_field, res['data']))
#     if user_id:
#         t_user = d_user.get_user_by_id(user_id)
#         if t_user:
#             # 更新系统用户级别
#             if t_user.level_id == 0:
#                 d_user.update_sysuser_active(t_user.id)
#             elif t_user.level_id == 1:
#                 d_user.update_sysuser_high(t_user.id)
#             elif t_user.level_id == 2:
#                 d_user.update_sysuser_top(t_user.id)
#             # 更新推广用户级别
#             d_user.update_user_top(user_id)
#
#     return {"code": 0, "data": items, "total": res['total']}

# @router.get('/zhongcao_recommend')
# async def zhongcao_recommend(user_id: int):
#     """
#     种草推荐区，参数为用户id，根据用户id提供种草推荐区
#     """
#     query_data = d_query.FilterQueryData.parse_obj({
#         "table": "banner",
#         "joins": [
#             {
#                 "table": "good",
#                 "on_left": "good_id",
#                 "on_right": "id"
#             },
#             {
#                 "table": "good_spec",
#                 "on_left": "good_spec_id",
#                 "on_right": "id"
#             }
#         ],
#         "filters": [{
#             "field": "type_id",
#             "value": 1
#         }]
#     })
#     res = d_query.filter_items(query_data)
#     return {"code": 0, "data": res['data'], 'total': res['total']}
#     # return jxhh_service.recommend(page=1, limit=5)
#
#
# @router.get('/zhongcao_food', response_model=GoodResponse)
# async def zhongcao_food(user_id: int) -> GoodResponse:
#     """
#     种草美食，参数为用户id，根据用户id提供种草美食
#     """
#     return jxhh_service.recommend(page=1, limit=5)
#
#
# @router.get('/search')
# async def search(user_id: int, keyword: str, is_wholesale:int = None, page: int = 1, page_size: int = 10):
#     with Dao() as db:
#         goods = db.query(schema.TGood, func.min(schema.TGoodSpec.id).label('min_good_spec_id'))\
#             .outerjoin(schema.TGoodSpec, schema.TGoodSpec.good_id==schema.TGood.id)\
#             .filter(schema.TGood.status == 1) \
#             .filter(schema.TGoodSpec.status == 1) \
#             .filter(schema.TGoodSpec.is_default == 1) \
#             .filter(
#             or_(
#                 schema.TGood.name.like(f'%{keyword}%'),
#                 schema.TGood.title.like(f'%{keyword}%'),
#                 schema.TGood.subtitle.like(f'%{keyword}%')
#             ))
#
#         if is_wholesale is not None:
#             goods = goods.filter(schema.TGood.is_wholesale == is_wholesale)
#         goods = goods.group_by(schema.TGood.id).order_by(schema.TGood.id.desc())\
#             .offset((page - 1) * page_size).limit(page_size).all()
#
#         items = list(map(fill_spec_field, goods))
#
#         return {"code": 0, "data": items}
#
#
# @router.post('/setcomment')
# async def setcomment(data: d_comment.TComment):
#     """
#     用户提交反馈，文本方式
#     """
#     if data.user_id is None or data.phone is None:
#         raise HTTPException(status_code=400, detail="缺少用户信息")
#     if data.content is None:
#         raise HTTPException(status_code=400, detail="缺少提交数据")
#     phone_search = re.search(r'\'', data.phone, flags=0)
#     user_search = re.search(r'\'', str(data.user_id), flags=0)
#     content_search = re.search(r'\'', data.content, flags=0)
#     if phone_search or user_search or content_search:
#         raise HTTPException(status_code=400, detail="非法数据")
#     d_comment.insert_comment(data)
#     return {"code": 200, "data": "success"}
#
# @router.get('/comment_filter', summary='反馈信息列表')
# async def filter(
#         user_id: Optional[int] = None,
#         phone: Optional[str] = None,
#         page: int = 1,
#         page_size: int = 10
# ):
#     return d_comment.get_filter(user_id, phone, page, page_size)
#
# @router.get('/get_notice', summary='小程序端获取通知消息')
# async def get_notice(
#         user_id: Optional[str] = None,
#         page: int = 1,
#         page_size: int = 20
# ):
#     re_data = {"total":0, "data":''}
#     with Dao() as db:
#         notices = db.query(schema.TNotice).filter(or_(schema.TNotice.user_ids.like(f'%{user_id}%'), schema.TNotice.user_ids == 'all'))\
#             .filter(schema.TNotice.status == 0)\
#             .order_by(schema.TNotice.id.desc())
#         re_data['total'] = notices.count()
#         re_data['data'] = notices.offset((page - 1) * page_size).limit(page_size).all()
#         return re_data

@router.get(f'/global/set/get', response_model=SBigorderSet, summary='获取全局配置')
async def get_bigorder_set(set_id: int) -> SBigorderSet:
    return d_db.get_bigorder_set(set_id)

