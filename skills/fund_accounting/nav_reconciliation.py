"""
nav_reconciliation — Calculates fund Net Asset Value per share and reconciles against prior NAV, flagging variance

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/nav_reconciliation.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "nav_reconciliation",
    "tier": "premium",
    "description": "Calculates fund Net Asset Value per share and reconciles against prior NAV, flagging variance. (Premium — subscribe at https://snowdrop.ai)",
}


def nav_reconciliation(assets: list[dict[str, Any]], liabilities: float, shares_outstanding: float, prior_nav_per_share: float | None = None) -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("nav_reconciliation")
