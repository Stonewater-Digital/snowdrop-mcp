"""
total_return_swap_analyzer — Breaks down TRS financing costs, received return, and net P&L

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/derivatives/total_return_swap_analyzer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "total_return_swap_analyzer",
    "tier": "premium",
    "description": "Breaks down TRS financing costs, received return, and net P&L. (Premium — subscribe at https://snowdrop.ai)",
}


def total_return_swap_analyzer(notional: float, reference_asset_return_pct: float, financing_spread_bps: float, risk_free_rate_pct: float, holding_period_days: int, dividend_yield_pct: float = 0.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("total_return_swap_analyzer")
