"""
credit_default_swap_pricer — Prices a CDS using flat hazard and discount rates, returning par spread and PVs

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/derivatives/credit_default_swap_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "credit_default_swap_pricer",
    "tier": "premium",
    "description": "Prices a CDS using flat hazard and discount rates, returning par spread and PVs. (Premium — subscribe at https://snowdrop.ai)",
}


def credit_default_swap_pricer(notional: float, hazard_rate_pct: float, recovery_rate_pct: float = 40.0, risk_free_rate_pct: float = 0.0, maturity_years: float = 5.0, existing_spread_bps: float | None = None) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("credit_default_swap_pricer")
