from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None

    @validator('email')
    def must_not_empty(cls, v):
        if len(v) <= 5:
            raise ValueError('email must be greater than 5 characters')
        return v


class UserOut(UserBase):
    created_date: datetime = None
    last_modified: datetime = None
    pass


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True

    @validator('password')
    def must_not_empty(cls, v):
        if len(v) <= 5:
            raise ValueError('password must be greater than 5 characters')
        return v


class UserEdit(UserBase):
    last_modified: datetime = None
    password: Optional[str] = None

    class Config:
        orm_mode = True

    @validator('last_modified', pre=True, always=True)
    def default_ts_modified(cls, v):
        return v or datetime.utcnow()


class User(UserBase):
    id: int
    created_date: datetime = None
    last_modified: datetime = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    name: str = None
    id: int = None
    permissions: str = "user"
