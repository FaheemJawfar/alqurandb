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
