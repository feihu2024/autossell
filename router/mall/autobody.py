from dao import d_db, d_query, d_user, d_autobody
from model.m_schema import *
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Request
from .user import verify_token
import requests, json

# router = APIRouter()
router = APIRouter(dependencies=[Depends(verify_token)])

class BaiLianTalk(BaseModel):
    session_id: Optional[str] = Field(title='百炼对话sessino_id, 新对话默认值 new')
    prompt: Optional[str] = Field(title='提示词')
    body_id: Optional[int] = Field(title='智能体id')

@router.post(f"/bailian/talk", summary="阿里百炼智能体对话")
async def bailian_talk(request: Request, item:BaiLianTalk):
    """
            session_id:      新对话默认值 new')
            prompt:      '提示词')
    """
    body_info = d_autobody.get_autobody_by_id(item.body_id)
    if body_info:
        if body_info.at_id:
            request_url = f"http://127.0.01:8700/bailian?session_id={item.session_id}"
            # response = requests.post(request_url, headers=request.headers, params=request.params, data=post_data)
            if item.prompt != 'init':
                request_data = {'prompt':item.prompt.encode('utf-8'),'app_id':body_info.at_id.encode('utf-8')}
            else:
                request_data = {'prompt': '', 'app_id': body_info.at_id.encode('utf-8')}
            response = requests.post(request_url, data=request_data)
            return response.text
        else:
            return '智能体配置错误'
    else:
        return '未知智能体'

@router.get(f"/bailian/type/list", summary="获取智能体分类列表")
async def get_bailian_type_list(request: Request, page:int=1):
    """
        page
    """
    page = page
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    res = d_autobody.get_autobody_list(page)
    return res

@router.get(f"/bailian/body/list", summary="按分类获取智能体列表")
async def get_bailian_body_list(request: Request, type_id:int=0, page:int=1):
    """
        type_id=0   表示全部
    """
    page = page
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if type_id > 0:
        query_data = d_query.FilterGroupQueryData.parse_obj({
            "table": "autobody",
            "selects": ["autobody"],
            "filters": [
                {
                    "field": "autobody.stat",
                    "value": 0
                },
                {
                    "field": "autobody.type_id",
                    "value": type_id
                }
            ],
            "order_by": [{"field": "autobody.id", "order": "desc"}],
            "page": page,
            "page_size": page_size
        })
        res = d_query.filter_items(query_data)
        return res
    else:
        query_data = d_query.FilterGroupQueryData.parse_obj({
            "table": "autobody",
            "selects": ["autobody"],
            "filters": [
                {
                    "field": "autobody.stat",
                    "value": 0
                }
            ],
            "order_by": [{"field": "autobody.id", "order": "asc"}],
            "page": page,
            "page_size": page_size
        })
        res = d_query.filter_items(query_data)
        return res

@router.get(f"/bailian/body/search", summary="获取智能体检索")
async def get_bailian_body_search(request: Request, search_key:str, page:int=1):
    """
        page
    """
    page = page
    page_size:int = 20
    welcomesession = request.headers.get('welcomesession')
    user_id = d_user.get_login_id(welcomesession)
    if search_key:
        res = d_autobody.search_autobody_by_tag_title(search_key, page)
        return res
    else:
        return '未定义搜索词'

