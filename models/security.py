from sqlalchemy import Column, String, DateTime, Integer, Float
from core.validators import utcnow
from db import session
import datetime


class Security(session.Base):
    __tablename__ = "security"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    time = Column(DateTime,  server_default=utcnow(),
                  default=datetime.datetime.utcnow)
    device = Column(String, nullable=False)
    os = Column(String, nullable=False)
    ip = Column(String, index=True, nullable=False)
    city = Column(String)
    region = Column(String)
    country_name = Column(String)
    postal = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    org = Column(String)


Security.__table__.create(session.engine, checkfirst=True)
