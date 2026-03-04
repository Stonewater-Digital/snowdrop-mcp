"""
debt_covenant_monitor — Evaluates debt covenants against current financial ratios

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/debt_covenant_monitor.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "debt_covenant_monitor",
    "tier": "premium",
    "description": "Evaluates debt covenants against current financial ratios. Supports leverage_ratio (lower is better), interest_coverage (higher is better), and current_ratio (higher is better) covenant types. Returns breach status and distance-to-breach for each covenant. (Premium — subscribe at https://snowdrop.ai)",
}


def debt_covenant_monitor() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("debt_covenant_monitor")
