from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_available_translations():
    """Get list of all available translations"""
    return {
        "translations": [
            {
                "id": "sahih",
                "name": "Sahih International",
                "language": "English",
                "language_code": "en",
                "available": True
            },
            {
                "id": "yusufali",
                "name": "Yusuf Ali",
                "language": "English",
                "language_code": "en",
                "available": True
            },
            {
                "id": "pickthall",
                "name": "Pickthall",
                "language": "English",
                "language_code": "en",
                "available": True
            },
            {
                "id": "khattab",
                "name": "Dr. Mustafa Khattab",
                "language": "English",
                "language_code": "en",
                "available": True
            },
            {
                "id": "maududi",
                "name": "Maududi",
                "language": "Urdu",
                "language_code": "ur",
                "available": True
            },
            {
                "id": "junagarhi",
                "name": "Muhammad Junagarhi",
                "language": "Urdu",
                "language_code": "ur",
                "available": True
            },
            {
                "id": "jalandhry",
                "name": "Fateh Muhammad Jalandhry",
                "language": "Urdu",
                "language_code": "ur",
                "available": True
            }
        ]
    }


@router.get("/{language_code}")
async def get_translations_by_language(language_code: str):
    """Get translations for a specific language"""
    all_translations = await get_available_translations()

    filtered = [
        t for t in all_translations["translations"]
        if t["language_code"] == language_code.lower()
    ]

    return {
        "language_code": language_code,
        "translations": filtered
    }
