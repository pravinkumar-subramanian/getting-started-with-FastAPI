from pydantic import BaseModel, validator
from datetime import datetime


class SecurityBase(BaseModel):
    device: str
    os: str
    ip: str = '0.0.0.0'
    city: str = None
    region: str = None
    country_name: str = None
    postal: int = None
    latitude: float = None
    longitude: float = None
    org: str = None

    @validator('device')
    def device_not_empty(cls, v):
        if len(v.strip()) == 0 or len(v.strip()) > 40:
            raise ValueError('Improper device name')
        return v

    @validator('os')
    def os_not_empty(cls, v):
        if len(v.strip()) == 0 or len(v.strip()) > 40:
            raise ValueError('Improper OS name')
        return v


class SecurityOut(SecurityBase):
    email: str
    time: datetime = None

    class Config:
        orm_mode = True
