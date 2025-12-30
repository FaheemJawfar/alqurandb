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

    def get_verse(self, translation_id: str, sura: int, aya: int) -> Verse:
        """Get a specific verse by translation, sura, and aya"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT translation_id, sura, aya, text FROM verses WHERE translation_id = ? AND sura = ? AND aya = ?',
            (translation_id, sura, aya)
        )

        row = cursor.fetchone()
        conn.close()

        if not row:
            raise VerseNotFoundException(translation_id, sura, aya)

        return Verse(*row)

    def get_verses_by_sura(self, translation_id: str, sura: int) -> list[Verse]:
        """Get all verses from a specific sura"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT translation_id, sura, aya, text FROM verses WHERE translation_id = ? AND sura = ? ORDER BY aya',
            (translation_id, sura)
        )

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            raise VerseNotFoundException(translation_id, sura)

        return [Verse(*row) for row in rows]

    def get_verses_by_range(
        self,
        translation_id: str,
        sura: int,
        from_aya: int,
        to_aya: int
    ) -> list[Verse]:
        """Get verses within a specific aya range in a sura"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            '''SELECT translation_id, sura, aya, text FROM verses
               WHERE translation_id = ? AND sura = ? AND aya >= ? AND aya <= ?
               ORDER BY aya''',
            (translation_id, sura, from_aya, to_aya)
        )

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            raise VerseNotFoundException(translation_id, sura, from_aya)

        return [Verse(*row) for row in rows]

    def get_all_verses(self, translation_id: str) -> list[Verse]:
        """Get all verses from a translation"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT translation_id, sura, aya, text FROM verses WHERE translation_id = ? ORDER BY sura, aya',
            (translation_id,)
        )

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            raise VerseNotFoundException(translation_id)

        return [Verse(*row) for row in rows]
