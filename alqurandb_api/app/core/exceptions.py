"""Custom exceptions for the application"""
from fastapi import HTTPException, status


class TranslationNotFoundException(HTTPException):
    """Raised when a translation is not found"""
    def __init__(self, translation_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Translation '{translation_id}' not found"
        )


class TranslationFileNotFoundException(HTTPException):
    """Raised when a translation file is not found"""
    def __init__(self, translation_id: str, file_type: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Translation file '{translation_id}.{file_type}' not found"
        )


class MetadataNotFoundException(HTTPException):
    """Raised when metadata file is not found"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Metadata file not found"
        )


class InvalidMetadataException(HTTPException):
    """Raised when metadata file is invalid"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid metadata file"
        )


class VerseNotFoundException(HTTPException):
    """Raised when a verse is not found"""
    def __init__(self, translation_id: str, surah: int | None = None, ayah: int | None = None):
        if ayah is not None and surah is not None:
            detail = f"Verse {surah}:{ayah} not found in translation '{translation_id}'"
        elif surah is not None:
            detail = f"Surah {surah} not found in translation '{translation_id}'"
        else:
            detail = f"No verses found for translation '{translation_id}'"

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )
