from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class URLType(str, Enum):
    PUBLIC = 'public'
    PRIVATE = 'private'


class ShortURLBase(BaseModel):
    type: Optional[URLType]


class ShortURLCreate(ShortURLBase):
    original_url: str = Field(..., example='https://www.google.com')


class ShortURLDB(ShortURLCreate):
    id: int
    short_url: str
    user_id: int
    type: URLType

    class Config:
        orm_mode = True
