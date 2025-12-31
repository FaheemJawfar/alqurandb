#!/usr/bin/env python3
"""
Check database status and metadata hash
"""
import sqlite3
import hashlib
from pathlib import Path


def calculate_metadata_hash(metadata_file):
    """Calculate SHA256 hash of metadata file"""
    sha256_hash = hashlib.sha256()
    with open(metadata_file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def get_stored_hash(db_path):
    """Get stored metadata hash from database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if table exists
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='metadata_info'
        """)

        if not cursor.fetchone():
            conn.close()
            return None

        cursor.execute("SELECT value FROM metadata_info WHERE key = 'metadata_hash'")
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None
    except Exception as e:
        return None


def main():
    data_dir = Path(__file__).parent / 'data'
    db_path = data_dir / 'quran_translations.db'
    metadata_file = data_dir / 'metadata.json'

    print("\n" + "="*80)
    print("  Database Status Check")
    print("="*80 + "\n")

    # Check database existence
    if not db_path.exists():
        print("❌ Database does not exist")
        print(f"   Expected location: {db_path}\n")
        return

    print(f"✓ Database exists: {db_path}")
    size_mb = db_path.stat().st_size / (1024 * 1024)
    print(f"  Size: {size_mb:.2f} MB\n")

    # Check metadata file
    if not metadata_file.exists():
        print(f"❌ Metadata file not found: {metadata_file}\n")
        return

    print(f"✓ Metadata file exists: {metadata_file}\n")

    # Get database info
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM translations')
        translation_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM verses')
        verse_count = cursor.fetchone()[0]

        print("Database Contents:")
        print(f"  Translations: {translation_count}")
        print(f"  Verses: {verse_count}\n")

        conn.close()
    except Exception as e:
        print(f"❌ Error reading database: {e}\n")
        return

    # Check metadata hash
    current_hash = calculate_metadata_hash(metadata_file)
    stored_hash = get_stored_hash(db_path)

    print("Metadata Hash Status:")
    print(f"  Current hash:  {current_hash[:16]}... (full: {current_hash})")

    if stored_hash:
        print(f"  Stored hash:   {stored_hash[:16]}... (full: {stored_hash})")

        if current_hash == stored_hash:
            print("\n  ✓ Status: UP TO DATE")
            print("  Database matches current metadata")
        else:
            print("\n  ⚠ Status: OUT OF DATE")
            print("  Database will be recreated on next API startup")
    else:
        print("  Stored hash:   Not found")
        print("\n  ⚠ Status: NO HASH FOUND")
        print("  Database will be recreated on next API startup")

    print("\n" + "="*80 + "\n")


if __name__ == '__main__':
    main()
