#!/usr/bin/env python3
"""
Convert CSV translations to individual SQLite database files

Reads from: alqurandb_api/data/translations/csv/ (base format)
Outputs to: alqurandb_api/data/translations/sqlite/

CSV is the source of truth - this converter generates SQLite databases from CSV.
"""
import csv
import sqlite3
from pathlib import Path


def create_translation_database(translation_id, csv_file_path, output_file):
    """Create SQLite database for a single translation from CSV"""

    # Remove existing database
    if output_file.exists():
        output_file.unlink()

    # Create database
    conn = sqlite3.connect(output_file)
    cursor = conn.cursor()

    # Read CSV fieldnames to check for footnotes
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        has_footnotes = 'footnotes' in reader.fieldnames
        verses_data = list(reader)

    # Create table
    if has_footnotes:
        cursor.execute('''
            CREATE TABLE verses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sura INTEGER NOT NULL,
                aya INTEGER NOT NULL,
                text TEXT NOT NULL,
                footnotes TEXT
            )
        ''')
    else:
        cursor.execute('''
            CREATE TABLE verses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sura INTEGER NOT NULL,
                aya INTEGER NOT NULL,
                text TEXT NOT NULL
            )
        ''')

    # Create indexes for better query performance
    cursor.execute('CREATE INDEX idx_sura ON verses(sura)')
    cursor.execute('CREATE INDEX idx_sura_aya ON verses(sura, aya)')

    # Insert verses from CSV
    verses = []
    for row in verses_data:
        if has_footnotes:
            verses.append((int(row['sura']), int(row['aya']), row['text'], row.get('footnotes', '')))
        else:
            verses.append((int(row['sura']), int(row['aya']), row['text']))

    if has_footnotes:
        cursor.executemany(
            'INSERT INTO verses (sura, aya, text, footnotes) VALUES (?, ?, ?, ?)',
            verses
        )
    else:
        cursor.executemany(
            'INSERT INTO verses (sura, aya, text) VALUES (?, ?, ?)',
            verses
        )

    # Commit and close
    conn.commit()
    conn.close()

    return len(verses)


def main():
    """Convert all CSV translations to SQLite format"""

    # Paths (CSV is the base format)
    script_dir = Path(__file__).parent
    api_data_dir = script_dir.parent.parent / 'alqurandb_api' / 'data'
    csv_dir = api_data_dir / 'translations' / 'csv'
    sqlite_dir = api_data_dir / 'translations' / 'sqlite'

    # Create output directory
    sqlite_dir.mkdir(parents=True, exist_ok=True)

    # Find all CSV files
    csv_files = sorted(csv_dir.glob('*.csv'))

    if not csv_files:
        print(f"❌ No CSV files found in {csv_dir}")
        return

    print(f"Converting {len(csv_files)} translations from CSV to SQLite...")

    successful = 0
    failed = 0

    for csv_file in csv_files:
        translation_id = csv_file.stem
        output_file = sqlite_dir / f"{translation_id}.db"

        try:
            verse_count = create_translation_database(translation_id, csv_file, output_file)

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
