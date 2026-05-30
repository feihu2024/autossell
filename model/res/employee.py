from typing import Optional, List
from pydantic import BaseModel
import datetime


class EmployeeDetailRes(BaseModel):
    user_id: int
    photo_path: Optional[str]
    kpi: float
    status: str
    employee_id: Optional[str]
    position: Optional[str]
    phone: str
    on_boarding_date: Optional[datetime.date]
    jobs: int
    hours: int
    leave_balance: float
    salary: Optional[float]
    first_name: str
    last_name: str
    eid: Optional[str]
    visa_expired_date: Optional[datetime.date]
    passport: Optional[str]
    driving_license: Optional[str]
    contract_expired_date: Optional[datetime.date]


class EmployeeLeaveRes(BaseModel):
    days: float




