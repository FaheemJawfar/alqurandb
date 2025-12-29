#!/usr/bin/env python3
"""
Create individual SQLite database files for each translation
"""
import json
import sqlite3
from pathlib import Path


def create_translation_database(translation_id, translation_data, output_file):
    """Create SQLite database for a single translation"""

    # Remove existing database
    if output_file.exists():
        output_file.unlink()

    # Create database
    conn = sqlite3.connect(output_file)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE verses (
            surah INTEGER NOT NULL,
            ayah INTEGER NOT NULL,
            text TEXT NOT NULL,
            PRIMARY KEY (surah, ayah)
        )
    ''')

    # Create index for better query performance
    cursor.execute('CREATE INDEX idx_surah ON verses(surah)')

    # Insert verses
    verses = []
    for key, text in translation_data.items():
        surah, ayah = key.split(':')
        verses.append((int(surah), int(ayah), text))

    cursor.executemany(
        'INSERT INTO verses (surah, ayah, text) VALUES (?, ?, ?)',
        verses
    )

    # Commit and close
    conn.commit()
    conn.close()

    return len(verses)


def main():
    """Create SQLite files for all translations"""

    # Paths
    script_dir = Path(__file__).parent
    api_data_dir = script_dir.parent / 'alqurandb_api' / 'data'
    metadata_file = api_data_dir / 'metadata.json'
    translations_json_dir = api_data_dir / 'translations' / 'json'
    output_dir = api_data_dir / 'translations' / 'sqlite'

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load metadata
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    print(f"Creating SQLite files for {len(metadata)} translations...")

    successful = 0
    failed = 0

    for item in metadata:
        translation_id = item['id']
        json_file = translations_json_dir / f"{translation_id}.json"
        output_file = output_dir / f"{translation_id}.db"

        if not json_file.exists():
            print(f"  ✗ {translation_id}: JSON file not found")
            failed += 1
            continue

        try:
            # Load translation data
            with open(json_file, 'r', encoding='utf-8') as f:
                translation_data = json.load(f)

            # Create SQLite database
            verse_count = create_translation_database(translation_id, translation_data, output_file)

            # Get file size
            size_kb = output_file.stat().st_size / 1024

            print(f"  ✓ {translation_id}: {verse_count} verses ({size_kb:.1f} KB)")
            successful += 1

        except Exception as e:
            print(f"  ✗ {translation_id}: Error - {e}")
            failed += 1

    print(f"\n✅ Created {successful} SQLite files")
    if failed > 0:
        print(f"❌ Failed: {failed}")


if __name__ == '__main__':
    main()
