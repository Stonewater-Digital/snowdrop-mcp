"""
australia_asics_checker — Determines Australian Financial Services Licence (AFSL) requirements under the Corporations Act 2001 (Cth) Part 7

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/compliance/australia_asics_checker.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "australia_asics_checker",
    "tier": "premium",
    "description": "Determines Australian Financial Services Licence (AFSL) requirements under the Corporations Act 2001 (Cth) Part 7.6. Evaluates service type, client classification (retail vs wholesale), product categories, and foreign provider relief under ASIC Class Orders and legislative instruments. (Premium — subscribe at https://snowdrop.ai)",
}


def australia_asics_checker(entity_data: dict[str, Any]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("australia_asics_checker")
