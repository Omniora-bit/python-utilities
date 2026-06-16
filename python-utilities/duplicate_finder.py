#!/usr/bin/env python3
"""Find duplicate files in a folder by content hash."""

import os
import hashlib
import argparse
from pathlib import Path
from collections import defaultdict


def hash_file(filepath, chunk_size=65536):
    """Compute SHA256 of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def find_duplicates(path, min_size=1, delete=False, dry_run=False):
    path = Path(path).resolve()
    if not path.is_dir():
        print(f"❌ Error: '{path}' is not a valid directory.")
        return

    print(f"🔍 Scanning {path} for duplicates (min size: {min_size} byte(s))...")

    # Group by size first (fast filter)
    size_map = defaultdict(list)
    total = 0
    for f in path.rglob("*"):
        if f.is_file() and f.stat().st_size >= min_size:
            size_map[f.stat().st_size].append(f)
            total += 1

    print(f"   {total} files scanned, {len(size_map)} unique sizes")

    # Hash files with same size
    hash_map = defaultdict(list)
    for size, files in size_map.items():
        if len(files) < 2:
            continue
        for f in files:
            file_hash = hash_file(f)
            hash_map[file_hash].append(f)

    # Report duplicates
    dupes = {h: flist for h, flist in hash_map.items() if len(flist) > 1}

    if not dupes:
        print("✅ No duplicates found.")
        return

    print(f"\n📋 Found {sum(len(v) for v in dupes)} files in {len(dupes)} duplicate group(s):\n")

    for file_hash, files in dupes.items():
        print(f"  Hash: {file_hash[:16]}...")
        for i, f in enumerate(files):
            label = " [ORIGINAL]" if i == 0 else " [DUPLICATE]"
            print(f"    {i+1}. {f}{label}")
        print()

    if delete:
        total_deleted = 0
        for file_hash, files in dupes.items():
            for f in files[1:]:  # Keep first, delete rest
                if dry_run:
                    print(f"[DRY RUN] Would delete: {f}")
                else:
                    os.remove(f)
                    print(f"  ✗ Deleted: {f}")
                total_deleted += 1
        action = "Would delete" if dry_run else "Deleted"
        print(f"\n✅ {action} {total_deleted} duplicate file(s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find duplicate files by content hash.")
    parser.add_argument("path", nargs="?", default=".", help="Folder to scan (default: current)")
    parser.add_argument("--min-size", type=int, default=1, help="Minimum file size in bytes (default: 1)")
    parser.add_argument("--delete", "-d", action="store_true", help="Delete duplicates (keeps oldest)")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Preview deletions")
    args = parser.parse_args()
    find_duplicates(args.path, args.min_size, args.delete, args.dry_run)
