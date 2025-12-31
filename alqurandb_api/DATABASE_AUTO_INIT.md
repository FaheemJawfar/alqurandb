# Database Auto-Initialization

The AlQuranDB API now automatically manages the SQLite database on startup.

## How It Works

The API automatically checks and updates the database on each startup through these steps:

1. **On API Startup**: The lifespan event handler runs `ensure_database_exists()`

2. **Database Check**: The system checks if:
   - Database file exists at `data/quran_translations.db`
   - Metadata has changed (by comparing SHA256 hash)

3. **Auto-Update**: If metadata.json changes are detected:
   - Old database is removed
   - New database is created with updated data
   - New metadata hash is stored in the database

4. **Skip When Current**: If database exists and metadata hasn't changed:
   - Initialization is skipped
   - API starts immediately

## Metadata Hash Tracking

The system tracks changes in `data/metadata.json` by:
- Calculating SHA256 hash of the metadata file
- Storing hash in `metadata_info` table in the database
- Comparing hashes on each startup to detect changes

## Database Schema

The database includes a special table for tracking metadata:

```sql
CREATE TABLE metadata_info (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
)
```

This stores the `metadata_hash` key with the SHA256 hash value.

## Manual Database Creation

You can still manually create the database using:

```bash
cd sources
python3 create_complete_db.py
```

This script now also stores the metadata hash for consistency.

## Logs

Database initialization logs are written to the console with INFO level:

```
2025-12-31 10:00:00 - __main__ - INFO - Starting AlQuranDB API...
2025-12-31 10:00:00 - __main__ - INFO - Checking database status...
2025-12-31 10:00:01 - app.core.database_init - INFO - Database is up to date
2025-12-31 10:00:01 - __main__ - INFO - Database is ready
```

## Configuration

Paths are configured in `app/core/database_init.py`:
- CSV translations: `data/translations/csv/`
- Metadata file: `data/metadata.json`
- Database file: `data/quran_translations.db`

## Error Handling

- If database initialization fails, the API still starts (degraded mode)
- Errors are logged but don't prevent API startup
- You can check logs to diagnose initialization issues

## Testing

Test database initialization manually:

```bash
cd alqurandb_api
python3 test_db_init.py
```

This runs the initialization logic without starting the full API.
