"""Translation repository for data access"""
from pathlib import Path
import json
import sqlite3
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
        self.db_path = self.data_dir / "quran_translations.db"
        self.translations_dir = self.data_dir / "translations"
        self._metadata_cache: Optional[list[TranslationMetadata]] = None

    def _get_db_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        if not self.db_path.exists():
            raise MetadataNotFoundException()
        return sqlite3.connect(self.db_path)

    def get_metadata(self) -> list[TranslationMetadata]:
        """Load and cache metadata from database"""
        if self._metadata_cache is None:
            try:
                conn = self._get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT id, language, translator, name_in_language, source FROM translations ORDER BY language, translator'
                )
                rows = cursor.fetchall()
                conn.close()

                self._metadata_cache = []
                for row in rows:
                    self._metadata_cache.append(TranslationMetadata(
                        id=row[0],
                        language=row[1],
                        translator=row[2],
                        name_in_language=row[3],
                        source=row[4]
                    ))
            except Exception as e:
                raise InvalidMetadataException()

        return self._metadata_cache

    def get_all_translations(self) -> list[TranslationMetadata]:
        """Get all translation metadata"""
        return self.get_metadata()

    def get_translation_by_id(self, translation_id: str) -> Optional[TranslationMetadata]:
        """Get translation metadata by ID"""
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id, language, translator, name_in_language, source FROM translations WHERE id = ?',
                (translation_id,)
            )
            row = cursor.fetchone()
            conn.close()

            if row:
                return TranslationMetadata(
                    id=row[0],
                    language=row[1],
                    translator=row[2],
                    name_in_language=row[3],
                    source=row[4]
                )
            return None
        except Exception:
            return None

    def translation_exists(self, translation_id: str) -> bool:
        """Check if translation exists"""
        translation = self.get_translation_by_id(translation_id)
        return translation is not None

    def get_translation_file_path(self, translation_id: str, file_type: str) -> Path:
        """Get path to translation file"""
        # Map file types to their extensions and directory names
        if file_type == "sqlite":
            file_extension = "db"
            directory = "sqlite"
        else:
            file_extension = file_type
            directory = file_type

        file_path = self.translations_dir / directory / f"{translation_id}.{file_extension}"
        if not file_path.exists():
            raise TranslationFileNotFoundException(translation_id, file_type)
        return file_path

    def load_translation_data(self, translation_id: str) -> dict:
        """Load translation data from database"""
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'SELECT surah, ayah, text FROM verses WHERE translation_id = ? ORDER BY surah, ayah',
                (translation_id,)
            )
            rows = cursor.fetchall()
            conn.close()

            # Convert to dictionary format: "surah:ayah" -> "text"
            data = {}
            for row in rows:
                key = f"{row[0]}:{row[1]}"
                data[key] = row[2]

            return data
        except Exception as e:
            raise TranslationFileNotFoundException(translation_id, "data")

    def clear_cache(self):
        """Clear metadata cache"""
        self._metadata_cache = None
