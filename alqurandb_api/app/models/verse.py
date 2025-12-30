"""Verse data models"""


class Verse:
    """Model for a Quran verse"""

    def __init__(self, translation_id: str, sura: int, aya: int, text: str):
        self.translation_id = translation_id
        self.sura = sura
        self.aya = aya
        self.text = text

    def to_dict(self):
        """Convert verse to dictionary"""
        return {
            "translation_id": self.translation_id,
            "sura": self.sura,
            "aya": self.aya,
            "text": self.text
        }
