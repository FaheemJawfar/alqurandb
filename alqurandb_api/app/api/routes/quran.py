
from fastapi import APIRouter, Depends, Path as PathParam
from pathlib import Path

from app.services.quran_service import QuranService
from app.repositories.quran_repository import QuranRepository
from app.schemas.verse import VerseResponse, VersesResponse, QuranVerseResponse, QuranVersesResponse
from app.core.config import settings

router = APIRouter()

def get_quran_repository() -> QuranRepository:
    db_path = Path(settings.DATA_DIR) / "quran_translations.db"
    return QuranRepository(db_path)

def get_quran_service(
    repository: QuranRepository = Depends(get_quran_repository)
) -> QuranService:
    return QuranService(repository)

@router.get(
    "/{sura}",
    response_model=QuranVersesResponse,
    summary="Get sura verses",
    description="Get all verses of a specific sura"
)
async def get_sura(
    sura: int = PathParam(..., ge=1, le=114, description="Sura number (1-114)"),
    service: QuranService = Depends(get_quran_service)
):
    """Get sura verses"""
    verses = service.get_verses_by_sura(sura)
    return QuranVersesResponse(
        sura=sura,
        total=len(verses),
        verses=[QuranVerseResponse(**v.to_dict()) for v in verses]
    )

@router.get(
    "/{sura}/{aya}",
    response_model=QuranVerseResponse,
    summary="Get specific verse",
    description="Get a specific verse by sura and aya number"
)
async def get_verse(
    sura: int = PathParam(..., ge=1, le=114, description="Sura number (1-114)"),
    aya: int = PathParam(..., ge=1, description="Aya number"),
    service: QuranService = Depends(get_quran_service)
):
    """Get specific verse"""
    verse = service.get_verse(sura, aya)
    return QuranVerseResponse(**verse.to_dict())
