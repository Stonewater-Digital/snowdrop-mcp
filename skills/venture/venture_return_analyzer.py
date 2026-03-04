"""
venture_return_analyzer — Computes proceeds for preferred vs common across exit scenarios, including participation caps

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/venture/venture_return_analyzer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "venture_return_analyzer",
    "tier": "premium",
    "description": "Computes proceeds for preferred vs common across exit scenarios, including participation caps. (Premium — subscribe at https://snowdrop.ai)",
}


def venture_return_analyzer(investment: dict[str, Any], exit_scenarios: list[float], total_shares: int, other_preferences: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("venture_return_analyzer")
