"""
callable_bond_oas — Builds a Black-Derman-Toy short-rate lattice calibrated to the input curve and solves for the OAS that matches market price, then reports duration and convexity

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/callable_bond_oas.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "callable_bond_oas",
    "tier": "premium",
    "description": "Builds a Black-Derman-Toy short-rate lattice calibrated to the input curve and solves for the OAS that matches market price, then reports duration and convexity. (Premium — subscribe at https://snowdrop.ai)",
}


def callable_bond_oas(market_price: float, coupon_rate: float, maturity_years: int, yield_curve: List[float], volatility: float, call_schedule: List[Dict[str, float]]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("callable_bond_oas")
