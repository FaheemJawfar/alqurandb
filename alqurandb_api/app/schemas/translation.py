"""Translation schemas for API validation"""
from typing import Optional
from pydantic import BaseModel, Field


class TranslationMetadata(BaseModel):
    """Translation metadata schema"""
    id: str = Field(..., description="Translation ID")
    language: str = Field(..., description="Language name")
    translator: str = Field(..., description="Translator name")
    name_in_language: Optional[str] = Field(None, description="Name in original language")
    source: str = Field(default="tanzil.net", description="Source of translation")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "english_sahih",
                "language": "English",
                "translator": "Saheeh International",
                "name_in_language": "Saheeh International",
                "source": "tanzil.net"
            }
        }


class TranslationList(BaseModel):
    """List of translations response"""
    total: int = Field(..., description="Total number of translations")
    translations: list[TranslationMetadata]


class TranslationData(BaseModel):
    """Translation data with metadata"""
    metadata: TranslationMetadata
    data: dict[str, str] = Field(..., description="Translation verses in 'sura:aya' format")
