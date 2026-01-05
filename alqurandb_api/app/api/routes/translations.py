"""Translation API endpoints"""
from fastapi import APIRouter, Depends, Query, Path as PathParam
from fastapi.responses import FileResponse
from pathlib import Path

from app.services.translation_service import TranslationService
from app.services.verse_service import VerseService
from app.repositories.verse_repository import VerseRepository
from app.schemas.translation import TranslationList
from app.schemas.verse import VerseResponse, VersesResponse, VerseItem
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
    - /api/translations/download/tamil_johntrust/json
    - /api/translations/download/tamil_johntrust/csv
    - /api/translations/download/tamil_johntrust/sqlite
    - /api/translations/download/tamil_johntrust/xml
    - /api/translations/download/tamil_johntrust/xlsx
    """
    file_path = service.get_translation_file(translation_id, filetype)

    # Set media type and filename based on file type
    if filetype == FileType.JSON:
        media_type = "application/json"
        filename = f"{translation_id}.json"
    elif filetype == FileType.CSV:
        media_type = "text/csv"
        filename = f"{translation_id}.csv"
    elif filetype in [FileType.SQLITE, FileType.DB]:
        media_type = "application/x-sqlite3"
        filename = f"{translation_id}.db"
    elif filetype == FileType.XML:
        media_type = "application/xml"
        filename = f"{translation_id}.xml"
    elif filetype == FileType.SQL:
        media_type = "application/sql"
        filename = f"{translation_id}.sql"
    else:
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"{translation_id}.xlsx"

    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename
    )


@router.get(
    "/{translation_id}/{sura}/{aya}",
    response_model=VerseResponse,
    summary="Get a specific verse",
    description="Get a specific verse by translation ID, sura number, and aya number"
)
async def get_verse(
    translation_id: str = PathParam(..., description="Translation identifier (e.g., english_sahih)"),
    sura: int = PathParam(..., ge=1, le=114, description="Sura number (1-114)"),
    aya: int = PathParam(..., ge=1, description="Aya number"),
    service: VerseService = Depends(get_verse_service)
):
    """Get a specific verse"""
    verse = service.get_verse(translation_id, sura, aya)
    return VerseResponse(**verse.to_dict())


@router.get(
    "/{translation_id}/{sura}",
    response_model=VersesResponse,
    summary="Get all verses from a sura",
    description="Get all verses from a specific sura in a translation"
)
async def get_sura(
    translation_id: str = PathParam(..., description="Translation identifier (e.g., english_sahih)"),
    sura: int = PathParam(..., ge=1, le=114, description="Sura number (1-114)"),
    from_aya: int | None = Query(None, ge=1, description="Starting aya number (optional)"),
    to_aya: int | None = Query(None, ge=1, description="Ending aya number (optional)"),
    service: VerseService = Depends(get_verse_service)
):
    """Get verses from a sura, optionally filtered by aya range"""
    if from_aya is not None and to_aya is not None:
        verses = service.get_verses_by_range(translation_id, sura, from_aya, to_aya)
    else:
        verses = service.get_verses_by_sura(translation_id, sura)

    return VersesResponse(
        translation_id=translation_id,
        sura=sura,
        total=len(verses),
        verses=[VerseItem(**v.to_item_dict()) for v in verses]
    )


@router.get(
    "/{translation_id}",
    summary="Get all verses from a translation",
    description="Get all 6236 verses from a complete translation"
)
async def get_translation_verses(
    translation_id: str = PathParam(..., description="Translation identifier (e.g., english_sahih)"),
    service: VerseService = Depends(get_verse_service)
):
    """Get all verses from a translation"""
    verses = service.get_all_verses(translation_id)

    response = VersesResponse(
        translation_id=translation_id,
        sura=None,
        total=len(verses),
        verses=[VerseItem(**v.to_item_dict()) for v in verses]
    )
    return response.model_dump(exclude_none=True)


