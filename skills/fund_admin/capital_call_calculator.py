"""
capital_call_calculator — Calculates LP capital call wire amounts based on commitment percentages

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/capital_call_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "capital_call_calculator",
    "tier": "premium",
    "description": "Calculates LP capital call wire amounts based on commitment percentages. Supports per-call fund expenses and validates that call_pct does not exceed remaining unfunded commitment. (Premium — subscribe at https://snowdrop.ai)",
}


def capital_call_calculator(lp_commitments: list[dict[str, Any]], call_pct: float, fees_pct: float = 0.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("capital_call_calculator")
