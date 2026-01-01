#!/usr/bin/env python3
"""
Convert CSV translations to individual SQL dump files (.sql)

Reads from: alqurandb_api/data/translations/csv/ (base format)
Outputs to: alqurandb_api/data/translations/sql/

CSV is the source of truth - this converter generates SQL dumps from CSV.
"""
import csv
from pathlib import Path

def create_sql_dump(translation_id, csv_file_path, output_file):
    """Create SQL dump for a single translation from CSV
    
    Generates SQL that is compatible with:
    - MySQL: Uses AUTO_INCREMENT
    - PostgreSQL: Uses SERIAL
    - SQLite: Uses AUTOINCREMENT
    
    The dump includes conditional statements for each database type.
    """

    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        verses = list(reader)

    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write(f"-- AlQuranDB SQL Dump\n")
        f.write(f"-- Translation: {translation_id}\n")
        f.write(f"-- Total Verses: {len(verses)}\n")
        f.write(f"-- Compatible with: MySQL, PostgreSQL, SQLite\n\n")

        # Drop table
        f.write("DROP TABLE IF EXISTS verses;\n\n")

        # Create table with database-specific syntax
        f.write("-- For MySQL (default):\n")
        f.write("CREATE TABLE verses (\n")
        f.write("    id INT AUTO_INCREMENT PRIMARY KEY,\n")
        f.write("    sura INT NOT NULL,\n")
        f.write("    aya INT NOT NULL,\n")
        f.write("    text TEXT NOT NULL,\n")
        f.write("    footnotes TEXT\n")
        f.write(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n\n")

        f.write("-- For PostgreSQL:\n")
        f.write("-- CREATE TABLE verses (\n")
        f.write("--     id SERIAL PRIMARY KEY,\n")
        f.write("--     sura INT NOT NULL,\n")
        f.write("--     aya INT NOT NULL,\n")
        f.write("--     text TEXT NOT NULL,\n")
        f.write("--     footnotes TEXT\n")
        f.write("-- );\n\n")

        f.write("-- For SQLite:\n")
        f.write("-- CREATE TABLE verses (\n")
        f.write("--     id INTEGER PRIMARY KEY AUTOINCREMENT,\n")
        f.write("--     sura INTEGER NOT NULL,\n")
        f.write("--     aya INTEGER NOT NULL,\n")
        f.write("--     text TEXT NOT NULL,\n")
        f.write("--     footnotes TEXT\n")
        f.write("-- );\n\n")

        # Create indexes (compatible with all databases)
        f.write("CREATE INDEX IF NOT EXISTS idx_sura ON verses(sura);\n")
        f.write("CREATE INDEX IF NOT EXISTS idx_sura_aya ON verses(sura, aya);\n\n")

        # Insert statements (Standard SQL - compatible with all)
        f.write("-- Insert statements\n")
        f.write("BEGIN;\n")
        for row in verses:
            text = row['text'].replace("'", "''") # Escape single quotes
            footnotes = row.get('footnotes', '').replace("'", "''")
            f.write(f"INSERT INTO verses (sura, aya, text, footnotes) VALUES ({row['sura']}, {row['aya']}, '{text}', '{footnotes}');\n")
        f.write("COMMIT;\n")

    return len(verses)

def main():
    """Convert all CSV translations to SQL format"""

    # Paths (CSV is the base format)
    script_dir = Path(__file__).parent
    api_data_dir = script_dir.parent.parent / 'alqurandb_api' / 'data'
    csv_dir = api_data_dir / 'translations' / 'csv'
    sql_dir = api_data_dir / 'translations' / 'sql'

    # Create output directory
    sql_dir.mkdir(parents=True, exist_ok=True)

    # Find all CSV files
    csv_files = sorted(csv_dir.glob('*.csv'))

    if not csv_files:
        print(f"❌ No CSV files found in {csv_dir}")
        return

    print(f"Converting {len(csv_files)} translations from CSV to SQL...")

    successful = 0
    failed = 0

    for csv_file in csv_files:
        translation_id = csv_file.stem
        output_file = sql_dir / f"{translation_id}.sql"

        try:
            verse_count = create_sql_dump(translation_id, csv_file, output_file)
            successful += 1
        except Exception as e:
            print(f"  ✗ {translation_id}: Error - {e}")
            failed += 1

    print(f"\n✅ Created {successful} SQL files")
    if failed > 0:
        print(f"❌ Failed: {failed}")

if __name__ == '__main__':
    main()
