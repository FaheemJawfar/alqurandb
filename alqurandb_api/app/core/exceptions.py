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
    def __init__(self, translation_id: str, file_type: str, actual_filename: str = None):
        detail = f"Translation file '{actual_filename}' not found" if actual_filename else f"Translation file '{translation_id}.{file_type}' not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
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
    def __init__(self, translation_id: str, sura: int | None = None, aya: int | None = None):
        if aya is not None and sura is not None:
            detail = f"Verse {sura}:{aya} not found in translation '{translation_id}'"
        elif sura is not None:
            detail = f"Sura {sura} not found in translation '{translation_id}'"
        else:
            detail = f"No verses found for translation '{translation_id}'"

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )
