import datetime
from typing import Union, Optional, List, Literal
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field


class Car(BaseModel):
    chassis_num: Optional[str]
    make_id: Optional[int]
    model_id: Optional[int]
    year: Optional[int]
    fuel: Optional[str]
    last_service_date: Optional[datetime.date]

class Customer(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str
    document_path: Optional[str]


class Quota(BaseModel):
    part_id: int
    labour_hours_amount: float
    labour_rate: float
    part_amount: int
    part_unit_price: float
    discount: float
    price: Optional[float]
    total_price: float

class Operation(BaseModel):
    operation_category_id: Optional[int]

class Inspection(BaseModel):
    part_id: int
    score: float
    usure_km: Optional[float]
    image_path: Optional[str]

class JobCardCreation(BaseModel):
    company_id: int
    customer_comments: Optional[str]
    advisor_comments: Optional[str]
    final_comments: Optional[str]
    assignee_user_id: Optional[int]
    mileage: Optional[int]
    plate: Optional[str]
    price: Optional[float]

    car: Car
    customer: Customer
    inspections: List[Inspection]

    front_path: Optional[str]
    back_path: Optional[str]
    body_path: Optional[str]
    files: Optional[List[str]]

    operations: List[Operation]
    quotas: List[Quota]


class JobCardUpdate(BaseModel):
    id: int
    status: Optional[Literal['pending', 'ongoing', 'pickup', 'done']]
