"""
carried_interest_calculator — Computes GP carried interest after returning LP capital and preferred return

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/carried_interest_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "carried_interest_calculator",
    "tier": "premium",
    "description": "Computes GP carried interest after returning LP capital and preferred return. Supports optional full GP catch-up tranche before profit split. Uses European-style (whole-fund) waterfall logic. (Premium — subscribe at https://snowdrop.ai)",
}


def carried_interest_calculator(total_distributions: float, capital_contributed: float, hurdle_rate_pct: float, carry_pct: float, catch_up: bool = True, years: float = 1.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("carried_interest_calculator")
