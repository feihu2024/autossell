from typing import Optional

from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    code: int = Field(0, title='状态码')
    message: str = Field('success', title='提示信息')
    data: Optional[dict] = Field(None, title='返回数据')


class SuccessRes(BaseModel):
    detail: str = Field(default='success', title='提示信息')
    data: Optional[dict] = Field(default=None, title='数据')
