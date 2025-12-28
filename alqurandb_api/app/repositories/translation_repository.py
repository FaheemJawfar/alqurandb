"""Translation repository for data access"""
from pathlib import Path
import json
from typing import Optional

from app.core.config import settings
from app.core.exceptions import (
    MetadataNotFoundException,
    InvalidMetadataException,
    TranslationFileNotFoundException
)
from app.schemas.translation import TranslationMetadata


class TranslationRepository:
    """Repository for translation data operations"""

    def __init__(self):
        self.data_dir = Path(settings.DATA_DIR)
        self.metadata_file = self.data_dir / "metadata.json"
        self.translations_dir = self.data_dir / "translations"
        self._metadata_cache: Optional[list[dict]] = None

    def get_metadata(self) -> list[dict]:
        """Load and cache metadata from JSON file"""
        if self._metadata_cache is None:
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self._metadata_cache = json.load(f)
            except FileNotFoundError:
                raise MetadataNotFoundException()
            except json.JSONDecodeError:
                raise InvalidMetadataException()
        return self._metadata_cache

    def get_all_translations(self) -> list[TranslationMetadata]:
        """Get all translation metadata"""
        metadata = self.get_metadata()
        translations = []
        for item in metadata:
            # Create a copy without source_id
            data = item.copy()
            data.pop('source_id', None)  # Remove source_id if it exists
            translations.append(TranslationMetadata(**data))
        return translations

    def get_translation_by_id(self, translation_id: str) -> Optional[TranslationMetadata]:
        """Get translation metadata by ID"""
        metadata = self.get_metadata()

        # Find the translation with matching ID
        translation_data = None
        for item in metadata:
            if item["id"] == translation_id:
                translation_data = item
                break

        if translation_data:
            # Create a copy without source_id
            data = translation_data.copy()
            data.pop('source_id', None)  # Remove source_id if it exists
            return TranslationMetadata(**data)

        return None

    def translation_exists(self, translation_id: str) -> bool:
        """Check if translation exists"""
        translation = self.get_translation_by_id(translation_id)
        if translation:
            return True
        return False

    def get_translation_file_path(self, translation_id: str, file_type: str) -> Path:
        """Get path to translation file"""
        file_path = self.translations_dir / file_type / f"{translation_id}.{file_type}"
        if not file_path.exists():
            raise TranslationFileNotFoundException(translation_id, file_type)
        return file_path

    def load_translation_data(self, translation_id: str) -> dict:
        """Load translation data from JSON file"""
        file_path = self.get_translation_file_path(translation_id, "json")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def clear_cache(self):
        """Clear metadata cache"""
        self._metadata_cache = None
