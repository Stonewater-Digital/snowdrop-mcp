"""
pe_valuation_dcf — Performs DCF valuation of a private equity investment using projected cash flows, terminal value, and discount rate

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/pe_valuation_dcf.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "pe_valuation_dcf",
    "tier": "premium",
    "description": "Performs DCF valuation of a private equity investment using projected cash flows, terminal value, and discount rate. (Premium — subscribe at https://snowdrop.ai)",
}


def pe_valuation_dcf(projected_cashflows: list[float], discount_rate: float, terminal_growth: float, net_debt: float = 0.0, total_invested: float = 0.0) -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("pe_valuation_dcf")
