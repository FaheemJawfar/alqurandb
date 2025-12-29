# Scripts Directory

This directory contains scripts for extracting, processing, and converting Quran translations.

## Directory Structure

```
scripts/
├── tanzil.net/              # Source data extraction from Tanzil.net
│   ├── parse_translation.py  # Parse XML translations to JSON (BASE FORMAT)
│   ├── extract_metadata.py   # Extract translation metadata
│   └── ...
│
├── converters/              # Convert JSON (base) to other formats
│   ├── json_to_csv.py       # JSON → CSV conversion
│   ├── json_to_xml.py       # JSON → XML conversion
│   ├── json_to_excel.py     # JSON → Excel (XLSX) conversion
│   └── json_to_sqlite.py    # JSON → SQLite database conversion
│
├── generate_all_formats.py # Generate all formats from JSON (one command)
└── create_sqlite_db.py      # Create complete database (optional)
```

## Data Flow

1. **Source Extraction** (`tanzil.net/`)
   - Download XML translations from Tanzil.net
   - Parse and extract to **JSON format** (stored in `alqurandb_api/data/translations/json/`)
   - **JSON is the base format** - all other formats are generated from it

2. **Format Conversion** (`converters/`)
   - Each converter reads from `data/translations/json/`
   - Generates format-specific files in respective directories:
     - CSV → `data/translations/csv/`
     - XML → `data/translations/xml/`
     - Excel → `data/translations/xlsx/`
     - SQLite → `data/translations/sqlite/`

## Usage

### Generate All Formats (Recommended)

```bash
python scripts/generate_all_formats.py
```

This will generate CSV, XML, Excel, and SQLite files for all 114 translations from the base JSON files.

### Generate Individual Formats

```bash
# Generate XML files
python scripts/converters/json_to_xml.py

# Generate Excel files
python scripts/converters/json_to_excel.py

# Generate SQLite databases
python scripts/converters/json_to_sqlite.py
```

### Extract from Source (Tanzil.net)

```bash
# Extract all translations from Tanzil XML to JSON
cd scripts/tanzil.net
python parse_translation.py
```

## File Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| JSON | `.json` | **Base format** - Web APIs, JavaScript apps |
| CSV | `.csv` | Excel, data analysis, spreadsheets |
| XML | `.xml` | Religious software, enterprise systems |
| Excel | `.xlsx` | Business users, researchers, non-technical users |
| SQLite | `.db` | Mobile apps, desktop applications, embedded databases |

## Requirements

Install dependencies before running converters:

```bash
cd alqurandb_api
source .venv/bin/activate
pip install -r requirements.txt
```

Required packages:
- `openpyxl` - Excel file generation
- Standard library modules for CSV, XML, and SQLite
