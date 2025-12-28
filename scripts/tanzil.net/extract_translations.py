#!/usr/bin/env python3
"""
Extract Quran translation metadata from Tanzil translations page
"""

import json
import re
from pathlib import Path
from urllib.request import urlopen, Request


def extract_translations(source):
    """Extract translation metadata from HTML source (URL or file path)

    Args:
        source: Either a URL string (starting with http) or a file path
    """

    # Fetch HTML content
    if source.startswith('http'):
        # Fetch from URL
        print(f"Fetching from {source}...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }
        req = Request(source, headers=headers)
        with urlopen(req, timeout=30) as response:
            html_content = response.read().decode('utf-8')
    else:
        # Read from file
        print(f"Reading from {source}...")
        with open(source, 'r', encoding='utf-8') as f:
            html_content = f.read()

    translations = []

    # Find all table rows in tbody
    # The HTML has malformed tags like </lang> and </name> instead of </td>
    row_pattern = r'<tr><td>(.*?)</tr>'
    rows = re.findall(row_pattern, html_content, re.DOTALL)

    for row in rows:
        # Extract language (after flag icon, before </lang> or next tag)
        lang_match = re.search(r'flag"></i>(.*?)(?:</lang>|<td>)', row)
        if not lang_match:
            continue
        language = lang_match.group(1).strip()

        # Extract name (after first <td>, before </name> or next tag)
        name_match = re.search(r'</i>.*?<td>(.*?)(?:</name>|<td>)', row)
        if not name_match:
            continue
        name = name_match.group(1).strip()

        # Extract translator (after second <td>, before third <td>)
        translator_match = re.search(r'</name><td>(.*?)<td>', row)
        if not translator_match:
            continue
        translator = translator_match.group(1).strip()

        # Remove HTML tags from translator (biography links, etc.)
        translator = re.sub(r'&nbsp;<a.*?</a>', '', translator)
        translator = re.sub(r'<.*?>', '', translator)
        translator = translator.replace('&amp;', '&')

        # Extract translation ID from download link
        id_match = re.search(r'href="/trans/([^"]+)".*?title="Download"', row)
        if not id_match:
            continue
        trans_id = id_match.group(1)

        translations.append({
            'id': trans_id,
            'language': language,
            'name': name,
            'translator': translator,
            'download': {
                'text': f'http://tanzil.net/trans/?transID={trans_id}&type=txt',
                'text_with_numbers': f'http://tanzil.net/trans/?transID={trans_id}&type=txt-2',
                'xml': f'http://tanzil.net/trans/?transID={trans_id}&type=xml',
                'sql': f'http://tanzil.net/trans/?transID={trans_id}&type=sql'
            }
        })

    return translations


def main():
    """Main function"""
    script_dir = Path(__file__).parent
    output_file = script_dir / 'tanzil_translations.json'

    # Use the Tanzil translations URL
    source_url = 'https://tanzil.net/trans/'

    print("Extracting translations from Tanzil...")

    # Extract translations
    translations = extract_translations(source_url)

    print(f"Found {len(translations)} translations")

    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)

    print(f"Saved metadata to {output_file}")

    # Print statistics
    languages = set(t['language'] for t in translations)
    print(f"\nStatistics:")
    print(f"  Total translations: {len(translations)}")
    print(f"  Total languages: {len(languages)}")
    print(f"\nSample translations:")
    for trans in translations[:5]:
        print(f"  - {trans['language']}: {trans['name']} by {trans['translator']} [{trans['id']}]")


if __name__ == '__main__':
    main()
