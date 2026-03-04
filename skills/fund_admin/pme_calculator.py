"""
pme_calculator — Calculates Kaplan-Schoar PME (Public Market Equivalent) by discounting fund contributions and distributions using the compounded index return path

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_admin/pme_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "pme_calculator",
    "tier": "premium",
    "description": "Calculates Kaplan-Schoar PME (Public Market Equivalent) by discounting fund contributions and distributions using the compounded index return path. PME > 1.0 means the fund outperformed the public market benchmark. (Premium — subscribe at https://snowdrop.ai)",
}


def pme_calculator(contributions: Sequence[float], distributions: Sequence[float], index_returns: Sequence[float], residual_nav: float = 0.0) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("pme_calculator")
