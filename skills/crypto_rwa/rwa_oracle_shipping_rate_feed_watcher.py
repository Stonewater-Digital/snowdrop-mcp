"""Executive Summary: Checks Baltic Dry and Freightos prints versus oracle shipping feeds for divergence.

Focus: Shipping coverage within the oracle reconciliation pillar.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from skills.crypto_rwa.shared import analyze_payload
from skills.utils._log_lesson import _log_lesson

TOOL_META: dict[str, Any] = {
    "name": "rwa_oracle_shipping_rate_feed_watcher",
    "description": "Checks Baltic Dry and Freightos prints versus oracle shipping feeds for divergence.",
    "tier": "free",
}


def rwa_oracle_shipping_rate_feed_watcher(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Evaluate control health for Shipping.

    Args:
        payload: Dictionary containing an ``observations`` list with on/off-chain values and tolerances.
        context: Optional execution context (caller, runbook pointers, overrides).

    Returns:
        Standard MCP response dict with status, telemetry payload, and ISO 8601 timestamp.
    """

    timestamp = datetime.now(timezone.utc).isoformat()
    try:
        data = analyze_payload(
            skill_name="rwa_oracle_shipping_rate_feed_watcher",
            description="Checks Baltic Dry and Freightos prints versus oracle shipping feeds for divergence.",
            payload=payload,
            focus_tag="shipping",
            category_tag="oracle_reconciliation",
            context=context,
        )
        return {
            "status": "ok",
            "data": data,
            "timestamp": timestamp,
        }
    except Exception as exc:  # noqa: BLE001 - propagate via lesson log
        _log_lesson("rwa_oracle_shipping_rate_feed_watcher", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": timestamp,
        }
