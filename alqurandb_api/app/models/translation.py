"""Translation data models"""
from enum import Enum


class FileType(str, Enum):
    """Supported file types for translations"""
    JSON = "json"
    CSV = "csv"
    SQLITE = "sqlite"
    DB = "db"
    XML = "xml"
    XLSX = "xlsx"
    SQL = "sql"
