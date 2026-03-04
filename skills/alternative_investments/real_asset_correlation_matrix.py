"""
real_asset_correlation_matrix — Computes Pearson correlations across provided asset return series and compares tail-period correlations to detect crisis regimes

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/alternative_investments/real_asset_correlation_matrix.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "real_asset_correlation_matrix",
    "tier": "premium",
    "description": "Computes Pearson correlations across provided asset return series and compares tail-period correlations to detect crisis regimes. (Premium — subscribe at https://snowdrop.ai)",
}


def real_asset_correlation_matrix(return_series: Dict[str, List[float]], crisis_threshold: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("real_asset_correlation_matrix")
