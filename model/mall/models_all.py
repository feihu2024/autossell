from pydantic import BaseModel
from typing import Optional


class FlashOrder(BaseModel):
    id: Optional[int]
    package_id: int
    status: str
    create_time: str
    paid_time: str
    amount: int


class Level(BaseModel):
    id: Optional[int]
    title: str


class MallOrder(BaseModel):
    id: Optional[int]
    product_id: int
    order_number: str
    buyer_id: int
    seller_id: int
    selling_price: int
    cost_price: int
    create_time: str
    paid_time: str


class Model(BaseModel):
    id: Optional[int]
    product_id: int


class Package(BaseModel):
    id: Optional[int]
    product_id: int
    amount: int


class Product(BaseModel):
    id: Optional[int]
    name: str
    stock: int
    is_flash_sale: int
    category_id: int
    type: str
    selling_price: int
    cost_price: int
    num_scales: int
    image_url: str
    priority: int
    sliver_coin: int
    model_id: int
    expired_time: str
    parent_product_id: int
    title: str
    subtitle: str
    stock_cordon: int
    status: str


class User(BaseModel):
    id: Optional[int]
    username: str
    email: str
    open_id: str
    union_id: str
    password: str
    nickname: str
    name: str
    phone: str
    id_card: str
    level_id: int
    status: str
    register_time: str
    avatar: str
    invited_user_id: int
    sliver_coin: int
    gold_coin: float
