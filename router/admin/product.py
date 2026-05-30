# from fastapi import APIRouter
# from pydantic import BaseModel
# from typing import List
#
# from model.vo.product import CreateProduct
#
# router = APIRouter()
#
#
# class ResCategory(BaseModel):
#     id: int
#     name: str
#
#
# class ResModel(BaseModel):
#     code: int = 0
#     message: str = 'success'
#
#
# @router.post('/create', response_model=ResModel)
# async def create(product: CreateProduct) -> ResModel:
#     return ResModel()
#
#
# @router.get('/categories', response_model=List[ResCategory])
# async def categories() -> List[ResCategory]
#     return
