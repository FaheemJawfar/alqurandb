from fastapi import APIRouter, HTTPException, Query
from typing import Optional

router = APIRouter()


@router.get("/{surah_number}/{ayah_number}")
async def get_ayah(
    surah_number: int,
    ayah_number: int,
    translation: Optional[str] = Query(
        None,
        description="Translation ID (e.g., 'sahih', 'yusufali', 'pickthall')"
    )
):
    """
    Get a specific Ayah with optional translation

    - **surah_number**: Surah number (1-114)
    - **ayah_number**: Ayah number
    - **translation**: Optional translation ID
    """
    if surah_number < 1 or surah_number > 114:
        raise HTTPException(status_code=404, detail="Surah not found")

    response = {
        "surah_number": surah_number,
        "ayah_number": ayah_number,
        "text_arabic": "Sample Arabic text will be here",
        "text_uthmani": "Sample Uthmani script will be here"
    }

    if translation:
        # This is where you would fetch the actual translation from database
        response["translation"] = {
            "id": translation,
            "text": f"Sample translation text for {translation}",
            "name": translation.title()
        }

    return response
