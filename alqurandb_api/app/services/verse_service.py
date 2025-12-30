"""Service layer for verse operations"""
from app.repositories.verse_repository import VerseRepository
from app.models.verse import Verse


class VerseService:
    """Service for verse operations"""

    def __init__(self, repository: VerseRepository):
        self.repository = repository

    def get_verse(self, translation_id: str, sura: int, aya: int) -> Verse:
        """Get a specific verse"""
        return self.repository.get_verse(translation_id, sura, aya)

    def get_verses_by_sura(self, translation_id: str, sura: int) -> list[Verse]:
        """Get all verses from a sura"""
        return self.repository.get_verses_by_sura(translation_id, sura)

    def get_verses_by_range(
        self,
        translation_id: str,
        sura: int,
        from_aya: int,
        to_aya: int
    ) -> list[Verse]:
        """Get verses within a range"""
        return self.repository.get_verses_by_range(translation_id, sura, from_aya, to_aya)

    def get_all_verses(self, translation_id: str) -> list[Verse]:
        """Get all verses from a translation"""
        return self.repository.get_all_verses(translation_id)
