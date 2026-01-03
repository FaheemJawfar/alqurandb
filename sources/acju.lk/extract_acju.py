#!/ reentry/env python3
import sqlite3
import csv
import re
from pathlib import Path
from bs4 import BeautifulSoup

def clean_html(html_content):
    """
    Extracts the Sinhala translation text from the HTML structure provided.
    Removes the Arabic text, verse numbers, and footnote markers.
    """
    if not html_content:
        return "", []

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # The translation is typically inside a div with align='left' or within a span with f1_2 class
    # based on the sample: <div align='left'><span dir='ltr' class='f1_2'>(1) සැමට ...
    
    # Extract footnote references before stripping tags
    # <a title="" href="#1_1" data-rel="popup" onclick="showFootNote(1);"><span class="f1_8">1</span></a>
    footnote_tags = soup.find_all('a', onclick=re.compile(r'showFootNote'))
    footnote_ids = []
    for tag in footnote_tags:
        href = tag.get('href', '')
        if href.startswith('#'):
            footnote_ids.append(href[1:]) # remove #
            
    # Remove the Arabic part (usually in <div align='right'>)
    arabic_div = soup.find('div', align='right')
    if arabic_div:
        arabic_div.decompose()
        
    # Get text
    text = soup.get_text(separator=' ', strip=True)
    
    # Remove leading verse numbers like "(1) ", "(2) "
    text = re.sub(r'^\(\d+\)\s*', '', text)
    
    # Remove footnote markers (they appear as numbers after get_text)
    # Since we use separator=' ', they might be isolated
    # But often they are just digits. Let's try to be more specific.
    # The markers are usually inside the text.
    # A better way might be to find the spans with f1_8 class and remove them
    for marker in soup.find_all('span', class_='f1_8'):
        marker.decompose()
    
    # Re-extract text after removing Arabic and markers
    text = soup.get_text(separator=' ', strip=True)
    
    # Clean up leading verse numbers again if they were inside some tag
    text = re.sub(r'^\(\d+\)\s*', '', text)
    
    # Clean up extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text, footnote_ids

def main():
    script_dir = Path(__file__).parent
    db_path = script_dir / 'source' / 'quran.db'
    output_csv = script_dir.parent.parent / 'alqurandb_api' / 'data' / 'translations' / 'csv' / 'sinhala_acju.csv'
    
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all footnotes into a dictionary for easy access
    cursor.execute("SELECT ID, FOOTNOTE FROM footnotes")
    footnotes_map = {}
    for fid, ftext in cursor.fetchall():
        # Remove leading numbers from footnotes if present (e.g., "1)...")
        ftext = re.sub(r'^\d+\)\s*', '', ftext).strip()
        footnotes_map[fid] = ftext
        
    # Fetch all ayahs including the CONCATS column
    cursor.execute("SELECT SURAHID, AYATHID, AYATH, AYATH_CONCATS FROM ayathsnew ORDER BY SURAHID, AYATHID")
    ayaths = cursor.fetchall()
    
    print(f"Processing {len(ayaths)} rows (unrolling to 6236 verses)...")
    
    data = []
    for sura, start_aya, html, concats in ayaths:
        text, f_ids = clean_html(html)
        
        # Resolve footnotes
        resolved_footnotes = []
        for fid in f_ids:
            if fid in footnotes_map:
                f_text = footnotes_map[fid].strip()
                if f_text and not f_text.endswith('.'):
                    f_text += "."
                resolved_footnotes.append(f_text)
            else:
                print(f"Warning: Footnote ID {fid} not found for Sura {sura} Aya {start_aya}")
        
        footnotes_str = " ".join(resolved_footnotes)
            
        # Unroll concatenated verses
        num_verses = (concats or 0) + 1
        for i in range(num_verses):
            aya = start_aya + i
            data.append({
                'sura': sura,
                'aya': aya,
                'text': text,
                'footnotes': footnotes_str
            })
        
    # Write to CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['sura', 'aya', 'text', 'footnotes'])
        writer.writeheader()
        writer.writerows(data)
        
    print(f"Successfully exported {len(data)} verses to {output_csv}")
    conn.close()

if __name__ == "__main__":
    main()
