from pydantic import BaseModel


class FileRes(BaseModel):
    file_type: str
    file_date: str
    file_name: str
