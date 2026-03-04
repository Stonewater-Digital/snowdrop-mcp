"""
moic_calculator — Computes MOIC (Multiple on Invested Capital) as total value (realized + unrealized) divided by invested capital

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/moic_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "moic_calculator",
    "tier": "premium",
    "description": "Computes MOIC (Multiple on Invested Capital) as total value (realized + unrealized) divided by invested capital. Also returns gain/loss in dollar terms. (Premium — subscribe at https://snowdrop.ai)",
}


def moic_calculator(invested_capital: float, realized_value: float = 0.0, unrealized_value: float = 0.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("moic_calculator")
