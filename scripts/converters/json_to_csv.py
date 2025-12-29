#!/usr/bin/env python3
"""
Convert JSON translations to CSV format

Reads from: alqurandb_api/data/translations/json/ (base format)
Outputs to: alqurandb_api/data/translations/csv/

JSON is the source of truth - this converter generates CSV files from JSON.
"""

import json
import csv
from pathlib import Path


def json_to_csv(json_file_path, output_file_path):
    """Convert a JSON translation file to CSV format

    Args:
        json_file_path: Path to the JSON file
        output_file_path: Path to the output CSV file

    Returns:
        Number of verses converted
    """
    # Load JSON data
    with open(json_file_path, 'r', encoding='utf-8') as f:
        translation = json.load(f)

    # Open CSV file for writing
    with open(output_file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)

        # Write header
        writer.writerow(['surah', 'ayah', 'text'])

        # Write data
        for key, text in translation.items():
            surah, ayah = key.split(':')
            writer.writerow([surah, ayah, text])

    return len(translation)


def main():
    """Convert all JSON translations to CSV format"""

    # Paths (JSON is the base format)
    script_dir = Path(__file__).parent
    api_data_dir = script_dir.parent.parent / 'alqurandb_api' / 'data'
    json_dir = api_data_dir / 'translations' / 'json'
    csv_dir = api_data_dir / 'translations' / 'csv'

    # Create CSV directory
    csv_dir.mkdir(parents=True, exist_ok=True)

    # Find all JSON files
    json_files = sorted(json_dir.glob('*.json'))

    if not json_files:
        print(f"❌ No JSON files found in {json_dir}")
        return

    print(f"Converting {len(json_files)} translations from JSON to CSV...")

    successful = 0
    failed = 0

    for json_file in json_files:
        csv_file = csv_dir / f"{json_file.stem}.csv"
        translation_id = json_file.stem

        try:
            verse_count = json_to_csv(json_file, csv_file)

            # Get file size
            size_kb = csv_file.stat().st_size / 1024

            print(f"  ✓ {translation_id}: {verse_count} verses ({size_kb:.1f} KB)")
            successful += 1
        except Exception as e:
            print(f"  ✗ {translation_id}: Error - {e}")
            failed += 1

    print(f"\n✅ Created {successful} CSV files")
    if failed > 0:
        print(f"❌ Failed: {failed}")


if __name__ == '__main__':
    main()
