"""
mlp_maintenance_capex_tracker — Aggregates maintenance capex budgets vs actuals per asset to surface overruns

PREMIUM SKILL — full implementation available to subscribers.
Subscribe: https://snowdrop.ai (launching soon)

AUTO-GENERATED STUB — do not edit manually.
Source of truth: snowdrop-core/skills/premium/mlps/mlp_maintenance_capex_tracker.py
Regenerate: python scripts/build_public_stubs.py
"""
from __future__ import annotations  # defers annotation evaluation (PEP 563)
from typing import Any, Optional, Union  # FastMCP resolves annotations via get_type_hints()

from skills._paywall import paywall_response

TOOL_META = {
    "name": "mlp_maintenance_capex_tracker",
    "tier": "premium",
    "description": "Aggregates maintenance capex budgets vs actuals per asset to surface overruns. (Premium — subscribe at https://snowdrop.ai)",
}


def mlp_maintenance_capex_tracker(projects: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """Premium skill — subscribe to access full implementation."""
    return paywall_response("mlp_maintenance_capex_tracker")
