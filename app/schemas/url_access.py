from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AccessLogBase(BaseModel):
    short_url_id: int
    access_time: datetime
    user_id: Optional[int]


class AccessLogDB(AccessLogBase):
    id: int

    class Config:
        orm_mode = True
