from fastapi import APIRouter
from app.api.routes import translations

api_router = APIRouter()
api_router.include_router(translations.router, prefix="/translations", tags=["translations"])
