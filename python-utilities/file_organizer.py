#!/usr/bin/env python3
"""Organize files in a folder by extension into subfolders."""

import os
import shutil
import argparse
from pathlib import Path


EXTENSION_MAP = {
    # Images
    '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images',
    '.gif': 'Images', '.webp': 'Images', '.svg': 'Images',
    '.bmp': 'Images', '.ico': 'Images',
    # Documents
    '.pdf': 'Documents', '.doc': 'Documents', '.docx': 'Documents',
    '.xls': 'Documents', '.xlsx': 'Documents', '.ppt': 'Documents',
    '.pptx': 'Documents', '.odt': 'Documents', '.txt': 'Documents',
    '.md': 'Documents', '.csv': 'Documents',
    # Archives
    '.zip': 'Archives', '.rar': 'Archives', '.7z': 'Archives',
    '.tar': 'Archives', '.gz': 'Archives', '.bz2': 'Archives',
    # Audio
    '.mp3': 'Audio', '.wav': 'Audio', '.flac': 'Audio',
    '.aac': 'Audio', '.ogg': 'Audio', '.m4a': 'Audio',
    # Video
    '.mp4': 'Video', '.mkv': 'Video', '.avi': 'Video',
    '.mov': 'Video', '.webm': 'Video',
    # Code
    '.py': 'Code', '.js': 'Code', '.ts': 'Code', '.html': 'Code',
    '.css': 'Code', '.json': 'Code', '.xml': 'Code', '.yaml': 'Code',
    '.yml': 'Code', '.sh': 'Code', '.bat': 'Code', '.ps1': 'Code',
    '.sql': 'Code', '.rb': 'Code', '.go': 'Code', '.rs': 'Code',
    '.java': 'Code', '.cpp': 'Code', '.c': 'Code', '.h': 'Code',
}


def organize_folder(path, dry_run=False):
    path = Path(path).resolve()
    if not path.is_dir():
        print(f"❌ Error: '{path}' is not a valid directory.")
        return

    files = [f for f in path.iterdir() if f.is_file() and not f.name.startswith('.')]
    organized = 0

    for file in files:
        ext = file.suffix.lower()
        folder_name = EXTENSION_MAP.get(ext, 'Other')
        dest_dir = path / folder_name
        dest_file = dest_dir / file.name

        if dry_run:
            print(f"[DRY RUN] Would move: {file.name} → {folder_name}/")
            organized += 1
            continue

        dest_dir.mkdir(exist_ok=True)

        # Handle name conflicts
        counter = 1
        while dest_file.exists():
            stem = file.stem
            dest_file = dest_dir / f"{stem}_{counter}{ext}"
            counter += 1

        shutil.move(str(file), str(dest_file))
        print(f"  ✓ {file.name} → {folder_name}/")
        organized += 1

    if organized == 0:
        print("📂 No files to organize.")
    else:
        print(f"\n✅ Organized {organized} file(s) in {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files by extension into subfolders.")
    parser.add_argument("path", nargs="?", default=".", help="Folder to organize (default: current)")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Preview without moving files")
    args = parser.parse_args()
    organize_folder(args.path, dry_run=args.dry_run)
