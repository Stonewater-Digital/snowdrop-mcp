"""
structured_deposit_pricer — Combines the discount cost of principal protection with the price of an embedded equity option to price structured deposits

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/structured_deposit_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "structured_deposit_pricer",
    "tier": "premium",
    "description": "Combines the discount cost of principal protection with the price of an embedded equity option to price structured deposits. (Premium — subscribe at https://snowdrop.ai)",
}


def structured_deposit_pricer(notional: float, zero_coupon_price: float, option_cost: float, participation_rate: float, cap_rate: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("structured_deposit_pricer")
