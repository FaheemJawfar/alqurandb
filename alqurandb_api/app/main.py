"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import api_router


def create_application() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="API for downloading Quran translations in multiple formats"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_application()
