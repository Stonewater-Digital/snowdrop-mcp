"""
convertible_bond_pricer — Approximates the Tsiveriotis-Fernandes convertible decomposition into straight bond and embedded call option to deliver price and Greeks

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/convertible_bond_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "convertible_bond_pricer",
    "tier": "premium",
    "description": "Approximates the Tsiveriotis-Fernandes convertible decomposition into straight bond and embedded call option to deliver price and Greeks. (Premium — subscribe at https://snowdrop.ai)",
}


def convertible_bond_pricer(stock_price: float, volatility: float, conversion_ratio: float, coupon_rate: float, maturity_years: float, credit_spread: float, risk_free_rate: float, call_price: float | None = None) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("convertible_bond_pricer")
