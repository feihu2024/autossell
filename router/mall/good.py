from fastapi import APIRouter
from pydantic import BaseModel
from dao import d_good, d_query, d_db, d_product, d_user, d_car
from model import m_schema
from common import Dao
from model.mall import m_good
from router import r_schema
from model import schema
from model.schema import TStore
from typing import List, Optional
from model.mall.good_favs import TGoodFav
from fastapi.exceptions import HTTPException
from datetime import datetime

from model.schema import TCart, TGood, TGoodSpec, TGoodImage
from service import create_service


router = APIRouter()

#
# @router.post(f'/create_favorite')
# def create_good_fav(user_id: int, good_id: int):
#     item = TGoodFav(user_id=user_id, good_id=good_id)
#     d_good.insert_good_fav(item)
#     return {'code': 200, 'message': 'success'}
#
#
# @router.post(f'/remove_favorite')
# def remove_good_fav(user_id: int, good_id: int):
#     d_good.remove_good_fav(user_id, good_id)
#     return {'code': 200, 'message': 'success'}
#
#
# @router.post(f'/get_favorites')
# def get_good_favorites(user_id: int):
#     t_favorites = d_good.get_good_fvs(user_id=user_id)
#     return [{'user_id': t.user_id, 'good_id': t.good_id} for t in t_favorites]
#     # return [TGoodFav.parse_obj(t.__dict__) for t in t_favorites]

#
# @router.get('/good_spec/{good_id}')
# async def get_good_spec(good_id: int):
#     query_data = d_query.FilterQueryData.parse_obj({
#         "table": "good_spec",
#         "joins": [
#         ],
#         "filters": [{
#             "field": "good_id",
#             "value": good_id
#         },{
#                 "field": "status",
#                 "value": 1
#             }],
#         "order_by":[{
#             "field": "id",
#             "order": "asc"
#         }]
#     })
#     res = d_query.filter_items(query_data)
#     return {"code": 0, "data": res['data'], "total": res['total']}


@router.get('/detail', summary='商品详情')
async def get_detail(good_id: int):
    query_data = d_query.QueryData.parse_obj({
        "table": "good",
        "joins": [
            # {"table": "good", "on_left": "good_id", "on_right": "id"},
            # {"table": "good_image", "on_left": "good.id", "on_right": "good_id"},
            {"table": "good_text", "on_left": "good.id", "on_right": "good_id"},
            {"table": "good_spec_image", "on_left": "good.id", "on_right": "spec_id"},
            {"table": "supplier", "on_left": "good.supplier_id"}
        ],
        "filters": [{
            "field": "good.id",
            "value": good_id
        }]
    })
    res = d_query.get(query_data)
    if res['data'] is None:
        raise HTTPException(status_code=400, detail='没有发现该商品')
    item = res['data']._asdict()

    if res['data']['TGood'] is None:
        raise HTTPException(status_code=400, detail='没有商品信息')
    item['TGoodRule'] = d_db.filter_good_rule(items={'good_id': res['data']['TGood'].id}, search_items={}, set_items={},
                                              page=1, page_size=100)
    with Dao() as db:
        item['TStoreNum'] = db.query(TStore).filter(TStore.supplier_id==item['TGood'].supplier_id).count()
        item['good_image'] = db.query(TGoodImage).filter(TGoodImage.good_id==item['TGood'].id).all()

    # item['TGoodSpecCombo'] = d_db.filter_good_spec_combo(items={'good_spec_id': spec_id}, search_items={},
    #                                                     set_items={}, page=1, page_size=1000)

    item['TDeliveryRule'] = d_db.filter_delivery_rule(items={'good_id': res['data']['TGood'].id}, search_items={},
                                                        set_items={}, page=1, page_size=1000)

    return {"code": 0, "data": item}



@router.get('/first_detail', summary='获取首单礼品详情')
async def get_first_detail(first_id: int):
    query_data = d_query.QueryData.parse_obj({
        "table": "bigorder_initbag",
        "joins": [
            # {"table": "good", "on_left": "good_id", "on_right": "id"},
            # {"table": "good_image", "on_left": "good.id", "on_right": "good_id"},
            {"table": "user", "on_left": "bigorder_initbag.tuan_id", "on_right": "id"}
        ],
        "filters": [{
            "field": "bigorder_initbag.id",
            "value": first_id
        }]
    })
    res = d_query.get(query_data)
    if res['data'] is None:
        raise HTTPException(status_code=400, detail='没有发现该礼品')
    item = res['data']._asdict()

    # if res['data']['bigorder_initbag'] is None:
    #     raise HTTPException(status_code=400, detail='没有礼品信息')

    return {"code": 0, "data": item}


# @router.get('/collect', response_model=dict, summary="查询商品是否收藏接口")
# async def get_collect(spec_id: int, user_id: int):
#     item = {'user_id': user_id, 'spec_id': spec_id}
#     s_user_collects: List[m_schema.SUserFav] = d_db.filter_user_fav(items=item, search_items={}, set_items={})
#     if s_user_collects:
#         return {"code": 0, "message": "success"}
#     else:
#         return {"code": 1, "message": "no collect"}
#
#
# @router.post('/delete_collect', response_model=dict, summary="取消收藏接口")
# async def delete_collect(spec_id: int, user_id: int):
#     item = {'user_id': user_id, 'spec_id': spec_id}
#     s_user_collects: List[m_schema.SUserFav] = d_db.filter_user_fav(items=item, search_items={}, set_items={})
#     for s_collect in s_user_collects:
#         d_db.delete_user_fav(user_fav_id=s_collect.id)
#     return {"code": 0, "message": "success"}
#
#
# @router.get('/collect_list', response_model=m_good.FilterGoodCollect, summary="获取收藏商品列表")
# async def get_good_collects(user_id: int, page: int):
#     collects: List[m_good.GoodCollect] = []
#
#     s_good_collects: m_schema.FilterResUserFav = await r_schema.filter_user_fav(user_id=str(user_id), page=page)
#
#     for good in s_good_collects.data:
#         s_good_spec: m_schema.SGoodSpec = d_db.get_good_spec(good_spec_id=good.spec_id)
#         if s_good_spec is not None:
#             s_good: m_schema.SGood = d_db.get_good(good_id=s_good_spec.good_id)
#             collects.append(m_good.GoodCollect(spec=s_good_spec, good=s_good))
#         else:
#             s_good_collects.total -= 1
#
#     return m_good.FilterGoodCollect(data=collects, total=s_good_collects.total)
#
#
# class ResCartItem(BaseModel):
#     good: Optional[m_schema.SGood] = None
#     spec: Optional[m_schema.SGoodSpec] = None
#     cart: Optional[m_schema.SCart] = None
#
# class ResCartList(BaseModel):
#     data: List[ResCartItem]
#     total: int
#
# @router.post(f'/carts', response_model=ResCartList, summary="购物车列表")
# async def get_cart_list(user_id: int, page: int) -> ResCartList:
#     with Dao() as db:
#         query = db.query(TCart, TGood, TGoodSpec).outerjoin(TGood, TGood.id==TCart.good_id).outerjoin(TGoodSpec, TGoodSpec.id==TCart.good_spec_id).filter(TCart.user_id == user_id)
#         total = query.count()
#         carts = query.order_by(TCart.id.desc()).offset((page - 1) * 20).limit(20).all()
#
#     cart_list = []
#     for cart, good, spec in carts:
#         item = {
#             "good": good.__dict__ if good else None,
#             "spec": spec.__dict__ if spec else None,
#             "cart": cart.__dict__ if cart else None
#         }
#         item = ResCartItem.parse_obj(item)
#         cart_list.append(item)
#
#     return ResCartList(data=cart_list, total=total)
#
# @router.get(f'/dcart', summary="删除购物车订单")
# async def del_dcart(user_id: int, cart_id: int):
#     """
#     user_id，当前购物车所属的用户的id；cart_id，当前订单所在购物车的ID
#     """
#     user_info = d_user.get_user_by_id(user_id)
#     if not user_info:
#         return {"code": 404, "message": "error!!!"}
#     cart_info = d_car.get_cart(cart_id)
#     if not cart_info:
#         return {"code": 404, "message": "error!!"}
#     if user_info.id != user_id:
#         return {"code": 404, "message": "error!"}
#
#     d_car.del_cart(cart_id)
#     return {"code": 200, "message": "success"}
#
# @router.post(f'/search', response_model=m_good.FilterSearchGood, summary='小程序商品搜索接口')
# async def good_search(city: Optional[str] = None, area: Optional[str] = None, parent_category: Optional[int] = None, category: Optional[int] = None,
#                       room: Optional[int] = None, people: Optional[str] = None,title: Optional[str] = None,is_wholesale: Optional[int] = None, status: Optional[int] = None, coinable_number: Optional[int] = None,
#                       page: int = 1, page_size: int = 20):
#     """
#     Post方式，get参数：city，供应商城市；area,供应商区域；parent_category,顶级分类id；category，子分类，若设置子分类，则顶级分类失效；room，规格的房间数；people，房间人数；page,第几页
#     过滤积分：coinable_number = 0
#     """
#     with Dao() as db:
#         session = db.query(schema.TGood, schema.TGoodRule, schema.TGoodPerson,
#                            schema.TGoodPersonState, schema.TSupplier, schema.TGoodSpec) \
#             .outerjoin(schema.TSupplier, schema.TGood.supplier_id == schema.TSupplier.id) \
#             .outerjoin(schema.TGoodRule, schema.TGood.id == schema.TGoodRule.good_id) \
#             .outerjoin(schema.TGoodPerson, schema.TGood.id == schema.TGoodPerson.good_id) \
#             .outerjoin(schema.TGoodPersonState, schema.TGoodPerson.person_id == schema.TGoodPersonState.id)\
#             .outerjoin(schema.TGoodSpec, schema.TGoodSpec.good_id == schema.TGood.id)
#
#         category_ids = []
#         if category is not None:
#             category_ids.append(category)
#         elif parent_category is not None:
#             res = d_product.get_sub_category(parent_category)
#             for r in res:
#                 category_ids.append(r.id)
#         if len(category_ids) > 0:
#             session = session.where(schema.TGood.category_id.in_(category_ids))
#         if room is not None:
#             session = session.where(schema.TGoodRule.room == room)
#         if people is not None:
#             people_a = int(people.split('-')[0])
#             people_b = int(people.split('-')[1])
#             session = session.where(schema.TGoodSpec.lower_num_people >= people_a)
#             session = session.where(schema.TGoodSpec.upper_num_people <= people_b)
#         if city is not None:
#             session = session.where(schema.TSupplier.city.like(f"%{city}%"))
#         if area is not None:
#             session = session.where(schema.TSupplier.area.like(f"%{area}%"))
#         if title is not None:
#             session = session.where(schema.TGood.title.like(f"%{title}%"))
#         if is_wholesale is not None:
#             session = session.where(schema.TGood.is_wholesale == is_wholesale)
#         if status is not None:
#             session = session.where(schema.TGood.status == status)
#         if coinable_number is not None:
#             if coinable_number > 0:
#                 session = session.where(schema.TGood.coinable_number > 0)
#             else:
#                 session = session.where(schema.TGood.coinable_number <= 0)
#
#         session = session.where(schema.TGood.status == 1)
#         session = session.where(schema.TGood.expired_time > datetime.now())
#         session = session.where(schema.TGoodSpec.is_default == 1)
#         session = session.group_by(schema.TGood.id)
#         session = session.order_by(schema.TGood.priority.desc())
#         session = session.order_by(schema.TGood.id.desc())
#
#         total_size = session.count()
#         items = session.offset(page * page_size - page_size).limit(page_size).all()
#
#         send_list: List[m_good.SearchGood] = [
#             m_good.SearchGood(SGood=m_schema.SGood.parse_obj(item[0].__dict__) if item[0] else None,
#                               SGoodRule=m_schema.SGoodRule.parse_obj(item[1].__dict__) if item[1] else None,
#                               SGoodPerson=m_schema.SGoodPerson.parse_obj(item[2].__dict__) if item[2] else None,
#                               SGoodPersonState=m_schema.SGoodPersonState.parse_obj(item[3].__dict__) if item[3]
#                               else None,
#                               SSupplier=m_schema.SSupplier.parse_obj(item[4].__dict__) if item[4] else None
#                               ) for item in items]
#
#         for good in send_list:
#             good_spec: List[m_schema.SGoodSpec] = d_db.filter_good_spec(items={'good_id': good.SGood.id, 'is_default': 1, 'status': 1},
#                                                                         search_items={}, set_items={}, page=1,
#                                                                         page_size=1)
#             good.SGoodSpec = good_spec[0] if good_spec else None
#
#         return m_good.FilterSearchGood(data=send_list, total=total_size)
#
#
# @router.post(f'/coins', response_model=m_good.FilterSearchGood, summary='积分专区商品搜索接口')
# async def good_search(word: Optional[str] = None, status: Optional[str] = None, page: int = 1, page_size: int = 20):
#     word = word if word != "null" else None
#     #if status is not None:
#     #    session = session.where(schema.TGood.status == status)
#     goods: m_schema.FilterResGood = await r_schema.filter_good(coinable='1', s_name=word, status=status, page=page,
#                                                                page_size=page_size)
#
#     total_size: int = goods.total
#     send_list: List[m_good.SearchGood] = []
#     for good in goods.data:
#         spec: List[m_schema.SGoodSpec] = d_db.filter_good_spec(items={'good_id': good.id, 'is_default': 1, 'status': 1}, search_items={},
#                                                                set_items={}, page=1,
#                                                                page_size=1)
#         if spec:
#             send_list.append(m_good.SearchGood(SGood=good, SGoodSpec=spec[0] if spec else None))
#
#     return m_good.FilterSearchGood(data=send_list, total=total_size)
#
#
# @router.get(f'/stores', response_model=m_schema.FilterResStore, summary="适用店铺列表")
# async def get_available_stores(good_id: int):
#     good_stores: m_schema.FilterResGoodStore = await r_schema.filter_good_store(good_id=str(good_id), page=1,
#                                                                                 page_size=100)
#     data = [d_db.get_store(store_id=good_store.store_id) for good_store in good_stores.data]
#     return m_schema.FilterResStore(data=data, total=len(data))
#
# @router.get(f'/get_delivery',summary="获取包邮信息")
# async def get_delivery(good_id: int):
#     return d_good.get_delivery(good_id)



