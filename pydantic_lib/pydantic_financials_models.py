from typing import List, Optional
from graphene_pydantic import PydanticObjectType
from pydantic import BaseModel
from sql_lib.db_models import PricesDayModel,Prices15MinModel,Prices1MinModel,FinancialModel

class PriceBaseModel(BaseModel):
    close: int
    open: int
    high:int
    low:int
    sym:str

 
# class P1Model(PriceBaseModel):
#     class Config:
#         orm_mode = True


# class P15Model(PriceBaseModel):
#     class Config:
#         orm_mode = True


# class PDayModel(PriceBaseModel):
#     class Config:
#         orm_mode = True

# class FinancialModel(BaseModel):
#     sector:str
#     symbol:str
#     shortRatio: float

#     class Config:
#         orm_mode = True


class FinancialGrapheneModel(PydanticObjectType):
    class Meta:
        model = FinancialModel


class P15GrapheneModel(PydanticObjectType):
    class Meta:
        model = Prices15MinModel


class PDayGrapheneModel(PydanticObjectType):
    class Meta:
        model = PricesDayModel
