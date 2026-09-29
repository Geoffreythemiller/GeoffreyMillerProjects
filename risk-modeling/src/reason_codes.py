"""Explainability catalog for hybrid rule-and-token credit decisions.

Each reason code maps to a human-readable explanation suitable for analyst
review logs. Codes are synthetic and do not mirror any production system.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True, slots=True)
class ReasonDetail:
    """Single factor contributing to an applicant decision."""

    code: str
    label: str
    impact: str
    points: int


REASON_CATALOG: Final[dict[str, tuple[str, str]]] = {
    "FP_HIGH": (
        "Elevated failed payment events",
        "Three or more failed payments in the lookback window increase default risk.",
    ),
    "NSF_PATTERN": (
        "Repeated insufficient-funds activity",
        "Multiple NSF events suggest cash-flow stress.",
    ),
    "MERCHANT_RISK": (
        "High-risk merchant exposure",
        "Several transactions matched generic high-risk merchant patterns.",
    ),
    "CASH_HEAVY": (
        "Cash-heavy outflows",
        "A large share of outflows are cash-like, reducing payment traceability.",
    ),
    "NEGATIVE_CASHFLOW": (
        "Outflows exceed inflows",
        "Average monthly outflows meet or exceed inflows with limited buffer.",
    ),
    "LOW_RECURRING_INCOME": (
        "Weak recurring income signal",
        "No stable recurring inflow flag was observed in the summary window.",
    ),
    "VOLATILE_INCOME": (
        "Volatile income pattern",
        "Income volatility index exceeds the review threshold.",
    ),
    "RECENT_OVERDRAFT": (
        "Recent overdraft activity",
        "Overdraft occurred within the recent monitoring window.",
    ),
    "TOKEN_PAYROLL_STABLE": (
        "Stable payroll tokens",
        "Transaction narrative includes payroll stability indicators.",
    ),
    "TOKEN_DIRECT_DEPOSIT": (
        "Direct deposit tokens",
        "Narrative tokens indicate recurring direct deposit inflows.",
    ),
    "TOKEN_RENT_PAYMENT": (
        "Rent payment tokens",
        "Regular rent-like payments suggest stable housing obligations.",
    ),
    "TOKEN_UTILITIES_RECURRING": (
        "Recurring utility tokens",
        "Utility-style recurring debits support household stability.",
    ),
    "TOKEN_SAVINGS_TRANSFER": (
        "Savings transfer tokens",
        "Transfers toward savings suggest positive financial behavior.",
    ),
    "TOKEN_GAMBLING_LIKE": (
        "Gambling-like merchant tokens",
        "Narrative tokens suggest gambling-like spend patterns.",
    ),
    "TOKEN_CRYPTO_EXCHANGE": (
        "Crypto exchange tokens",
        "Narrative tokens reference crypto exchange activity.",
    ),
    "TOKEN_P2P_HEAVY": (
        "Peer-to-peer transfer tokens",
        "Narrative tokens suggest heavy P2P money movement.",
    ),
    "TOKEN_SUBSCRIPTION_STACK": (
        "Subscription stack tokens",
        "Multiple subscription-like tokens increase fixed obligations.",
    ),
    "TOKEN_EMPLOYMENT_GAP": (
        "Employment gap tokens",
        "Narrative tokens reference employment or income gaps.",
    ),
}

TOKEN_WEIGHTS: Final[dict[str, int]] = {
    "payroll_stable": 8,
    "direct_deposit": 5,
    "utilities_recurring": 3,
    "gambling_like": -12,
    "crypto_exchange": -8,
    "p2p_heavy": -6,
    "subscription_stack": -4,
    "employment_gap": -10,
    "rent_payment": 4,
    "savings_transfer": 3,
}


def reason_from_rule(code: str, points: int) -> ReasonDetail:
    """Build a reason row from a rule flag code."""
    label, impact = REASON_CATALOG[code]
    return ReasonDetail(code=code, label=label, impact=impact, points=points)


def reason_from_token(token: str, points: int) -> ReasonDetail:
    """Build a reason row from a narrative token hit."""
    catalog_key = f"TOKEN_{token.upper()}"
    if catalog_key in REASON_CATALOG:
        label, impact = REASON_CATALOG[catalog_key]
    else:
        label = f"Token: {token.replace('_', ' ')}"
        impact = "Narrative token contributed to the composite token score."
    return ReasonDetail(code=catalog_key, label=label, impact=impact, points=points)
