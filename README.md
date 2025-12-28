# AlQuranDB

A comprehensive resource center for Quranic data, translations, and downloadable resources. AlQuranDB provides easy access to the Holy Quran through a modern web interface and RESTful API.

## Overview

AlQuranDB serves as a central hub for:
- **Downloadable Resources**: Quranic text and translations in multiple formats (JSON, XML, CSV, TXT)
- **Translation Access**: Multiple translations in various languages via API
- **Developer Tools**: RESTful API for integrating Quranic data into applications
- **Web Interface**: Browse and study the Quran online

## Project Structure

This monorepo contains two main components:

### 1. AlQuranDB API (`alqurandb_api/`)
FastAPI backend providing RESTful API endpoints for Quranic data and translations.

**Tech Stack:**
- FastAPI
- Python 3.12
- Pydantic
- Uvicorn

**Features:**
- RESTful API for Quran data
- Multiple translation support (English, Urdu, and more)
- Surah and Ayah endpoints with translation queries
- CORS support for frontend integration
- Auto-generated API documentation (Swagger/ReDoc)

### 2. AlQuranDB Site (`alqurandb_site/`)
Next.js frontend serving as the resource center interface.

**Tech Stack:**
- Next.js 16
- React 19
- TypeScript
- Tailwind CSS

**Features:**
- Resource download center
- API documentation page
- Translation browser
- Surah and Ayah viewer
- Responsive design with dark mode
- Clean, modern UI

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- npm or yarn

### Running the API

```bash
cd alqurandb_api
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

API will be available at `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Running the Site

```bash
cd alqurandb_site
npm install
cp .env.example .env.local
npm run dev
```

Site will be available at `http://localhost:3000`

## API Endpoints

### Base URL: `http://localhost:8000/api/v1`

- `GET /quran/` - Get general Quran information
- `GET /surah/` - Get all Surahs
- `GET /surah/{surah_number}` - Get specific Surah
- `GET /ayah/{surah_number}/{ayah_number}` - Get specific Ayah with optional translation
  - Query params: `?translation=sahih` (optional)
- `GET /translations/` - Get list of available translations
- `GET /translations/{language_code}` - Get translations for a specific language

### Example API Calls

```bash
# Get Ayah with English translation
curl "http://localhost:8000/api/v1/ayah/1/1?translation=sahih"

# Get available translations
curl "http://localhost:8000/api/v1/translations/"

# Get English translations only
curl "http://localhost:8000/api/v1/translations/en"
```

## Development

### API Development
```bash
cd alqurandb_api
source .venv/bin/activate
uvicorn main:app --reload
```

### Site Development
```bash
cd alqurandb_site
npm run dev
```

## License

See [LICENSE](LICENSE) file for details.
