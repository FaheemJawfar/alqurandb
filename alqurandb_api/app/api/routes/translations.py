"""Translation API endpoints"""
from fastapi import APIRouter, Depends, Query, Path as PathParam
from fastapi.responses import FileResponse
from pathlib import Path

from app.services.translation_service import TranslationService
from app.services.verse_service import VerseService
from app.repositories.verse_repository import VerseRepository
from app.schemas.translation import TranslationList
from app.schemas.verse import VerseResponse, VersesResponse
from app.models.translation import FileType
from app.core.config import settings


router = APIRouter()


def get_translation_service() -> TranslationService:
    """Dependency injection for translation service"""
    return TranslationService()


def get_verse_repository() -> VerseRepository:
    """Dependency for verse repository"""
    db_path = Path(settings.DATA_DIR) / "quran_translations.db"
    return VerseRepository(db_path)


def get_verse_service(
    repository: VerseRepository = Depends(get_verse_repository)
) -> VerseService:
    """Dependency for verse service"""
    return VerseService(repository)


@router.get("/", response_model=TranslationList)
async def list_translations(service: TranslationService = Depends(get_translation_service)):
    """
    Get list of all available translations

    Returns:
    - total: Total number of translations
    - translations: List of translation metadata
    """
    return service.get_all_translations()


@router.get("/download/{translation_id}/{filetype}")
async def download_translation(
    translation_id: str = PathParam(..., description="Translation ID"),
    filetype: FileType = PathParam(..., description="File type (json, csv, sqlite, xml, or xlsx)"),
    service: TranslationService = Depends(get_translation_service)
):
    """
    Download a translation file

    Parameters:
    - translation_id: Translation ID
    - filetype: File type (json, csv, sqlite, xml, or xlsx)

    Examples:
    - /api/v1/translations/download/tamil_johntrust/json
    - /api/v1/translations/download/tamil_johntrust/csv
    - /api/v1/translations/download/tamil_johntrust/sqlite
    - /api/v1/translations/download/tamil_johntrust/xml
    - /api/v1/translations/download/tamil_johntrust/xlsx
    """
    file_path = service.get_translation_file(translation_id, filetype)

    # Set media type and filename based on file type
    if filetype == FileType.JSON:
        media_type = "application/json"
        filename = f"{translation_id}.json"
    elif filetype == FileType.CSV:
        media_type = "text/csv"
        filename = f"{translation_id}.csv"
    elif filetype == FileType.SQLITE:
        media_type = "application/x-sqlite3"
        filename = f"{translation_id}.db"
    elif filetype == FileType.XML:
        media_type = "application/xml"
        filename = f"{translation_id}.xml"
    else:
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"{translation_id}.xlsx"

    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename
    )


@router.get(
    "/{translation_id}/{surah}/{ayah}",
    response_model=VerseResponse,
    summary="Get a specific verse",
    description="Get a specific verse by translation ID, surah number, and ayah number"
)
async def get_verse(
    translation_id: str = PathParam(..., description="Translation identifier (e.g., english_sahih)"),
    surah: int = PathParam(..., ge=1, le=114, description="Surah number (1-114)"),
    ayah: int = PathParam(..., ge=1, description="Ayah number"),
    service: VerseService = Depends(get_verse_service)
):
    """Get a specific verse"""
    verse = service.get_verse(translation_id, surah, ayah)
    return VerseResponse(**verse.to_dict())


@router.get(
    "/{translation_id}/{surah}",
    response_model=VersesResponse,
    summary="Get all verses from a surah",
    description="Get all verses from a specific surah in a translation"
)
async def get_surah(
    translation_id: str = PathParam(..., description="Translation identifier (e.g., english_sahih)"),
    surah: int = PathParam(..., ge=1, le=114, description="Surah number (1-114)"),
    from_ayah: int | None = Query(None, ge=1, description="Starting ayah number (optional)"),
    to_ayah: int | None = Query(None, ge=1, description="Ending ayah number (optional)"),
    service: VerseService = Depends(get_verse_service)
):
    """Get verses from a surah, optionally filtered by ayah range"""
    if from_ayah is not None and to_ayah is not None:
        verses = service.get_verses_by_range(translation_id, surah, from_ayah, to_ayah)
    else:
        verses = service.get_verses_by_surah(translation_id, surah)

    return VersesResponse(
        translation_id=translation_id,
        surah=surah,
        total=len(verses),
        verses=[VerseResponse(**v.to_dict()) for v in verses]
    )


@router.get(
    "/{translation_id}",
    response_model=VersesResponse,
    summary="Get all verses from a translation",
    description="Get all 6236 verses from a complete translation"
)
async def get_translation_verses(
    translation_id: str = PathParam(..., description="Translation identifier (e.g., english_sahih)"),
    service: VerseService = Depends(get_verse_service)
):
    """Get all verses from a translation"""
    verses = service.get_all_verses(translation_id)

    return VersesResponse(
        translation_id=translation_id,
        surah=None,
        total=len(verses),
        verses=[VerseResponse(**v.to_dict()) for v in verses]
    )


