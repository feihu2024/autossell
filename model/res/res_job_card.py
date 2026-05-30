from pydantic import BaseModel


class JobCardCreationRes(BaseModel):
    code: int
    message: str
    job_card_id: int