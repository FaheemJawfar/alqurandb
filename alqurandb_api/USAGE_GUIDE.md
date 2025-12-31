# Database Auto-Initialization Usage Guide

## Quick Start

The database now initializes automatically when you start the API:

```bash
cd alqurandb_api
uvicorn main:app --reload
```

That's it! No manual database creation needed.

## What Happens on Startup

1. API checks if database exists
2. If exists, compares metadata.json hash
3. If changed or missing, recreates database
4. If unchanged, skips initialization
5. API starts and is ready to use

## Checking Database Status

### Option 1: Check Database Status Script
```bash
cd alqurandb_api
python3 check_db_status.py
```

Output example:
```
================================================================================
  Database Status Check
================================================================================

✓ Database exists: /path/to/data/quran_translations.db
  Size: 45.23 MB

✓ Metadata file exists: /path/to/data/metadata.json

Database Contents:
  Translations: 150
  Verses: 93750

Metadata Hash Status:
  Current hash:  a1b2c3d4e5f6g7h8...
  Stored hash:   a1b2c3d4e5f6g7h8...

  ✓ Status: UP TO DATE
  Database matches current metadata
```

### Option 2: Test Initialization
```bash
cd alqurandb_api
python3 test_db_init.py
```

This runs the initialization logic without starting the API.

## Forcing Database Rebuild

If you want to force a database rebuild:

### Method 1: Delete the database file
```bash
rm alqurandb_api/data/quran_translations.db
uvicorn main:app --reload  # Will recreate on startup
```

### Method 2: Use the manual script
```bash
cd sources
python3 create_complete_db.py
```

### Method 3: Modify metadata.json
Any change to metadata.json will trigger rebuild on next startup.

## Typical Workflows

### Development Workflow
```bash
# 1. Make changes to metadata.json or add new translations
# 2. Start the API
uvicorn main:app --reload

# Database automatically updates if needed
# No manual steps required!
```

### Production Deployment
```bash
# 1. Deploy new code with updated metadata.json
# 2. Start the API
uvicorn main:app --host 0.0.0.0 --port 8000

# Database automatically initializes on first run
# Updates automatically when metadata changes
```

### Check Before Deployment
```bash
# Verify database status before deploying
python3 alqurandb_api/check_db_status.py

# Test initialization works
python3 alqurandb_api/test_db_init.py
```

## Monitoring Logs

Watch for these log messages on API startup:

### Database is up to date:
```
INFO - Starting AlQuranDB API...
INFO - Checking database status...
INFO - Database is up to date
INFO - Database is current at /path/to/quran_translations.db
INFO - Database is ready
```

### Database needs update:
```
INFO - Starting AlQuranDB API...
INFO - Checking database status...
INFO - Metadata has changed - database needs update
INFO - Creating/updating complete translations database...
INFO - Creating database with 150 translations...
INFO - Database created successfully!
INFO - Stored metadata hash: a1b2c3d4e5f6g7h8...
INFO - Database is ready
```

### First time creation:
```
INFO - Starting AlQuranDB API...
INFO - Checking database status...
INFO - Database does not exist - needs creation
INFO - Creating/updating complete translations database...
INFO - Creating database with 150 translations...
INFO - Database created successfully!
INFO - Database is ready
```

## Troubleshooting

### Database initialization fails

Check logs for errors:
```bash
uvicorn main:app --log-level debug
```

Common issues:
- Missing CSV files in `data/translations/csv/`
- Missing or corrupt `metadata.json`
- Permission issues writing to `data/` directory

### Database exists but seems outdated

Force a rebuild:
```bash
rm alqurandb_api/data/quran_translations.db
python3 alqurandb_api/test_db_init.py
```

### Want to verify metadata hash

```bash
python3 alqurandb_api/check_db_status.py
```

This shows both current and stored hashes.

## Best Practices

1. **Let it auto-initialize**: Don't manually create the database unless needed
2. **Check status before major changes**: Use `check_db_status.py` before modifying metadata
3. **Monitor startup logs**: Watch for initialization messages
4. **Test locally first**: Use `test_db_init.py` before deploying
5. **Backup before updates**: Keep backups when updating metadata.json in production

## Advanced Usage

### Custom database location

Edit `app/core/database_init.py` to change paths:
```python
data_dir = app_dir.parent / 'data'
csv_dir = data_dir / 'translations' / 'csv'
metadata_file = data_dir / 'metadata.json'
db_path = data_dir / 'quran_translations.db'
```

### Add more metadata tracking

The `metadata_info` table can store additional tracking data:
```python
cursor.execute("""
    INSERT OR REPLACE INTO metadata_info (key, value)
    VALUES ('last_updated', ?)
""", (datetime.now().isoformat(),))
```
