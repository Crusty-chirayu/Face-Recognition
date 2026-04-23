from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from sqlalchemy import select

from .config import settings
from .database import engine, async_session
from .logger import logger
from . import models
from .services.auth_service import create_user
from .models.user import User

from .routers.auth import router as auth_router
from .routers.users import router as users_router
from .routers.departments import router as departments_router
from .routers.zones import router as zones_router
from .routers.faces import router as faces_router
from .routers.attendance import router as attendance_router
from .routers.watchlist import router as watchlist_router
from .routers.notifications import router as notifications_router
from .routers.analytics import router as analytics_router

from .core.middleware import RequestLoggingMiddleware, SecurityHeadersMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    # Create default admin user if not exists
    async with async_session() as db:
        result = await db.execute(select(User).where(User.email == "admin@gmail.com"))
        if not result.scalar_one_or_none():
            await create_user(db, "admin@gmail.com", "Admin", "AdminPass123!", "admin")
            logger.info("Default admin user created")
    logger.info("Application started")
    yield
    await engine.dispose()
    logger.info("Application shutdown")


# 🚀 Disable default docs
app = FastAPI(
    title="FaceGate",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None
)


# 🚀 Serve local static files (Swagger)
app.mount("/static", StaticFiles(directory="static"), name="static")


# 🚀 FIXED Swagger UI (proper initialization)
@app.get("/docs", include_in_schema=False)
async def custom_docs():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FaceGate API Docs</title>
        <link rel="stylesheet" href="/static/swagger-ui.css">
    </head>
    <body>
        <div id="swagger-ui"></div>

        <script src="/static/swagger-ui-bundle.js"></script>
        <script>
        window.onload = function() {
            const ui = SwaggerUIBundle({
                url: "/openapi.json",
                dom_id: "#swagger-ui",
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout"
            });
        };
        </script>
    </body>
    </html>
    """)


# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)


# Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(departments_router)
app.include_router(zones_router)
app.include_router(faces_router)
app.include_router(attendance_router)
app.include_router(watchlist_router)
app.include_router(notifications_router)
app.include_router(analytics_router)


# Root endpoint
@app.get("/")
async def root():
    return {"message": "FaceGate API"}