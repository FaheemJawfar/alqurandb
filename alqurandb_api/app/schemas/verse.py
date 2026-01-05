"""Verse API schemas"""
from pydantic import BaseModel, Field


class VerseItem(BaseModel):
    """Schema for a verse item within a collection (no translation_id)"""
    sura: int = Field(..., ge=1, le=114, description="Sura number (1-114)")
    aya: int = Field(..., ge=1, description="Aya number")
    text: str = Field(..., description="Verse text")
    footnotes: str | None = Field(None, description="Footnotes for the verse")


class VerseResponse(BaseModel):
    """Response schema for a single verse"""
    translation_id: str = Field(..., description="Translation identifier")
    sura: int = Field(..., ge=1, le=114, description="Sura number (1-114)")
    aya: int = Field(..., ge=1, description="Aya number")
    text: str = Field(..., description="Verse text")
    footnotes: str | None = Field(None, description="Footnotes for the verse")


class VersesResponse(BaseModel):
    """Response schema for multiple verses"""
    model_config = {"exclude_none": True}
    
    translation_id: str = Field(..., description="Translation identifier")
    sura: int | None = Field(None, description="Sura number if filtered")
    total: int = Field(..., description="Total number of verses")
    verses: list[VerseItem] = Field(..., description="List of verses")


class QuranVerseResponse(BaseModel):
    """Response schema for a single Quran verse (no footnotes)"""
    sura: int = Field(..., ge=1, le=114, description="Sura number (1-114)")
    aya: int = Field(..., ge=1, description="Aya number")
    text: str = Field(..., description="Verse text")


class QuranVersesResponse(BaseModel):
    """Response schema for multiple Quran verses (no footnotes)"""
    model_config = {"exclude_none": True}
    
    sura: int | None = Field(None, description="Sura number if filtered")
    total: int = Field(..., description="Total number of verses")
    verses: list[QuranVerseResponse] = Field(..., description="List of verses")
