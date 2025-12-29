"""Verse API schemas"""
from pydantic import BaseModel, Field


class VerseResponse(BaseModel):
    """Response schema for a single verse"""
    translation_id: str = Field(..., description="Translation identifier")
    surah: int = Field(..., ge=1, le=114, description="Surah number (1-114)")
    ayah: int = Field(..., ge=1, description="Ayah number")
    text: str = Field(..., description="Verse text")


class VersesResponse(BaseModel):
    """Response schema for multiple verses"""
    translation_id: str = Field(..., description="Translation identifier")
    surah: int | None = Field(None, description="Surah number if filtered")
    total: int = Field(..., description="Total number of verses")
    verses: list[VerseResponse] = Field(..., description="List of verses")
