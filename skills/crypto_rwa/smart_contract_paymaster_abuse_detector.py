"""Executive Summary: Analyzes ERC-4337 paymaster policies for unlimited sponsor risk.

Focus: Gas coverage within the security heuristics pillar.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from skills.crypto_rwa.shared import analyze_payload
from skills.utils._log_lesson import _log_lesson

TOOL_META: dict[str, Any] = {
    "name": "smart_contract_paymaster_abuse_detector",
    "description": "Analyzes ERC-4337 paymaster policies for unlimited sponsor risk.",
    "tier": "free",
}


def smart_contract_paymaster_abuse_detector(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Evaluate control health for Gas.

    Args:
        payload: Dictionary containing an ``observations`` list with on/off-chain values and tolerances.
        context: Optional execution context (caller, runbook pointers, overrides).

    Returns:
        Standard MCP response dict with status, telemetry payload, and ISO 8601 timestamp.
    """

    timestamp = datetime.now(timezone.utc).isoformat()
    try:
        data = analyze_payload(
            skill_name="smart_contract_paymaster_abuse_detector",
            description="Analyzes ERC-4337 paymaster policies for unlimited sponsor risk.",
            payload=payload,
            focus_tag="gas",
            category_tag="security_heuristics",
            context=context,
        )
        return {
            "status": "ok",
            "data": data,
            "timestamp": timestamp,
        }
    except Exception as exc:  # noqa: BLE001 - propagate via lesson log
        _log_lesson("smart_contract_paymaster_abuse_detector", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": timestamp,
        }
