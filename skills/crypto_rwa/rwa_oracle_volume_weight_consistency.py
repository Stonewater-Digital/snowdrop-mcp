"""Executive Summary: Ensures oracle VWAP calculations match reported venue volumes.

Focus: Market Structure coverage within the oracle reconciliation pillar.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from skills.crypto_rwa.shared import analyze_payload
from skills.utils._log_lesson import _log_lesson

TOOL_META: dict[str, Any] = {
    "name": "rwa_oracle_volume_weight_consistency",
    "description": "Ensures oracle VWAP calculations match reported venue volumes.",
    "tier": "free",
}


def rwa_oracle_volume_weight_consistency(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Evaluate control health for Market Structure.

    Args:
        payload: Dictionary containing an ``observations`` list with on/off-chain values and tolerances.
        context: Optional execution context (caller, runbook pointers, overrides).

    Returns:
        Standard MCP response dict with status, telemetry payload, and ISO 8601 timestamp.
    """

    timestamp = datetime.now(timezone.utc).isoformat()
    try:
        data = analyze_payload(
            skill_name="rwa_oracle_volume_weight_consistency",
            description="Ensures oracle VWAP calculations match reported venue volumes.",
            payload=payload,
            focus_tag="market_structure",
            category_tag="oracle_reconciliation",
            context=context,
        )
        return {
            "status": "ok",
            "data": data,
            "timestamp": timestamp,
        }
    except Exception as exc:  # noqa: BLE001 - propagate via lesson log
        _log_lesson("rwa_oracle_volume_weight_consistency", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": timestamp,
        }
