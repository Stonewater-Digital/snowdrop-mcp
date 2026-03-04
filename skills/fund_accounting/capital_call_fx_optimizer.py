"""
capital_call_fx_optimizer — Allocates multi-currency balances to satisfy a capital call with minimal FX drag

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/capital_call_fx_optimizer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "capital_call_fx_optimizer",
    "tier": "premium",
    "description": "Allocates multi-currency balances to satisfy a capital call with minimal FX drag. (Premium — subscribe at https://snowdrop.ai)",
}


def capital_call_fx_optimizer(fund_currency: str, capital_call_amount: float, currency_positions: list[dict[str, Any]], notify_thunder: bool = False) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("capital_call_fx_optimizer")
