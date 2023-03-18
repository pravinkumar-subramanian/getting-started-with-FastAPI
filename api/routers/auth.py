from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Response, Form, HTTPException
from fastapi.responses import JSONResponse

from crud.security import create_login
from crud.session import create_session, delete_session
from crud.password import update_password

from core import security
from core.auth import authenticate_user, get_current_active_user

from schemas.security import SecurityBase
from db.session import get_db
from datetime import datetime, timedelta
from uuid import uuid4


auth_router = r = APIRouter()


# ----------------------------- TOKEN CREATOR FUNCTION -------------------------- #


async def create_token(user):
    """  create and set token as response cookie """
    access_token_expires = timedelta(
        minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    if user.is_superuser:
        permissions = "admin"
    else:
        permissions = "user"
    """ creating local session """
    session = uuid4()
    await create_session(user.user_uuid, session)
    """ creating access token """
    access_token = security.create_access_token(
        data={"email": user.email,
              "name": user.first_name+" "+user.last_name,
              "permissions": permissions,
              "session": str(session)},
        expires_delta=access_token_expires,
    )
    # set access token as cookies
    max_age = security.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    response = JSONResponse(content={"email": user.email})
    response.set_cookie(key=security.TOKEN,
                        value=f"Bearer {access_token}",
                        secure=True,
                        httponly=True,
                        max_age=max_age,
                        samesite='none')
    return response

# ----------------------------- TOKEN APIS -------------------------- #


# 1. Create access token
@r.post("/token")
async def login(
    db=Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    device: str = 'Unknown',
    os: str = 'Unknown'
):
    """  generate token  """
    user = authenticate_user(db, form_data.username, form_data.password)
    create_login(db, SecurityBase(os=os, device=device), user.email)
    return await create_token(user)


# 2. Refresh logged in session
@r.post("/refresh")
async def refresh_token(
    current_user=Depends(get_current_active_user),
):
    """  create and refresh token as response cookie """
    await delete_session(current_user.user_uuid)
    return await create_token(current_user)


# 3. Terminate logged in session
@r.get("/logout")
async def route_logout_and_remove_cookie(
    response: Response,
    current_user=Depends(get_current_active_user)
):
    """  remove response cookie """
    await delete_session(current_user.user_uuid)
    content = {"message": 'Successfully logged out!'}
    response = JSONResponse(content=content)
    response.set_cookie(key=security.TOKEN,
                        max_age=0,
                        expires=0,
                        secure=True,
                        samesite='none')
    return response


# 4. Reset old password
@r.post("/reset-password")
async def reset_password(
    db=Depends(get_db),
    username: str = Form(None),
    password: str = Form(None),
    new_password: str = Form(None),
    confirm_password: str = Form(None),
):
    if new_password != confirm_password:
        raise HTTPException(
            status_code=400, detail="new password do not match")
    elif password == new_password:
        raise HTTPException(
            status_code=400, detail="new password should not be same as old password")
    user = authenticate_user(db, username, password)
    # create new password entry in password table
    update_password(db, new_password, user.user_uuid)
    # update password in users table
    update_data = {}
    update_data["hashed_password"] = security.get_password_hash(
        new_password)
    update_data['last_modified'] = datetime.utcnow()
    for key, value in update_data.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"detail": "password reset successful"}
