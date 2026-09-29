"""Tests for synthetic FPD KPI helpers."""

from __future__ import annotations

from analytics.fpd_kpis import CohortRow, aggregate_fpd_by_month, fpd_rate


def test_fpd_rate_zero_when_no_loans() -> None:
    assert fpd_rate(0, 0) == 0.0


def test_fpd_rate_percentage() -> None:
    assert fpd_rate(1, 4) == 25.0


def test_aggregate_by_month_sorts_and_rollups() -> None:
    rows = [
        CohortRow("L1", "2024-02", 1, 1000.0, 12, "standard"),
        CohortRow("L2", "2024-01", 0, 2000.0, 24, "standard"),
        CohortRow("L3", "2024-01", 1, 3000.0, 24, "near_prime"),
    ]
    summary = aggregate_fpd_by_month(rows)
    assert [s.origination_month for s in summary] == ["2024-01", "2024-02"]
    jan = summary[0]
    assert jan.loan_count == 2
    assert jan.fpd_count == 1
    assert jan.fpd_rate_pct == 50.0
    assert jan.total_balance_usd == 5000.0
    assert jan.avg_balance_usd == 2500.0
