from pydantic import BaseModel
from typing import Dict, NewType, Text, Optional
from datetime import datetime
from pydantic.types import constr
import pytz


class PostBase(BaseModel):
    title: constr(max_length=20)
    author: constr(max_length=50)
    content: Text
    published_at: datetime = pytz.utc.localize(
        datetime.utcnow().replace(second=0, microsecond=0))
    published: bool = False
    class Config:
        orm_mode = True

    
class PostOut(PostBase):
    id:int
    created_at: datetime = pytz.utc.localize(
        datetime.utcnow().replace(second=0, microsecond=0))

    class Config:
        orm_mode = True



PostDictT = NewType("PostDictT", Dict[int, PostOut])

