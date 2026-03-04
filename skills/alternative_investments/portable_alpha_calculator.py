"""
portable_alpha_calculator — Aggregates returns from alpha and beta sleeves, subtracts hedge cost, and reports contribution along with realized tracking error

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/alternative_investments/portable_alpha_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "portable_alpha_calculator",
    "tier": "premium",
    "description": "Aggregates returns from alpha and beta sleeves, subtracts hedge cost, and reports contribution along with realized tracking error. (Premium — subscribe at https://snowdrop.ai)",
}


def portable_alpha_calculator(alpha_returns: List[float], beta_returns: List[float], hedge_cost: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("portable_alpha_calculator")
