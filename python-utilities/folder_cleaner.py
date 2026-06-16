#!/usr/bin/env python3
"""Clean empty folders and common temp files."""

import os
import argparse
import shutil
from pathlib import Path


TEMP_PATTERNS = [
    "*.log", "*.tmp", "*.temp", "*.cache",
    "Thumbs.db", ".DS_Store", "desktop.ini",
    "*.bak", "*.swp",
]


def delete_empty_folders(path, dry_run=False):
    removed = 0
    # Process bottom-up so nested empty dirs get cleaned
    for root, dirs, files in os.walk(path, topdown=False):
        root = Path(root)
        if root == Path(path).resolve():
            continue  # Skip the root folder
        try:
            # Check if folder is empty (no files, no remaining subdirs)
            remaining = list(root.iterdir())
            if not remaining:
                if dry_run:
                    print(f"[DRY RUN] Would delete empty folder: {root}")
                else:
                    root.rmdir()
                    print(f"  ✓ Removed empty folder: {root}")
                removed += 1
        except PermissionError:
            pass
    return removed


def delete_temp_files(path, dry_run=False):
    removed = 0
    for pattern in TEMP_PATTERNS:
        for f in Path(path).rglob(pattern):
            if f.is_file():
                if dry_run:
                    print(f"[DRY RUN] Would delete: {f}")
                else:
                    f.unlink()
                    print(f"  ✓ Deleted: {f}")
                removed += 1
    return removed


def clean_folder(path, dry_run=False, temp_only=False, empty_only=False):
    path = Path(path).resolve()
    if not path.is_dir():
        print(f"❌ Error: '{path}' is not a valid directory.")
        return

    print(f"🧹 Cleaning: {path}\n")
    total = 0

    if not temp_only:
        print("--- Empty Folders ---")
        removed = delete_empty_folders(path, dry_run)
        total += removed
        print()

    if not empty_only:
        print("--- Temp Files ---")
        removed = delete_temp_files(path, dry_run)
        total += removed
        print()

    action = "Would clean" if dry_run else "Cleaned"
    print(f"✅ {action} {total} item(s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean empty folders and temp files.")
    parser.add_argument("path", nargs="?", default=".", help="Folder to clean (default: current)")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Preview without deleting")
    parser.add_argument("--temp-only", action="store_true", help="Only delete temp files")
    parser.add_argument("--empty-only", action="store_true", help="Only delete empty folders")
    args = parser.parse_args()
    clean_folder(args.path, args.dry_run, args.temp_only, args.empty_only)
