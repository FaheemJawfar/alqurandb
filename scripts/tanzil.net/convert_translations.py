#!/usr/bin/env python3
"""
Convert Tanzil translation XML files to JSON format
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import sys
import json
import re


# Load metadata at module level
_metadata = None


def get_id_mapping():
    """Load and cache the ID mapping from metadata"""
    global _metadata
    if _metadata is None:
        script_dir = Path(__file__).parent
        metadata_file = script_dir / 'metadata.json'
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata_list = json.load(f)
            # Create mapping: tanzilnet_id -> new_id
            _metadata = {}
            for entry in metadata_list:
                if 'tanzilnet_id' in entry:
                    _metadata[entry['tanzilnet_id']] = {
                        'new_id': entry['id'],
                        'language': entry['language'],
                        'translator': entry['translator']
                    }
    return _metadata


def extract_metadata_from_header(content):
    """Extract metadata from XML header comments"""
    metadata = {
        'id': '',
        'language': '',
        'name_in_language': '',
        'translator': '',
        'source': 'tanzil.net'
    }

    # Extract header comment section
    comment_start = content.find('<!--')
    comment_end = content.find('-->')

    if comment_start != -1 and comment_end != -1:
        header = content[comment_start:comment_end]

        # Extract ID
        id_match = re.search(r'#\s*ID:\s*(.+)', header)
        if id_match:
            metadata['id'] = id_match.group(1).strip()

        # Extract Language
        lang_match = re.search(r'#\s*Language:\s*(.+)', header)
        if lang_match:
            metadata['language'] = lang_match.group(1).strip()

        # Extract Name (in original language)
        name_match = re.search(r'#\s*Name:\s*(.+)', header)
        if name_match:
            metadata['name_in_language'] = name_match.group(1).strip()

        # Extract Translator
        trans_match = re.search(r'#\s*Translator:\s*(.+)', header)
        if trans_match:
            metadata['translator'] = trans_match.group(1).strip()

    return metadata


def xml_to_json(xml_file_path, output_file_path=None, quiet=False):
    """Convert XML translation to JSON format

    Args:
        xml_file_path: Path to the XML file
        output_file_path: Optional output JSON file path. If not provided,
                         will save to translations_json folder
        quiet: If True, suppress output messages

    Returns:
        Dictionary with "surah:ayah" keys and translation text values
    """

    # Read and clean XML file (skip header comments)
    try:
        with open(xml_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract metadata from header
        metadata = extract_metadata_from_header(content)

        # Find the start of the actual XML content (after comments)
        # Look for the <quran> tag
        quran_start = content.find('<quran')
        if quran_start == -1:
            if not quiet:
                print(f"❌ Error: No <quran> tag found in {xml_file_path.name}")
            return None

        # Extract XML declaration if present
        xml_decl = ''
        if content.startswith('<?xml'):
            xml_decl_end = content.find('?>') + 2
            xml_decl = content[:xml_decl_end] + '\n'

        # Combine XML declaration with the quran content
        clean_content = xml_decl + content[quran_start:]

        # Parse the cleaned XML
        root = ET.fromstring(clean_content)

    except Exception as e:
        if not quiet:
            print(f"❌ Error parsing {xml_file_path.name}: {e}")
        return None

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
        # Create translations_json folder in the same directory as script
        script_dir = Path(__file__).parent
        json_dir = script_dir / 'translations_json'
        json_dir.mkdir(exist_ok=True)

        # Extract old ID from XML filename (e.g., "ta.tamil" from "ta.tamil.xml")
        old_id = xml_file_path.stem

        # Get ID mapping and look up new ID
        id_mapping = get_id_mapping()
        if old_id in id_mapping:
            new_id = id_mapping[old_id]['new_id']
        else:
            # Fallback to old ID if not found in mapping
            new_id = old_id
            if not quiet:
                print(f"⚠️  Warning: No mapping found for {old_id}, using original ID")

        # Use new ID for output filename
        output_file_path = json_dir / f"{new_id}.json"

    # Save to JSON
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(translation, f, ensure_ascii=False, indent=2)

    if not quiet:
        print(f"\n✅ JSON file created successfully!")
        print(f"Input:  {xml_file_path}")
        print(f"Output: {output_file_path}")
        print(f"Total verses: {len(translation)}")

    return translation


def convert_all_translations():
    """Convert all XML translations to JSON format"""

    script_dir = Path(__file__).parent
    xml_dir = script_dir / 'translations_xml'

    if not xml_dir.exists():
        print(f"❌ Error: {xml_dir} directory not found")
        return

    # Find all XML files
    xml_files = sorted(xml_dir.glob('*.xml'))

    if not xml_files:
        print(f"❌ No XML files found in {xml_dir}")
        return

    print(f"\n🔄 Converting {len(xml_files)} translations to JSON...")
    print("=" * 80)

    successful = 0
    failed = 0
    failed_files = []

    for i, xml_file in enumerate(xml_files, 1):
        print(f"[{i}/{len(xml_files)}] Converting {xml_file.name}...", end=" ")

        result = xml_to_json(xml_file, quiet=True)

        if result:
            successful += 1
            print(f"✅ ({len(result)} verses)")
        else:
            failed += 1
            failed_files.append(xml_file.name)
            print("❌ Failed")

    # Summary
    print("\n" + "=" * 80)
    print("📊 Conversion Summary")
    print("=" * 80)
    print(f"Total files: {len(xml_files)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    if failed_files:
        print(f"\nFailed files:")
        for filename in failed_files[:10]:  # Show first 10
            print(f"  - {filename}")
        if len(failed_files) > 10:
            print(f"  ... and {len(failed_files) - 10} more")

    print(f"\nOutput directory: {script_dir / 'translations_json'}")
    print("=" * 80)


def main():
    """Main function"""

    script_dir = Path(__file__).parent
    default_file = script_dir / 'translations_xml' / 'ta.tamil.xml'

    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--json':
            # Convert to JSON
            xml_file = Path(sys.argv[2]) if len(sys.argv) > 2 else default_file
            output_file = Path(sys.argv[3]) if len(sys.argv) > 3 else None
            xml_to_json(xml_file, output_file)
            return
        elif sys.argv[1] == '--convert-all' or sys.argv[1] == '--all':
            # Convert all XML files to JSON
            convert_all_translations()
            return
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("Tanzil Translation Converter - Convert XML to JSON")
            print("\nUsage:")
            print("  python parse_translation.py --json [FILE] [OUT]   # Convert single file")
            print("  python parse_translation.py --all                 # Convert all XML files")
            print("\nExamples:")
            print("  python parse_translation.py --json                        # Convert default (Tamil)")
            print("  python parse_translation.py --json ta.tamil.xml           # Convert specific file")
            print("  python parse_translation.py --json input.xml output.json  # Custom output")
            print("  python parse_translation.py --all                         # Convert all files")
            return
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Use --help for usage information")
            return

    # Default: convert all translations
    convert_all_translations()


if __name__ == '__main__':
    main()
