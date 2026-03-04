"""
yield_curve_bootstrapper — Bootstraps spot and forward curves from par coupon instruments consistent with U

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fixed_income_analytics/yield_curve_bootstrapper.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "yield_curve_bootstrapper",
    "tier": "premium",
    "description": "Bootstraps spot and forward curves from par coupon instruments consistent with U.S. Treasury STRIPS methodology. (Premium — subscribe at https://snowdrop.ai)",
}


def yield_curve_bootstrapper(maturities: List[float], par_rates: List[float], coupon_frequency: int = 2) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("yield_curve_bootstrapper")
