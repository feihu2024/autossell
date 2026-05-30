from pydantic import BaseModel


class RegisterRes(BaseModel):
    user_id: int
    company_id: int
