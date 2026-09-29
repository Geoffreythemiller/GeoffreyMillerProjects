"""Command-line entry point for batch scoring synthetic applicants."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from src.score import ApplicantFeatures, DecisionOutcome, score_applicant


def _parse_tokens(raw: str) -> tuple[str, ...]:
    if not raw or not raw.strip():
        return ()
    return tuple(part.strip() for part in raw.split("|") if part.strip())


def row_to_features(row: dict[str, str]) -> ApplicantFeatures:
    """Map a CSV row to typed applicant features."""
    return ApplicantFeatures(
        applicant_id=row["applicant_id"].strip(),
        avg_monthly_inflow_usd=float(row["avg_monthly_inflow_usd"]),
        avg_monthly_outflow_usd=float(row["avg_monthly_outflow_usd"]),
        failed_payment_count_90d=int(row["failed_payment_count_90d"]),
        nsf_event_count_90d=int(row["nsf_event_count_90d"]),
        unique_merchant_count_30d=int(row["unique_merchant_count_30d"]),
        high_risk_merchant_hits_90d=int(row["high_risk_merchant_hits_90d"]),
        cash_withdrawal_ratio=float(row["cash_withdrawal_ratio"]),
        income_volatility_index=float(row["income_volatility_index"]),
        days_since_last_overdraft=int(row["days_since_last_overdraft"]),
        recurring_income_flag=int(row["recurring_income_flag"]),
        narrative_tokens=_parse_tokens(row.get("narrative_tokens", "")),
    )


def load_applicants(csv_path: Path) -> list[ApplicantFeatures]:
    """Read applicant feature rows from a UTF-8 CSV file."""
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [row_to_features(row) for row in reader]


def format_outcome(outcome: DecisionOutcome) -> str:
    """Render one decision block for terminal output."""
    lines = [
        f"{outcome.applicant_id}\t{outcome.decision}\tscore={outcome.score}",
    ]
    if outcome.rule_hits:
        lines.append(f"  rules: {', '.join(outcome.rule_hits)}")
    for reason in outcome.reasons:
        sign = "+" if reason.points >= 0 else ""
        lines.append(
            f"  - [{reason.code}] {reason.label} ({sign}{reason.points}): {reason.impact}"
        )
    return "\n".join(lines)


def outcome_to_row(outcome: DecisionOutcome) -> dict[str, str]:
    """Flatten a decision for CSV export."""
    rule_hits = "|".join(outcome.rule_hits)
    reason_codes = "|".join(r.code for r in outcome.reasons)
    return {
        "applicant_id": outcome.applicant_id,
        "risk_score": str(outcome.score),
        "decision": outcome.decision,
        "rule_hits": rule_hits,
        "reason_codes": reason_codes,
    }


def write_decisions_csv(outcomes: list[DecisionOutcome], output_path: Path) -> None:
    """Write batch scoring results to UTF-8 CSV."""
    fieldnames = ["applicant_id", "risk_score", "decision", "rule_hits", "reason_codes"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for outcome in outcomes:
            writer.writerow(outcome_to_row(outcome))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Score synthetic applicants with rules, tokens, and reason codes.",
    )
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        default=Path("data/synthetic_applicants.csv"),
        help="Path to applicant feature CSV (default: data/synthetic_applicants.csv)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Optional path to write decisions CSV (applicant_id, risk_score, decision, ...)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.input.is_file():
        print(f"Input file not found: {args.input}", file=sys.stderr)
        return 1

    applicants = load_applicants(args.input)
    if not applicants:
        print("No applicant rows found.", file=sys.stderr)
        return 1

    outcomes = [score_applicant(features) for features in applicants]

    print(f"Scored {len(applicants)} synthetic applicant(s) from {args.input}\n")
    for outcome in outcomes:
        print(format_outcome(outcome))
        print()

    if args.output is not None:
        write_decisions_csv(outcomes, args.output)
        print(f"Wrote decisions CSV: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
