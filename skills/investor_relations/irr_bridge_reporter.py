"""
irr_bridge_reporter — Calculates IRR, DPI, RVPI, and TVPI along with driver bridge for investor reporting

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/investor_relations/irr_bridge_reporter.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "irr_bridge_reporter",
    "tier": "premium",
    "description": "Calculates IRR, DPI, RVPI, and TVPI along with driver bridge for investor reporting. (Premium — subscribe at https://snowdrop.ai)",
}


def irr_bridge_reporter(cash_flows: list[dict[str, Any]], period_label: str | None = None) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("irr_bridge_reporter")
