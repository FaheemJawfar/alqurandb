#!/usr/bin/env python3
"""
Convert CSV translations to JSON format

Reads from: alqurandb_api/data/translations/csv/ (base format)
Outputs to: alqurandb_api/data/translations/json/

CSV is the source of truth - this converter generates JSON from CSV.
"""

import csv
import json
import re
from pathlib import Path


def parse_footnotes(footnotes_text):
    """
    Parse footnotes from text like "[1] Note 1\n[2] Note 2"
    Returns a dict mapping note number to note text
    """
    if not footnotes_text:
        return {}
    
    # Pattern to find each footnote starting with [n]
    # Uses positive lookahead to find the start of the next footnote or end of string
    pattern = r'\[(\d+)\]\s*(.*?)(?=\s*\[\d+\]|$)'
    matches = re.findall(pattern, footnotes_text, re.DOTALL)
    
    return {num: text.strip() for num, text in matches}


def csv_to_json(csv_file_path, output_file_path):
    """Convert a CSV translation file to JSON format

    Args:
        csv_file_path: Path to the CSV file
        output_file_path: Path to the output JSON file

    Returns:
        Number of verses converted
    """
    translation = {"sura": {}}

    # Read CSV file
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        verse_count = 0
        for row in reader:
            sura_id = row['sura']
            aya_id = row['aya']
            text = row['text']
            
            if sura_id not in translation["sura"]:
                translation["sura"][sura_id] = {"aya": {}}
            
            translation["sura"][sura_id]["aya"][aya_id] = text
            
            # Add footnotes if present in the CSV
            if 'footnotes' in row and row['footnotes']:
                if 'footnotes' not in translation["sura"][sura_id]:
                    translation["sura"][sura_id]["footnotes"] = {}
                
                notes = parse_footnotes(row['footnotes'])
                translation["sura"][sura_id]["footnotes"].update(notes)
            
            verse_count += 1

    # Write JSON file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(translation, f, ensure_ascii=False, indent=2)

    return verse_count


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
