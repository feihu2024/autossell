from dao import d_db, d_query
from model import m_schema
from typing import Optional
from fastapi import APIRouter, Depends
from .user import verify_token
from model.m_schema import *

# router = APIRouter()
router = APIRouter(dependencies=[Depends(verify_token)])

@router.get(f'/getregist', response_model=m_schema.SPlatformLaw, summary='注册协议')
async def get_platform_text():
    platform_id = 49
    return d_db.get_platform_law(platform_law_id=platform_id)

@router.get(f'/getself', response_model=m_schema.SPlatformLaw, summary='隐私政策')
async def get_platform_self():
    platform_id = 50
    return d_db.get_platform_law(platform_law_id=platform_id)


@router.get('/slider', summary='banner广告列表')
async def slider(class_id:int = 0):
    """
    轮播图
    """
    query_data = d_query.FilterQueryData.parse_obj({
        "table": "banner",
        "joins": [
            {
                "table": "good",
                "on_left": "good_id",
                "on_right": "id"
            }
        ],
        "filters": [{
            "field": "type_id",
            "value": 0
        },{
            "field": "class_id",
            "value": class_id
        }]
    })
    res = d_query.filter_items(query_data)
    return {"code": 0, "data": res['data'], 'total': res['total']}
    # return jxhh_service.recommend(page=1, limit=5)

@router.get(f'/banner/get/info', response_model=SBanner, summary='banner广告详情')
async def get_banner(banner_id: int) -> SBanner:
    return d_db.get_banner(banner_id)

