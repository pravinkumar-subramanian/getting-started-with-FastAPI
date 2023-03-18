from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
import uvicorn

from api.routers.default import default_router
from api.routers.users import users_router
from api.routers.auth import auth_router
from api.routers.security import security_router

from core import config
from db.session import Session
import metadata
import time


app = FastAPI(
    title=config.PROJECT_NAME,
    description=config.DESCRIPTION,
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url="/api/openapi.json",
    openapi_tags=metadata.tags_metadata
)

# ------------------------------ Middleware Starts --------------------------------------#

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=['X-Requested-With', 'X-HTTP-Method-Override', 'Content-Type',
                   'Accept', 'Content-Security-Policy', 'Strict-Transport-Security',
                   'X-Frame-Options', 'X-Content-Type-Options', 'Referrer-Policy',
                   'X-XSS-Protection'],
    expose_headers=["set-cookie"]
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    # security headers startss
    response.headers["Content-Security-Policy"] = "default-src 'self' data:;" + \
        "font-src 'self' https://fonts.gstatic.com/;" + \
        "style-src 'self' https://fonts.googleapis.com 'unsafe-inline';" + \
        "script-src 'self' 'unsafe-inline' blob:; frame-ancestors 'none'"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains;preload'
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    # security headers ends
    request.state.db.close()
    return response

# ------------------------------ Middleware Ends --------------------------------------#
# ------------------------------ Swagger UI Starts ------------------------------------#

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/api/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="/static/api.png"
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/api/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
        redoc_favicon_url="/static/api.png"
    )


# ------------------------------ Swagger UI Ends ------------------------------------#
# ------------------------------ Router Declaration Starts --------------------------#

# default router
app.include_router(
    default_router,
    prefix="/api",
    tags=["default"]
)
# users router
app.include_router(
    users_router,
    prefix="/api",
    tags=["users"],
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
    tags=["security"]
)

# ------------------------------ Router Declaration Ends --------------------------#

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
