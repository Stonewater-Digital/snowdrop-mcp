"""
weekly_pnl_report — Aggregates revenue and expense items into a weekly P&L rollup

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/weekly_pnl_report.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "weekly_pnl_report",
    "tier": "premium",
    "description": "Aggregates revenue and expense items into a weekly P&L rollup. (Premium — subscribe at https://snowdrop.ai)",
}


def weekly_pnl_report(revenue_items: list[dict[str, Any]], expense_items: list[dict[str, Any]], period_start: str, period_end: str) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("weekly_pnl_report")
