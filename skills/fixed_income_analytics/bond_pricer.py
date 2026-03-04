"""
bond_pricer — Prices a fixed-rate bond using standard street-convention accrued interest under 30/360, ACT/ACT, or ACT/360 day-count with support for semi-annual or quarterly coupons

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fixed_income_analytics/bond_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "bond_pricer",
    "tier": "premium",
    "description": "Prices a fixed-rate bond using standard street-convention accrued interest under 30/360, ACT/ACT, or ACT/360 day-count with support for semi-annual or quarterly coupons. (Premium — subscribe at https://snowdrop.ai)",
}


def bond_pricer(face_value: float, coupon_rate: float, yield_to_maturity: float, settlement_date: str, maturity_date: str, frequency: int, day_count_convention: str) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("bond_pricer")
