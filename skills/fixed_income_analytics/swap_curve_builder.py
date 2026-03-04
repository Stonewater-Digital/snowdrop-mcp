"""
swap_curve_builder — Bootstraps an overnight-indexed swap (OIS) discount curve and overlays vanilla IRS par rates with turn-of-year adjustments per ISDA methodology

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fixed_income_analytics/swap_curve_builder.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "swap_curve_builder",
    "tier": "premium",
    "description": "Bootstraps an overnight-indexed swap (OIS) discount curve and overlays vanilla IRS par rates with turn-of-year adjustments per ISDA methodology. (Premium — subscribe at https://snowdrop.ai)",
}


def swap_curve_builder(ois_quotes: List[Dict[str, float]], irs_quotes: List[Dict[str, float]], turn_adjustment_bps: float = 0.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("swap_curve_builder")
