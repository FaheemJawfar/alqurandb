"""Repository for verse data access"""
import sqlite3
from pathlib import Path
from typing import Optional

from app.models.verse import Verse
from app.core.exceptions import VerseNotFoundException


class VerseRepository:
    """Repository for accessing verse data from SQLite database"""

    def __init__(self, db_path: Path):
        self.db_path = db_path

    def _get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    def get_verse(self, translation_id: str, surah: int, ayah: int) -> Verse:
        """Get a specific verse by translation, surah, and ayah"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT translation_id, surah, ayah, text FROM verses WHERE translation_id = ? AND surah = ? AND ayah = ?',
            (translation_id, surah, ayah)
        )

        row = cursor.fetchone()
        conn.close()

        if not row:
            raise VerseNotFoundException(translation_id, surah, ayah)

        return Verse(*row)

    def get_verses_by_surah(self, translation_id: str, surah: int) -> list[Verse]:
        """Get all verses from a specific surah"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT translation_id, surah, ayah, text FROM verses WHERE translation_id = ? AND surah = ? ORDER BY ayah',
            (translation_id, surah)
        )

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            raise VerseNotFoundException(translation_id, surah)

        return [Verse(*row) for row in rows]

    def get_verses_by_range(
        self,
        translation_id: str,
        surah: int,
        from_ayah: int,
        to_ayah: int
    ) -> list[Verse]:
        """Get verses within a specific ayah range in a surah"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            '''SELECT translation_id, surah, ayah, text FROM verses
               WHERE translation_id = ? AND surah = ? AND ayah >= ? AND ayah <= ?
               ORDER BY ayah''',
            (translation_id, surah, from_ayah, to_ayah)
        )

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            raise VerseNotFoundException(translation_id, surah, from_ayah)

        return [Verse(*row) for row in rows]

    def get_all_verses(self, translation_id: str) -> list[Verse]:
        """Get all verses from a translation"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT translation_id, surah, ayah, text FROM verses WHERE translation_id = ? ORDER BY surah, ayah',
            (translation_id,)
        )

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            raise VerseNotFoundException(translation_id)

        return [Verse(*row) for row in rows]
