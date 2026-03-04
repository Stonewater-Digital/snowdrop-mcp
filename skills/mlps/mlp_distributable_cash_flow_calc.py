"""
mlp_distributable_cash_flow_calc — Calculates Distributable Cash Flow (DCF) and coverage ratios for Master Limited Partnerships

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/mlps/mlp_distributable_cash_flow_calc.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "mlp_distributable_cash_flow_calc",
    "tier": "premium",
    "description": "Calculates Distributable Cash Flow (DCF) and coverage ratios for Master Limited Partnerships. (Premium — subscribe at https://snowdrop.ai)",
}


def mlp_distributable_cash_flow_calc(net_income: float, dda: float, maintenance_capex: float, distributions_paid: float) -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("mlp_distributable_cash_flow_calc")
