#!/usr/bin/env python3
"""
Convert CSV translations to JSON format

Reads from: alqurandb_api/data/translations/csv/ (base format)
Outputs to: alqurandb_api/data/translations/json/

CSV is the source of truth - this converter generates JSON from CSV.
"""

import csv
import json
from pathlib import Path


def csv_to_json(csv_file_path, output_file_path):
    """Convert a CSV translation file to JSON format

    Args:
        csv_file_path: Path to the CSV file
        output_file_path: Path to the output JSON file

    Returns:
        Number of verses converted
    """
    translation = {}

    # Read CSV file
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = f"{row['surah']}:{row['ayah']}"
            translation[key] = row['text']

    # Write JSON file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(translation, f, ensure_ascii=False, indent=2)

    return len(translation)


def main():
    """Convert all CSV translations to JSON format"""

    # Paths (CSV is the base format)
    script_dir = Path(__file__).parent
    api_data_dir = script_dir.parent.parent / 'alqurandb_api' / 'data'
    csv_dir = api_data_dir / 'translations' / 'csv'
    json_dir = api_data_dir / 'translations' / 'json'

    # Create JSON directory
    json_dir.mkdir(parents=True, exist_ok=True)

    # Find all CSV files
    csv_files = sorted(csv_dir.glob('*.csv'))

    if not csv_files:
        print(f"❌ No CSV files found in {csv_dir}")
        return

    print(f"Converting {len(csv_files)} translations from CSV to JSON...")

    successful = 0
    failed = 0

    for csv_file in csv_files:
        json_file = json_dir / f"{csv_file.stem}.json"
        translation_id = csv_file.stem

        try:
            verse_count = csv_to_json(csv_file, json_file)

            # Get file size
            size_kb = json_file.stat().st_size / 1024

            print(f"  ✓ {translation_id}: {verse_count} verses ({size_kb:.1f} KB)")
            successful += 1
        except Exception as e:
            print(f"  ✗ {translation_id}: Error - {e}")
            failed += 1

    print(f"\n✅ Created {successful} JSON files")
    if failed > 0:
        print(f"❌ Failed: {failed}")


if __name__ == '__main__':
    main()
