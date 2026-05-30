from pydantic import BaseModel


class TokenInfo(BaseModel):
    user_id: int
    time: int