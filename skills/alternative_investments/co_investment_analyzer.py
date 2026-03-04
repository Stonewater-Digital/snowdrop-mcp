"""
co_investment_analyzer — Calculates fee savings, carry relief, and net IRR uplift from co-investment structures

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/alternative_investments/co_investment_analyzer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "co_investment_analyzer",
    "tier": "premium",
    "description": "Calculates fee savings, carry relief, and net IRR uplift from co-investment structures. (Premium — subscribe at https://snowdrop.ai)",
}


def co_investment_analyzer(deal_irr: float, management_fee_saved: float, carry_saved: float, co_invest_allocation: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("co_investment_analyzer")
