"""
cap_floor_pricer — Prices interest rate caps or floors using Black's model for each caplet/floorlet

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/derivatives/cap_floor_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "cap_floor_pricer",
    "tier": "premium",
    "description": "Prices interest rate caps or floors using Black's model for each caplet/floorlet. (Premium — subscribe at https://snowdrop.ai)",
}


def cap_floor_pricer(notional: float, strike_rate_pct: float, forward_rates: list[float], volatilities: list[float], discount_factors: list[float], payment_dates: list[float], instrument_type: str) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("cap_floor_pricer")
