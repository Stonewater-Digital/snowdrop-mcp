"""
tail_risk_hedging_cost — Aggregates put option strikes/premiums to estimate hedge cost, drawdown coverage, and breakeven levels

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/alternative_investments/tail_risk_hedging_cost.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "tail_risk_hedging_cost",
    "tier": "premium",
    "description": "Aggregates put option strikes/premiums to estimate hedge cost, drawdown coverage, and breakeven levels. (Premium — subscribe at https://snowdrop.ai)",
}


def tail_risk_hedging_cost(portfolio_value: float, put_strikes: List[float], put_premiums: List[float], target_protection_level: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("tail_risk_hedging_cost")
