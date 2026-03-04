"""
bond_futures_ctd — Evaluates conversion-factor adjusted invoice price, carry, and implied repo rate to identify the CTD bond per CME Treasury delivery rules

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fixed_income_analytics/bond_futures_ctd.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "bond_futures_ctd",
    "tier": "premium",
    "description": "Evaluates conversion-factor adjusted invoice price, carry, and implied repo rate to identify the CTD bond per CME Treasury delivery rules. (Premium — subscribe at https://snowdrop.ai)",
}


def bond_futures_ctd(bonds: List[Dict[str, Any]], futures_price: float, repo_rate: float, days_to_delivery: int) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("bond_futures_ctd")
