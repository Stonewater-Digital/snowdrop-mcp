"""
credit_spread_decomposer — Breaks a corporate bond option-adjusted spread into expected loss (PD*LGD), liquidity premium, risk premium, and tax component per BIS credit risk methodology

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fixed_income_analytics/credit_spread_decomposer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "credit_spread_decomposer",
    "tier": "premium",
    "description": "Breaks a corporate bond option-adjusted spread into expected loss (PD*LGD), liquidity premium, risk premium, and tax component per BIS credit risk methodology. (Premium — subscribe at https://snowdrop.ai)",
}


def credit_spread_decomposer(spread_bps: float, default_probability: float, recovery_rate: float, liquidity_premium_bps: float, tax_rate: float) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("credit_spread_decomposer")
