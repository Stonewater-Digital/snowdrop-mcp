"""
callable_bond_pricer — Values a callable bond on a single-factor Hull-White lattice, providing model price, duration, and call exercise probabilities

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fixed_income_analytics/callable_bond_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "callable_bond_pricer",
    "tier": "premium",
    "description": "Values a callable bond on a single-factor Hull-White lattice, providing model price, duration, and call exercise probabilities. (Premium — subscribe at https://snowdrop.ai)",
}


def callable_bond_pricer(face_value: float, coupon_rate: float, maturity_years: float, frequency: int, zero_curve: List[Dict[str, float]], mean_reversion: float, volatility: float, call_schedule: List[Dict[str, float]] | None = None) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("callable_bond_pricer")
