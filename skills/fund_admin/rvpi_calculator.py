"""
rvpi_calculator — Calculates RVPI (Residual Value to Paid-In) = residual_value / paid_in_capital

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/rvpi_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "rvpi_calculator",
    "tier": "premium",
    "description": "Calculates RVPI (Residual Value to Paid-In) = residual_value / paid_in_capital. RVPI is the unrealized component of fund value — what the portfolio is still worth. (Premium — subscribe at https://snowdrop.ai)",
}


def rvpi_calculator(residual_value: float, paid_in_capital: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("rvpi_calculator")
