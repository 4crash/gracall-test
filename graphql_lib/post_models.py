from graphene_pydantic import PydanticObjectType, PydanticInputObjectType
from pydantic_lib.pydantic_post import PostBase, PostOut

class PostGrapheneOutModel(PydanticObjectType):
    class Meta:
        model = PostOut


class PostGrapheneInputModel(PydanticInputObjectType):
    class Meta:
        model = PostBase
        # exclude_fields = ('id', 'created_at')
        

class PostGrapheneInputIDModel(PydanticInputObjectType):
    class Meta:
        model = PostOut
