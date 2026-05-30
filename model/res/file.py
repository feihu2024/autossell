from pydantic import BaseModel


class FileRes(BaseModel):
    file_type: str
    file_date: str
    file_name: str

class FileResTowx(BaseModel):
    file_type: str
    file_date: str
    file_name: str
    media_code: str
    media_id: str
    media_msg: str