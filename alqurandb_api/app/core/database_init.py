import csv
import json
import sqlite3
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
                source TEXT NOT NULL,
                has_footnotes INTEGER DEFAULT 0
            )
        ''')

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

        # Insert translations and create individual tables
        for csv_file in csv_files:
            translation_id = csv_file.stem

            try:
                # Get metadata
                meta = metadata_dict.get(translation_id, {})

                # Check if CSV has footnotes column
                has_footnotes = False
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    if 'footnotes' in reader.fieldnames:
                        has_footnotes = True

                # Insert translation metadata
                cursor.execute(
                    'INSERT INTO translations (id, language, translator, name_in_language, source, has_footnotes) VALUES (?, ?, ?, ?, ?, ?)',
                    (
                        translation_id,
                        meta.get('language', 'Unknown'),
                        meta.get('translator', 'Unknown'),
                        meta.get('name_in_language', ''),
                        meta.get('source', 'tanzil.net'),
                        1 if has_footnotes else 0
                    )
                )

                # Create table for this translation
                # Sanitize table name: replace hyphens with underscores
                table_name = f"translation_{translation_id.replace('-', '_')}"
                
                if has_footnotes:
                    cursor.execute(f'''
                        CREATE TABLE {table_name} (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            sura INTEGER NOT NULL,
                            aya INTEGER NOT NULL,
                            text TEXT NOT NULL,
                            footnotes TEXT
                        )
                    ''')
                else:
                    cursor.execute(f'''
                        CREATE TABLE {table_name} (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            sura INTEGER NOT NULL,
                            aya INTEGER NOT NULL,
                            text TEXT NOT NULL
                        )
                    ''')

                # Create indexes for this translation table
                sanitized_id = translation_id.replace('-', '_')
                cursor.execute(f'CREATE INDEX idx_{sanitized_id}_sura ON {table_name}(sura)')
                cursor.execute(f'CREATE INDEX idx_{sanitized_id}_sura_aya ON {table_name}(sura, aya)')

                # Insert verses
                verses = []
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if has_footnotes:
                            verses.append((
                                int(row['sura']),
                                int(row['aya']),
                                row['text'],
                                row.get('footnotes', '')
                            ))
                        else:
                            verses.append((
                                int(row['sura']),
                                int(row['aya']),
                                row['text']
                            ))

                if has_footnotes:
                    cursor.executemany(
                        f'INSERT INTO {table_name} (sura, aya, text, footnotes) VALUES (?, ?, ?, ?)',
                        verses
                    )
                else:
                    cursor.executemany(
                        f'INSERT INTO {table_name} (sura, aya, text) VALUES (?, ?, ?)',
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

        # Calculate total verses across all translation tables
        verse_count = 0
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'translation_%'")
        for (table_name,) in cursor.fetchall():
            cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
            verse_count += cursor.fetchone()[0]

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


def ensure_database_exists() -> bool:
    """
    Ensure the complete translations database exists and is current.
    Forces recreation of the database on every startup to ensure schema changes are applied.

    Returns:
        True if database was created successfully
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

    # always Create or update database
    logger.info("Forcing recreation of complete translations database...")

    return create_complete_database(db_path, csv_dir, metadata_file)
