"""
gp_co_invest_calculator — Calculates GP and LP capital allocations plus promote economics for co-investment deals

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/gp_co_invest_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "gp_co_invest_calculator",
    "tier": "premium",
    "description": "Calculates GP and LP capital allocations plus promote economics for co-investment deals. Returns GP commitment, LP commitment, and the promote pool available for the GP. (Premium — subscribe at https://snowdrop.ai)",
}


def gp_co_invest_calculator(deal_equity: float, gp_commit_pct: float, promote_pct: float = 20.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("gp_co_invest_calculator")
