"""
fund_leverage_analyzer — Calculates fund-level leverage ratios including subscription line leverage, asset-level debt, look-through leverage, and debt-to-equity ratios

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/fund_leverage_analyzer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "fund_leverage_analyzer",
    "tier": "premium",
    "description": "Calculates fund-level leverage ratios including subscription line leverage, asset-level debt, look-through leverage, and debt-to-equity ratios. (Premium — subscribe at https://snowdrop.ai)",
}


def fund_leverage_analyzer(nav: float, subscription_line_debt: float, asset_level_debt: float, gross_asset_value: float | None = None) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("fund_leverage_analyzer")
