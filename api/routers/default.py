from fastapi import APIRouter, Depends
from db.session import get_db
from schemas.users import User
from crud.users import create_rootuser

default_router = r = APIRouter()


@r.post("/rootuser", response_model=User, response_model_exclude_none=False)
async def rootuser_create(db=Depends(get_db)):
    """
    Create root user. 
    Running this API wil create rootuser for the first time post which user exist error will be thrown
    """
    return create_rootuser(db)
