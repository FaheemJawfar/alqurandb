"""Service layer for verse operations"""
from app.repositories.verse_repository import VerseRepository
from app.models.verse import Verse


class VerseService:
    """Service for verse operations"""

    def __init__(self, repository: VerseRepository):
        self.repository = repository

    def get_verse(self, translation_id: str, surah: int, ayah: int) -> Verse:
        """Get a specific verse"""
        return self.repository.get_verse(translation_id, surah, ayah)

    def get_verses_by_surah(self, translation_id: str, surah: int) -> list[Verse]:
        """Get all verses from a surah"""
        return self.repository.get_verses_by_surah(translation_id, surah)

    def get_verses_by_range(
        self,
        translation_id: str,
        surah: int,
        from_ayah: int,
        to_ayah: int
    ) -> list[Verse]:
        """Get verses within a range"""
        return self.repository.get_verses_by_range(translation_id, surah, from_ayah, to_ayah)

    def get_all_verses(self, translation_id: str) -> list[Verse]:
        """Get all verses from a translation"""
        return self.repository.get_all_verses(translation_id)
