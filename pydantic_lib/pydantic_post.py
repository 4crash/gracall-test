from datetime import datetime
from typing import List, NewType, Text
from pydantic.main import BaseModel
from pydantic.types import constr
# from pydantic_sqlalchemy import sqlalchemy_to_pydantic
import pytz
# Create pydantic models from SQlAlchemy declaration, import from qlchemy
# doesnt dupport advanced restrictions like str length

# PostOut = sqlalchemy_to_pydantic(PostModel)
# PostBase = sqlalchemy_to_pydantic(PostModel, exclude=["id", "created_at"])


class PostBase(BaseModel):
    """ Pydantic structure input model for creation
        for type checking throws validation errors

    Args:
        BaseModel ([type]): pydantic base mmodel
    """
    title: constr(max_length=20)
    author: constr(max_length=50)
    content: Text
    published_at: datetime = pytz.utc.localize(
        datetime.utcnow().replace(second=0, microsecond=0))
    published: bool = False

    class Config:
        orm_mode = True


class PostOut(PostBase):
    """ output post model to client
        with id and created:at

    Args:
        PostBase ([type]): post pydantic momdel
    """
    id: int
    created_at: datetime = pytz.utc.localize(
        datetime.utcnow().replace(second=0, microsecond=0))

    class Config:
        orm_mode = True


PostDictT = NewType("PostDictT", List[PostOut])
