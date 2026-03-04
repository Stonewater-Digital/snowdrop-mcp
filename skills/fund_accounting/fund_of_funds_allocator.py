"""
fund_of_funds_allocator — Creates a heuristic allocation maximizing expected return under diversification rules

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/fund_of_funds_allocator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "fund_of_funds_allocator",
    "tier": "premium",
    "description": "Creates a heuristic allocation maximizing expected return under diversification rules. (Premium — subscribe at https://snowdrop.ai)",
}


def fund_of_funds_allocator(fof_capital: float, underlying_funds: list[dict[str, Any]], constraints: dict[str, Any]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("fund_of_funds_allocator")
