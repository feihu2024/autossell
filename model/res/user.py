from pydantic import BaseModel, Field

class BaseResponse(BaseModel):
    code: int = Field(0, description="错误码")
    message: str = Field("success", description="错误信息")


class PhoneNumber(BaseResponse):
    phoneNumber: str
    purePhoneNumber: str
    countryCode: str