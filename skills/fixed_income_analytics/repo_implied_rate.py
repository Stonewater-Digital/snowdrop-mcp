"""
repo_implied_rate — Derives the implied repurchase (repo) rate from the Treasury cash-futures basis, adjusting for coupons and accrued interest

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fixed_income_analytics/repo_implied_rate.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "repo_implied_rate",
    "tier": "premium",
    "description": "Derives the implied repurchase (repo) rate from the Treasury cash-futures basis, adjusting for coupons and accrued interest. (Premium — subscribe at https://snowdrop.ai)",
}


def repo_implied_rate(cash_price: float, futures_price: float, days_to_maturity: int, coupon_rate: float, face_value: float = 100.0, accrued_interest: float = 0.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("repo_implied_rate")
