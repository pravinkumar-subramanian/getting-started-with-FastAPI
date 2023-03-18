from fastapi import APIRouter, Depends, Response
from typing import List
from db.session import get_db
from crud.security import get_login, get_logins
from schemas.security import SecurityOut
from core.auth import get_current_active_user, get_current_active_superuser

security_router = r = APIRouter()


# -------------------- READ SECURITY ENTRY ---------------------------- #


# read security entries of all users
@r.get("/security", response_model=List[SecurityOut])
async def get_all_logins(
    response: Response,
    db=Depends(get_db),
    _=Depends(get_current_active_superuser),
):
    """
    Get login entries for all users
    """
    security = get_logins(db)
    response.headers["Content-Range"] = f"0-9/{len(security)}"
    return security


# read your scurity entries
@r.get("/security/me", response_model=List[SecurityOut])
async def get_login_by_mail(
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get login entries by email
    """
    return get_login(db, current_user.email)
