"""Translation API endpoints"""
from fastapi import APIRouter, Depends, Path as PathParam
from fastapi.responses import FileResponse

from app.services.translation_service import TranslationService
from app.schemas.translation import TranslationList
from app.models.translation import FileType


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
    filetype: FileType = PathParam(..., description="File type (json or csv)"),
    service: TranslationService = Depends(get_translation_service)
):
    """
    Download a translation file

    Parameters:
    - translation_id: Translation ID
    - filetype: File type (json or csv)

    Examples:
    - /api/v1/translations/download/tamil_johntrust/json
    - /api/v1/translations/download/tamil_johntrust/csv
    """
    file_path = service.get_translation_file(translation_id, filetype)

    # Set media type based on file type
    if filetype == FileType.JSON:
        media_type = "application/json"
    else:
        media_type = "text/csv"

    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=f"{translation_id}.{filetype.value}"
    )
