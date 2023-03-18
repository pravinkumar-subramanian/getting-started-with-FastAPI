from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from core.validators import utcnow
from db import session
import datetime


class Password(session.Base):
    __tablename__ = "password"

    id = Column(Integer, primary_key=True, index=True)
    user_uuid = Column(UUID(as_uuid=True), nullable=False)
    password = Column(String, nullable=False)
    created_date = Column(DateTime, server_default=utcnow(),
                          default=datetime.datetime.utcnow)


Password.__table__.create(session.engine, checkfirst=True)
