"""
mbs_prepayment_model — Generates PSA-based CPR and SMM projections plus collateral amortization and balance run-off stats

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/mbs_prepayment_model.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "mbs_prepayment_model",
    "tier": "premium",
    "description": "Generates PSA-based CPR and SMM projections plus collateral amortization and balance run-off stats. (Premium — subscribe at https://snowdrop.ai)",
}


def mbs_prepayment_model(current_balance: float, weighted_average_coupon: float, weighted_average_maturity_months: int, psa_multiple: float, seasoning_months: int, horizon_months: int | None = None) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("mbs_prepayment_model")
