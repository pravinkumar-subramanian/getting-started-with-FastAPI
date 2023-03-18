from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from core import config
from core.validators import utcnow
from db import session
import datetime


class User(session.Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    user_uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default='t', default=True)
    is_superuser = Column(Boolean, server_default='f', default=False)
    login_attempt = Column(Integer, server_default='0', default=0)
    expires_on = Column(DateTime, server_default=utcnow(),
                        default=datetime.datetime.utcnow() +
                        datetime.timedelta(days=int(config.PASSWORD_EXPIRY)))
    created_date = Column(DateTime, server_default=utcnow(),
                          default=datetime.datetime.utcnow)
    last_modified = Column(DateTime, server_default=utcnow(),
                           default=datetime.datetime.utcnow)


User.__table__.create(session.engine, checkfirst=True)
