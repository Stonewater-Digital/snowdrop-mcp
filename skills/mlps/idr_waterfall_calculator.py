"""
idr_waterfall_calculator — Allocates distributable cash through IDR tiers for MLPs

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/mlps/idr_waterfall_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "idr_waterfall_calculator",
    "tier": "premium",
    "description": "Allocates distributable cash through IDR tiers for MLPs. (Premium — subscribe at https://snowdrop.ai)",
}


def idr_waterfall_calculator(total_distributable_cash: float, lp_units: int, gp_units: int, idr_tiers: list[dict[str, Any]], minimum_quarterly_distribution: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("idr_waterfall_calculator")
