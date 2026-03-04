"""
cdo_squared_correlation — Aggregates inner CDO tranche correlations to infer compound/base metrics and reports spread sensitivity across the outer tranche

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/cdo_squared_correlation.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "cdo_squared_correlation",
    "tier": "premium",
    "description": "Aggregates inner CDO tranche correlations to infer compound/base metrics and reports spread sensitivity across the outer tranche. (Premium — subscribe at https://snowdrop.ai)",
}


def cdo_squared_correlation(inner_tranches: List[Dict[str, float]], outer_tranche: Dict[str, float], correlation_matrix: List[List[float]] | None = None) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("cdo_squared_correlation")
