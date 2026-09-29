#!/usr/bin/env python3
"""
Compute FPD KPI rollups and charts from a synthetic origination cohort CSV.

Author: Geoffrey Miller
Illustrative analytics only — not production underwriting or reporting.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

import matplotlib.pyplot as plt

from analytics.fpd_kpis import aggregate_fpd_by_month, rows_from_dicts


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_cohort(path: Path) -> list:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return rows_from_dicts(reader)


def write_summary_csv(path: Path, summary) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "origination_month",
        "loan_count",
        "total_balance_usd",
        "fpd_count",
        "fpd_rate_pct",
        "avg_balance_usd",
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary:
            writer.writerow(
                {
                    "origination_month": row.origination_month,
                    "loan_count": row.loan_count,
                    "total_balance_usd": row.total_balance_usd,
                    "fpd_count": row.fpd_count,
                    "fpd_rate_pct": row.fpd_rate_pct,
                    "avg_balance_usd": row.avg_balance_usd,
                }
            )


def plot_fpd_rate_by_month(summary, path: Path) -> None:
    months = [r.origination_month for r in summary]
    rates = [r.fpd_rate_pct for r in summary]
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(months, rates, marker="o", color="#c0392b", linewidth=1.8, markersize=4)
    ax.set_title("Synthetic FPD rate by origination month (illustrative)")
    ax.set_xlabel("Origination month")
    ax.set_ylabel("FPD rate (%)")
    ax.grid(True, axis="y", alpha=0.35)
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=120)
    plt.close(fig)


def plot_origination_volume(summary, path: Path) -> None:
    months = [r.origination_month for r in summary]
    counts = [r.loan_count for r in summary]
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.bar(months, counts, color="#2980b9", width=0.72)
    ax.set_title("Synthetic origination volume by month")
    ax.set_xlabel("Origination month")
    ax.set_ylabel("Loan count")
    ax.grid(True, axis="y", alpha=0.35)
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=120)
    plt.close(fig)


def run_analysis(input_csv: Path, output_dir: Path) -> None:
    rows = load_cohort(input_csv)
    summary = aggregate_fpd_by_month(rows)
    write_summary_csv(output_dir / "fpd_kpi_summary.csv", summary)
    plot_fpd_rate_by_month(summary, output_dir / "fpd_rate_by_cohort.png")
    plot_origination_volume(summary, output_dir / "origination_volume_by_month.png")


def main() -> int:
    root = _repo_root()
    parser = argparse.ArgumentParser(description="Analyze synthetic FPD cohort KPIs.")
    parser.add_argument(
        "--input",
        type=Path,
        default=root / "data" / "synthetic_origination_cohort.csv",
        help="Input cohort CSV",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "sample_outputs",
        help="Directory for KPI CSV and PNG charts",
    )
    args = parser.parse_args()
    if not args.input.is_file():
        print(f"Input not found: {args.input}. Run analytics/generate_synthetic_cohort.py first.")
        return 1
    run_analysis(args.input, args.output_dir)
    print(f"Wrote KPI summary and charts under {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
