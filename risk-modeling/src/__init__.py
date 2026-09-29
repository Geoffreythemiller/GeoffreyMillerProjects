"""Synthetic lending risk decision engine (portfolio demonstration)."""

from src.reason_codes import ReasonDetail
from src.score import ApplicantFeatures, DecisionOutcome, score_applicant

__all__ = [
    "ApplicantFeatures",
    "DecisionOutcome",
    "ReasonDetail",
    "score_applicant",
]

__version__ = "0.1.0"
