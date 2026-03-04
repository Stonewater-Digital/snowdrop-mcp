"""
dpi_calculator — Calculates DPI (Distributions to Paid-In) = cumulative_distributions / paid_in_capital

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/dpi_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "dpi_calculator",
    "tier": "premium",
    "description": "Calculates DPI (Distributions to Paid-In) = cumulative_distributions / paid_in_capital. DPI is the realized component of fund performance — cash actually returned to LPs. (Premium — subscribe at https://snowdrop.ai)",
}


def dpi_calculator(cumulative_distributions: float, paid_in_capital: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("dpi_calculator")
