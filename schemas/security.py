from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class SecurityBase(BaseModel):
    email: str
    device: Optional[str] = 'Unidentified'
    os: Optional[str] = 'Unidentified'
    ip: Optional[str] = 'Anonymous'
    city: Optional[str] = None
    region: Optional[str] = None
    country_name: Optional[str] = None
    postal: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    org: Optional[str] = None

    @validator('email')
    def must_not_empty(cls, v):
        print(cls, v)
        if len(v) <= 5:
            raise ValueError('email must be greater than 5 characters')
        return v


class SecurityCreate(SecurityBase):
    pass


class SecurityOut(SecurityBase):
    time: datetime = None

    class Config:
        orm_mode = True


class Security(SecurityBase):
    id: int

    class Config:
        orm_mode = True
