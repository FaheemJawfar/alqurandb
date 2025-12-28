#!/usr/bin/env python3
"""
Parse Tanzil translation XML file and display verses
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import sys
import json


def parse_translation(xml_file_path, surah=None, ayah=None, limit=10):
    """Parse translation XML and print verses

    Args:
        xml_file_path: Path to the XML file
        surah: Optional surah number to display (1-114)
        ayah: Optional ayah number to display (requires surah)
        limit: Maximum number of verses to display (default 10)
    """

    # Parse XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    print(f"\nParsing: {xml_file_path.name}")
    print("=" * 80)

    verse_count = 0

    # Iterate through surahs
    for sura in root.findall('sura'):
        sura_index = int(sura.get('index'))
        sura_name = sura.get('name', '')

        # Filter by surah if specified
        if surah is not None and sura_index != surah:
            continue

        # Print surah header
        print(f"\n📖 Surah {sura_index}{': ' + sura_name if sura_name else ''}")
        print("-" * 80)

        # Iterate through ayahs
        for aya in sura.findall('aya'):
            aya_index = int(aya.get('index'))
            aya_text = aya.get('text', '')

            # Filter by ayah if specified
            if ayah is not None and aya_index != ayah:
                continue

            # Print ayah
            print(f"[{sura_index}:{aya_index}] {aya_text}")
            verse_count += 1

            # Check limit
            if limit and verse_count >= limit:
                print(f"\n... (showing first {limit} verses)")
                return

            # If specific ayah requested, return after showing it
            if ayah is not None:
                return

        # If specific surah requested without ayah, show all ayahs of that surah
        if surah is not None:
            return

    print(f"\n{'=' * 80}")
    print(f"Total verses displayed: {verse_count}")


def get_stats(xml_file_path):
    """Get statistics about the translation file"""

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    total_surahs = len(root.findall('sura'))
    total_ayahs = sum(len(sura.findall('aya')) for sura in root.findall('sura'))

    print(f"\n📊 Translation Statistics")
    print("=" * 80)
    print(f"File: {xml_file_path.name}")
    print(f"Total Surahs: {total_surahs}")
    print(f"Total Ayahs: {total_ayahs}")
    print("=" * 80)


def xml_to_json(xml_file_path, output_file_path=None):
    """Convert XML translation to JSON format

    Args:
        xml_file_path: Path to the XML file
        output_file_path: Optional output JSON file path. If not provided,
                         will use the same name as XML with .json extension

    Returns:
        Dictionary with "surah:ayah" keys and translation text values
    """

    # Parse XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Build translation dictionary
    translation = {}

    # Iterate through surahs
    for sura in root.findall('sura'):
        sura_index = sura.get('index')

        # Iterate through ayahs
        for aya in sura.findall('aya'):
            aya_index = aya.get('index')
            aya_text = aya.get('text', '')

            # Create key in format "surah:ayah"
            key = f"{sura_index}:{aya_index}"
            translation[key] = aya_text

    # Determine output file path
    if output_file_path is None:
        output_file_path = xml_file_path.with_suffix('.json')

    # Save to JSON
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(translation, f, ensure_ascii=False, indent=2)

    print(f"\n✅ JSON file created successfully!")
    print(f"Input:  {xml_file_path}")
    print(f"Output: {output_file_path}")
    print(f"Total verses: {len(translation)}")

    return translation


def main():
    """Main function"""

    # Default to Tamil translation
    script_dir = Path(__file__).parent
    default_file = script_dir / 'translations_xml' / 'ta.tamil.xml'

    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--stats':
            # Show statistics
            xml_file = Path(sys.argv[2]) if len(sys.argv) > 2 else default_file
            get_stats(xml_file)
            return
        elif sys.argv[1] == '--json':
            # Convert to JSON
            xml_file = Path(sys.argv[2]) if len(sys.argv) > 2 else default_file
            output_file = Path(sys.argv[3]) if len(sys.argv) > 3 else None
            xml_to_json(xml_file, output_file)
            return
        elif sys.argv[1] == '--help':
            print("Usage:")
            print("  python parse_translation.py                       # Show first 10 verses")
            print("  python parse_translation.py --stats [FILE]        # Show statistics")
            print("  python parse_translation.py --json [FILE] [OUT]   # Convert to JSON")
            print("  python parse_translation.py SURAH [AYAH]          # Show specific verse(s)")
            print("  python parse_translation.py --all [FILE]          # Show all verses")
            print("\nExamples:")
            print("  python parse_translation.py                       # First 10 verses")
            print("  python parse_translation.py 1                     # All verses of Surah 1")
            print("  python parse_translation.py 2 255                 # Ayat al-Kursi")
            print("  python parse_translation.py --stats               # Statistics")
            print("  python parse_translation.py --json                # Convert to JSON")
            print("  python parse_translation.py --json ta.tamil.xml   # Convert specific file")
            return
        elif sys.argv[1] == '--all':
            # Show all verses
            xml_file = Path(sys.argv[2]) if len(sys.argv) > 2 else default_file
            parse_translation(xml_file, limit=None)
            return
        else:
            # Show specific surah/ayah
            try:
                surah = int(sys.argv[1])
                ayah = int(sys.argv[2]) if len(sys.argv) > 2 else None
                parse_translation(default_file, surah=surah, ayah=ayah, limit=None)
                return
            except ValueError:
                print("Error: Invalid surah/ayah number")
                return

    # Default: show first 10 verses
    parse_translation(default_file, limit=10)


if __name__ == '__main__':
    main()
