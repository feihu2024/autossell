from pydantic import BaseModel, Field


class LoginBody(BaseModel):
    username: str = Field(description='The username of user')
    password: str = Field(description='Hashed password')


class LoginByEmailVo(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
