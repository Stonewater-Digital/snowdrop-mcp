"""
cap_table_simulator — Models equity dilution across funding rounds, tracking ownership percentages per stakeholder with option pool

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/cap_table_simulator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "cap_table_simulator",
    "tier": "premium",
    "description": "Models equity dilution across funding rounds, tracking ownership percentages per stakeholder with option pool. (Premium — subscribe at https://snowdrop.ai)",
}


def cap_table_simulator(rounds: list[dict[str, Any]], option_pool_pct: float) -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("cap_table_simulator")
