"""
management_fee_calculator — Computes management fees with investment period step-down: before step_down_year, fees are based on committed capital; after step_down_year, fees step down to invested/cost basis

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/management_fee_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "management_fee_calculator",
    "tier": "premium",
    "description": "Computes management fees with investment period step-down: before step_down_year, fees are based on committed capital; after step_down_year, fees step down to invested/cost basis. (Premium — subscribe at https://snowdrop.ai)",
}


def management_fee_calculator(commitment_base: float, invested_capital: float, fee_rate_pct: float, fund_age_years: float, step_down_year: float = 5.0, post_step_down_rate_pct: float | None = None) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("management_fee_calculator")
