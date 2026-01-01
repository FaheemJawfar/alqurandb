#!/usr/bin/env python3
"""
Create a comprehensive SQLite database with all Quran translations

This script creates a single SQLite database containing all translations
with proper indexing for fast queries.

Database Schema:
- translations: metadata for each translation (includes has_footnotes flag)
- translation_<id>: individual table for each translation with verses
  - Each table has: id (auto-increment), sura, aya, text, footnotes (if applicable)
  - Indexed on sura and (sura, aya) for fast queries
- metadata_info: stores metadata hash for change detection

Note: This script is kept for manual database creation. The API now
automatically creates/updates the database on startup using the same logic
from app.core.database_init module.
"""

import csv
import json
import sqlite3
import hashlib
from pathlib import Path


def create_database(db_path, csv_dir, metadata_file):
    """Create SQLite database with all translations"""

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
        print(f"❌ No CSV files found in {csv_dir}")
        return

    print(f"\nCreating database with {len(csv_files)} translations...")

    total_verses = 0
    successful = 0
    failed = 0

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
            # Sanitize table name: replace hyphens with underscores to avoid SQL syntax errors
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

            footnote_indicator = " (with footnotes)" if has_footnotes else ""
            print(f"  ✓ {translation_id}: {verse_count} verses{footnote_indicator}")

        except Exception as e:
            print(f"  ✗ {translation_id}: Error - {e}")
            failed += 1

    # Commit changes
    conn.commit()

    # Create metadata_info table and store metadata hash
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metadata_info (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    # Calculate and store metadata hash
    sha256_hash = hashlib.sha256()
    with open(metadata_file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    metadata_hash = sha256_hash.hexdigest()

    cursor.execute("""
        INSERT OR REPLACE INTO metadata_info (key, value)
        VALUES ('metadata_hash', ?)
    """, (metadata_hash,))

    conn.commit()

    # Get database statistics
    cursor.execute('SELECT COUNT(*) FROM translations')
    translation_count = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM translations WHERE has_footnotes = 1')
    footnote_count = cursor.fetchone()[0]

    # Count total verses across all translation tables
    total_verse_count = 0
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'translation_%'")
    for (table_name,) in cursor.fetchall():
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        total_verse_count += cursor.fetchone()[0]

    conn.close()

    # Get file size
    size_mb = db_path.stat().st_size / (1024 * 1024)

    print(f"\n{'='*80}")
    print(f"  Database created successfully!")
    print(f"{'='*80}")
    print(f"  Location: {db_path}")
    print(f"  Size: {size_mb:.2f} MB")
    print(f"  Translations: {translation_count}")
    print(f"  Translations with footnotes: {footnote_count}")
    print(f"  Total verses: {total_verse_count}")
    print(f"  Successful: {successful}")
    if failed > 0:
        print(f"  Failed: {failed}")
    print(f"  Metadata hash: {metadata_hash[:16]}...")
    print(f"  Schema: Individual tables per translation")
    print(f"{'='*80}\n")


def main():
    """Main function"""

    # Paths
    script_dir = Path(__file__).parent
    api_data_dir = script_dir.parent / 'alqurandb_api' / 'data'
    csv_dir = api_data_dir / 'translations' / 'csv'
    metadata_file = api_data_dir / 'metadata.json'
    db_path = api_data_dir / 'quran_translations.db'

    print("\n" + "="*80)
    print("  AlQuranDB - Create Complete SQLite Database")
    print("="*80)
    print("\nCreating a comprehensive database with all Quran translations...")
    print(f"Source: {csv_dir}")
    print(f"Output: {db_path}")
    print("="*80)

    create_database(db_path, csv_dir, metadata_file)


if __name__ == '__main__':
    main()
