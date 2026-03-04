"""
inflation_linker_pricer — Values Treasury Inflation-Protected Securities (TIPS) by discounting real cash flows, and derives breakeven inflation relative to nominal Treasuries with monthly seasonality adjustments

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fixed_income_analytics/inflation_linker_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "inflation_linker_pricer",
    "tier": "premium",
    "description": "Values Treasury Inflation-Protected Securities (TIPS) by discounting real cash flows, and derives breakeven inflation relative to nominal Treasuries with monthly seasonality adjustments. (Premium — subscribe at https://snowdrop.ai)",
}


def inflation_linker_pricer(principal: float, coupon_rate: float, maturity_years: float, real_yield_curve: List[Dict[str, float]], nominal_yield_curve: List[Dict[str, float]], seasonality_adjustments: List[float] | None = None, cpi_ratio: float = 1.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("inflation_linker_pricer")
