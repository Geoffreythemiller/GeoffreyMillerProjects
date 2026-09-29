#!/usr/bin/env python3
"""Build engineered feature CSV from synthetic_applicants via in-memory DuckDB."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import duckdb


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _statements(sql_text: str) -> list[str]:
    """Split SQL file into executable statements (strip comments and preview SELECT)."""
    cleaned_lines: list[str] = []
    for line in sql_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("--"):
            continue
        cleaned_lines.append(line)
    body = "\n".join(cleaned_lines)
    parts = re.split(r";\s*\n", body)
    statements: list[str] = []
    for part in parts:
        stmt = part.strip()
        if not stmt:
            continue
        if stmt.upper().startswith("SELECT * FROM COHORT_SUMMARY"):
            continue
        statements.append(stmt + ";")
    return statements


def build_features(
    input_csv: Path,
    output_csv: Path,
    metrics_sql: Path,
) -> int:
    root = _repo_root()
    if not input_csv.is_file():
        print(f"Input CSV not found: {input_csv}", file=sys.stderr)
        return 1
    if not metrics_sql.is_file():
        print(f"SQL file not found: {metrics_sql}", file=sys.stderr)
        return 1

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    rel_input = os.path.relpath(input_csv.resolve(), root)

    con = duckdb.connect(database=":memory:")
    try:
        original_cwd = os.getcwd()
        os.chdir(root)
        try:
            for stmt in _statements(metrics_sql.read_text(encoding="utf-8")):
                if "read_csv_auto(" in stmt and "raw_applicants" in stmt:
                    stmt = (
                        "CREATE OR REPLACE VIEW raw_applicants AS "
                        f"SELECT * FROM read_csv_auto('{rel_input.replace(chr(92), '/')}', header := true);"
                    )
                con.execute(stmt)
            con.execute(
                f"""
                COPY (
                    SELECT * FROM applicant_features ORDER BY applicant_id
                ) TO '{output_csv.resolve().as_posix()}' (HEADER, DELIMITER ',')
                """
            )
        finally:
            os.chdir(original_cwd)
    finally:
        con.close()

    print(f"Wrote {output_csv} ({output_csv.stat().st_size} bytes)")
    return 0


def main(argv: list[str] | None = None) -> int:
    root = _repo_root()
    parser = argparse.ArgumentParser(description="Export DuckDB feature table to CSV.")
    parser.add_argument(
        "--input",
        type=Path,
        default=root / "data" / "synthetic_applicants.csv",
        help="Synthetic applicant CSV (default: data/synthetic_applicants.csv)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=root / "data" / "engineered_features.csv",
        help="Output CSV path (default: data/engineered_features.csv)",
    )
    parser.add_argument(
        "--sql",
        type=Path,
        default=root / "sql" / "metrics.sql",
        help="Metrics SQL definitions (default: sql/metrics.sql)",
    )
    args = parser.parse_args(argv)
    return build_features(args.input, args.output, args.sql)


if __name__ == "__main__":
    raise SystemExit(main())
