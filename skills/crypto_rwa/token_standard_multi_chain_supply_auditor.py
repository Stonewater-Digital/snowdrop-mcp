"""Executive Summary: Audits circulating supply across chains to prevent double listings.

Focus: Operations coverage within the token compliance pillar.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from skills.crypto_rwa.shared import analyze_payload
from skills.utils._log_lesson import _log_lesson

TOOL_META: dict[str, Any] = {
    "name": "token_standard_multi_chain_supply_auditor",
    "description": "Audits circulating supply across chains to prevent double listings.",
    "tier": "free",
}


def token_standard_multi_chain_supply_auditor(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Evaluate control health for Operations.

    Args:
        payload: Dictionary containing an ``observations`` list with on/off-chain values and tolerances.
        context: Optional execution context (caller, runbook pointers, overrides).

    Returns:
        Standard MCP response dict with status, telemetry payload, and ISO 8601 timestamp.
    """

    timestamp = datetime.now(timezone.utc).isoformat()
    try:
        data = analyze_payload(
            skill_name="token_standard_multi_chain_supply_auditor",
            description="Audits circulating supply across chains to prevent double listings.",
            payload=payload,
            focus_tag="operations",
            category_tag="token_compliance",
            context=context,
        )
        return {
            "status": "ok",
            "data": data,
            "timestamp": timestamp,
        }
    except Exception as exc:  # noqa: BLE001 - propagate via lesson log
        _log_lesson("token_standard_multi_chain_supply_auditor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": timestamp,
        }
