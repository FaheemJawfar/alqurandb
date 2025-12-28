"""Translation service for business logic"""
from pathlib import Path
from typing import Optional

from app.repositories.translation_repository import TranslationRepository
from app.schemas.translation import TranslationMetadata, TranslationList, TranslationData
from app.models.translation import FileType
from app.core.exceptions import TranslationNotFoundException


class TranslationService:
    """Service for translation business logic"""

    def __init__(self):
        self.repository = TranslationRepository()

    def get_all_translations(self) -> TranslationList:
        """Get all available translations"""
        translations = self.repository.get_all_translations()
        return TranslationList(
            total=len(translations),
            translations=translations
        )

    def get_translation_metadata(self, translation_id: str) -> TranslationMetadata:
        """Get metadata for a specific translation"""
        translation = self.repository.get_translation_by_id(translation_id)
        if not translation:
            raise TranslationNotFoundException(translation_id)
        return translation

    def get_translation_file(self, translation_id: str, file_type: FileType) -> Path:
        """Get path to translation file"""
        # Verify translation exists first
        if not self.repository.translation_exists(translation_id):
            raise TranslationNotFoundException(translation_id)

        # Get the file path (will raise TranslationFileNotFoundException if not found)
        return self.repository.get_translation_file_path(translation_id, file_type.value)

    def get_translation_data(self, translation_id: str) -> TranslationData:
        """Get translation data with metadata"""
        # Verify translation exists
        metadata = self.get_translation_metadata(translation_id)

        # Load translation data
        data = self.repository.load_translation_data(translation_id)

        return TranslationData(
            metadata=metadata,
            data=data
        )

    def clear_cache(self):
        """Clear metadata cache"""
        self.repository.clear_cache()
