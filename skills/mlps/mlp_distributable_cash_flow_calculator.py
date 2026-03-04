"""
mlp_distributable_cash_flow_calculator — Derives MLP distributable cash flow from EBITDA, capex, and non-cash adjustments

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/mlps/mlp_distributable_cash_flow_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "mlp_distributable_cash_flow_calculator",
    "tier": "premium",
    "description": "Derives MLP distributable cash flow from EBITDA, capex, and non-cash adjustments. (Premium — subscribe at https://snowdrop.ai)",
}


def mlp_distributable_cash_flow_calculator(ebitda: float, maintenance_capex: float, interest_expense: float, growth_capex: float = 0.0, non_cash_adjustments: float = 0.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("mlp_distributable_cash_flow_calculator")
