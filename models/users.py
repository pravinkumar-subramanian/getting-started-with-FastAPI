from sqlalchemy import Boolean, Column, Integer, String, DateTime
from db import session
import datetime

#from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base() #classes associate to the tables in database


class User(session.Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    last_modified = Column(DateTime, default=datetime.datetime.utcnow)


User.__table__.create(session.engine, checkfirst=True)
