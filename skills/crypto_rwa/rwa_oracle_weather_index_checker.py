"""Executive Summary: Validates weather derivative indexes powering parametric insurance tokens.

Focus: Climate coverage within the oracle reconciliation pillar.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from skills.crypto_rwa.shared import analyze_payload
from skills.utils._log_lesson import _log_lesson

TOOL_META: dict[str, Any] = {
    "name": "rwa_oracle_weather_index_checker",
    "description": "Validates weather derivative indexes powering parametric insurance tokens.",
    "tier": "free",
}


def rwa_oracle_weather_index_checker(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Evaluate control health for Climate.

    Args:
        payload: Dictionary containing an ``observations`` list with on/off-chain values and tolerances.
        context: Optional execution context (caller, runbook pointers, overrides).

    Returns:
        Standard MCP response dict with status, telemetry payload, and ISO 8601 timestamp.
    """

    timestamp = datetime.now(timezone.utc).isoformat()
    try:
        data = analyze_payload(
            skill_name="rwa_oracle_weather_index_checker",
            description="Validates weather derivative indexes powering parametric insurance tokens.",
            payload=payload,
            focus_tag="climate",
            category_tag="oracle_reconciliation",
            context=context,
        )
        return {
            "status": "ok",
            "data": data,
            "timestamp": timestamp,
        }
    except Exception as exc:  # noqa: BLE001 - propagate via lesson log
        _log_lesson("rwa_oracle_weather_index_checker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": timestamp,
        }
