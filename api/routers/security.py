from fastapi import APIRouter, Request, Depends, Response
from typing import List

from db.session import get_db
from crud.security import (
    get_login,
    get_logins,
    create_login
)
from schemas.security import Security, SecurityBase, SecurityOut
from core.auth import get_current_active_user

security_router = r = APIRouter()


@r.post("/security", response_model=Security, response_model_exclude_none=True)
async def login_create(
    request: Request,
    login: SecurityBase,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create login entry
    """
    return create_login(db, login)


@r.get("/security", response_model=List[SecurityOut])
async def get_all_logins(
    response: Response,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get all logins
    """
    # This is necessary for react-admin to work
    security = get_logins(db)
    response.headers["Content-Range"] = f"0-9/{len(security)}"
    return security


@r.get("/security/{email}", response_model=List[SecurityOut])
async def get_login_by_mail(
    request: Request,
    email: str,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get all logins by email
    """
    return get_login(db, email)
