#!/usr/bin/env python3
"""
Test script to verify database initialization
"""
import logging
from pathlib import Path
from app.core.database_init import ensure_database_exists

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    print("\n" + "="*80)
    print("  Testing Database Initialization")
    print("="*80 + "\n")

    # Run the initialization
    success = ensure_database_exists()

    print("\n" + "="*80)
    if success:
        print("  ✓ Database initialization successful!")
    else:
        print("  ✗ Database initialization failed!")
    print("="*80 + "\n")

    # Check if database file exists
    data_dir = Path(__file__).parent / 'data'
    db_path = data_dir / 'quran_translations.db'

    if db_path.exists():
        size_mb = db_path.stat().st_size / (1024 * 1024)
        print(f"Database file: {db_path}")
        print(f"Database size: {size_mb:.2f} MB\n")
    else:
        print(f"Database file not found at: {db_path}\n")

if __name__ == '__main__':
    main()
