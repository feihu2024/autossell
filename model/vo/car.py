from pydantic import BaseModel, Field
from typing import Optional


class RegisterCar(BaseModel):
    user_id: Optional[int]
    plate: str
    chassis_num: str
    model: str
    make: str
    year: str