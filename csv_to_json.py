#!/usr/bin/env python3
"""Convert CSV files to JSON."""

import csv
import json
import argparse
from pathlib import Path


def csv_to_json(input_file, output_file=None, pretty=True, indent=2):
    input_path = Path(input_file).resolve()

    if not input_path.exists():
        print(f"❌ Error: '{input_file}' not found.")
        return

    if output_file is None:
        output_file = input_path.with_suffix(".json")

    output_path = Path(output_file)

    data = []
    with open(input_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            print("❌ Error: Empty CSV file.")
            return
        for row in reader:
            data.append(row)

    with open(output_path, "w", encoding="utf-8") as f:
        if pretty:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        else:
            json.dump(data, f, ensure_ascii=False)

    print(f"✅ Converted {len(data)} rows")
    print(f"   Input:  {input_path}")
    print(f"   Output: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CSV to JSON.")
    parser.add_argument("input", help="Input CSV file")
    parser.add_argument("output", nargs="?", default=None, help="Output JSON file (default: same name)")
    parser.add_argument("--minify", "-m", action="store_true", help="Output minified JSON (no indentation)")
    args = parser.parse_args()
    csv_to_json(args.input, args.output, pretty=not args.minify)
