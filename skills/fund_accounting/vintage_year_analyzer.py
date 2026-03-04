"""
vintage_year_analyzer — Compares funds across vintages and computes quartiles/PME proxies

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/vintage_year_analyzer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "vintage_year_analyzer",
    "tier": "premium",
    "description": "Compares funds across vintages and computes quartiles/PME proxies. (Premium — subscribe at https://snowdrop.ai)",
}


def vintage_year_analyzer(funds: list[dict[str, Any]]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("vintage_year_analyzer")
