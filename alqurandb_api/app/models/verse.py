"""Verse data models"""


class Verse:
    """Model for a Quran verse"""

    def __init__(self, translation_id: str, surah: int, ayah: int, text: str):
        self.translation_id = translation_id
        self.surah = surah
        self.ayah = ayah
        self.text = text

    def to_dict(self):
        """Convert verse to dictionary"""
        return {
            "translation_id": self.translation_id,
            "surah": self.surah,
            "ayah": self.ayah,
            "text": self.text
        }
