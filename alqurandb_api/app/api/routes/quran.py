from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_quran_info():
    return {
        "total_surahs": 114,
        "total_ayahs": 6236,
        "message": "AlQuran Database"
    }
