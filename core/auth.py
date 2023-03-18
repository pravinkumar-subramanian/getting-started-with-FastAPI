import jwt
from fastapi import Depends, HTTPException, status
from jwt import PyJWTError

from db import session
from models import users as models
from schemas import users as schemas
from crud.users import get_user_by_email
from crud.session import read_session
from core import security
from datetime import datetime


async def get_current_user(
    db=Depends(session.get_db), token: str = Depends(security.oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    """ Decode JWT """
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        permissions: str = payload.get("permissions")
        session: str = payload.get("session")
        token_data = schemas.TokenData(
            email=email, permissions=permissions, id=session)
    except PyJWTError:
        raise credentials_exception
    """ Fetch user data """
    user = get_user_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception
    """ Check for existing user session """
    await read_session(user.user_uuid, token_data.id)
    return user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


def authenticate_user(db, email: str, password: str):
    user = get_user_by_email(db, email)
    # check for password expiry
    expiry = user.expires_on
    now = datetime.utcnow()
    if now > expiry:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password expired. Reset your password to access the application"
        )
    # check for inactive account
    if not user.is_active:
        if user.login_attempt > 4:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID is locked after 5 incorrect login attempts. Contact your admin to unlock your account",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID is inactive. Contact your admin",
                headers={"WWW-Authenticate": "Bearer"},
            )
    # check password
    if not security.verify_password(password, user.hashed_password):
        user.login_attempt += 1
        if user.login_attempt <= 4:
            db.add(user)
            db.commit()
            raise HTTPException(
                status_code=401, detail=f"Failed login attempt {user.login_attempt}/5. Incorrect credentials.")
        if user.login_attempt > 4:
            user.is_active = False
            user.last_modified = datetime.utcnow()
            db.add(user)
            db.commit()
            raise HTTPException(
                status_code=401, detail="Incorrect credentials. Your account is locked after 5 unsuccessful attempts. Contact your admin to unlock your account.")
    else:
        user.login_attempt = 0
        db.add(user)
        db.commit()
        return user
