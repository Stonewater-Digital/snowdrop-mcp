"""
mlp_distribution_analyzer — Calculates DCF coverage, leverage, and GP take for MLP distributions

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/mlps/mlp_distribution_analyzer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "mlp_distribution_analyzer",
    "tier": "premium",
    "description": "Calculates DCF coverage, leverage, and GP take for MLP distributions. (Premium — subscribe at https://snowdrop.ai)",
}


def mlp_distribution_analyzer(distributable_cash_flow: float, total_distributions: float, gp_idr_distributions: float, lp_distributions: float, maintenance_capex: float, growth_capex: float, total_debt: float, ebitda: float, units_outstanding: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("mlp_distribution_analyzer")
