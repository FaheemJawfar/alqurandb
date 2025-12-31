# AlQuranDB - Automatic Database Management

## Overview

The AlQuranDB API features intelligent automatic database management that:
- ✅ Creates the database automatically on first startup
- ✅ Detects changes in metadata.json using SHA256 hashing
- ✅ Auto-updates database when metadata changes
- ✅ Skips initialization when database is current (fast startup)
- ✅ Requires zero manual intervention

## Architecture

### Components

1. **Database Initialization Module** ([app/core/database_init.py](app/core/database_init.py))
   - Core logic for database creation
   - Metadata hash calculation and comparison
   - Change detection and update triggers

2. **API Startup Handler** ([main.py](main.py))
   - Lifespan context manager
   - Calls initialization on startup
   - Logs initialization status

3. **Manual Creation Script** ([../sources/create_complete_db.py](../sources/create_complete_db.py))
   - Standalone database creation
   - Useful for testing or manual builds

4. **Utility Scripts**
   - `check_db_status.py` - Check database and hash status
   - `test_db_init.py` - Test initialization without API

### Database Schema

```sql
-- Translations metadata
CREATE TABLE translations (
    id TEXT PRIMARY KEY,
    language TEXT NOT NULL,
    translator TEXT NOT NULL,
    name_in_language TEXT,
    source TEXT NOT NULL
);

-- Verse texts
CREATE TABLE verses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    translation_id TEXT NOT NULL,
    sura INTEGER NOT NULL,
    aya INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (translation_id) REFERENCES translations(id)
);

-- Metadata tracking (for change detection)
CREATE TABLE metadata_info (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- Indexes for performance
CREATE INDEX idx_translation_id ON verses(translation_id);
CREATE INDEX idx_sura ON verses(sura);
CREATE INDEX idx_sura_aya ON verses(sura, aya);
CREATE INDEX idx_translation_sura ON verses(translation_id, sura);
CREATE INDEX idx_translation_sura_aya ON verses(translation_id, sura, aya);
```

## How It Works

### Initialization Flow

```
┌─────────────────────┐
│   API Startup       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Check DB Exists?   │
└──────────┬──────────┘
           │
           ├─── No ──────────────────────┐
           │                             ▼
           ├─── Yes                  ┌───────────────┐
           │                         │  Create New   │
           ▼                         │   Database    │
┌─────────────────────┐             └───────┬───────┘
│ Calculate Current   │                     │
│  Metadata Hash      │                     │
└──────────┬──────────┘                     │
           │                                │
           ▼                                │
┌─────────────────────┐                     │
│  Get Stored Hash    │                     │
└──────────┬──────────┘                     │
           │                                │
           ├─── Not Found ────┐             │
           │                  │             │
           ▼                  │             │
┌─────────────────────┐       │             │
│  Compare Hashes     │       │             │
└──────────┬──────────┘       │             │
           │                  │             │
           ├─── Different ────┤             │
           │                  │             │
           │                  ▼             │
           │          ┌───────────────┐     │
           │          │ Recreate DB   │     │
           │          └───────┬───────┘     │
           │                  │             │
           │                  ▼             │
           │          ┌───────────────┐     │
           │          │  Store New    │◄────┘
           │          │     Hash      │
           │          └───────┬───────┘
           │                  │
           ├─── Same ─────────┤
           │                  │
           ▼                  ▼
    ┌─────────────────────────┐
    │   Skip Init - Use       │
    │   Existing Database     │
    └────────────┬────────────┘
                 │
                 ▼
         ┌───────────────┐
         │  API Ready    │
         └───────────────┘
```

### Change Detection

The system uses SHA256 hashing for reliable change detection:

1. **Hash Calculation**: Read metadata.json in chunks and compute SHA256
2. **Hash Storage**: Store hash in `metadata_info` table
3. **Hash Comparison**: On startup, compare current vs stored hash
4. **Update Trigger**: If hashes differ, recreate database

## Usage

### Basic Usage

Just start the API:

```bash
cd alqurandb_api
uvicorn main:app --reload
```

The database initializes automatically!

### Check Database Status

```bash
python3 check_db_status.py
```

Example output:
```
================================================================================
  Database Status Check
================================================================================

✓ Database exists: data/quran_translations.db
  Size: 45.23 MB

✓ Metadata file exists: data/metadata.json

Database Contents:
  Translations: 150
  Verses: 93750

Metadata Hash Status:
  Current hash:  a1b2c3d4e5f6g7h8...
  Stored hash:   a1b2c3d4e5f6g7h8...

  ✓ Status: UP TO DATE
  Database matches current metadata
```

### Test Initialization

```bash
python3 test_db_init.py
```

### Force Database Rebuild

```bash
# Delete existing database
rm data/quran_translations.db

# Start API (or run test script)
uvicorn main:app --reload
```

## Configuration

Paths are defined in `app/core/database_init.py`:

```python
data_dir = app_dir.parent / 'data'
csv_dir = data_dir / 'translations' / 'csv'
metadata_file = data_dir / 'metadata.json'
db_path = data_dir / 'quran_translations.db'
```

## Logging

The system logs all initialization steps:

```python
INFO - Starting AlQuranDB API...
INFO - Checking database status...
INFO - Database is up to date
INFO - Database is ready
```

Or when updating:

```python
INFO - Metadata has changed - database needs update
INFO - Creating database with 150 translations...
INFO - Database created successfully!
INFO - Stored metadata hash: a1b2c3d4...
```

## Error Handling

- Database initialization failures don't prevent API startup
- Errors are logged with ERROR level
- API runs in degraded mode if database unavailable
- Check logs for troubleshooting

## Performance

### Initialization Time
- First creation: ~30-60 seconds (150 translations, ~94K verses)
- Hash check: <100ms
- Skip when current: <1 second total startup overhead

### Storage
- Database size: ~40-50 MB (150 translations)
- Indexes included for query optimization
- SQLite VACUUM not run automatically (manual optimization possible)

## Files

- `app/core/database_init.py` - Core initialization logic
- `main.py` - API startup with lifespan handler
- `check_db_status.py` - Database status checker
- `test_db_init.py` - Initialization test script
- `DATABASE_AUTO_INIT.md` - Detailed feature documentation
- `USAGE_GUIDE.md` - User guide with examples
- `README_DATABASE.md` - This file

## API Endpoints

The database is used by these endpoints:

- `GET /api/v1/translations` - List all translations
- `GET /api/v1/translations/{translation_id}` - Get translation metadata
- `GET /api/v1/verses/{translation_id}` - Get verses for translation
- `GET /api/v1/verses/{translation_id}/{sura}` - Get sura verses
- `GET /api/v1/verses/{translation_id}/{sura}/{aya}` - Get specific verse

## Development

### Adding New Translations

1. Add translation metadata to `data/metadata.json`
2. Add CSV file to `data/translations/csv/`
3. Start API - database auto-updates!

### Testing Changes

```bash
# Check current status
python3 check_db_status.py

# Make changes to metadata.json

# Test initialization
python3 test_db_init.py

# Verify new status
python3 check_db_status.py
```

### Debugging

Enable debug logging:

```bash
uvicorn main:app --log-level debug
```

## Production Deployment

### Docker Example

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY alqurandb_api /app
RUN pip install -r requirements.txt

# Database will be created on first startup
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

No special environment variables needed - all paths are relative.

### Health Checks

```bash
curl http://localhost:8000/health
```

Returns: `{"status": "healthy"}`

## Troubleshooting

### Database not updating after metadata change

Check hash status:
```bash
python3 check_db_status.py
```

Force rebuild:
```bash
rm data/quran_translations.db
python3 test_db_init.py
```

### Permission errors

Ensure write access to `data/` directory:
```bash
chmod -R u+w data/
```

### CSV files not found

Verify directory structure:
```bash
ls -la data/translations/csv/
```

Should contain `*.csv` files.

## Future Enhancements

Potential improvements:
- [ ] Incremental updates (update only changed translations)
- [ ] Track CSV file hashes (detect content changes)
- [ ] Database migration system
- [ ] Compression for large databases
- [ ] Health check endpoint with DB status
- [ ] Admin endpoint to trigger manual rebuild

## License

Same as parent project.

## Support

For issues or questions:
- Check logs for error messages
- Review documentation files
- Test with utility scripts
- Open issue on project repository
