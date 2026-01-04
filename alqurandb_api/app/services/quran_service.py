
from typing import List
from app.repositories.quran_repository import QuranRepository
from app.models.verse import Verse

class QuranService:
    def __init__(self, repository: QuranRepository):
        self.repository = repository

    def get_verse(self, sura: int, aya: int) -> Verse:
        return self.repository.get_verse(sura, aya)

    def get_verses_by_sura(self, sura: int) -> List[Verse]:
        return self.repository.get_verses_by_sura(sura)

    def get_all_verses(self) -> List[Verse]:
        return self.repository.get_all_verses()
