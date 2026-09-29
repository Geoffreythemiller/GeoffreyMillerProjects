"""Hybrid applicant score: deterministic rules plus weighted narrative tokens."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from src.reason_codes import (
    TOKEN_WEIGHTS,
    ReasonDetail,
    reason_from_rule,
    reason_from_token,
)

DecisionLabel = Literal["Approve", "Review", "Decline"]

# Synthetic portfolio thresholds — not calibrated to any lender population.
APPROVE_MIN_SCORE = 70
REVIEW_MIN_SCORE = 40
BASE_SCORE = 55


@dataclass(frozen=True, slots=True)
class ApplicantFeatures:
    """Transaction-summary features for one synthetic applicant."""

    applicant_id: str
    avg_monthly_inflow_usd: float
    avg_monthly_outflow_usd: float
    failed_payment_count_90d: int
    nsf_event_count_90d: int
    unique_merchant_count_30d: int
    high_risk_merchant_hits_90d: int
    cash_withdrawal_ratio: float
    income_volatility_index: float
    days_since_last_overdraft: int
    recurring_income_flag: int
    narrative_tokens: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DecisionOutcome:
    """Full scoring result with explainability payload."""

    applicant_id: str
    score: int
    decision: DecisionLabel
    rule_hits: tuple[str, ...]
    reasons: tuple[ReasonDetail, ...] = field(default_factory=tuple)


def _clamp_score(raw: float) -> int:
    return max(0, min(100, int(round(raw))))


def _decision_from_score(score: int) -> DecisionLabel:
    if score >= APPROVE_MIN_SCORE:
        return "Approve"
    if score >= REVIEW_MIN_SCORE:
        return "Review"
    return "Decline"


def evaluate_rules(features: ApplicantFeatures) -> tuple[list[str], int, list]:
    """Apply deterministic rule flags; return codes, point delta, and reasons."""
    codes: list[str] = []
    delta = 0
    reasons: list = []

    if features.failed_payment_count_90d >= 3:
        codes.append("FP_HIGH")
        delta -= 18
        reasons.append(reason_from_rule("FP_HIGH", -18))

    if features.nsf_event_count_90d >= 2:
        codes.append("NSF_PATTERN")
        delta -= 14
        reasons.append(reason_from_rule("NSF_PATTERN", -14))

    if features.high_risk_merchant_hits_90d >= 4:
        codes.append("MERCHANT_RISK")
        delta -= 12
        reasons.append(reason_from_rule("MERCHANT_RISK", -12))

    if features.cash_withdrawal_ratio > 0.5:
        codes.append("CASH_HEAVY")
        delta -= 8
        reasons.append(reason_from_rule("CASH_HEAVY", -8))

    inflow = features.avg_monthly_inflow_usd
    outflow = features.avg_monthly_outflow_usd
    if outflow > 0 and inflow < outflow * 1.1:
        codes.append("NEGATIVE_CASHFLOW")
        delta -= 10
        reasons.append(reason_from_rule("NEGATIVE_CASHFLOW", -10))

    if features.recurring_income_flag == 0:
        codes.append("LOW_RECURRING_INCOME")
        delta -= 6
        reasons.append(reason_from_rule("LOW_RECURRING_INCOME", -6))

    if features.income_volatility_index > 0.65:
        codes.append("VOLATILE_INCOME")
        delta -= 7
        reasons.append(reason_from_rule("VOLATILE_INCOME", -7))

    if features.days_since_last_overdraft < 45:
        codes.append("RECENT_OVERDRAFT")
        delta -= 9
        reasons.append(reason_from_rule("RECENT_OVERDRAFT", -9))

    return codes, delta, reasons


def evaluate_tokens(tokens: tuple[str, ...]) -> tuple[int, list]:
    """Sum weighted token contributions and emit one reason per matched token."""
    delta = 0
    reasons: list = []
    for token in tokens:
        normalized = token.strip().lower()
        if not normalized:
            continue
        weight = TOKEN_WEIGHTS.get(normalized, 0)
        if weight == 0:
            continue
        delta += weight
        reasons.append(reason_from_token(normalized, weight))
    return delta, reasons


def score_applicant(features: ApplicantFeatures) -> DecisionOutcome:
    """Compute hybrid score and map to Approve / Review / Decline."""
    rule_codes, rule_delta, rule_reasons = evaluate_rules(features)
    token_delta, token_reasons = evaluate_tokens(features.narrative_tokens)

    raw_score = BASE_SCORE + rule_delta + token_delta
    score = _clamp_score(raw_score)
    decision = _decision_from_score(score)

    # Hard guardrails: severe rule stacks cap at Review or Decline regardless of tokens.
    severe = {"FP_HIGH", "NSF_PATTERN", "MERCHANT_RISK"}
    if len(severe.intersection(rule_codes)) >= 2 and decision == "Approve":
        decision = "Review"
    if "FP_HIGH" in rule_codes and "NEGATIVE_CASHFLOW" in rule_codes:
        decision = "Decline"
        score = min(score, REVIEW_MIN_SCORE - 1)

    all_reasons = tuple(rule_reasons + token_reasons)
    return DecisionOutcome(
        applicant_id=features.applicant_id,
        score=score,
        decision=decision,
        rule_hits=tuple(rule_codes),
        reasons=all_reasons,
    )
