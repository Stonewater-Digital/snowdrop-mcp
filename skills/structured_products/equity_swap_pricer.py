"""
equity_swap_pricer — Discounts realized equity leg returns against fixed rate leg to compute PV, DV01, and carry

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/equity_swap_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "equity_swap_pricer",
    "tier": "premium",
    "description": "Discounts realized equity leg returns against fixed rate leg to compute PV, DV01, and carry. (Premium — subscribe at https://snowdrop.ai)",
}


def equity_swap_pricer(notional: float, equity_returns: List[float], fixed_rate: float, reset_year_fractions: List[float], discount_rate: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("equity_swap_pricer")
