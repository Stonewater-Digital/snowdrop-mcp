"""
installment_option_pricer — Binomial tree valuation of installment (pay-as-you-go) options with optimal abandonment before the next premium is due

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/exotic_options/installment_option_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "installment_option_pricer",
    "tier": "premium",
    "description": "Binomial tree valuation of installment (pay-as-you-go) options with optimal abandonment before the next premium is due. (Premium — subscribe at https://snowdrop.ai)",
}


def installment_option_pricer() -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("installment_option_pricer")
