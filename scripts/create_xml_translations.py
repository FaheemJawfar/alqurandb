#!/usr/bin/env python3
"""
Create individual XML files for each translation
"""
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom


def create_translation_xml(translation_id, translation_data, output_file):
    """Create XML file for a single translation"""

    # Create root element
    root = ET.Element('translation')
    root.set('id', translation_id)

    # Create verses container
    verses = ET.SubElement(root, 'verses')

    # Add each verse
    for key, text in translation_data.items():
        surah, ayah = key.split(':')
        verse = ET.SubElement(verses, 'verse')
        verse.set('surah', surah)
        verse.set('ayah', ayah)
        verse.text = text

    # Pretty print the XML
    xml_str = minidom.parseString(ET.tostring(root, encoding='utf-8')).toprettyxml(indent="  ")

    # Remove extra blank lines
    xml_lines = [line for line in xml_str.split('\n') if line.strip()]
    xml_str = '\n'.join(xml_lines)

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)

    return len(translation_data)


def main():
    """Create XML files for all translations"""

    # Paths
    script_dir = Path(__file__).parent
    api_data_dir = script_dir.parent / 'alqurandb_api' / 'data'
    metadata_file = api_data_dir / 'metadata.json'
    translations_json_dir = api_data_dir / 'translations' / 'json'
    output_dir = api_data_dir / 'translations' / 'xml'

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load metadata
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    print(f"Creating XML files for {len(metadata)} translations...")

    successful = 0
    failed = 0

    for item in metadata:
        translation_id = item['id']
        json_file = translations_json_dir / f"{translation_id}.json"
        output_file = output_dir / f"{translation_id}.xml"

        if not json_file.exists():
            print(f"  ✗ {translation_id}: JSON file not found")
            failed += 1
            continue

        try:
            # Load translation data
            with open(json_file, 'r', encoding='utf-8') as f:
                translation_data = json.load(f)

            # Create XML file
            verse_count = create_translation_xml(translation_id, translation_data, output_file)

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
