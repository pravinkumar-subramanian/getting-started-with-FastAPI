from fastapi import FastAPI, Depends
from starlette.requests import Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from api.routers.default import default_router
from api.routers.users import users_router
from api.routers.auth import auth_router
from api.routers.security import security_router

from core import config
from db.session import Session
from core.auth import get_current_active_user
from core.celery_app import celery_app
import tasks
import metadata


app = FastAPI(
    title=config.PROJECT_NAME,
    description=config.DESCRIPTION,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url='/api/redoc',
    openapi_url="/api/openapi.json",
    openapi_tags=metadata.tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


# @app.get("/api/", tags=['default'])
# async def root():
#    return {"message": "Hello there!!! Welcome to the WatchTower DataCenter"}


# Routers
# default router
app.include_router(
    default_router,
    prefix="/api",
    tags=["default"],
)
# users router
app.include_router(
    users_router,
    prefix="/api",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
# auth router
app.include_router(
    auth_router,
    prefix="/api",
    tags=["auth"]
)
# security router
app.include_router(
    security_router,
    prefix="/api",
    tags=["security"],
    dependencies=[Depends(get_current_active_user)],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
