from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path


class Settings(BaseSettings):
    PROJECT_NAME: str = "AlQuranDB API"
    API_PREFIX: str = "/api"
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    # Data directory path
    DATA_DIR: Path = Path(__file__).parent.parent.parent / "data"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
