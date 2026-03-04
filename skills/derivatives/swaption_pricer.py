"""
swaption_pricer — Prices payer or receiver swaptions via Black's model and returns Greeks

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/derivatives/swaption_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "swaption_pricer",
    "tier": "premium",
    "description": "Prices payer or receiver swaptions via Black's model and returns Greeks. (Premium — subscribe at https://snowdrop.ai)",
}


def swaption_pricer(notional: float, option_type: str, strike_rate_pct: float, forward_swap_rate_pct: float, volatility_pct: float, time_to_expiry_years: float, swap_tenor_years: float, discount_rate_pct: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("swaption_pricer")
