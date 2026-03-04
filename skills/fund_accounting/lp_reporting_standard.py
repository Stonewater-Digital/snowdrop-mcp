"""
lp_reporting_standard — Generates an ILPA (Institutional Limited Partners Association) compliant quarterly fund report in markdown format

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/fund_accounting/lp_reporting_standard.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "lp_reporting_standard",
    "tier": "premium",
    "description": "Generates an ILPA (Institutional Limited Partners Association) compliant quarterly fund report in markdown format. Validates presence of all required ILPA Reporting Template v2 fields and flags any that are missing or null. Produces structured markdown with sections for Fund Overview, Performance Metrics, Top Holdings, Cash Position, and Upcoming Events. (Premium — subscribe at https://snowdrop.ai)",
}


def lp_reporting_standard() -> dict:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("lp_reporting_standard")
