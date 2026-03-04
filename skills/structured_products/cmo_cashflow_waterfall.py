"""
cmo_cashflow_waterfall — Projects mortgage collateral cashflows with PSA prepayments and allocates them through sequential/PAC/TAC tranches to report WALs and yields

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/cmo_cashflow_waterfall.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "cmo_cashflow_waterfall",
    "tier": "premium",
    "description": "Projects mortgage collateral cashflows with PSA prepayments and allocates them through sequential/PAC/TAC tranches to report WALs and yields. (Premium — subscribe at https://snowdrop.ai)",
}


def cmo_cashflow_waterfall(mortgage_pool: Dict[str, Any], psa_speed: float, tranches: List[Dict[str, Any]], servicing_fee: float = 0.0025) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("cmo_cashflow_waterfall")
