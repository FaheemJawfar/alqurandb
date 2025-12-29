#!/usr/bin/env python3
"""
Generate all translation formats from CSV base files

This script runs all format converters to generate CSV, XML, Excel (XLSX),
and SQLite database files from the base CSV translations.

CSV files are the source of truth - all other formats are derived from them.
"""
import subprocess
import sys
from pathlib import Path


def run_converter(script_path, format_name):
    """Run a format converter script"""
    print(f"\n{'='*80}")
    print(f"  Generating {format_name} files from CSV...")
    print(f"{'='*80}\n")

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=False
        )
        print(f"\n✅ {format_name} generation completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {format_name} generation failed with error code {e.returncode}")
        return False


def main():
    """Generate all translation formats"""

    script_dir = Path(__file__).parent
    converters_dir = script_dir / 'converters'

    # Define converters in order of execution
    converters = [
        (converters_dir / 'csv_to_json.py', 'JSON'),
        (converters_dir / 'csv_to_xml.py', 'XML'),
        (converters_dir / 'csv_to_excel.py', 'Excel (XLSX)'),
        (converters_dir / 'csv_to_sqlite.py', 'SQLite'),
    ]

    print("\n" + "="*80)
    print("  AlQuranDB - Generate All Translation Formats")
    print("="*80)
    print("\nThis will generate all translation files from the base CSV format:")
    print("  • CSV files (spreadsheets, data analysis)")
    print("  • XML files (religious software, enterprise systems)")
    print("  • Excel files (business users, researchers)")
    print("  • SQLite databases (mobile apps, desktop applications)")
    print("\nSource: alqurandb_api/data/translations/csv/")
    print("="*80)

    # Track results
    results = {}

    # Run each converter
    for script_path, format_name in converters:
        if not script_path.exists():
            print(f"\n⚠️  Skipping {format_name}: converter not found at {script_path}")
            results[format_name] = False
            continue

        success = run_converter(script_path, format_name)
        results[format_name] = success

    # Print summary
    print("\n" + "="*80)
    print("  Summary")
    print("="*80)

    successful = sum(1 for success in results.values() if success)
    failed = sum(1 for success in results.values() if not success)

    for format_name, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {format_name}")

    print(f"\n  Total: {successful} successful, {failed} failed")
    print("="*80 + "\n")

    # Return exit code
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
