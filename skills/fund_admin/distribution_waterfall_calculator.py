"""
distribution_waterfall_calculator — Runs a full 4-tier distribution waterfall: (1) return of capital, (2) preferred return, (3) GP catch-up, (4) residual profit split

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/distribution_waterfall_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "distribution_waterfall_calculator",
    "tier": "premium",
    "description": "Runs a full 4-tier distribution waterfall: (1) return of capital, (2) preferred return, (3) GP catch-up, (4) residual profit split. Supports both European (whole-fund) and American (deal-by-deal) modes. Uses correct catch-up formula: GP gets 100% until carry% of total profits is met. (Premium — subscribe at https://snowdrop.ai)",
}


def distribution_waterfall_calculator(gross_proceeds: float, capital_contributed: float, preferred_return_pct: float, carry_pct: float, catch_up_pct: float = 100.0, years: float = 1.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("distribution_waterfall_calculator")
