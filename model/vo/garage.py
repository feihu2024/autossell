from pydantic import BaseModel, Field
from typing import Optional


class RegisterUser(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str
    password: str
    eid: Optional[str]
    passport: Optional[str]


class RegisterGarage(BaseModel):
    name: str
    location: str
    specialisation: str
    num_employee: int
    volume_sale: float = Field(title='volume of sales')
    trade_license_path: str = Field(description='/{file_type}/{file_date}/{file_name}')
    logo_path: str = Field(description='/{file_type}/{file_date}/{file_name}')


class RegisterVo(BaseModel):
    user: RegisterUser
    garage: RegisterGarage

