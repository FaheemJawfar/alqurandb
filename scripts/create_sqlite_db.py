#!/usr/bin/env python3
"""
Create SQLite database with all Quran translations
"""
import json
import sqlite3
from pathlib import Path


def create_database():
    """Create SQLite database with translations"""

    # Paths
    script_dir = Path(__file__).parent
    api_data_dir = script_dir.parent / 'alqurandb_api' / 'data'
    metadata_file = api_data_dir / 'metadata.json'
    translations_dir = api_data_dir / 'translations' / 'json'
    output_file = api_data_dir / 'quran_translations.db'

    # Remove existing database
    if output_file.exists():
        output_file.unlink()

    # Create database
    conn = sqlite3.connect(output_file)
    cursor = conn.cursor()

    # Create metadata table
    cursor.execute('''
        CREATE TABLE metadata (
            id TEXT PRIMARY KEY,
            language TEXT NOT NULL,
            translator TEXT NOT NULL,
            name_in_language TEXT,
            source TEXT NOT NULL
        )
    ''')

    # Create translations table
    cursor.execute('''
        CREATE TABLE translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            translation_id TEXT NOT NULL,
            surah INTEGER NOT NULL,
            ayah INTEGER NOT NULL,
            text TEXT NOT NULL,
            FOREIGN KEY (translation_id) REFERENCES metadata(id),
            UNIQUE(translation_id, surah, ayah)
        )
    ''')

    # Create indexes for better query performance
    cursor.execute('CREATE INDEX idx_translation_id ON translations(translation_id)')
    cursor.execute('CREATE INDEX idx_surah_ayah ON translations(surah, ayah)')

    # Load metadata
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    print(f"Loading {len(metadata)} translations...")

    # Insert metadata
    for item in metadata:
        cursor.execute(
            'INSERT INTO metadata (id, language, translator, name_in_language, source) VALUES (?, ?, ?, ?, ?)',
            (item['id'], item['language'], item['translator'], item.get('name_in_language', ''), item['source'])
        )

    # Insert translations
    total_verses = 0
    for item in metadata:
        translation_file = translations_dir / f"{item['id']}.json"

        if not translation_file.exists():
            print(f"Warning: {translation_file.name} not found, skipping...")
            continue

        with open(translation_file, 'r', encoding='utf-8') as f:
            translation_data = json.load(f)

        # Insert each verse
        verses = []
        for key, text in translation_data.items():
            surah, ayah = key.split(':')
            verses.append((item['id'], int(surah), int(ayah), text))

        cursor.executemany(
            'INSERT INTO translations (translation_id, surah, ayah, text) VALUES (?, ?, ?, ?)',
            verses
        )

        total_verses += len(verses)
        print(f"  ✓ {item['id']}: {len(verses)} verses")

    # Commit and close
    conn.commit()
    conn.close()

    # Get file size
    size_mb = output_file.stat().st_size / (1024 * 1024)

    print(f"\n✅ Database created successfully!")
    print(f"   Location: {output_file}")
    print(f"   Size: {size_mb:.2f} MB")
    print(f"   Translations: {len(metadata)}")
    print(f"   Total verses: {total_verses}")


if __name__ == '__main__':
    create_database()
