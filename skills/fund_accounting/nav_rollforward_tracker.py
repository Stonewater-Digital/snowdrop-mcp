"""
nav_rollforward_tracker — Bridges opening NAV to closing NAV using period cash flows and valuation changes

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/nav_rollforward_tracker.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "nav_rollforward_tracker",
    "tier": "premium",
    "description": "Bridges opening NAV to closing NAV using period cash flows and valuation changes. (Premium — subscribe at https://snowdrop.ai)",
}


def nav_rollforward_tracker(opening_nav: float, cash_flows: list[dict[str, Any]], valuation_change: float = 0.0, management_fees: float = 0.0, period_label: str | None = None) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("nav_rollforward_tracker")
