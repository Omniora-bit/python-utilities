#!/usr/bin/env python3
"""Batch rename files with pattern substitution."""

import os
import re
import argparse
from pathlib import Path


def batch_rename(path, pattern, replacement, dry_run=False, recursive=False):
    path = Path(path).resolve()

    if not path.is_dir():
        print(f"❌ Error: '{path}' is not a valid directory.")
        return

    glob_pattern = "**/*" if recursive else "*"
    files = [f for f in path.glob(glob_pattern) if f.is_file()]
    renamed = 0

    for file in files:
        old_name = file.name
        new_name = re.sub(pattern, replacement, old_name)

        if new_name == old_name:
            continue

        new_path = file.parent / new_name

        if dry_run:
            print(f"[DRY RUN] {old_name} → {new_name}")
            renamed += 1
            continue

        counter = 1
        final_path = new_path
        while final_path.exists():
            stem = new_path.stem
            ext = new_path.suffix
            final_path = new_path.parent / f"{stem}_{counter}{ext}"
            counter += 1

        file.rename(final_path)
        print(f"  ✓ {old_name} → {final_path.name}")
        renamed += 1

    if renamed == 0:
        print("📂 No files matched the pattern.")
    else:
        print(f"\n✅ Renamed {renamed} file(s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch rename files with regex.")
    parser.add_argument("pattern", help="Regex pattern to match")
    parser.add_argument("replacement", help="Replacement string (use \\1, \\2 for groups)")
    parser.add_argument("path", nargs="?", default=".", help="Target folder (default: current)")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Preview without renaming")
    parser.add_argument("--recursive", "-r", action="store_true", help="Include subfolders")
    args = parser.parse_args()
    batch_rename(args.path, args.pattern, args.replacement, args.dry_run, args.recursive)
