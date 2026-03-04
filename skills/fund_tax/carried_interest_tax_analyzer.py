"""
carried_interest_tax_analyzer — Calculates tax liability for carried interest under three-year rule

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/carried_interest_tax_analyzer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "carried_interest_tax_analyzer",
    "tier": "premium",
    "description": "Calculates tax liability for carried interest under three-year rule. (Premium — subscribe at https://snowdrop.ai)",
}


def carried_interest_tax_analyzer(carried_interest: float, holding_period_years: float, capital_gains_rate_pct: float = 20.0, ordinary_rate_pct: float = 37.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("carried_interest_tax_analyzer")
