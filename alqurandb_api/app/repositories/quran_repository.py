
import sqlite3
from typing import List, Optional
from pathlib import Path

from app.models.verse import Verse
from app.core.exceptions import VerseNotFoundException

class QuranRepository:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.table_name = "quran_text"

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_verse(self, sura: int, aya: int) -> Verse:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            f'SELECT sura, aya, text FROM {self.table_name} WHERE sura = ? AND aya = ?',
            (sura, aya)
        )
        row = cursor.fetchone()
        conn.close()

        if not row:
            raise VerseNotFoundException("quran", sura, aya) # using "quran" as placeholder translation_id

        return Verse("quran", row[0], row[1], row[2])

    def get_verses_by_sura(self, sura: int) -> List[Verse]:
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f'SELECT sura, aya, text FROM {self.table_name} WHERE sura = ? ORDER BY aya',
            (sura,)
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            # If no verses found for sura 1-114, it might mean the DB isn't populated or invalid sura
             # But for now, returning empty list or raising exception is fine.
             # Existing behavior seems to be raise exception if empty? checking verse_repo
             pass 
        
        # If we want to be strict about sura validity (1-114), we could check that first.
        # But if the query returns empty, it effectively means not found.
        if not rows and 1 <= sura <= 114:
             # It might be a valid sura but we have no data? unlikely for Quran.
             pass

        return [Verse("quran", row[0], row[1], row[2]) for row in rows]

    def get_all_verses(self) -> List[Verse]:
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(f'SELECT sura, aya, text FROM {self.table_name} ORDER BY sura, aya')
        rows = cursor.fetchall()
        conn.close()

        return [Verse("quran", row[0], row[1], row[2]) for row in rows]
