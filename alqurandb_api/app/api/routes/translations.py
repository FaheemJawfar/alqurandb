from fastapi import APIRouter, HTTPException, Path as PathParam
from fastapi.responses import FileResponse
from pathlib import Path
from enum import Enum
import json

router = APIRouter()

# Data directory paths
DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"
METADATA_FILE = DATA_DIR / "metadata.json"
TRANSLATIONS_DIR = DATA_DIR / "translations"


class FileType(str, Enum):
    json = "json"


def load_metadata():
    """Load translation metadata from JSON file"""
    try:
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Metadata file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid metadata file")


@router.get("/")
async def list_translations():
    """Get list of all available translations"""
    metadata = load_metadata()

    return {
        "total": len(metadata),
        "translations": [
            {
                "id": t["id"],
                "language": t["language"],
                "translator": t["translator"],
                "name_in_language": t.get("name_in_language", ""),
                "source": t.get("source", "tanzil.net")
            }
            for t in metadata
        ]
    }


@router.get("/download/{id}/{filetype}")
async def download_translation(
    id: str = PathParam(..., description="Translation ID"),
    filetype: FileType = PathParam(..., description="File type (json)")
):
    """
    Download a translation file

    Parameters:
    - id: Translation ID
    - filetype: File type (json)

    Example:
    - /api/v1/translations/download/tamil_johntrust/json
    """
    metadata = load_metadata()

    # Verify translation exists
    if not any(t["id"] == id for t in metadata):
        raise HTTPException(status_code=404, detail=f"Translation '{id}' not found")

    # Build file path based on filetype
    file_path = TRANSLATIONS_DIR / filetype.value / f"{id}.json"

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Translation file not found")

    return FileResponse(
        path=file_path,
        media_type="application/json",
        filename=f"{id}.json"
    )
