"""
cdo_tranche_pricer — Prices a CDO tranche using the Li (2000) Gaussian copula and Vasicek LHP model to deliver expected loss, spread, and delta analytics

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/cdo_tranche_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "cdo_tranche_pricer",
    "tier": "premium",
    "description": "Prices a CDO tranche using the Li (2000) Gaussian copula and Vasicek LHP model to deliver expected loss, spread, and delta analytics. (Premium — subscribe at https://snowdrop.ai)",
}


def cdo_tranche_pricer(attachment_point: float, detachment_point: float, default_probability: float, recovery_rate: float, asset_correlation: float, num_grid: int = 61) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("cdo_tranche_pricer")
