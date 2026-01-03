#!/usr/bin/env python3
import sqlite3
import csv
import re
import html
from pathlib import Path
from bs4 import BeautifulSoup

def clean_text(text):
    """
    Strips any remaining HTML tags and decodes entities like &nbsp; and &zwj;.
    """
    if not text:
        return ""
    # Strip any remaining tags that BeautifulSoup might have missed or that were in footnote strings
    text = BeautifulSoup(text, 'html.parser').get_text(separator=' ', strip=True)
    # Decode entities
    text = html.unescape(text)
    # Replace non-breaking spaces and Zero Width Joiners with standard spaces/empty
    text = text.replace('\xa0', ' ')  # &nbsp;
    text = text.replace('\u200d', '')  # &zwj;
    # Remove asterisks as they are typically used as redundant footnote markers in the source
    text = text.replace('*', '')
    # Clean up extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def clean_html(html_content, sura_footnote_counter):
    """
    Extracts the Sinhala translation text from the HTML structure provided.
    Replaces footnote markers with [n].
    """
    if not html_content:
        return "", [], sura_footnote_counter

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # The Arabic part (usually in <div align='right'>)
    arabic_div = soup.find('div', align='right')
    if arabic_div:
        arabic_div.decompose()
            
    # Find all footnote links and replace them with [n]
    footnote_tags = soup.find_all('a', onclick=re.compile(r'showFootNote'))
    footnote_ids = []
    
    for tag in footnote_tags:
        sura_footnote_counter += 1
        marker = f" [{sura_footnote_counter}]"
        
        href = tag.get('href', '')
        if href.startswith('#'):
            footnote_ids.append((sura_footnote_counter, href[1:]))
            
        # Replace the tag with our standard marker
        tag.replace_with(marker)
    
    # Get text and clean it
    text = clean_text(soup.get_text(separator=' ', strip=True))
    
    # Remove leading verse numbers like "(1) ", "(1, 2) "
    text = re.sub(r'^\(\d+(,\s*\d+)*\)\s*', '', text)
    
    return text, footnote_ids, sura_footnote_counter

def main():
    script_dir = Path(__file__).parent
    db_path = script_dir / 'source' / 'quran.db'
    output_csv = script_dir.parent.parent / 'alqurandb_api' / 'data' / 'translations' / 'csv' / 'sinhalese_acju.csv'
    
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all footnotes into a dictionary
    cursor.execute("SELECT ID, FOOTNOTE FROM footnotes")
    footnotes_map = {}
    for fid, ftext in cursor.fetchall():
        # Clean the footnote text immediately
        ftext = re.sub(r'^\d+\)\s*', '', ftext).strip()
        ftext = clean_text(ftext)
        footnotes_map[fid] = ftext
        
    # Fetch all ayahs including the CONCATS column
    cursor.execute("SELECT SURAHID, AYATHID, AYATH, AYATH_CONCATS FROM ayathsnew ORDER BY SURAHID, AYATHID")
    ayaths = cursor.fetchall()
    
    print(f"Processing {len(ayaths)} rows (unrolling to 6236 verses)...")
    
    data = []
    current_sura = 0
    sura_footnote_counter = 0
    
    for sura, start_aya, html_content, concats in ayaths:
        if sura != current_sura:
            current_sura = sura
            sura_footnote_counter = 0
            
        text, f_info, sura_footnote_counter = clean_html(html_content, sura_footnote_counter)
        
        # Resolve footnotes
        resolved_footnotes = []
        for index, fid in f_info:
            if fid in footnotes_map:
                f_text = footnotes_map[fid]
                if f_text:
                    if not f_text.endswith('.'):
                        f_text += "."
                    resolved_footnotes.append(f"[{index}] {f_text}")
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
