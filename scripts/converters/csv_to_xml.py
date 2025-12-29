#!/usr/bin/env python3
"""
Convert CSV translations to XML format

Reads from: alqurandb_api/data/translations/csv/ (base format)
Outputs to: alqurandb_api/data/translations/xml/

CSV is the source of truth - this converter generates XML from CSV.
"""
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom


def create_translation_xml(translation_id, csv_file_path, output_file):
    """Create XML file for a single translation from CSV"""

    # Create root element
    root = ET.Element('translation')
    root.set('id', translation_id)

    # Create verses container
    verses = ET.SubElement(root, 'verses')

    verse_count = 0

    # Read CSV and add verses
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            verse = ET.SubElement(verses, 'verse')
            verse.set('surah', row['surah'])
            verse.set('ayah', row['ayah'])
            verse.text = row['text']
            verse_count += 1

    # Pretty print the XML
    xml_str = minidom.parseString(ET.tostring(root, encoding='utf-8')).toprettyxml(indent="  ")

    # Remove extra blank lines
    xml_lines = [line for line in xml_str.split('\n') if line.strip()]
    xml_str = '\n'.join(xml_lines)

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)

    return verse_count


def main():
    """Convert all CSV translations to XML format"""

    # Paths (CSV is the base format)
    script_dir = Path(__file__).parent
    api_data_dir = script_dir.parent.parent / 'alqurandb_api' / 'data'
    csv_dir = api_data_dir / 'translations' / 'csv'
    xml_dir = api_data_dir / 'translations' / 'xml'

    # Create output directory
    xml_dir.mkdir(parents=True, exist_ok=True)

    # Find all CSV files
    csv_files = sorted(csv_dir.glob('*.csv'))

    if not csv_files:
        print(f"❌ No CSV files found in {csv_dir}")
        return

    print(f"Converting {len(csv_files)} translations from CSV to XML...")

    successful = 0
    failed = 0

    for csv_file in csv_files:
        translation_id = csv_file.stem
        output_file = xml_dir / f"{translation_id}.xml"

        try:
            verse_count = create_translation_xml(translation_id, csv_file, output_file)

            # Get file size
            size_kb = output_file.stat().st_size / 1024

            print(f"  ✓ {translation_id}: {verse_count} verses ({size_kb:.1f} KB)")
            successful += 1

        except Exception as e:
            print(f"  ✗ {translation_id}: Error - {e}")
            failed += 1

    print(f"\n✅ Created {successful} XML files")
    if failed > 0:
        print(f"❌ Failed: {failed}")


if __name__ == '__main__':
    main()
