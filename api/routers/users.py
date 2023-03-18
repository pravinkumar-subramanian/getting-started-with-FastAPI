from fastapi import APIRouter, Request, Depends, Response
from typing import List

from db.session import get_db
from crud.users import (
    get_users,
    get_user,
    create_user,
    delete_user,
    edit_user,
)
from schemas.users import UserCreate, UserEdit, UserMeEdit, User
from core.auth import get_current_active_user, get_current_active_superuser

users_router = r = APIRouter()


# -------------------- READ USERS -------------------------- #

@r.get("/users", response_model=List[User], response_model_exclude_none=True)
async def users_list(
    response: Response,
    db=Depends(get_db),
    _=Depends(get_current_active_superuser),
    skip: int = 0,  limit: int = 100
):
    """
    Get all users
    """
    users = get_users(db, skip, limit)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(users)}"
    return users


@r.get("/users/me", response_model=User, response_model_exclude_none=True)
async def user_me(current_user=Depends(get_current_active_user)):
    """
    Get your information
    """
    return current_user


@r.get("/users/{user_id}", response_model=User, response_model_exclude_none=True)
async def user_details(
    user_id: str,
    db=Depends(get_db),
    _=Depends(get_current_active_superuser)
):
    """
    Get any user details by user ID
    """
    user = get_user(db, user_id)
    return user


# -------------------- CREATE USERS -------------------------- #

@r.post("/users", response_model=User, response_model_exclude_none=False)
async def user_create(
    user: UserCreate,
    db=Depends(get_db),
    _=Depends(get_current_active_superuser)
):
    """
    Create a new user
    1. email: must be an email with bridgei2i domain
    2. is_active: True or False
    3. is_superuser: True or False
    4. first_name: must be alpha numeric
    5. last_name: must be alpha numeric
    6. password: must contain 1 uppercase, 1 lowercase, 1 number and 1 special character
    """
    return create_user(db, user)


# -------------------- EDIT USERS -------------------------- #

@r.put("/users/me", response_model=User, response_model_exclude_none=True)
async def user_self_edit(
    user: UserMeEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """
    Update self details
    1. first_name: must be alpha numeric
    2. last_name: must be alpha numeric
    3. password: must contain 1 uppercase, 1 lowercase, 1 number and 1 special character
    """
    return edit_user(db, current_user.user_uuid, user)


@r.put("/users/{user_id}", response_model=User, response_model_exclude_none=True)
async def user_edit(
    user_id: str,
    user: UserEdit,
    db=Depends(get_db),
    _=Depends(get_current_active_superuser)
):
    """
    Update existing user
    1. is_active: True or False
    2. is_superuser: True or False
    3. first_name: must be alpha numeric
    4. last_name: must be alpha numeric
    5. password: OPTIONAL - must contain 1 uppercase, 1 lowercase, 1 number and 1 special character
    """
    return edit_user(db, user_id, user)


# -------------------- DELETE USERS -------------------------- #

@r.delete("/users/{user_id}", response_model=User, response_model_exclude_none=True)
async def user_delete(
    user_id: str,
    db=Depends(get_db),
    _=Depends(get_current_active_superuser)
):
    """
    Delete existing user by user ID
    """
    return delete_user(db, user_id)
