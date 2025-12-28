from fastapi import APIRouter
from app.api.routes import quran, ayah, surah, translations

api_router = APIRouter()
api_router.include_router(quran.router, prefix="/quran", tags=["quran"])
api_router.include_router(surah.router, prefix="/surah", tags=["surah"])
api_router.include_router(ayah.router, prefix="/ayah", tags=["ayah"])
api_router.include_router(translations.router, prefix="/translations", tags=["translations"])
