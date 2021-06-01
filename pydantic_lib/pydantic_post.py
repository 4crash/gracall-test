from pydantic import BaseModel
from typing import  List, NewType, Set, Text
from datetime import datetime
from pydantic.types import constr
import pytz
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from db_lib.post_model import PostModel


PostOut = sqlalchemy_to_pydantic(PostModel)
PostBase = sqlalchemy_to_pydantic(PostModel,exclude=["id","created_at"])
PostDictT = NewType("PostDictT", List[PostOut])

