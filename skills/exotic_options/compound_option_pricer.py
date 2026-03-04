"""
compound_option_pricer — Geske (1979) closed-form pricer for call-on-call and put-on-call compound options using bivariate normals

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/exotic_options/compound_option_pricer.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "compound_option_pricer",
    "tier": "premium",
    "description": "Geske (1979) closed-form pricer for call-on-call and put-on-call compound options using bivariate normals. (Premium — subscribe at https://snowdrop.ai)",
}


def compound_option_pricer() -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("compound_option_pricer")
