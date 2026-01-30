from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.api import api_router
from app.core.config import settings
from app.core.database_init import ensure_database_exists

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI startup and shutdown events
    """
    # Startup: Ensure database exists and is up to date
    logger.info("Starting AlQuranDB API...")
    logger.info("Checking database status...")

    if ensure_database_exists():
        logger.info("Database is ready")
    else:
        logger.error("Failed to initialize database")
        # Note: We don't raise an exception here to allow the API to start
        # even if database initialization fails

    yield

    # Shutdown
    logger.info("Shutting down AlQuranDB API...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    return {"message": "Welcome to AlQuranDB API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
