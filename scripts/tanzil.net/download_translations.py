#!/usr/bin/env python3
"""
Download all Quran translations from Tanzil in XML format
"""

import json
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


def download_file(url, output_path, trans_id):
    """Download a file from URL to output_path"""
    try:
        # Create request with user agent to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }
        req = Request(url, headers=headers)

        with urlopen(req, timeout=30) as response:
            content = response.read()

        with open(output_path, 'wb') as f:
            f.write(content)

        return True, len(content)

    except HTTPError as e:
        return False, f"HTTP Error {e.code}: {e.reason}"
    except URLError as e:
        return False, f"URL Error: {e.reason}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    """Main function"""
    script_dir = Path(__file__).parent
    json_file = script_dir / 'tanzil_translations.json'
    output_dir = script_dir / 'translations_xml'

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Load translations metadata
    print(f"Loading translations from {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        translations = json.load(f)

    print(f"Found {len(translations)} translations to download\n")

    # Track statistics
    successful = 0
    failed = 0
    skipped = 0
    total_size = 0

    # Download each translation
    for i, trans in enumerate(translations, 1):
        trans_id = trans['id']
        language = trans['language']
        name = trans['name']
        xml_url = trans['download']['xml']

        # Output filename
        output_file = output_dir / f"{trans_id}.xml"

        # Skip if already downloaded
        if output_file.exists():
            print(f"[{i}/{len(translations)}] ⏭️  Skipping {trans_id} (already exists)")
            skipped += 1
            continue

        print(f"[{i}/{len(translations)}] 📥 Downloading {trans_id} ({language} - {name})...")

        # Download the file
        success, result = download_file(xml_url, output_file, trans_id)

        if success:
            size_kb = result / 1024
            total_size += result
            successful += 1
            print(f"            ✅ Downloaded {size_kb:.1f} KB")
        else:
            failed += 1
            print(f"            ❌ Failed: {result}")

        # Be nice to the server - small delay between downloads
        if i < len(translations):
            time.sleep(0.5)

    # Print summary
    print("\n" + "=" * 60)
    print("Download Summary")
    print("=" * 60)
    print(f"Total translations:  {len(translations)}")
    print(f"Successfully downloaded: {successful}")
    print(f"Already existed: {skipped}")
    print(f"Failed: {failed}")
    print(f"Total size: {total_size / (1024 * 1024):.2f} MB")
    print(f"Output directory: {output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()
