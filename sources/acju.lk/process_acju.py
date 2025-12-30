#!/usr/bin/env python3
"""
Process ACJU translations - Full automated pipeline

This script:
1. Extracts CSV from XML source files
2. Generates all formats (JSON, XML, Excel, SQLite) from CSV
3. Moves generated files to API data folder

Source files: source/*.xml
Output: ../../alqurandb_api/data/translations/
"""
import xml.etree.ElementTree as ET
import csv
import json
import sys
from pathlib import Path
import shutil

# Import converters
sys.path.insert(0, str(Path(__file__).parent.parent))
from converters.csv_to_json import csv_to_json
from converters.csv_to_xml import create_translation_xml
from converters.csv_to_excel import create_translation_excel
from converters.csv_to_sqlite import create_translation_database


def load_metadata():
    """Load metadata for acju translations"""
    project_root = Path(__file__).parent.parent.parent
    metadata_file = project_root / 'alqurandb_api' / 'data' / 'metadata.json'

    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata_list = json.load(f)

    # Create mapping: translation_id -> full metadata
    metadata_mapping = {}
    for entry in metadata_list:
        if entry.get('source') == 'acju.lk':
            metadata_mapping[entry['id']] = entry

    return metadata_mapping


def xml_to_csv(xml_file: Path, csv_file: Path) -> int:
    """
    Convert ACJU XML translation to CSV format

    Args:
        xml_file: Path to source XML file
        csv_file: Path to output CSV file

    Returns:
        Number of verses converted
    """
    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Write CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['sura', 'aya', 'text'])

        verse_count = 0
        for sura in root.findall('sura'):
            sura_num = int(sura.get('index'))
            for aya in sura.findall('aya'):
                aya_num = int(aya.get('index'))
                text = aya.get('text', '').strip()
                writer.writerow([sura_num, aya_num, text])
                verse_count += 1

    return verse_count


def extract_all_csv():
    """Extract CSV from all XML source files"""
    script_dir = Path(__file__).parent
    source_dir = script_dir / 'source'
    csv_dir = script_dir / 'csv_output'

    # Create CSV output directory
    csv_dir.mkdir(exist_ok=True)

    # Define translation mappings (source file → output CSV)
    conversions = {
        'acju.xml': 'sinhala_acju.csv',
    }

    print(f"\n🔄 Extracting CSV from {len(conversions)} XML files...")
    print("=" * 80)

    successful = 0
    failed = 0

    for i, (xml_name, csv_name) in enumerate(conversions.items(), 1):
        xml_file = source_dir / xml_name
        csv_file = csv_dir / csv_name

        if not xml_file.exists():
            print(f"[{i}/{len(conversions)}] ⚠️  Skipping {xml_name} - file not found")
            continue

        try:
            print(f"[{i}/{len(conversions)}] {xml_name} → {csv_name}...", end=" ")
            verse_count = xml_to_csv(xml_file, csv_file)
            successful += 1
            print(f"✅ ({verse_count} verses)")
        except Exception as e:
            failed += 1
            print(f"❌ Failed: {e}")

    print("\n" + "=" * 80)
    print(f"CSV Extraction: {successful} successful, {failed} failed")
    print(f"Output: {csv_dir}")
    print("=" * 80)

    return successful


def generate_all_formats():
    """Generate all formats (JSON, XML, Excel, SQLite) from CSV files"""
    script_dir = Path(__file__).parent
    csv_source_dir = script_dir / 'csv_output'

    # Define output directories
    output_dirs = {
        'json': script_dir / 'json_output',
        'xml': script_dir / 'xml_output',
        'xlsx': script_dir / 'xlsx_output',
        'sqlite': script_dir / 'sqlite_output',
    }

    # Create output directories
    for output_dir in output_dirs.values():
        output_dir.mkdir(exist_ok=True)

    # Get list of CSV files to convert
    csv_files = sorted(csv_source_dir.glob('*.csv'))

    if not csv_files:
        print(f"\n❌ No CSV files found in {csv_source_dir}")
        return False

    # Load metadata for Excel generation
    metadata_mapping = load_metadata()

    print(f"\n🔄 Generating all formats for {len(csv_files)} translations...")
    print("=" * 80)

    results = {
        'JSON': 0,
        'XML': 0,
        'Excel': 0,
        'SQLite': 0
    }

    for csv_file in csv_files:
        translation_id = csv_file.stem
        print(f"\n→ Processing {translation_id}...")

        # Get metadata for this translation
        metadata_item = metadata_mapping.get(translation_id, {})

        # Generate JSON
        try:
            json_file = output_dirs['json'] / f"{translation_id}.json"
            csv_to_json(csv_file, json_file)
            results['JSON'] += 1
            print(f"  ✅ JSON")
        except Exception as e:
            print(f"  ❌ JSON failed: {e}")

        # Generate XML
        try:
            xml_file = output_dirs['xml'] / f"{translation_id}.xml"
            create_translation_xml(translation_id, csv_file, xml_file)
            results['XML'] += 1
            print(f"  ✅ XML")
        except Exception as e:
            print(f"  ❌ XML failed: {e}")

        # Generate Excel
        try:
            xlsx_file = output_dirs['xlsx'] / f"{translation_id}.xlsx"
            create_translation_excel(translation_id, csv_file, metadata_item, xlsx_file)
            results['Excel'] += 1
            print(f"  ✅ Excel")
        except Exception as e:
            print(f"  ❌ Excel failed: {e}")

        # Generate SQLite
        try:
            sqlite_file = output_dirs['sqlite'] / f"{translation_id}.sqlite"
            create_translation_database(translation_id, csv_file, sqlite_file)
            results['SQLite'] += 1
            print(f"  ✅ SQLite")
        except Exception as e:
            print(f"  ❌ SQLite failed: {e}")

    print("\n" + "=" * 80)
    print("Format Generation Summary:")
    total_files = len(csv_files)
    for format_name, success_count in results.items():
        status = "✅" if success_count == total_files else "⚠️"
        print(f"  {status} {format_name}: {success_count}/{total_files} files")
    print("=" * 80)

    return all(count == total_files for count in results.values())


def move_to_api_data():
    """Move all generated files to API data folder"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    api_data_dir = project_root / 'alqurandb_api' / 'data' / 'translations'

    # Define source and destination mappings
    moves = [
        (script_dir / 'csv_output', api_data_dir / 'csv'),
        (script_dir / 'json_output', api_data_dir / 'json'),
        (script_dir / 'xml_output', api_data_dir / 'xml'),
        (script_dir / 'xlsx_output', api_data_dir / 'xlsx'),
        (script_dir / 'sqlite_output', api_data_dir / 'sqlite'),
    ]

    print(f"\n🔄 Moving files to API data folder...")
    print("=" * 80)

    total_moved = 0

    for source_dir, dest_dir in moves:
        if not source_dir.exists():
            continue

        # Ensure destination exists
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Move all files
        files = list(source_dir.glob('*.*'))
        for file in files:
            dest_file = dest_dir / file.name
            shutil.copy2(file, dest_file)
            total_moved += 1

        if files:
            print(f"  ✅ {source_dir.name}: {len(files)} files → {dest_dir}")

    print("=" * 80)
    print(f"Total files moved: {total_moved}")
    print(f"Destination: {api_data_dir}")
    print("=" * 80)

    return total_moved > 0


def main():
    """Main processing pipeline"""
    print("\n" + "="*80)
    print("  ACJU Translation Processing Pipeline")
    print("="*80)
    print("\nSteps:")
    print("  1. Extract CSV from XML source files")
    print("  2. Generate JSON, XML, Excel, SQLite from CSV")
    print("  3. Move all files to API data folder")
    print("="*80)

    # Step 1: Extract CSV
    csv_count = extract_all_csv()
    if csv_count == 0:
        print("\n❌ No CSV files extracted. Aborting.")
        sys.exit(1)

    # Step 2: Generate all formats
    if not generate_all_formats():
        print("\n⚠️  Some formats failed to generate")

    # Step 3: Move to API data
    if not move_to_api_data():
        print("\n❌ Failed to move files to API data folder")
        sys.exit(1)

    print("\n" + "="*80)
    print("  ✅ Pipeline completed successfully!")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
