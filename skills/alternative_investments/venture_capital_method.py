"""
venture_capital_method — Discounts exit value by target IRR, layers dilution, and solves for pre/post-money valuations per the VC method

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/alternative_investments/venture_capital_method.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "venture_capital_method",
    "tier": "premium",
    "description": "Discounts exit value by target IRR, layers dilution, and solves for pre/post-money valuations per the VC method. (Premium — subscribe at https://snowdrop.ai)",
}


def venture_capital_method(expected_exit_value: float, exit_year: int, target_irr: float, dilution_per_round: List[float], investment_amount: float = 1.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("venture_capital_method")
