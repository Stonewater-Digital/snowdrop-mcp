"""
fee_drag_calculator — Estimates net IRR after management fees, performance carry, and other charges

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/fee_drag_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "fee_drag_calculator",
    "tier": "premium",
    "description": "Estimates net IRR after management fees, performance carry, and other charges. Carry drag is only applied to returns above the hurdle rate. (Premium — subscribe at https://snowdrop.ai)",
}


def fee_drag_calculator(gross_irr_pct: float, management_fee_pct: float, carry_pct: float, hurdle_rate_pct: float = 8.0, other_fees_bps: float = 0.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("fee_drag_calculator")
