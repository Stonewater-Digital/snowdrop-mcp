"""
mlp_k1_estimator — Estimates income, return of capital, and UBTI exposure for MLP units

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/mlps/mlp_k1_estimator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "mlp_k1_estimator",
    "tier": "premium",
    "description": "Estimates income, return of capital, and UBTI exposure for MLP units. (Premium — subscribe at https://snowdrop.ai)",
}


def mlp_k1_estimator(dpu: float, units_held: int, acquisition_cost_per_unit: float, depreciation_allocation_pct: float, ubti_pct: float, section_199a_eligible_pct: float, state_income_states: list[str]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("mlp_k1_estimator")
