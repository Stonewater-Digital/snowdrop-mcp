"""
gp_clawback_calculator — Evaluates carry distributions versus whole-fund entitlement and recommends clawback

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/gp_clawback_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "gp_clawback_calculator",
    "tier": "premium",
    "description": "Evaluates carry distributions versus whole-fund entitlement and recommends clawback. (Premium — subscribe at https://snowdrop.ai)",
}


def gp_clawback_calculator(fund_distributions: list[dict[str, Any]], fund_total_contributions: float, preferred_return_pct: float = 8.0, gp_carry_pct: float = 20.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("gp_clawback_calculator")
