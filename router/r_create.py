from fastapi import APIRouter
from service import create_service

router = APIRouter()


@router.post('')
async def create(items: dict) -> dict:
    return create_service.create(items)
