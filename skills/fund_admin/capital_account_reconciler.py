"""
capital_account_reconciler — Rolls forward an LP capital account from beginning balance with all activity: contributions, distributions, realized gains/losses, unrealized gains/losses, and fees

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/capital_account_reconciler.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "capital_account_reconciler",
    "tier": "premium",
    "description": "Rolls forward an LP capital account from beginning balance with all activity: contributions, distributions, realized gains/losses, unrealized gains/losses, and fees. (Premium — subscribe at https://snowdrop.ai)",
}


def capital_account_reconciler(beginning_balance: float, contributions: float = 0.0, distributions: float = 0.0, realized_gains: float = 0.0, unrealized_gains: float = 0.0, fees: float = 0.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("capital_account_reconciler")
