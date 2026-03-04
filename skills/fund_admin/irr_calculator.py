"""
irr_calculator — Computes IRR via Newton-Raphson iteration for periodic cash flows

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/irr_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "irr_calculator",
    "tier": "premium",
    "description": "Computes IRR via Newton-Raphson iteration for periodic cash flows. Requires at least one sign change in the cash flow series. Returns IRR as an annualized percentage. (Premium — subscribe at https://snowdrop.ai)",
}


def irr_calculator(cash_flows: Sequence[float], guess_rate_pct: float = 10.0, max_iterations: int = 1000, tolerance: float = 1e-08) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("irr_calculator")
