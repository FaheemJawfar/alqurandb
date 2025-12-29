# Sources and Scripts Directory

This directory contains source translation files and scripts for extracting, processing, and converting Quran translations.

## Directory Structure

```
sources_and_scripts/
├── tanzil.net/              # Tanzil.net translations
│   ├── source/              # Source XML files
│   └── process_tanzil.py    # Automated processing pipeline
│
├── tamililquran.com/        # Tamil translations
│   ├── source/              # Source XML files
│   └── process_tamilil.py   # Automated processing pipeline
│
├── acju.lk/                 # ACJU Sinhala translation
│   ├── source/              # Source XML files
│   └── process_acju.py      # Automated processing pipeline
│
├── converters/              # Convert CSV (base) to other formats
│   ├── csv_to_json.py      # CSV → JSON conversion
│   ├── csv_to_xml.py       # CSV → XML conversion
│   ├── csv_to_excel.py     # CSV → Excel (XLSX) conversion
│   └── csv_to_sqlite.py    # CSV → SQLite database conversion
│
├── generate_all_formats.py # Generate all formats from CSV (one command)
└── create_complete_db.py    # Create complete database with all translations
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

### Process All Translations (Automated)

Each translation source has its own automated processing script:

```bash
# Process all Tanzil translations (114 translations)
python sources_and_scripts/tanzil.net/process_tanzil.py

# Process Tamil translations (2 translations)
python sources_and_scripts/tamililquran.com/process_tamilil.py

# Process ACJU Sinhala translation (1 translation)
python sources_and_scripts/acju.lk/process_acju.py
```

Each script automatically:
1. Extracts CSV from XML source files
2. Generates all formats (JSON, XML, Excel, SQLite)
3. Moves files to the API data folder

### Generate All Formats (from existing CSV)

```bash
python sources_and_scripts/generate_all_formats.py
```

This will generate JSON, XML, Excel, and SQLite files for all translations from the base CSV files.

### Generate Individual Formats

```bash
# Generate XML files
python sources_and_scripts/converters/csv_to_xml.py

# Generate Excel files
python sources_and_scripts/converters/csv_to_excel.py

# Generate SQLite databases
python sources_and_scripts/converters/csv_to_sqlite.py
```

### Create Complete Database

```bash
# Create comprehensive database with all translations
python sources_and_scripts/create_complete_db.py
```

Note: The database is automatically created on FastAPI startup if missing.

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
