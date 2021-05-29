import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session
import databases
from settings import settings
from fastapi import Depends

database = databases.Database(settings.sqlite_database_url)
logging.debug(database) 
print(database)
engine = create_engine(
    settings.sqlite_database_url,
    # connect_args={"check_same_thread": False}
)

Base = declarative_base()
Base.metadata.create_all(engine)
LocalSession = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base.query = LocalSession.query_property()


def get_db():
    db: Session = LocalSession()
    try:
        return db
    finally:
        db.close()



