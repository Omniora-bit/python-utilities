#!/usr/bin/env python3
"""Simple folder backup with timestamp and compression."""

import os
import argparse
import shutil
import zipfile
from pathlib import Path
from datetime import datetime


def backup_folder(source, destination=None, compress=True, exclude=None):
    source = Path(source).resolve()

    if not source.is_dir():
        print(f"❌ Error: '{source}' is not a valid directory.")
        return

    if destination is None:
        destination = source.parent / f"{source.name}_backup"
    else:
        destination = Path(destination).resolve()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{source.name}_{timestamp}"

    if compress:
        archive_path = destination / f"{backup_name}.zip"
        destination.mkdir(parents=True, exist_ok=True)

        print(f"📦 Creating archive: {archive_path}")

        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in source.rglob("*"):
                # Apply exclude patterns
                if exclude and any(file_path.match(p) for p in exclude):
                    continue
                arcname = str(file_path.relative_to(source))
                zf.write(file_path, arcname)

        size_mb = os.path.getsize(archive_path) / (1024 * 1024)
        print(f"✅ Backup created: {archive_path} ({size_mb:.2f} MB)")
    else:
        backup_dir = destination / backup_name
        print(f"📂 Copying to: {backup_dir}")

        def ignore_patterns(dir, files):
            if exclude:
                return [f for f in files if any(Path(f).match(p) for p in exclude)]
            return []

        shutil.copytree(source, backup_dir, ignore=ignore_patterns, dirs_exist_ok=True)
        print(f"✅ Backup created: {backup_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup a folder with timestamp.")
    parser.add_argument("source", help="Folder to backup")
    parser.add_argument("destination", nargs="?", default=None, help="Backup destination (default: parent folder)")
    parser.add_argument("--no-compress", "-n", action="store_true", help="Copy folder instead of zipping")
    parser.add_argument("--exclude", "-e", nargs="*", default=[], help="Exclude patterns (e.g. '*.tmp' '__pycache__')")
    args = parser.parse_args()
    backup_folder(args.source, args.destination, compress=not args.no_compress, exclude=args.exclude)
