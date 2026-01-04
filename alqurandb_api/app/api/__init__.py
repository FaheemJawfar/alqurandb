from fastapi import APIRouter
from app.api.routes import translations, quran

api_router = APIRouter()
api_router.include_router(translations.router, prefix="/translations", tags=["translations"])
api_router.include_router(quran.router, prefix="/quran", tags=["quran"])
