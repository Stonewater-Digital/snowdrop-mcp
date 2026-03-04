"""
range_accrual_note — Uses Black-style lognormal assumption for the reference rate to compute expected coupons on a range accrual structured note

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/range_accrual_note.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "range_accrual_note",
    "tier": "premium",
    "description": "Uses Black-style lognormal assumption for the reference rate to compute expected coupons on a range accrual structured note. (Premium — subscribe at https://snowdrop.ai)",
}


def range_accrual_note(forward_rate: float, lower_barrier: float, upper_barrier: float, observation_days: int, volatility: float, notional: float, coupon_spread: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("range_accrual_note")
