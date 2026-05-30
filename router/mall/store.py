from fastapi import APIRouter
from typing import Optional, List
from datetime import datetime
from dao import d_store
from model.mall import m_store

router = APIRouter()


@router.post(f'/create', response_model=m_store.SMallStore)
async def create_mall_store(items: m_store.CreateStore) -> m_store.SMallStore:
    """添加商家"""
    items = m_store.Tstore(**items.dict())
    return m_store.SMallStore(**d_store.create_store(items).__dict__)


@router.post(f'/update', response_model=m_store.SMallStore)
async def update_mall_store(store_id: int, items: m_store.CreateStore) -> m_store.SMallStore:
    """更新商家信息"""
    d_store.update_store(store_id, items.dict())
    return m_store.SMallStore(id=store_id, **items.__dict__)


@router.get(f'/get', response_model=m_store.SMallStore)
async def get_mall_store(store_id: int) -> m_store.SMallStore:
    """获取商家"""
    item = d_store.get_store(store_id)
    return m_store.SMallStore(**item.__dict__)


