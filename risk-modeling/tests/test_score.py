"""Unit tests for hybrid rule-and-token scoring."""

from __future__ import annotations

import pytest

from src.score import (
    APPROVE_MIN_SCORE,
    REVIEW_MIN_SCORE,
    ApplicantFeatures,
    score_applicant,
)


def _features(**overrides: object) -> ApplicantFeatures:
    base = dict(
        applicant_id="TEST-000",
        avg_monthly_inflow_usd=5200.0,
        avg_monthly_outflow_usd=4100.0,
        failed_payment_count_90d=0,
        nsf_event_count_90d=0,
        unique_merchant_count_30d=18,
        high_risk_merchant_hits_90d=0,
        cash_withdrawal_ratio=0.12,
        income_volatility_index=0.25,
        days_since_last_overdraft=999,
        recurring_income_flag=1,
        narrative_tokens=("payroll_stable", "direct_deposit", "rent_payment"),
    )
    base.update(overrides)
    return ApplicantFeatures(**base)


def test_strong_applicant_approves_with_positive_tokens() -> None:
    outcome = score_applicant(_features(applicant_id="APP-STRONG"))
    assert outcome.decision == "Approve"
    assert outcome.score >= APPROVE_MIN_SCORE
    assert "FP_HIGH" not in outcome.rule_hits
    assert any(r.code == "TOKEN_PAYROLL_STABLE" for r in outcome.reasons)


def test_failed_payments_and_nsf_trigger_review_or_decline() -> None:
    outcome = score_applicant(
        _features(
            applicant_id="RISK-MID",
            failed_payment_count_90d=3,
            nsf_event_count_90d=2,
            narrative_tokens=(),
        )
    )
    assert outcome.decision in {"Review", "Decline"}
    assert outcome.score < APPROVE_MIN_SCORE
    assert "FP_HIGH" in outcome.rule_hits
    assert "NSF_PATTERN" in outcome.rule_hits


def test_severe_stack_forces_decline_when_cashflow_negative() -> None:
    outcome = score_applicant(
        _features(
            applicant_id="DEC-STACK",
            failed_payment_count_90d=4,
            avg_monthly_inflow_usd=2800.0,
            avg_monthly_outflow_usd=3200.0,
            narrative_tokens=("gambling_like", "employment_gap"),
        )
    )
    assert outcome.decision == "Decline"
    assert outcome.score < REVIEW_MIN_SCORE
    assert "FP_HIGH" in outcome.rule_hits
    assert "NEGATIVE_CASHFLOW" in outcome.rule_hits


def test_gambling_tokens_reduce_score_monotonically() -> None:
    clean = score_applicant(_features(applicant_id="A", narrative_tokens=("payroll_stable",)))
    risky = score_applicant(
        _features(applicant_id="B", narrative_tokens=("payroll_stable", "gambling_like"))
    )
    assert risky.score < clean.score


def test_empty_tokens_still_apply_rules_only() -> None:
    outcome = score_applicant(
        _features(
            applicant_id="RULES-ONLY",
            high_risk_merchant_hits_90d=5,
            narrative_tokens=(),
        )
    )
    assert "MERCHANT_RISK" in outcome.rule_hits
    assert outcome.score < APPROVE_MIN_SCORE
