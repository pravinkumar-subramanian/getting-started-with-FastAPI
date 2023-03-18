from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from typing import Union
from core.validators import checkemail, checkpassword

name_error = 'should contain only alphabetic letters and must not exceed 26 characters'
password_error = 'Password should atleast be 8 characters with minimum 1 uppercase, 1 lowercase, 1 special character and 1 number'


class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str
    last_name: str

    @validator('first_name')
    def fn_not_empty(cls, v):
        if len(v) < 1 or len(v) > 26 or not v.isalpha():
            raise ValueError('First name ' + name_error)
        return v

    @validator('last_name')
    def ln_not_empty(cls, v):
        if len(v) < 1 or len(v) > 26 or not v.isalpha():
            raise ValueError('Last name ' + name_error)
        return v

    @validator('email')
    def email_not_empty(cls, v):
        if not checkemail(v):
            raise ValueError('email is not valid')
        return v


class User(UserBase):
    user_uuid: Union[str, UUID]
    expires_on: datetime = None
    created_date: datetime = None
    last_modified: datetime = None

    class Config:
        orm_mode = True


# 1. User Create Validation
class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True

    @validator('password')
    def must_not_empty(cls, v):
        if not checkpassword(v):
            raise ValueError(password_error)
        return v


# 2. User Self data Edit Validation
class UserMeEdit(BaseModel):
    first_name: str = None
    last_name: str = None
    password: Optional[str] = None

    @validator('first_name')
    def fn_not_empty(cls, v):
        if len(v) < 1 or len(v) > 26 or not v.isalpha():
            raise ValueError('First name ' + name_error)
        return v

    @validator('last_name')
    def ln_not_empty(cls, v):
        if len(v) < 1 or len(v) > 26 or not v.isalpha():
            raise ValueError('Last name ' + name_error)
        return v

    @validator('password')
    def pwd_not_empty(cls, v):
        if not checkpassword(v):
            raise ValueError(password_error)
        return v


# 3. User Edit Validation
class UserEdit(UserMeEdit):
    is_active: bool = True
    is_superuser: bool = False

    class Config:
        orm_mode = True


# ------------------------------------- TOKEN SCHEMA -------------------------------------------------#


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    name: str = None
    id: str = None
    permissions: str = "user"
