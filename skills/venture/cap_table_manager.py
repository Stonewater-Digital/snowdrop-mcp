"""
cap_table_manager — Computes fully diluted ownership after venture rounds including option pools and notes

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/venture/cap_table_manager.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "cap_table_manager",
    "tier": "premium",
    "description": "Computes fully diluted ownership after venture rounds including option pools and notes. (Premium — subscribe at https://snowdrop.ai)",
}


def cap_table_manager(rounds: list[dict[str, Any]], founders: list[dict[str, Any]], option_pool_pct: float = 10.0, outstanding_safes: list[dict[str, Any]] | None = None, outstanding_convertibles: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("cap_table_manager")
