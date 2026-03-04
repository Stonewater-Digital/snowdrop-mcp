"""
muni_taxable_equivalent — Computes taxable-equivalent yields for tax-exempt municipal bonds incorporating AMT exposure, state deductibility, and the 3

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fixed_income_analytics/muni_taxable_equivalent.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "muni_taxable_equivalent",
    "tier": "premium",
    "description": "Computes taxable-equivalent yields for tax-exempt municipal bonds incorporating AMT exposure, state deductibility, and the 3.8% Medicare net investment income surtax. (Premium — subscribe at https://snowdrop.ai)",
}


def muni_taxable_equivalent(tax_exempt_yield: float, federal_rate: float, state_rate: float, is_amt_subject: bool, amt_rate: float, medicare_surtax: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("muni_taxable_equivalent")
