"""
ubti_blocker_analyzer — Computes unrelated business taxable income under IRC §§512-514 and recommends blocker structures

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_tax/ubti_blocker_analyzer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "ubti_blocker_analyzer",
    "tier": "premium",
    "description": "Computes unrelated business taxable income under IRC §§512-514 and recommends blocker structures. (Premium — subscribe at https://snowdrop.ai)",
}


def ubti_blocker_analyzer() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("ubti_blocker_analyzer")
