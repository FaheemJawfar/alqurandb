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

    def _get_table_name(self, translation_id: str) -> str:
        """Get the table name for a translation, sanitizing the ID"""
        # Replace hyphens with underscores to match the database schema
        sanitized_id = translation_id.replace('-', '_')
        return f"translation_{sanitized_id}"

    def _table_has_footnotes(self, table_name: str) -> bool:
        """Check if a table has a footnotes column"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f'PRAGMA table_info({table_name})')
        columns = [row[1] for row in cursor.fetchall()]
        conn.close()
        return 'footnotes' in columns

    def get_verse(self, translation_id: str, sura: int, aya: int) -> Verse:
        """Get a specific verse by translation, sura, and aya"""
        conn = self._get_connection()
        cursor = conn.cursor()

        table_name = self._get_table_name(translation_id)
        has_footnotes = self._table_has_footnotes(table_name)
        
        if has_footnotes:
            cursor.execute(
                f'SELECT sura, aya, text, footnotes FROM {table_name} WHERE sura = ? AND aya = ?',
                (sura, aya)
            )
        else:
            cursor.execute(
                f'SELECT sura, aya, text FROM {table_name} WHERE sura = ? AND aya = ?',
                (sura, aya)
            )

        row = cursor.fetchone()
        conn.close()

        if not row:
            raise VerseNotFoundException(translation_id, sura, aya)

        # Return Verse with translation_id prepended
        if has_footnotes:
            return Verse(translation_id, row[0], row[1], row[2], row[3])
        else:
            return Verse(translation_id, row[0], row[1], row[2])

    def get_verses_by_sura(self, translation_id: str, sura: int) -> list[Verse]:
        """Get all verses from a specific sura"""
        conn = self._get_connection()
        cursor = conn.cursor()

        table_name = self._get_table_name(translation_id)
        has_footnotes = self._table_has_footnotes(table_name)

        if has_footnotes:
            cursor.execute(
                f'SELECT sura, aya, text, footnotes FROM {table_name} WHERE sura = ? ORDER BY aya',
                (sura,)
            )
        else:
            cursor.execute(
                f'SELECT sura, aya, text FROM {table_name} WHERE sura = ? ORDER BY aya',
                (sura,)
            )

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            raise VerseNotFoundException(translation_id, sura)

        if has_footnotes:
            return [Verse(translation_id, row[0], row[1], row[2], row[3]) for row in rows]
        else:
            return [Verse(translation_id, row[0], row[1], row[2]) for row in rows]

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

        table_name = self._get_table_name(translation_id)
        has_footnotes = self._table_has_footnotes(table_name)

        if has_footnotes:
            cursor.execute(
                f'''SELECT sura, aya, text, footnotes FROM {table_name}
                   WHERE sura = ? AND aya >= ? AND aya <= ?
                   ORDER BY aya''',
                (sura, from_aya, to_aya)
            )
        else:
            cursor.execute(
                f'''SELECT sura, aya, text FROM {table_name}
                   WHERE sura = ? AND aya >= ? AND aya <= ?
                   ORDER BY aya''',
                (sura, from_aya, to_aya)
            )

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            raise VerseNotFoundException(translation_id, sura, from_aya)

        if has_footnotes:
            return [Verse(translation_id, row[0], row[1], row[2], row[3]) for row in rows]
        else:
            return [Verse(translation_id, row[0], row[1], row[2]) for row in rows]

    def get_all_verses(self, translation_id: str) -> list[Verse]:
        """Get all verses from a translation"""
        conn = self._get_connection()
        cursor = conn.cursor()

        table_name = self._get_table_name(translation_id)
        has_footnotes = self._table_has_footnotes(table_name)

        if has_footnotes:
            cursor.execute(
                f'SELECT sura, aya, text, footnotes FROM {table_name} ORDER BY sura, aya'
            )
        else:
            cursor.execute(
                f'SELECT sura, aya, text FROM {table_name} ORDER BY sura, aya'
            )

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            raise VerseNotFoundException(translation_id)

        if has_footnotes:
            return [Verse(translation_id, row[0], row[1], row[2], row[3]) for row in rows]
        else:
            return [Verse(translation_id, row[0], row[1], row[2]) for row in rows]
