"""
preferred_return_calculator — Calculates accrued preferred return on LP capital with configurable compounding frequency

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/preferred_return_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "preferred_return_calculator",
    "tier": "premium",
    "description": "Calculates accrued preferred return on LP capital with configurable compounding frequency. Supports annual, quarterly, monthly, and daily compounding. (Premium — subscribe at https://snowdrop.ai)",
}


def preferred_return_calculator(capital_balance: float, pref_rate_pct: float, period_years: float, compounding: str = 'quarterly') -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("preferred_return_calculator")
