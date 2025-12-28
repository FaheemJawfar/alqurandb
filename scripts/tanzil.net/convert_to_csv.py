#!/usr/bin/env python3
"""
Convert JSON translations to CSV format
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


def convert_all_to_csv():
    """Convert all JSON translations to CSV format"""

    script_dir = Path(__file__).parent
    json_dir = script_dir / 'translations_json'
    csv_dir = script_dir / 'translations_csv'

    # Create CSV directory
    csv_dir.mkdir(exist_ok=True)

    # Find all JSON files
    json_files = sorted(json_dir.glob('*.json'))

    if not json_files:
        print(f"❌ No JSON files found in {json_dir}")
        return

    print(f"\n🔄 Converting {len(json_files)} translations to CSV...")
    print("=" * 80)

    successful = 0
    failed = 0

    for i, json_file in enumerate(json_files, 1):
        csv_file = csv_dir / f"{json_file.stem}.csv"

        try:
            print(f"[{i}/{len(json_files)}] Converting {json_file.name}...", end=" ")
            verse_count = json_to_csv(json_file, csv_file)
            successful += 1
            print(f"✅ ({verse_count} verses)")
        except Exception as e:
            failed += 1
            print(f"❌ Failed: {e}")

    # Summary
    print("\n" + "=" * 80)
    print("📊 Conversion Summary")
    print("=" * 80)
    print(f"Total files: {len(json_files)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"\nOutput directory: {csv_dir}")
    print("=" * 80)


if __name__ == '__main__':
    convert_all_to_csv()
