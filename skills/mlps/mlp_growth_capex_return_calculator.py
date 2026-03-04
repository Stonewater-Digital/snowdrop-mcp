"""
mlp_growth_capex_return_calculator — Evaluates projected EBITDA gains versus growth capex to estimate cash-on-cash returns

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/mlps/mlp_growth_capex_return_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "mlp_growth_capex_return_calculator",
    "tier": "premium",
    "description": "Evaluates projected EBITDA gains versus growth capex to estimate cash-on-cash returns. (Premium — subscribe at https://snowdrop.ai)",
}


def mlp_growth_capex_return_calculator(project_cost: float, projected_ebitda: float, ramp_years: float = 1.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("mlp_growth_capex_return_calculator")
