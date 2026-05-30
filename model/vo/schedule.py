from pydantic import BaseModel, Field
from typing import Optional
import datetime


class UserRangeVo(BaseModel):
    user_id: int
    from_time: datetime.datetime
    to_time: datetime.datetime


class EmployeesRangeVo(BaseModel):
    company_id: int
    from_time: datetime.datetime
    to_time: datetime.datetime


class UserScheduleVo(BaseModel):
    user_id: int
    start_time: datetime.datetime
    end_time: datetime.datetime
    type_id: int
    description: Optional[str]


class UpdateScheduleVo(BaseModel):
    id: int
    user_id: Optional[int]
    start_time: Optional[datetime.datetime]
    end_time: Optional[datetime.datetime]
    type_id: Optional[int]
    description: Optional[str]


class DeleteScheduleVo(BaseModel):
    schedule_id: int


class ScheduleTypeVo(BaseModel):
    name: str


class UpdateScheduleTypeVo(BaseModel):
    id: int
    name: str


class DeleteScheduleTypeVo(BaseModel):
    schedule_type_id: int


class DeleteUserScheduleVo(BaseModel):
    schedule_id: int
