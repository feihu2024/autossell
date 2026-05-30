from pydantic import BaseModel
from typing import Optional

class ResWxLogin(BaseModel):
    openid: str # 用户唯一标识
    session_key: str # 会话密钥
    unionid: Optional[str] # 用户在开放平台的唯一标识符，若当前小程序已绑定到微信开放平台帐号下会返回.
    errcode: Optional[int] # 错误码
    errmsg: Optional[str] # 错误信息
