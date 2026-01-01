#!/usr/bin/env python3
"""
Process QuranEnc translations - Full automated pipeline

This script:
1. Loads existing translations to avoid duplicates
2. Downloads CSV files directly from QuranEnc.com
3. Generates all formats (JSON, XML, Excel, SQLite) from CSV
4. Moves generated files to API data folder
"""
import json
import csv
import sys
import urllib.request
import re
from pathlib import Path

# Import converters
sys.path.insert(0, str(Path(__file__).parent.parent))
from converters.csv_to_json import csv_to_json
from converters.csv_to_xml import create_translation_xml
from converters.csv_to_excel import create_translation_excel
from converters.csv_to_sqlite import create_translation_database


def load_existing_translations():
    """Load existing translations with full metadata for duplicate detection"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    metadata_file = project_root / 'alqurandb_api' / 'data' / 'metadata.json'

    existing_translations = []
    if metadata_file.exists():
        with open(metadata_file, 'r', encoding='utf-8') as f:
            existing_translations = json.load(f)

    return existing_translations


def load_quranenc_metadata():
    """Load QuranEnc translation metadata"""
    script_dir = Path(__file__).parent
    metadata_file = script_dir / 'quranenc_metadata.json'

    with open(metadata_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['translations']


def strip_verse_number(text: str) -> str:
    """
    Strip verse numbers from the beginning of translation text

    Handles multiple numbering patterns:
    - Western/Arabic numerals: 1, 2, 3, etc.
    - Gujarati numerals: ૧, ૨, ૩, etc.
    - With or without period: "1. " or "1 "
    - Always followed by space

    Examples:
        "1. Text here" -> "Text here"
        "1 Text here" -> "Text here"
        "૧. Text here" -> "Text here"
    """
    # Pattern matches: digit(s) + optional period + space at the start
    # Supports Western (0-9) and Gujarati (૦-૯) numerals
    pattern = r'^(\d+|[૦-૯]+)\.?\s+'
    cleaned = re.sub(pattern, '', text)
    return cleaned


def download_csv_from_quranenc(translation_id: str, source_file: Path, csv_file: Path) -> bool:
    """
    Download CSV from QuranEnc to source folder and normalize to csv_output

    Args:
        translation_id: Translation identifier (e.g., 'uzbek_mansour')
        source_file: Path to save raw downloaded CSV
        csv_file: Path to save normalized CSV file

    Returns:
        True if download successful, False otherwise
    """
    url = f"https://quranenc.com/en/home/download/csv/{translation_id}"

    try:
        print(f"    Downloading CSV from {url}...", flush=True)

        # Download the raw file to source directory
        with urllib.request.urlopen(url) as response:
            content = response.read()
            with open(source_file, 'wb') as f:
                f.write(content)

        print(f"    ✅ Downloaded to source folder", flush=True)

        # Normalize the CSV format
        print(f"    Normalizing CSV format...", flush=True)

        # Read the QuranEnc CSV (skip metadata header, normalize columns)
        normalized_rows = []
        with open(source_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            # Find the actual CSV header (should be around line 12)
            csv_start_idx = None
            for idx, line in enumerate(lines):
                if line.startswith('id,sura,aya,translation'):
                    csv_start_idx = idx
                    break

            if csv_start_idx is None:
                print(f"    ❌ Could not find CSV header", flush=True)
                return False

            # Parse CSV data
            csv_reader = csv.DictReader(lines[csv_start_idx:])
            for row in csv_reader:
                # Normalize column names: translation -> text (keep sura and aya as-is)
                # Keep footnotes if present
                normalized_row = {
                    'sura': row['sura'],
                    'aya': row['aya'],
                    'text': row['translation'],
                    'footnotes': row.get('footnotes', '')
                }
                normalized_rows.append(normalized_row)

        # Write normalized CSV
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['sura', 'aya', 'text', 'footnotes'])
            writer.writeheader()
            writer.writerows(normalized_rows)

        # Verify the normalized file
        if csv_file.exists() and len(normalized_rows) > 6000:  # Should have ~6236 verses
            print(f"    ✅ Downloaded and normalized ({len(normalized_rows)} verses)", flush=True)
            return True
        else:
            print(f"    ⚠️  File seems incomplete ({len(normalized_rows)} verses)", flush=True)
            return False

    except Exception as e:
        print(f"    ❌ Download failed: {e}", flush=True)
        return False


def extract_all_csv():
    """
    Download ALL source CSV files from QuranEnc, then process non-duplicates

    Workflow:
    1. Download ALL valid source files to source/ folder
    2. Check for duplicates from other sources
    3. Process only non-duplicates to csv_output/ folder
    """
    script_dir = Path(__file__).parent
    source_dir = script_dir / 'source'
    csv_dir = script_dir / 'csv_output'

    # Create directories
    source_dir.mkdir(exist_ok=True)
    csv_dir.mkdir(exist_ok=True)

    # Load QuranEnc metadata
    quranenc_translations = load_quranenc_metadata()
    print(f"\n📋 Found {len(quranenc_translations)} QuranEnc translations in metadata", flush=True)

    # Filter out invalid entries
    valid_translations = []
    for trans in quranenc_translations:
        if trans.get('title') == False or trans.get('description') == False:
            print(f"  ⚠️  Skipping {trans['key']} - invalid metadata", flush=True)
        else:
            valid_translations.append(trans)

    print(f"📋 {len(valid_translations)} valid translations to download", flush=True)
    print("=" * 80, flush=True)

    # STEP 1: Download ALL source files
    print(f"\n🔽 STEP 1: Downloading ALL source CSV files...", flush=True)
    print("=" * 80, flush=True)

    downloaded = 0
    skipped = 0
    failed = 0

    for i, trans in enumerate(valid_translations, 1):
        trans_id = trans['key']
        source_file = source_dir / f"{trans_id}.csv"

        print(f"\n[{i}/{len(valid_translations)}] {trans_id}...", flush=True)

        # Check if source file already exists
        if source_file.exists():
            try:
                with open(source_file, 'r', encoding='utf-8') as f:
                    line_count = sum(1 for _ in f)
                    if line_count > 100:  # Has content
                        print(f"  ✓ Source file already exists ({line_count} lines)", flush=True)
                        skipped += 1
                        continue
            except:
                pass

        # Download source file
        url = f"https://quranenc.com/en/home/download/csv/{trans_id}"
        try:
            print(f"  Downloading from {url}...", flush=True)
            with urllib.request.urlopen(url, timeout=30) as response:
                content = response.read()
                with open(source_file, 'wb') as f:
                    f.write(content)

            # Verify download
            with open(source_file, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)

            print(f"  ✅ Downloaded ({line_count} lines)", flush=True)
            downloaded += 1

        except Exception as e:
            print(f"  ❌ Download failed: {e}", flush=True)
            failed += 1

    print("\n" + "=" * 80, flush=True)
    print(f"Source files: {downloaded} downloaded, {skipped} already exist, {failed} failed", flush=True)
    print(f"Total source files: {len(list(source_dir.glob('*.csv')))}", flush=True)

    # STEP 2: Check for duplicates and determine which to process
    print(f"\n🔍 STEP 2: Checking for duplicates from other sources...", flush=True)
    print("=" * 80, flush=True)

    existing_translations = load_existing_translations()
    print(f"📋 Found {len(existing_translations)} existing translations in main metadata", flush=True)

    translations_to_process = []
    duplicates_skipped = []

    for trans in valid_translations:
        trans_id = trans['key']
        source_file = source_dir / f"{trans_id}.csv"

        # Only process if source file exists
        if not source_file.exists():
            continue

        # Parse QuranEnc metadata
        quranenc_meta = parse_quranenc_metadata(trans)

        # Check for duplicate by language and translator
        duplicate = find_duplicate_translation(quranenc_meta, existing_translations)

        if duplicate:
            print(f"  ⏭️  {trans_id} - duplicate of {duplicate['id']} ({duplicate['source']})", flush=True)
            duplicates_skipped.append(trans_id)
        else:
            print(f"  ✅ {trans_id} - will process", flush=True)
            translations_to_process.append(trans)

    print(f"\n📊 {len(translations_to_process)} to process, {len(duplicates_skipped)} duplicates skipped", flush=True)

    # STEP 3: Process non-duplicates (normalize from source/ to csv_output/)
    print(f"\n⚙️  STEP 3: Processing non-duplicate translations...", flush=True)
    print("=" * 80, flush=True)

    successful = 0
    failed = 0

    for i, trans in enumerate(translations_to_process, 1):
        trans_id = trans['key']
        source_file = source_dir / f"{trans_id}.csv"
        csv_file = csv_dir / f"{trans_id}.csv"

        print(f"\n[{i}/{len(translations_to_process)}] {trans_id}...", flush=True)

        # Check if normalized CSV already exists
        if csv_file.exists():
            try:
                with open(csv_file, 'r', encoding='utf-8') as f:
                    line_count = sum(1 for _ in f)
                    if line_count > 6000:  # Should have ~6236 verses + header
                        print(f"  ✓ Already processed ({line_count} lines)", flush=True)
                        successful += 1
                        continue
            except:
                pass

        # Normalize from source to csv_output
        try:
            normalized_rows = []
            with open(source_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

                # Find CSV header
                csv_start_idx = None
                for idx, line in enumerate(lines):
                    if line.startswith('id,sura,aya,translation'):
                        csv_start_idx = idx
                        break

                if csv_start_idx is None:
                    print(f"  ❌ No CSV header found in source file", flush=True)
                    failed += 1
                    continue

                # Parse and normalize: translation -> text, strip verse numbers
                # Keep footnotes if present
                csv_reader = csv.DictReader(lines[csv_start_idx:])
                for row in csv_reader:
                    # Strip verse numbers from translation text
                    # Use raw translation text directly
                    cleaned_text = row['translation']
                    normalized_rows.append({
                        'sura': row['sura'],
                        'aya': row['aya'],
                        'text': cleaned_text,
                        'footnotes': row.get('footnotes', '')
                    })

            # Write normalized CSV
            with open(csv_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['sura', 'aya', 'text', 'footnotes'])
                writer.writeheader()
                writer.writerows(normalized_rows)

            print(f"  ✅ Normalized to csv_output ({len(normalized_rows)} verses)", flush=True)
            successful += 1

        except Exception as e:
            print(f"  ❌ Processing failed: {e}", flush=True)
            failed += 1

    print("\n" + "=" * 80, flush=True)
    print(f"Processing: {successful} successful, {failed} failed", flush=True)
    print(f"Output: {csv_dir}", flush=True)

    # Return successful count and list of processed translations (for metadata update)
    return successful, translations_to_process


def parse_quranenc_metadata(trans):
    """Parse QuranEnc translation metadata to extract language and translator"""
    title = trans.get('title', '')

    # Handle invalid title (False, None, etc.)
    if not title or title == False:
        title = trans.get('key', 'Unknown')

    # Extract language and translator from title
    # Format is usually: "Language translation - Translator Name"
    if ' - ' in title:
        parts = title.split(' - ')
        language = parts[0].replace(' translation', '').strip()
        translator = parts[-1].strip()
    else:
        language = title.replace(' translation', '').strip()
        translator = 'Unknown'

    return {
        'id': trans['key'],
        'language': language,
        'translator': translator,
        'name_in_language': title,
        'source': 'quranenc.com'
    }


def find_duplicate_translation(quranenc_meta, existing_translations):
    """Find duplicate translation by matching language AND translator"""
    for existing in existing_translations:
        # Match by language AND translator (case-insensitive)
        if (existing.get('language', '').lower() == quranenc_meta['language'].lower() and
            existing.get('translator', '').lower() == quranenc_meta['translator'].lower()):
            return existing
    return None


def remove_translation_files(translation_id):
    """Remove all files for a translation (csv, json, xml, xlsx, sqlite)"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    translations_dir = project_root / 'alqurandb_api' / 'data' / 'translations'

    formats = ['csv', 'json', 'xml', 'xlsx', 'sqlite']
    removed = []

    for fmt in formats:
        if fmt == 'sqlite':
            file_path = translations_dir / fmt / f"{translation_id}.db"
        else:
            file_path = translations_dir / fmt / f"{translation_id}.{fmt}"

        if file_path.exists():
            file_path.unlink()
            removed.append(fmt)

    return removed


def load_quranenc_metadata_mapping():
    """Load QuranEnc metadata for translation info"""
    script_dir = Path(__file__).parent
    metadata_file = script_dir / 'quranenc_metadata.json'

    with open(metadata_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        mapping = {}
        for trans in data['translations']:
            mapping[trans['key']] = parse_quranenc_metadata(trans)
        return mapping


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
        print(f"\n❌ No CSV files found in {csv_source_dir}", flush=True)
        return False

    # Load metadata for translation info
    metadata_mapping = load_quranenc_metadata_mapping()

    print(f"\n🔄 Generating all formats for {len(csv_files)} translations...", flush=True)
    print("=" * 80, flush=True)

    results = {
        'JSON': 0,
        'XML': 0,
        'Excel': 0,
        'SQLite': 0
    }

    for idx, csv_file in enumerate(csv_files, 1):
        translation_id = csv_file.stem
        print(f"\n→ [{idx}/{len(csv_files)}] Processing {translation_id}...", flush=True)

        # Get metadata for this translation
        metadata_item = metadata_mapping.get(translation_id, {})

        # Generate JSON
        try:
            json_file = output_dirs['json'] / f"{translation_id}.json"
            csv_to_json(csv_file, json_file)
            results['JSON'] += 1
            print(f"  ✅ JSON", flush=True)
        except Exception as e:
            print(f"  ❌ JSON failed: {e}", flush=True)

        # Generate XML
        try:
            xml_file = output_dirs['xml'] / f"{translation_id}.xml"
            create_translation_xml(translation_id, csv_file, xml_file)
            results['XML'] += 1
            print(f"  ✅ XML", flush=True)
        except Exception as e:
            print(f"  ❌ XML failed: {e}", flush=True)

        # Generate Excel
        try:
            xlsx_file = output_dirs['xlsx'] / f"{translation_id}.xlsx"
            create_translation_excel(translation_id, csv_file, metadata_item, xlsx_file)
            results['Excel'] += 1
            print(f"  ✅ Excel", flush=True)
        except Exception as e:
            print(f"  ❌ Excel failed: {e}", flush=True)

        # Generate SQLite
        try:
            sqlite_file = output_dirs['sqlite'] / f"{translation_id}.sqlite"
            create_translation_database(translation_id, csv_file, sqlite_file)
            results['SQLite'] += 1
            print(f"  ✅ SQLite", flush=True)
        except Exception as e:
            print(f"  ❌ SQLite failed: {e}", flush=True)

    print("\n" + "=" * 80, flush=True)
    print("Format Generation Summary:", flush=True)
    total_files = len(csv_files)
    for format_name, success_count in results.items():
        status = "✅" if success_count == total_files else "⚠️"
        print(f"  {status} {format_name}: {success_count}/{total_files} files", flush=True)
    print("=" * 80, flush=True)

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

    print(f"\n🔄 Moving files to API data folder...", flush=True)
    print("=" * 80, flush=True)

    total_moved = 0

    for source_dir, dest_dir in moves:
        if not source_dir.exists():
            continue

        # Ensure destination exists
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Move all files
        import shutil
        files = list(source_dir.glob('*.*'))
        for file in files:
            dest_file = dest_dir / file.name
            shutil.copy2(file, dest_file)
            total_moved += 1

        if files:
            print(f"  ✅ {source_dir.name}: {len(files)} files → {dest_dir}", flush=True)

    print("=" * 80, flush=True)
    print(f"Total files moved: {total_moved}", flush=True)
    print(f"Destination: {api_data_dir}", flush=True)
    print("=" * 80, flush=True)

    return total_moved > 0


def update_metadata(processed_translations):
    """Update metadata.json: add new QuranEnc translations (skip duplicates)"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    metadata_file = project_root / 'alqurandb_api' / 'data' / 'metadata.json'
    csv_dir = script_dir / 'csv_output'

    # Load existing metadata
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    existing_ids = {entry['id'] for entry in metadata}

    # Load QuranEnc metadata
    quranenc_metadata = load_quranenc_metadata_mapping()

    # Add new translations to metadata
    added = 0

    for trans in processed_translations:
        trans_id = trans['key']

        # Check if translation was actually processed (has CSV file)
        csv_file = csv_dir / f"{trans_id}.csv"
        if not csv_file.exists():
            continue

        # Add to metadata if not already there
        if trans_id not in existing_ids:
            meta = quranenc_metadata.get(trans_id)
            if meta:
                metadata.append(meta)
                added += 1
                print(f"  ✅ Added {trans_id} to metadata", flush=True)

    if added > 0:
        # Write updated metadata
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Metadata updated: {added} new translations added", flush=True)
    else:
        print("\n⏭️  No new translations to add to metadata", flush=True)

    return added


def main():
    """Main processing pipeline"""
    print("\n" + "="*80, flush=True)
    print("  QuranEnc.com Translation Processing Pipeline", flush=True)
    print("="*80, flush=True)
    print("\nWorkflow:", flush=True)
    print("  1. Download ALL source CSV files from QuranEnc", flush=True)
    print("  2. Check for duplicates from other sources", flush=True)
    print("  3. Process only non-duplicates to csv_output", flush=True)
    print("  4. Generate JSON, XML, Excel, SQLite formats", flush=True)
    print("  5. Move all files to API data folder", flush=True)
    print("  6. Update metadata.json with new translations", flush=True)
    print("="*80, flush=True)

    # Steps 1-3: Download and process CSV files (combined in extract_all_csv)
    csv_count, processed_translations = extract_all_csv()
    if csv_count == 0:
        print("\n⏭️  No new translations to process.", flush=True)
        return

    # Step 4: Generate all formats
    print("\n📦 STEP 4: Generating all formats...", flush=True)
    print("="*80, flush=True)
    if not generate_all_formats():
        print("\n⚠️  Some formats failed to generate", flush=True)

    # Step 5: Move to API data
    print("\n📁 STEP 5: Moving files to API data folder...", flush=True)
    print("="*80, flush=True)
    if not move_to_api_data():
        print("\n❌ Failed to move files to API data folder", flush=True)
        sys.exit(1)

    # Step 6: Update metadata (add new translations only)
    print("\n📝 STEP 6: Updating metadata...", flush=True)
    print("="*80, flush=True)
    update_metadata(processed_translations)

    print("\n" + "="*80, flush=True)
    print("  ✅ Pipeline completed successfully!", flush=True)
    print("="*80 + "\n", flush=True)


if __name__ == '__main__':
    main()
