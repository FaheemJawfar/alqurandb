"""Verse API schemas"""
from pydantic import BaseModel, Field


class VerseResponse(BaseModel):
    """Response schema for a single verse"""
    translation_id: str = Field(..., description="Translation identifier")
    sura: int = Field(..., ge=1, le=114, description="Sura number (1-114)")
    aya: int = Field(..., ge=1, description="Aya number")
    text: str = Field(..., description="Verse text")
    footnotes: str | None = Field(None, description="Footnotes for the verse")


class VersesResponse(BaseModel):
    """Response schema for multiple verses"""
    translation_id: str = Field(..., description="Translation identifier")
    sura: int | None = Field(None, description="Sura number if filtered")
    total: int = Field(..., description="Total number of verses")
    verses: list[VerseResponse] = Field(..., description="List of verses")
