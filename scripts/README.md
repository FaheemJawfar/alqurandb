# Scripts Directory

This directory contains scripts for extracting, processing, and converting Quran translations.

## Directory Structure

```
scripts/
├── tanzil.net/              # Source data extraction from Tanzil.net
│   ├── parse_translation.py  # Parse XML translations to CSV (BASE FORMAT)
│   ├── extract_metadata.py   # Extract translation metadata
│   └── ...
│
├── converters/              # Convert CSV (base) to other formats
│   ├── csv_to_json.py      # CSV → JSON conversion
│   ├── csv_to_xml.py       # CSV → XML conversion
│   ├── csv_to_excel.py     # CSV → Excel (XLSX) conversion
│   └── csv_to_sqlite.py    # CSV → SQLite database conversion
│
├── generate_all_formats.py # Generate all formats from CSV (one command)
└── create_sqlite_db.py      # Create complete database (optional)
```

## Data Flow

1. **Source Extraction** (`tanzil.net/`)
   - Download XML translations from Tanzil.net
   - Parse and extract to **CSV format** (stored in `alqurandb_api/data/translations/csv/`)
   - **CSV is the base format** - all other formats are generated from it

2. **Format Conversion** (`converters/`)
   - Each converter reads from `data/translations/csv/`
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

This will generate JSON, XML, Excel, and SQLite files for all 114 translations from the base CSV files.

### Generate Individual Formats

```bash
# Generate XML files
python scripts/converters/csv_to_xml.py

# Generate Excel files
python scripts/converters/csv_to_excel.py

# Generate SQLite databases
python scripts/converters/csv_to_sqlite.py
```

### Extract from Source (Tanzil.net)

```bash
# Extract all translations from Tanzil XML to CSV
cd scripts/tanzil.net
python parse_translation.py
```

## File Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| CSV | `.csv` | **Base format** - Excel, data analysis, spreadsheets |
| JSON | `.json` | Web APIs, JavaScript apps |
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
