#!/usr/bin/env python3
"""Report basic quality indicators for a CSV dataset."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


MISSING_VALUES = {"", "na", "n/a", "null", "none", "."}


def is_missing(value: str | None) -> bool:
    """Return True when a value is empty or a common missing-value marker."""
    return value is None or value.strip().lower() in MISSING_VALUES


def inspect_csv(path: Path, encoding: str = "utf-8-sig") -> dict[str, Any]:
    """Inspect a CSV file and return a serializable quality report."""
    with path.open("r", encoding=encoding, newline="") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames:
            raise ValueError("The CSV file has no header row.")

        columns = [name.strip() for name in reader.fieldnames]
        missing = Counter({name: 0 for name in columns})
        seen: Counter[tuple[str, ...]] = Counter()
        total_rows = 0
        empty_rows = 0

        for raw_row in reader:
            total_rows += 1
            values = tuple((raw_row.get(name) or "").strip() for name in reader.fieldnames)
            seen[values] += 1

            if all(is_missing(value) for value in values):
                empty_rows += 1

            for source_name, output_name in zip(reader.fieldnames, columns):
                if is_missing(raw_row.get(source_name)):
                    missing[output_name] += 1

    duplicate_rows = sum(count - 1 for count in seen.values() if count > 1)
    return {
        "file": str(path),
        "rows": total_rows,
        "columns": len(columns),
        "column_names": columns,
        "duplicate_rows": duplicate_rows,
        "empty_rows": empty_rows,
        "missing_values": dict(missing),
    }


def print_report(report: dict[str, Any]) -> None:
    """Print a readable quality report."""
    print(f"File: {report['file']}")
    print(f"Rows: {report['rows']}")
    print(f"Columns: {report['columns']}")
    print(f"Duplicate rows: {report['duplicate_rows']}")
    print(f"Completely empty rows: {report['empty_rows']}")
    print("Missing values:")
    for column, count in report["missing_values"].items():
        print(f"  {column}: {count}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, help="CSV file to inspect")
    parser.add_argument("--encoding", default="utf-8-sig", help="Input text encoding")
    parser.add_argument("--json", type=Path, dest="json_path", help="Write the report as JSON")
    args = parser.parse_args()

    if not args.csv_file.is_file():
        parser.error(f"File not found: {args.csv_file}")

    try:
        report = inspect_csv(args.csv_file, args.encoding)
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        parser.error(str(error))

    print_report(report)
    if args.json_path:
        args.json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"JSON report written to: {args.json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
