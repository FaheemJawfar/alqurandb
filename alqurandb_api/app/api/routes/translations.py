"""Translation API endpoints"""
from fastapi import APIRouter, Depends, Path as PathParam
from fastapi.responses import FileResponse
from pathlib import Path

from app.services.translation_service import TranslationService
from app.schemas.translation import TranslationList
from app.models.translation import FileType
from app.core.config import settings


router = APIRouter()


def get_translation_service() -> TranslationService:
    """Dependency injection for translation service"""
    return TranslationService()


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


