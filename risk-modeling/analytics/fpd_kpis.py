"""Pure helpers for first-payment-default (FPD) cohort KPIs — synthetic data only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class CohortRow:
    """One originated loan in a synthetic cohort export."""

    loan_id: str
    origination_month: str
    fpd_flag: int
    balance_usd: float
    term_months: int
    product_tier: str


@dataclass(frozen=True)
class MonthKpi:
    origination_month: str
    loan_count: int
    total_balance_usd: float
    fpd_count: int
    fpd_rate_pct: float
    avg_balance_usd: float


def fpd_rate(fpd_count: int, loan_count: int) -> float:
    """Return FPD rate as a percentage (0–100), or 0.0 when loan_count is zero."""
    if loan_count <= 0:
        return 0.0
    return 100.0 * fpd_count / loan_count


def aggregate_fpd_by_month(rows: Sequence[CohortRow]) -> list[MonthKpi]:
    """Roll up loan-level rows to origination-month KPIs, sorted by month."""
    buckets: dict[str, list[CohortRow]] = {}
    for row in rows:
        buckets.setdefault(row.origination_month, []).append(row)

    summary: list[MonthKpi] = []
    for month in sorted(buckets.keys()):
        cohort = buckets[month]
        loan_count = len(cohort)
        fpd_count = sum(1 for r in cohort if r.fpd_flag == 1)
        total_balance = sum(r.balance_usd for r in cohort)
        avg_balance = total_balance / loan_count if loan_count else 0.0
        summary.append(
            MonthKpi(
                origination_month=month,
                loan_count=loan_count,
                total_balance_usd=round(total_balance, 2),
                fpd_count=fpd_count,
                fpd_rate_pct=round(fpd_rate(fpd_count, loan_count), 4),
                avg_balance_usd=round(avg_balance, 2),
            )
        )
    return summary


def rows_from_dicts(records: Iterable[Mapping[str, object]]) -> list[CohortRow]:
    """Build CohortRow list from CSV-like dict records."""
    out: list[CohortRow] = []
    for rec in records:
        fpd_raw = rec.get("fpd_flag", 0)
        fpd = int(fpd_raw)  # type: ignore[arg-type]
        out.append(
            CohortRow(
                loan_id=str(rec["loan_id"]),
                origination_month=str(rec["origination_month"]),
                fpd_flag=1 if fpd else 0,
                balance_usd=float(rec["balance_usd"]),  # type: ignore[arg-type]
                term_months=int(rec["term_months"]),  # type: ignore[arg-type]
                product_tier=str(rec.get("product_tier", "standard")),
            )
        )
    return out
