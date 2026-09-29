#!/usr/bin/env python3
"""
Generate a synthetic origination cohort CSV for FPD analytics demos.

Author: Geoffrey Miller
Data is entirely fictional — not representative of any employer portfolio.
"""

from __future__ import annotations

import argparse
import csv
import random
from datetime import date
from pathlib import Path


def _month_labels(start: date, count: int) -> list[str]:
    months: list[str] = []
    year, month = start.year, start.month
    for _ in range(count):
        months.append(f"{year:04d}-{month:02d}")
        month += 1
        if month > 12:
            month = 1
            year += 1
    return months


def _illustrative_fpd_probability(month_index: int, tier: str, rng: random.Random) -> float:
    """Seasonal + tier skew — illustrative only, not a production model."""
    base = 0.06 + 0.025 * ((month_index % 12) / 11.0)
    if tier == "near_prime":
        base -= 0.02
    elif tier == "subprime":
        base += 0.035
    jitter = rng.uniform(-0.008, 0.008)
    return max(0.01, min(0.22, base + jitter))


def generate_cohort(
    *,
    seed: int,
    months: int,
    loans_per_month: int,
    start: date,
) -> list[dict[str, object]]:
    rng = random.Random(seed)
    labels = _month_labels(start, months)
    tiers = ("near_prime", "standard", "subprime")
    tier_weights = (0.25, 0.55, 0.20)
    rows: list[dict[str, object]] = []
    loan_seq = 1
    for idx, orig_month in enumerate(labels):
        volume = loans_per_month + rng.randint(-12, 18)
        for _ in range(max(40, volume)):
            tier = rng.choices(tiers, weights=tier_weights, k=1)[0]
            balance = round(rng.uniform(800, 18_500) * (1.15 if tier == "subprime" else 1.0), 2)
            term = rng.choice([12, 18, 24, 36])
            p_fpd = _illustrative_fpd_probability(idx, tier, rng)
            fpd_flag = 1 if rng.random() < p_fpd else 0
            rows.append(
                {
                    "loan_id": f"SYN-{loan_seq:06d}",
                    "origination_month": orig_month,
                    "fpd_flag": fpd_flag,
                    "balance_usd": balance,
                    "term_months": term,
                    "product_tier": tier,
                    "state_code": rng.choice(["CA", "TX", "FL", "NY", "IL", "WA", "GA", "OH"]),
                }
            )
            loan_seq += 1
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "loan_id",
        "origination_month",
        "fpd_flag",
        "balance_usd",
        "term_months",
        "product_tier",
        "state_code",
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic origination cohort CSV.")
    parser.add_argument(
        "--output",
        type=Path,
        default=_repo_root() / "data" / "synthetic_origination_cohort.csv",
        help="Output CSV path (default: data/synthetic_origination_cohort.csv)",
    )
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for reproducibility")
    parser.add_argument("--months", type=int, default=24, help="Number of origination months")
    parser.add_argument(
        "--loans-per-month",
        type=int,
        default=120,
        dest="loans_per_month",
        help="Target loans per month before jitter",
    )
    parser.add_argument(
        "--start",
        type=str,
        default="2023-01",
        help="First origination month (YYYY-MM)",
    )
    args = parser.parse_args()
    year_s, month_s = args.start.split("-", maxsplit=1)
    start = date(int(year_s), int(month_s), 1)
    rows = generate_cohort(
        seed=args.seed,
        months=args.months,
        loans_per_month=args.loans_per_month,
        start=start,
    )
    write_csv(args.output, rows)
    print(f"Wrote {len(rows)} synthetic loans to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
