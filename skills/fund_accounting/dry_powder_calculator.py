"""
dry_powder_calculator — Calculates available dry powder (uninvested capital), deployment rate, and deployment runway for a private equity fund

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/dry_powder_calculator.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "dry_powder_calculator",
    "tier": "premium",
    "description": "Calculates available dry powder (uninvested capital), deployment rate, and deployment runway for a private equity fund. Dry powder = total_commitments - capital_called - reserves. If monthly_deployment_rate is provided, runway_months = dry_powder / rate. Useful for fund pacing, LP reporting, and GP investment planning. (Premium — subscribe at https://snowdrop.ai)",
}


def dry_powder_calculator() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("dry_powder_calculator")
