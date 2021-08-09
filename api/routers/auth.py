from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta

from db.session import get_db
from core import config
from core import security
from core.auth import authenticate_user, sign_up_new_user

auth_router = r = APIRouter()

token_secret = config.TOKEN_SECRET

@r.post("/token")
async def login(
    db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID is not active. Contact your admin",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    if user.is_superuser:
        permissions = "admin"
    else:
        permissions = "user"
    access_token = security.create_access_token(
        data={"email": user.email,
              "name": user.first_name + ' ' + user.last_name,
              token_secret: user.id,
              "permissions": permissions},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@r.post("/signup")
async def signup(
    db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = sign_up_new_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    if user.is_superuser:
        permissions = "admin"
    else:
        permissions = "user"
    access_token = security.create_access_token(
        data={"email": user.email,
              "name": user.first_name + ' ' + user.last_name,
              token_secret: user.id,
              "permissions": permissions},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
