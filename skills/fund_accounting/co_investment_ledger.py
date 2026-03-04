"""
co_investment_ledger — Constructs a co-investment ledger for a private equity fund, showing main fund capital alongside co-investor capital for each deal

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/co_investment_ledger.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "co_investment_ledger",
    "tier": "premium",
    "description": "Constructs a co-investment ledger for a private equity fund, showing main fund capital alongside co-investor capital for each deal. Calculates total combined exposure per deal, percentage ownership split, and aggregate exposure totals across the portfolio. (Premium — subscribe at https://snowdrop.ai)",
}


def co_investment_ledger() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("co_investment_ledger")
