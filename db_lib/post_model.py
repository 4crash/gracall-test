from datetime import datetime
from sqlalchemy import  Column,  Integer, String
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from db_lib.connect import Base
import pytz


class PostModel(Base):

    __tablename__ = "Posts"
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(50))
    author = Column(String(50))
    content = Column(String(500))
    published_at = Column(DateTime, default=pytz.utc.localize(
        datetime.utcnow().replace(second=0, microsecond=0))) 
    published = Column(Boolean)
    created_at = Column(DateTime, default=pytz.utc.localize(
        datetime.utcnow().replace(second=0, microsecond=0)))
    
    def asdict(self):
        return self.__dict__