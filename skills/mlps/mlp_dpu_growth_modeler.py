"""
mlp_dpu_growth_modeler — Projects DPU growth considering EBITDA growth, IDRs, and dropdowns

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/mlps/mlp_dpu_growth_modeler.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "mlp_dpu_growth_modeler",
    "tier": "premium",
    "description": "Projects DPU growth considering EBITDA growth, IDRs, and dropdowns. (Premium — subscribe at https://snowdrop.ai)",
}


def mlp_dpu_growth_modeler(current_dpu_annual: float, ebitda: float, ebitda_growth_rate: float, maintenance_capex_pct: float, leverage_target: float, gp_idr_tier: str, organic_growth_capex: float, dropdown_pipeline: list[dict[str, Any]]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("mlp_dpu_growth_modeler")
