"""Verse data models"""


class Verse:
    """Model for a Quran verse"""

    def __init__(self, translation_id: str, sura: int, aya: int, text: str, footnotes: str = None):
        self.translation_id = translation_id
        self.sura = sura
        self.aya = aya
        self.text = text
        self.footnotes = footnotes

    def to_dict(self):
        """Convert verse to dictionary"""
        result = {
            "translation_id": self.translation_id,
            "sura": self.sura,
            "aya": self.aya,
            "text": self.text
        }
        # Include footnotes if they exist and are not empty
        if self.footnotes and self.footnotes.strip():
            result["footnotes"] = self.footnotes
        return result
