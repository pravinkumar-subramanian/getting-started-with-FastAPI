from fastapi import APIRouter, Depends, Request
from db.session import get_db
from schemas.users import User
from crud.users import create_rootuser

default_router = r = APIRouter()


@r.get("/api/")
async def root():
    return {"message": "Hello there!!! Welcome to the WatchTower DataCenter"}


@r.get("/api/task", deprecated=True)
async def example_task():
    celery_app.send_task("app.tasks.example_task", args=["Hello World"])
    return {"message": "success"}


@r.post("/rootuser", response_model=User, response_model_exclude_none=False)
async def rootuser_create(
    request: Request,
    db=Depends(get_db),
):
    """
    Create root user
    """
    return create_rootuser(db)
