import datetime

from pydantic import BaseModel
from typing import Optional, List
import datetime

from .car import RegisterCar


class RegisterUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    dob: Optional[datetime.date]
    email: Optional[str]
    phone: Optional[str]
    eid: Optional[str]
    driving_license: Optional[str]
    cars: Optional[List[RegisterCar]]
    company_id: Optional[int]


class RegisterEmployeeVo(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    dob: Optional[datetime.date]
    email: Optional[str]
    phone: Optional[str]
    eid: Optional[str]
    driving_license: Optional[str]
    company_id: Optional[int]
    role_id: Optional[int]
