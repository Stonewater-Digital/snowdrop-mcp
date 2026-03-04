"""
synthetic_cdo_pricer — Implements the Gaussian copula with Vasicek closed form to deliver expected loss and spreads for each tranche

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/synthetic_cdo_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "synthetic_cdo_pricer",
    "tier": "premium",
    "description": "Implements the Gaussian copula with Vasicek closed form to deliver expected loss and spreads for each tranche. (Premium — subscribe at https://snowdrop.ai)",
}


def synthetic_cdo_pricer(portfolio_notional: float, num_names: int, default_probability: float, recovery_rate: float, asset_correlation: float, tranches: List[Dict[str, Any]]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("synthetic_cdo_pricer")
