#!/usr/bin/env python3
"""Batch resize images in a folder."""

import os
import argparse
from pathlib import Path

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False


def resize_images(path, max_width=None, max_height=None, output=None, quality=85, recursive=False):
    if not HAS_PILLOW:
        print("❌ Pillow not installed. Run: pip install Pillow")
        return

    path = Path(path).resolve()
    if not path.is_dir():
        print(f"❌ Error: '{path}' is not a valid directory.")
        return

    if output:
        output_dir = Path(output).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = path / "resized"

    extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}
    glob_pattern = "**/*" if recursive else "*"
    resized = 0

    for f in path.glob(glob_pattern):
        if f.suffix.lower() not in extensions:
            continue

        try:
            img = Image.open(f)
            original_size = img.size

            if max_width or max_height:
                ratio_w = max_width / img.width if max_width else 1
                ratio_h = max_height / img.height if max_height else 1
                ratio = min(ratio_w, ratio_h, 1)  # Don't upscale
                new_size = (int(img.width * ratio), int(img.height * ratio))

                if new_size != img.size:
                    img = img.resize(new_size, Image.LANCZOS)

            rel_path = f.relative_to(path)
            output_path = output_dir / rel_path
            output_path.parent.mkdir(parents=True, exist_ok=True)

            if output_path.suffix.lower() in (".jpg", ".jpeg"):
                img.save(output_path, quality=quality, optimize=True)
            else:
                img.save(output_path)

            resized += 1
            print(f"  ✓ {f.name} ({original_size[0]}x{original_size[1]} → {img.width}x{img.height})")

        except Exception as e:
            print(f"  ⚠ {f.name}: {e}")

    if resized == 0:
        print("📂 No images found.")
    else:
        print(f"\n✅ Resized {resized} image(s) → {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch resize images.")
    parser.add_argument("path", nargs="?", default=".", help="Folder with images (default: current)")
    parser.add_argument("--max-width", "-w", type=int, help="Maximum width in pixels")
    parser.add_argument("--max-height", "-h", type=int, help="Maximum height in pixels")
    parser.add_argument("--output", "-o", help="Output folder (default: ./resized)")
    parser.add_argument("--quality", "-q", type=int, default=85, help="JPEG quality 1-100 (default: 85)")
    parser.add_argument("--recursive", "-r", action="store_true", help="Include subfolders")
    args = parser.parse_args()

    if not args.max_width and not args.max_height:
        parser.error("At least one of --max-width or --max-height is required.")

    resize_images(args.path, args.max_width, args.max_height, args.output, args.quality, args.recursive)
