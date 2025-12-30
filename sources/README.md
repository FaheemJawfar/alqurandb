# Sources Directory

This directory contains source translation files and automated processing scripts for extracting, processing, and converting Quran translations into multiple formats.

## Table of Contents

- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [How It Works](#how-it-works)
- [Data Flow](#data-flow)
- [Translation Sources](#translation-sources)
- [Converters](#converters)
- [Database Generation](#database-generation)
- [Usage](#usage)
- [Adding New Translations](#adding-new-translations)
- [File Formats](#file-formats)
- [Technical Details](#technical-details)

---

## Overview

The AlQuranDB project maintains **178 translations** of the Quran in **40+ languages**. This directory contains:

- **Source files** from various translation providers (XML and CSV formats)
- **Automated processing scripts** that extract and convert translations
- **Format converters** that generate JSON, XML, Excel, and SQLite files
- **Database generator** that creates a comprehensive SQLite database

**Key Principle**: CSV is the **base format**. All other formats are generated from CSV files stored in `alqurandb_api/data/translations/csv/`.

---

## Directory Structure

```
sources/
├── tanzil.net/              # Tanzil.net translations (111 translations)
│   ├── source/              # 111 XML source files
│   └── process_tanzil.py    # Automated processing pipeline
│
├── quranenc.com/            # QuranEnc.com translations (64 translations)
│   ├── source/              # 68 raw CSV downloads (includes duplicates)
│   ├── csv_output/          # 68 normalized CSV files
│   ├── quranenc_metadata.json  # QuranEnc-specific metadata
│   └── process_quranenc.py  # Automated processing pipeline
│
├── tamililquran.com/        # Tamil translations (2 translations)
│   ├── source/              # 2 XML source files (IFT, King Fahd)
│   └── process_tamilil.py   # Automated processing pipeline
│
├── acju.lk/                 # ACJU Sinhala translation (1 translation)
│   ├── source/              # 1 XML source file
│   └── process_acju.py      # Automated processing pipeline
│
├── converters/              # Format conversion utilities
│   ├── csv_to_json.py      # CSV → JSON converter
│   ├── csv_to_xml.py       # CSV → XML converter
│   ├── csv_to_excel.py     # CSV → Excel (XLSX) converter
│   └── csv_to_sqlite.py    # CSV → SQLite database converter
│
├── generate_all_formats.py # Generate all formats from existing CSV files
├── create_complete_db.py    # Create comprehensive database (all translations)
└── README.md               # This file
```

---

## How It Works

### The Automated Pipeline

Each translation source has an automated processing script. There are two main workflows:

**Workflow A: XML-based sources** (Tanzil, TamilIL, ACJU)
```
┌─────────────────┐
│  Source XML     │  Translation provider's XML files
│  (source/)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Extract CSV    │  Parse XML → Extract verses → Write CSV
│  (csv_output/)  │  CSV is the base format
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Generate       │  CSV → JSON, XML, Excel, SQLite
│  All Formats    │  Using converter scripts
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Move to API    │  Copy all files to:
│  Data Folder    │  alqurandb_api/data/translations/
└─────────────────┘
```

**Workflow B: CSV-based sources** (QuranEnc)
```
┌─────────────────┐
│  Download CSV   │  Download ALL source CSV files
│  (source/)      │  from quranenc.com
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Check          │  Compare with existing metadata
│  Duplicates     │  Skip duplicates from other sources
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Normalize CSV  │  Process non-duplicates only
│  (csv_output/)  │  Normalize column names (sura, aya, text)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Generate       │  CSV → JSON, XML, Excel, SQLite
│  All Formats    │  Using converter scripts
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Move to API    │  Copy all files to:
│  Data Folder    │  alqurandb_api/data/translations/
└─────────────────┘
```

### Processing Script Workflow

Each `process_*.py` script performs these steps automatically:

**For XML-based sources (Tanzil, TamilIL, ACJU):**

1. **Extract CSV** from XML source files
   - Parse XML structure (different for each source)
   - Extract sura number, aya number, and text
   - Write to CSV format: `sura,aya,text`

2. **Generate All Formats**
   - Import converter functions directly
   - Generate JSON, XML, Excel, SQLite from CSV
   - Create temporary output folders

3. **Move to API Data**
   - Copy all generated files to `alqurandb_api/data/translations/`
   - Organized by format: `csv/`, `json/`, `xml/`, `xlsx/`, `sqlite/`

**For CSV-based sources (QuranEnc):**

1. **Download ALL source CSV files**
   - Download from quranenc.com using translation IDs
   - Save raw CSV files to `source/` folder
   - All valid translations downloaded regardless of duplicates

2. **Check for Duplicates**
   - Compare with existing translations by language AND translator
   - Identify duplicates from other sources
   - Determine which translations to process

3. **Normalize CSV** (non-duplicates only)
   - Read from `source/` folder
   - Normalize column names: `translation` → `text`
   - Write to `csv_output/` with standard format: `sura,aya,text`

4. **Generate All Formats**
   - Generate JSON, XML, Excel, SQLite from normalized CSV
   - Create output folders for each format

5. **Move to API Data**
   - Copy all generated files to `alqurandb_api/data/translations/`
   - Update metadata.json with new translations

---

## Data Flow

### 1. Source Extraction

Each translation source has unique structure:

**Tanzil.net** (111 translations) - XML format:
```xml
<quran>
  <sura index="1">
    <aya index="1" text="In the name of Allah..."/>
  </sura>
</quran>
```

**QuranEnc.com** (64 translations) - CSV format:
```csv
id,sura,aya,translation
1,1,1,"In the name of Allah, the Entirely Merciful..."
2,1,2,"[All] praise is [due] to Allah, Lord of the worlds"
```
Note: QuranEnc CSVs have extra columns and metadata headers that are removed during normalization.

**TamililQuran.com** (2 translations) - XML format:
```xml
<quran>
  <sura index="1">
    <aya index="1" text="அல்லாஹ்வின் பெயரால்..."/>
  </sura>
</quran>
```

**ACJU.lk** (1 translation) - XML format:
```xml
<quran>
  <sura index="1">
    <aya index="1" text="සැමට කරුණාතරිත..."/>
  </sura>
</quran>
```

### 2. CSV Base Format

All sources are converted to a standard CSV format:

```csv
sura,aya,text
1,1,"In the name of Allah, the Entirely Merciful, the Especially Merciful."
1,2,"[All] praise is [due] to Allah, Lord of the worlds -"
1,3,"The Entirely Merciful, the Especially Merciful,"
...
```

**Note**: Column naming follows the standard: `sura`, `aya`, `text` (not `surah`, `ayah`).

**Why CSV?**
- Simple, universal format
- Easy to edit and verify
- Compatible with all data tools
- Single source of truth for all other formats

### 3. Format Generation

From CSV, we generate:

| Format | Purpose | Generated By |
|--------|---------|--------------|
| **JSON** | Web APIs, JavaScript apps | `csv_to_json.py` |
| **XML** | Religious software, enterprise | `csv_to_xml.py` |
| **Excel** | Researchers, non-technical users | `csv_to_excel.py` |
| **SQLite** | Individual translation databases | `csv_to_sqlite.py` |

### 4. Complete Database

The `create_complete_db.py` script creates a **comprehensive SQLite database** containing all 178 translations:

```sql
-- Database Schema
CREATE TABLE translations (
    id TEXT PRIMARY KEY,
    language TEXT NOT NULL,
    translator TEXT NOT NULL,
    name_in_language TEXT,
    source TEXT NOT NULL
);

CREATE TABLE verses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    translation_id TEXT NOT NULL,
    sura INTEGER NOT NULL,
    aya INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (translation_id) REFERENCES translations(id)
);

-- Indexes for fast queries
CREATE INDEX idx_translation_id ON verses(translation_id);
CREATE INDEX idx_sura ON verses(sura);
CREATE INDEX idx_sura_aya ON verses(sura, aya);
CREATE INDEX idx_translation_sura ON verses(translation_id, sura);
CREATE INDEX idx_translation_sura_aya ON verses(translation_id, sura, aya);
```

**Database Stats:**
- Size: ~419 MB
- Translations: 178
- Total verses: 1,109,823
- Automatic creation on FastAPI startup

---

## Translation Sources

### Tanzil.net (111 Translations)

**Source**: http://tanzil.net/trans/

**Languages**: 40+ languages including English, Arabic, Urdu, Persian, Turkish, French, German, Spanish, Russian, Indonesian, Malay, and many more.

**Processing**: `python sources/tanzil.net/process_tanzil.py`

**Format**: XML source files

**Metadata Mapping**: Uses `metadata.json` to map Tanzil source IDs (e.g., `en.sahih`) to translation IDs (e.g., `english_sahih`).

### QuranEnc.com (64 Translations)

**Source**: https://quranenc.com/

**Languages**: 50+ languages including many less common languages like Afar, Akan, Assamese, Lithuanian, Pashto, and more.

**Processing**: `python sources/quranenc.com/process_quranenc.py`

**Format**: CSV files downloaded directly from QuranEnc API

**URL Pattern**: `https://quranenc.com/en/home/download/csv/{translation_id}`

**Special Features**:
- Downloads ALL source files first (68 total)
- Detects duplicates from other sources
- Only processes unique translations (64 final)
- Maintains both raw downloads (source/) and normalized CSVs (csv_output/)

**Metadata**: Uses `quranenc_metadata.json` for QuranEnc-specific metadata

### TamililQuran.com (2 Translations)

**Source**: Custom Tamil translations

**Translations**:
1. Islamic Foundation Trust (IFT)
2. King Fahd Quran Complex

**Processing**: `python sources/tamililquran.com/process_tamilil.py`

**Format**: XML source files

### ACJU.lk (1 Translation)

**Source**: All Ceylon Jamiyyathul Ulama

**Language**: Sinhala (සිංහල)

**Processing**: `python sources/acju.lk/process_acju.py`

**Format**: XML source file

---

## Converters

### CSV to JSON (`csv_to_json.py`)

Converts CSV to JSON format with verse references as keys:

```json
{
  "1:1": "In the name of Allah, the Entirely Merciful...",
  "1:2": "[All] praise is [due] to Allah, Lord of the worlds -",
  "1:3": "The Entirely Merciful, the Especially Merciful,"
}
```

**Usage**: Read from `data/translations/csv/`, write to `data/translations/json/`

### CSV to XML (`csv_to_xml.py`)

Converts CSV to XML format:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<quran translation_id="english_sahih">
  <sura index="1">
    <aya index="1" text="In the name of Allah..."/>
    <aya index="2" text="[All] praise is [due] to Allah..."/>
  </sura>
</quran>
```

### CSV to Excel (`csv_to_excel.py`)

Converts CSV to Excel format with metadata and proper formatting:

**Features**:
- Translation metadata in header
- Formatted columns (Surah, Ayah, Translation)
- Professional styling
- Frozen header row

**Dependencies**: `openpyxl`

### CSV to SQLite (`csv_to_sqlite.py`)

Creates individual SQLite database for each translation:

**Schema**:
```sql
CREATE TABLE verses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sura INTEGER NOT NULL,
    aya INTEGER NOT NULL,
    text TEXT NOT NULL
);
CREATE INDEX idx_sura ON verses(sura);
CREATE INDEX idx_aya ON verses(aya);
CREATE INDEX idx_sura_aya ON verses(sura, aya);
```

---

## Database Generation

### Complete Database (`create_complete_db.py`)

Creates a comprehensive SQLite database with **all 178 translations**.

**Process**:
1. Read all CSV files from `data/translations/csv/`
2. Load metadata from `data/metadata.json`
3. Create database schema (translations + verses tables)
4. Insert all translations and verses
5. Create indexes for fast queries
6. Save to `data/quran_translations.db`

**Automatic Creation**: The database is automatically created on FastAPI startup if it doesn't exist (see `alqurandb_api/app/core/database_init.py`).

**Query Examples**:
```sql
-- Get all translations
SELECT * FROM translations;

-- Get specific verse in all translations
SELECT t.language, t.translator, v.text
FROM verses v
JOIN translations t ON v.translation_id = t.id
WHERE v.sura = 1 AND v.aya = 1;

-- Get all verses from a sura in a specific translation
SELECT * FROM verses
WHERE translation_id = 'english_sahih' AND sura = 1;
```

---

## Usage

### Process All Translations (Automated)

Each translation source has its own automated processing script:

```bash
# Process all Tanzil translations (111 translations)
python sources/tanzil.net/process_tanzil.py

# Process all QuranEnc translations (64 translations)
python sources/quranenc.com/process_quranenc.py

# Process Tamil translations (2 translations)
python sources/tamililquran.com/process_tamilil.py

# Process ACJU Sinhala translation (1 translation)
python sources/acju.lk/process_acju.py
```

Each script automatically:
1. Extracts/downloads and normalizes CSV files
2. Generates all formats (JSON, XML, Excel, SQLite)
3. Moves files to the API data folder
4. Updates metadata (QuranEnc only)

### Generate All Formats (from existing CSV)

If you already have CSV files and want to regenerate other formats:

```bash
python sources/generate_all_formats.py
```

This will generate JSON, XML, Excel, and SQLite files for all translations from the base CSV files.

### Generate Individual Formats

```bash
# Generate XML files
python sources/converters/csv_to_xml.py

# Generate Excel files
python sources/converters/csv_to_excel.py

# Generate SQLite databases
python sources/converters/csv_to_sqlite.py

# Generate JSON files
python sources/converters/csv_to_json.py
```

### Create Complete Database

```bash
# Create comprehensive database with all translations
python sources/create_complete_db.py
```

**Note**: The database is automatically created on FastAPI startup if missing.

---

## Adding New Translations

To add a new translation source, follow this workflow:

### 1. Create Source Folder

```bash
mkdir -p sources/newsource.com/source
```

### 2. Add Source XML Files

Place the XML translation files in `sources/newsource.com/source/`

### 3. Create Processing Script

Create `sources/newsource.com/process_newsource.py`:

```python
#!/usr/bin/env python3
"""Process NewSource translations - Full automated pipeline"""
import xml.etree.ElementTree as ET
import csv
import sys
from pathlib import Path

# Import converters
sys.path.insert(0, str(Path(__file__).parent.parent))
from converters.csv_to_json import csv_to_json
from converters.csv_to_xml import create_translation_xml
from converters.csv_to_excel import create_translation_excel
from converters.csv_to_sqlite import create_translation_database

def xml_to_csv(xml_file: Path, csv_file: Path) -> int:
    """Convert XML to CSV - customize based on XML structure"""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['surah', 'ayah', 'text'])

        verse_count = 0
        # Parse XML based on source structure
        for sura in root.findall('sura'):
            surah_num = int(sura.get('index'))
            for aya in sura.findall('aya'):
                ayah_num = int(aya.get('index'))
                text = aya.get('text', '').strip()
                writer.writerow([surah_num, ayah_num, text])
                verse_count += 1

    return verse_count

def extract_all_csv():
    """Extract CSV from all XML source files"""
    # Implementation similar to existing process_*.py scripts
    pass

def generate_all_formats():
    """Generate all formats from CSV"""
    # Implementation similar to existing process_*.py scripts
    pass

def move_to_api_data():
    """Move files to API data folder"""
    # Implementation similar to existing process_*.py scripts
    pass

def main():
    """Main processing pipeline"""
    extract_all_csv()
    generate_all_formats()
    move_to_api_data()

if __name__ == '__main__':
    main()
```

### 4. Add Metadata

Add translation metadata to `alqurandb_api/data/metadata.json`:

```json
{
  "id": "language_translator",
  "language": "Language Name",
  "translator": "Translator Name",
  "name_in_language": "Name in Original Language",
  "source": "newsource.com",
  "source_id": "source_identifier"
}
```

### 5. Run Processing Script

```bash
python sources/newsource.com/process_newsource.py
```

### 6. Verify Output

Check that files were generated in `alqurandb_api/data/translations/`:
- CSV in `csv/`
- JSON in `json/`
- XML in `xml/`
- Excel in `xlsx/`
- SQLite in `sqlite/`

### 7. Regenerate Complete Database

```bash
python sources/create_complete_db.py
```

Or just restart the FastAPI server - it will automatically regenerate the database.

---

## File Formats

| Format | Extension | Use Case | Size (avg) |
|--------|-----------|----------|------------|
| **CSV** | `.csv` | Base format, Excel, data analysis | ~350 KB |
| **JSON** | `.json` | Web APIs, JavaScript apps | ~370 KB |
| **XML** | `.xml` | Religious software, enterprise | ~400 KB |
| **Excel** | `.xlsx` | Researchers, non-technical users | ~80 KB |
| **SQLite** | `.db` | Mobile apps, desktop apps | ~450 KB |

**Complete Database**: `quran_translations.db` (~419 MB) - All 178 translations in one database

---

## Technical Details

### Path Resolution

All scripts use dynamic path resolution with `Path(__file__).parent` to ensure they work regardless of folder location:

```python
# Get script directory
script_dir = Path(__file__).parent

# Get project root (two levels up)
project_root = script_dir.parent.parent

# Get API data directory
api_data_dir = project_root / 'alqurandb_api' / 'data'
```

### CSV Format Specification

**Standard CSV format** used across all translations:

```csv
sura,aya,text
1,1,"First verse text"
1,2,"Second verse text"
...
114,6,"Last verse text"
```

**Rules**:
- Header row: `sura,aya,text`
- Sura: 1-114
- Aya: 1-286 (varies by sura)
- Text: UTF-8 encoded, quoted if contains commas

**Note**: We use `sura` and `aya` (not `surah` and `ayah`) for consistency across the codebase.

### Verse Count

Most translations have **6,236 verses**. Some exceptions:
- Sinhala ACJU: **6,051 verses**

### Encoding

All files use **UTF-8 encoding** to support:
- Arabic script
- Asian languages (Tamil, Sinhala, Chinese, Japanese, Korean)
- Cyrillic (Russian)
- Special characters

### Dependencies

**Python Standard Library**:
- `csv` - CSV processing
- `json` - JSON generation
- `sqlite3` - SQLite database creation
- `xml.etree.ElementTree` - XML parsing and generation
- `pathlib` - Path handling

**External Dependencies**:
- `openpyxl` - Excel file generation

Install dependencies:
```bash
cd alqurandb_api
source .venv/bin/activate
pip install openpyxl
```

### Performance

**Processing Times** (approximate):
- CSV extraction: 1-2 seconds per translation
- CSV download (QuranEnc): 1-2 seconds per translation
- Format generation: 3-5 seconds per translation
- Complete database creation: 45-60 seconds (all 178 translations)

**Optimization**:
- Batch insertions for SQLite (faster)
- Indexed database queries
- Cached metadata in memory

---

## Troubleshooting

### Issue: Script not found

**Error**: `python: can't open file 'sources/...'`

**Solution**: Run from project root directory:
```bash
cd /path/to/alqurandb
python sources/tanzil.net/process_tanzil.py
```

### Issue: Import errors

**Error**: `ModuleNotFoundError: No module named 'converters'`

**Solution**: Scripts automatically add parent directory to Python path. If issues persist, check `sys.path.insert(0, str(Path(__file__).parent.parent))`

### Issue: Missing openpyxl

**Error**: `ModuleNotFoundError: No module named 'openpyxl'`

**Solution**: Install dependencies:
```bash
cd alqurandb_api
source .venv/bin/activate
pip install openpyxl
```

### Issue: Database not created

**Problem**: Database file missing after running script

**Solution**:
1. Check if CSV files exist in `alqurandb_api/data/translations/csv/`
2. Check if `metadata.json` exists
3. Run with verbose output to see errors
4. Database is auto-created on FastAPI startup if missing

### Issue: Incorrect verse count

**Problem**: Translation has different number of verses

**Solution**: Some translations have variations in verse numbering. This is normal. Most have 6,236 verses, but some (like Sinhala ACJU) may have fewer.

---

## Summary

This directory implements a **robust, automated translation processing system** that:

✅ Supports **178 translations** in **50+ languages**
✅ Uses **CSV as single source of truth**
✅ Generates **5 different formats** automatically
✅ Creates **comprehensive SQLite database**
✅ Provides **automated pipelines** for each source
✅ Supports both **XML and CSV** source formats
✅ Implements **intelligent duplicate detection**
✅ Enables **easy addition** of new translations
✅ Ensures **data consistency** across all formats

The system is designed to be maintainable, extensible, and efficient for managing Quran translations at scale.
