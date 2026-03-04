"""
cds_index_basis — Measures the difference between traded CDS index spread and the weighted intrinsic spread and derives implied correlation using variance decomposition

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/cds_index_basis.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "cds_index_basis",
    "tier": "premium",
    "description": "Measures the difference between traded CDS index spread and the weighted intrinsic spread and derives implied correlation using variance decomposition. (Premium — subscribe at https://snowdrop.ai)",
}


def cds_index_basis(index_spread_bps: float, constituent_spreads_bps: List[float], weights: List[float], tenor_years: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("cds_index_basis")
