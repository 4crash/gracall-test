from typing import  List, NewType
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from db_lib.post_model import PostModel

# Create pydantic models from SQlAlchemy declaration
PostOut = sqlalchemy_to_pydantic(PostModel)
PostBase = sqlalchemy_to_pydantic(PostModel,exclude=["id","created_at"])
PostDictT = NewType("PostDictT", List[PostOut])

