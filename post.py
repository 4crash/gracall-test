from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime

class Post(BaseModel):
    id: Optional[int]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: datetime
    published: bool = False



