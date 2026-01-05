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


import re

def parse_footnotes(footnotes_text):
    """Parse footnotes from string format like '[1] text [2] text' into a dictionary"""
    if not footnotes_text:
        return {}
    
    footnotes = {}
    # Helper to clean text
    def clean_text(t):
        return t.strip().strip('"').strip("'")
    
    # Split by the pattern [number]
    # This regex looks for [digits] followed by text until the next [digits] or end of string
    pattern = r'\[(\d+)\]\s*(.*?)(?=\s*\[\d+\]|$)'
    matches = re.finditer(pattern, footnotes_text, re.DOTALL)
    
    for match in matches:
        note_id = match.group(1)
        note_text = clean_text(match.group(2))
        if note_text:
            footnotes[note_id] = note_text
            
    return footnotes


def create_translation_xml(translation_id, csv_file_path, output_file):
    """Create XML file for a single translation from CSV"""

    # Create root element
    root = ET.Element('translation')
    root.set('id', translation_id)

    # Create sura container
    sura_container = ET.SubElement(root, 'sura')

    current_sura_id = None
    current_sura_elem = None
    verse_count = 0
    
    # Track footnotes to add at end of each sura
    sura_footnotes = {}

    # Read CSV and add verses
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sura_id = row['sura']
            aya_id = row['aya']
            text = row['text']
            footnotes_text = row.get('footnotes', '')
            
            # Start new sura if needed
            if sura_id != current_sura_id:
                # Process footnotes for previous sura
                if current_sura_elem is not None and sura_footnotes:
                    footnotes_elem = ET.SubElement(current_sura_elem, 'footnotes')
                    for note_id, note_text in sura_footnotes.items():
                        note_elem = ET.SubElement(footnotes_elem, 'note')
                        note_elem.set('id', str(note_id))
                        note_elem.text = note_text
                
                # Reset for new sura
                current_sura_id = sura_id
                current_sura_elem = ET.SubElement(sura_container, 'sura')
                current_sura_elem.set('id', sura_id)
                sura_footnotes = {}
            
            # Add verse
            verse = ET.SubElement(current_sura_elem, 'aya')
            verse.set('id', aya_id)
            verse.text = text
            
            # Parse and collect footnotes
            if footnotes_text:
                parsed_notes = parse_footnotes(footnotes_text)
                sura_footnotes.update(parsed_notes)
                
            verse_count += 1
            
        # Process footnotes for the last sura
        if current_sura_elem is not None and sura_footnotes:
            footnotes_elem = ET.SubElement(current_sura_elem, 'footnotes')
            for note_id, note_text in sura_footnotes.items():
                note_elem = ET.SubElement(footnotes_elem, 'note')
                note_elem.set('id', str(note_id))
                note_elem.text = note_text

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
