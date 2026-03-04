"""
mortgage_pool_analyzer — Calculates single-month mortality, conditional prepayment rate (CPR), conditional default rate (CDR), and loss severity for mortgage pools

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fixed_income_analytics/mortgage_pool_analyzer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "mortgage_pool_analyzer",
    "tier": "premium",
    "description": "Calculates single-month mortality, conditional prepayment rate (CPR), conditional default rate (CDR), and loss severity for mortgage pools. (Premium — subscribe at https://snowdrop.ai)",
}


def mortgage_pool_analyzer(pool_balance: float, scheduled_principal: float, prepayments: List[float], defaults: List[float], severities: List[float]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("mortgage_pool_analyzer")
