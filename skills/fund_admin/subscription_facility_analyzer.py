"""
subscription_facility_analyzer — Evaluates subscription credit facility utilization, annualized interest cost, unused fee drag, and NAV impact

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/subscription_facility_analyzer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "subscription_facility_analyzer",
    "tier": "premium",
    "description": "Evaluates subscription credit facility utilization, annualized interest cost, unused fee drag, and NAV impact. Subscription lines are backed by LP commitments. (Premium — subscribe at https://snowdrop.ai)",
}


def subscription_facility_analyzer(facility_limit: float, drawn_amount: float, spread_bps: float, nav: float, base_rate_pct: float = 0.0, unused_fee_bps: float = 50.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("subscription_facility_analyzer")
