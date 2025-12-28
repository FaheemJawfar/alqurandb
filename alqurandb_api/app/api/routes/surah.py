from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
async def get_all_surahs():
    return {
        "message": "List of all surahs will be returned here"
    }


@router.get("/{surah_number}")
async def get_surah(surah_number: int):
    if surah_number < 1 or surah_number > 114:
        raise HTTPException(status_code=404, detail="Surah not found")

    return {
        "surah_number": surah_number,
        "message": "Surah details will be returned here"
    }
