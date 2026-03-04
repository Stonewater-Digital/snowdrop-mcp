"""
schedule_d_8949_generator — Classifies transactions into short- and long-term gains for tax filing

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/compliance/schedule_d_8949_generator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "schedule_d_8949_generator",
    "tier": "premium",
    "description": "Classifies transactions into short- and long-term gains for tax filing. (Premium — subscribe at https://snowdrop.ai)",
}


def schedule_d_8949_generator(transactions: list[dict[str, Any]]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("schedule_d_8949_generator")
