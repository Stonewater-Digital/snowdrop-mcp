"""
cln_pricer — Discounts CLN coupons and principal with expected loss per Hull (2006) to estimate fair price and incremental spread

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/cln_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "cln_pricer",
    "tier": "premium",
    "description": "Discounts CLN coupons and principal with expected loss per Hull (2006) to estimate fair price and incremental spread. (Premium — subscribe at https://snowdrop.ai)",
}


def cln_pricer(notional: float, coupon_rate: float, maturity_years: float, reference_default_probability: float, recovery_rate: float, risk_free_rate: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("cln_pricer")
