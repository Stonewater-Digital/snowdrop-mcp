"""
drawdown_analyzer — Computes drawdown metrics from an equity curve or NAV series

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/drawdown_analyzer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "drawdown_analyzer",
    "tier": "premium",
    "description": "Computes drawdown metrics from an equity curve or NAV series. (Premium — subscribe at https://snowdrop.ai)",
}


def drawdown_analyzer(equity_curve: list[float], period_label: str = 'daily') -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("drawdown_analyzer")
