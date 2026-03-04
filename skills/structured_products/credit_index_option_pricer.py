"""
credit_index_option_pricer — Applies Black's formula on CDS index spreads with PV01 scaling to deliver payer/receiver option values and Greeks

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/structured_products/credit_index_option_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "credit_index_option_pricer",
    "tier": "premium",
    "description": "Applies Black's formula on CDS index spreads with PV01 scaling to deliver payer/receiver option values and Greeks. (Premium — subscribe at https://snowdrop.ai)",
}


def credit_index_option_pricer(notional: float, index_spread_bps: float, strike_spread_bps: float, volatility: float, expiry_years: float, recovery_rate: float, option_type: str) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("credit_index_option_pricer")
