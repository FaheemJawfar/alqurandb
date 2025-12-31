#!/usr/bin/env python3
"""
Create a comprehensive SQLite database with all Quran translations

This script creates a single SQLite database containing all translations
with proper indexing for fast queries.

Database Schema:
- translations: metadata for each translation
- verses: all verses from all translations with translation_id reference
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
        print(f"❌ No CSV files found in {csv_dir}")
        return

    print(f"\nCreating database with {len(csv_files)} translations...")

    total_verses = 0
    successful = 0
    failed = 0

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

            print(f"  ✓ {translation_id}: {verse_count} verses")

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

    cursor.execute('SELECT COUNT(*) FROM verses')
    verse_count = cursor.fetchone()[0]

    conn.close()

    # Get file size
    size_mb = db_path.stat().st_size / (1024 * 1024)

    print(f"\n{'='*80}")
    print(f"  Database created successfully!")
    print(f"{'='*80}")
    print(f"  Location: {db_path}")
    print(f"  Size: {size_mb:.2f} MB")
    print(f"  Translations: {translation_count}")
    print(f"  Total verses: {verse_count}")
    print(f"  Successful: {successful}")
    if failed > 0:
        print(f"  Failed: {failed}")
    print(f"  Metadata hash: {metadata_hash[:16]}...")
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
