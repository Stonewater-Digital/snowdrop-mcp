"""
oas_calculator — Calibrates a lognormal Black-Derman-Toy short-rate lattice to the supplied zero curve and derives the option-adjusted spread (OAS) required to reconcile the lattice price with the observed market price

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fixed_income_analytics/oas_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "oas_calculator",
    "tier": "premium",
    "description": "Calibrates a lognormal Black-Derman-Toy short-rate lattice to the supplied zero curve and derives the option-adjusted spread (OAS) required to reconcile the lattice price with the observed market price. (Premium — subscribe at https://snowdrop.ai)",
}


def oas_calculator(cashflows: List[Dict[str, float]], zero_curve: List[Dict[str, float]], market_price: float, volatility: float, call_schedule: List[Dict[str, float]] | None = None) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("oas_calculator")
