"""Database initialization utility for complete translations database"""
import csv
import json
import sqlite3
import hashlib
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def create_complete_database(db_path: Path, csv_dir: Path, metadata_file: Path) -> bool:
    """
    Create SQLite database with all translations

    Args:
        db_path: Path to the output database file
        csv_dir: Directory containing CSV translation files
        metadata_file: Path to metadata.json file

    Returns:
        True if successful, False otherwise
    """
    try:
        # Remove existing database
        if db_path.exists():
            db_path.unlink()

        # Create database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create translations metadata table
        cursor.execute('''
            CREATE TABLE translations (
                id TEXT PRIMARY KEY,
                language TEXT NOT NULL,
                translator TEXT NOT NULL,
                name_in_language TEXT,
                source TEXT NOT NULL
            )
        ''')

        # Create verses table
        cursor.execute('''
            CREATE TABLE verses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                translation_id TEXT NOT NULL,
                sura INTEGER NOT NULL,
                aya INTEGER NOT NULL,
                text TEXT NOT NULL,
                FOREIGN KEY (translation_id) REFERENCES translations(id)
            )
        ''')

        # Create indexes for fast queries
        cursor.execute('CREATE INDEX idx_translation_id ON verses(translation_id)')
        cursor.execute('CREATE INDEX idx_sura ON verses(sura)')
        cursor.execute('CREATE INDEX idx_sura_aya ON verses(sura, aya)')
        cursor.execute('CREATE INDEX idx_translation_sura ON verses(translation_id, sura)')
        cursor.execute('CREATE INDEX idx_translation_sura_aya ON verses(translation_id, sura, aya)')

        # Load metadata
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        # Create metadata lookup
        metadata_dict = {item['id']: item for item in metadata}

        # Find all CSV files
        csv_files = sorted(csv_dir.glob('*.csv'))

        if not csv_files:
            logger.error(f"No CSV files found in {csv_dir}")
            return False

        logger.info(f"Creating database with {len(csv_files)} translations...")

        total_verses = 0
        successful = 0

        # Insert translations and verses
        for csv_file in csv_files:
            translation_id = csv_file.stem

            try:
                # Get metadata
                meta = metadata_dict.get(translation_id, {})

                # Insert translation metadata
                cursor.execute(
                    'INSERT INTO translations (id, language, translator, name_in_language, source) VALUES (?, ?, ?, ?, ?)',
                    (
                        translation_id,
                        meta.get('language', 'Unknown'),
                        meta.get('translator', 'Unknown'),
                        meta.get('name_in_language', ''),
                        meta.get('source', 'tanzil.net')
                    )
                )

                # Insert verses
                verses = []
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        verses.append((
                            translation_id,
                            int(row['sura']),
                            int(row['aya']),
                            row['text']
                        ))

                cursor.executemany(
                    'INSERT INTO verses (translation_id, sura, aya, text) VALUES (?, ?, ?, ?)',
                    verses
                )

                verse_count = len(verses)
                total_verses += verse_count
                successful += 1

                logger.info(f"  ✓ {translation_id}: {verse_count} verses")

            except Exception as e:
                logger.error(f"  ✗ {translation_id}: Error - {e}")

        # Commit and close
        conn.commit()

        # Get database statistics
        cursor.execute('SELECT COUNT(*) FROM translations')
        translation_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM verses')
        verse_count = cursor.fetchone()[0]

        conn.close()

        # Get file size
        size_mb = db_path.stat().st_size / (1024 * 1024)

        logger.info(f"Database created successfully!")
        logger.info(f"  Location: {db_path}")
        logger.info(f"  Size: {size_mb:.2f} MB")
        logger.info(f"  Translations: {translation_count}")
        logger.info(f"  Total verses: {verse_count}")

        return True

    except Exception as e:
        logger.error(f"Failed to create database: {e}")
        return False


def _calculate_metadata_hash(metadata_file: Path) -> str:
    """
    Calculate SHA256 hash of metadata.json file

    Args:
        metadata_file: Path to metadata.json

    Returns:
        Hexadecimal hash string
    """
    sha256_hash = hashlib.sha256()
    with open(metadata_file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def _get_stored_metadata_hash(db_path: Path) -> str | None:
    """
    Get the stored metadata hash from database

    Args:
        db_path: Path to the database file

    Returns:
        Stored hash string or None if not found
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if metadata_info table exists
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='metadata_info'
        """)

        if not cursor.fetchone():
            conn.close()
            return None

        # Get stored hash
        cursor.execute("SELECT value FROM metadata_info WHERE key = 'metadata_hash'")
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None
    except Exception as e:
        logger.error(f"Error reading metadata hash from database: {e}")
        return None


def _store_metadata_hash(db_path: Path, metadata_hash: str) -> None:
    """
    Store metadata hash in database

    Args:
        db_path: Path to the database file
        metadata_hash: Hash string to store
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create metadata_info table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata_info (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)

        # Store or update the hash
        cursor.execute("""
            INSERT OR REPLACE INTO metadata_info (key, value)
            VALUES ('metadata_hash', ?)
        """, (metadata_hash,))

        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error storing metadata hash: {e}")


def _needs_database_update(db_path: Path, metadata_file: Path) -> bool:
    """
    Check if database needs to be updated based on metadata changes

    Args:
        db_path: Path to the database file
        metadata_file: Path to metadata.json

    Returns:
        True if database needs update, False otherwise
    """
    if not db_path.exists():
        logger.info("Database does not exist - needs creation")
        return True

    current_hash = _calculate_metadata_hash(metadata_file)
    stored_hash = _get_stored_metadata_hash(db_path)

    if stored_hash is None:
        logger.info("No metadata hash found in database - needs update")
        return True

    if current_hash != stored_hash:
        logger.info("Metadata has changed - database needs update")
        logger.info(f"  Stored hash: {stored_hash[:16]}...")
        logger.info(f"  Current hash: {current_hash[:16]}...")
        return True

    logger.info("Database is up to date")
    return False


def ensure_database_exists() -> bool:
    """
    Ensure the complete translations database exists and is up to date.
    Creates it if it doesn't exist, or updates it if metadata has changed.

    Returns:
        True if database exists or was created/updated successfully
    """
    # Define paths
    app_dir = Path(__file__).parent.parent
    data_dir = app_dir.parent / 'data'
    csv_dir = data_dir / 'translations' / 'csv'
    metadata_file = data_dir / 'metadata.json'
    db_path = data_dir / 'quran_translations.db'

    # Validate required files exist
    if not csv_dir.exists():
        logger.error(f"CSV directory not found: {csv_dir}")
        return False

    if not metadata_file.exists():
        logger.error(f"Metadata file not found: {metadata_file}")
        return False

    # Check if database needs update
    if not _needs_database_update(db_path, metadata_file):
        logger.info(f"Database is current at {db_path}")
        return True

    # Create or update database
    logger.info("Creating/updating complete translations database...")

    if create_complete_database(db_path, csv_dir, metadata_file):
        # Store the new metadata hash
        current_hash = _calculate_metadata_hash(metadata_file)
        _store_metadata_hash(db_path, current_hash)
        logger.info(f"Stored metadata hash: {current_hash[:16]}...")
        return True

    return False
