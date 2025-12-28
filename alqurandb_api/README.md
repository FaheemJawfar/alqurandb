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

### Base URL: `/api/v1`

#### Quran
- `GET /quran/` - Get general Quran information

#### Surahs
- `GET /surah/` - Get list of all Surahs
- `GET /surah/{surah_number}` - Get specific Surah details

#### Ayahs
- `GET /ayah/{surah_number}/{ayah_number}` - Get specific Ayah
  - Query parameters:
    - `translation` (optional): Translation ID (e.g., `sahih`, `yusufali`, `pickthall`)

#### Translations
- `GET /translations/` - Get list of all available translations
- `GET /translations/{language_code}` - Get translations for a specific language (e.g., `en`, `ur`)

### Example Requests

```bash
# Get general Quran info
curl http://localhost:8000/api/v1/quran/

# Get a specific Ayah
curl http://localhost:8000/api/v1/ayah/1/1

# Get Ayah with Sahih International translation
curl "http://localhost:8000/api/v1/ayah/1/1?translation=sahih"

# Get all available translations
curl http://localhost:8000/api/v1/translations/

# Get English translations only
curl http://localhost:8000/api/v1/translations/en
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
