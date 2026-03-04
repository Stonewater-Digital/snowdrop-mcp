"""
bridge_loan_pricing — Prices a fixed-rate amortizing bridge loan

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/bridge_loan_pricing.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "bridge_loan_pricing",
    "tier": "premium",
    "description": "Prices a fixed-rate amortizing bridge loan. Computes the monthly payment using the standard annuity formula, total interest cost, effective APR (nominal, monthly compounding), and a partial amortization schedule showing the first 3 months and final month. Rates are expressed as annual decimals (e.g. 0.05 = 5%). (Premium — subscribe at https://snowdrop.ai)",
}


def bridge_loan_pricing() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("bridge_loan_pricing")
