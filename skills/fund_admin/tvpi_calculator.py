"""
tvpi_calculator — Calculates TVPI (Total Value to Paid-In) = (DPI + RVPI)

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/tvpi_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "tvpi_calculator",
    "tier": "premium",
    "description": "Calculates TVPI (Total Value to Paid-In) = (DPI + RVPI). TVPI = (cumulative_distributions + residual_value) / paid_in_capital. Also reports DPI, RVPI, and NAV share. (Premium — subscribe at https://snowdrop.ai)",
}


def tvpi_calculator(residual_value: float, cumulative_distributions: float, paid_in_capital: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("tvpi_calculator")
