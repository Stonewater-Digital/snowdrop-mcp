"""
drawdown_notice_generator — Produce structured LP drawdown notices and routing metadata

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/drawdown_notice_generator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "drawdown_notice_generator",
    "tier": "premium",
    "description": "Produce structured LP drawdown notices and routing metadata. (Premium — subscribe at https://snowdrop.ai)",
}


def drawdown_notice_generator(fund_name: str, capital_call_pct: float, lp_commitments: list[dict[str, Any]], call_date: str | None = None, notify_thunder: bool = False) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("drawdown_notice_generator")
