# AlQuranDB API

FastAPI backend providing RESTful API endpoints for Quranic data and translations.

## Features

- Complete Quran data access via REST API
- Multiple translation support (English, Urdu, and more)
- Surah and Ayah endpoints with optional translation queries
- Auto-generated interactive API documentation
- CORS support for frontend integration
- Fast and efficient with FastAPI

## Setup

1. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Run the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Base URL: `/api`

#### Translations
- `GET /translations/` - Get list of all available translations (178 translations)
- `GET /translations/{translation_id}/{sura}/{aya}` - Get specific verse
- `GET /translations/{translation_id}/{sura}` - Get all verses from a sura
  - Query parameters:
    - `from_aya` (optional): Starting aya number
    - `to_aya` (optional): Ending aya number
- `GET /translations/{translation_id}` - Get all 6236 verses from a translation
- `GET /translations/download/{translation_id}/{filetype}` - Download translation file
  - File types: `json`, `csv`, `sqlite`, `xml`, `xlsx`

### Example Requests

```bash
# Get all available translations
curl http://localhost:8000/api/translations/

# Get specific verse (Surah 1, Ayah 1 in English)
curl http://localhost:8000/api/translations/english_sahih/1/1

# Get all verses from Surah Al-Fatiha
curl http://localhost:8000/api/translations/english_sahih/1

# Get verse range (Surah 2, Ayah 1-5)
curl "http://localhost:8000/api/translations/english_sahih/2?from_aya=1&to_aya=5"

# Download translation as JSON
curl http://localhost:8000/api/translations/download/english_sahih/json
```

## Project Structure

```
alqurandb_api/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── quran.py         # Quran info endpoints
│   │   │   ├── surah.py         # Surah endpoints
│   │   │   ├── ayah.py          # Ayah endpoints with translations
│   │   │   └── translations.py  # Translation endpoints
│   │   └── __init__.py
│   └── core/
│       └── config.py
├── main.py
├── requirements.txt
└── .env
```

## Available Translations

The API currently supports the following translations:

**English:**
- Sahih International (`sahih`)
- Yusuf Ali (`yusufali`)
- Pickthall (`pickthall`)
- Dr. Mustafa Khattab (`khattab`)

**Urdu:**
- Maududi (`maududi`)
- Muhammad Junagarhi (`junagarhi`)
- Fateh Muhammad Jalandhry (`jalandhry`)
