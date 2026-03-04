"""
j_curve_modeler — Simulates fund cash flows, NAV, and J-curve inflection metrics

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/j_curve_modeler.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "j_curve_modeler",
    "tier": "premium",
    "description": "Simulates fund cash flows, NAV, and J-curve inflection metrics. (Premium — subscribe at https://snowdrop.ai)",
}


def j_curve_modeler(fund_size: float, investment_period_years: int, fund_life_years: int, management_fee_pct: float, deployment_pace: list[float], exit_multiples: list[dict[str, Any]], loss_rate_pct: float = 15.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("j_curve_modeler")
