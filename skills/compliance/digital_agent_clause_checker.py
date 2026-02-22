"""Validate proposed actions against Snowdrop's digital agent charter."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

SAFE_EXTERNAL_ACTIONS = {"status_update", "a2a_request", "heartbeat"}

TOOL_META: dict[str, Any] = {
    "name": "digital_agent_clause_checker",
    "description": "Evaluates actions against identity, spend, and communication rules.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "action_type": {"type": "string"},
            "amount": {"type": "number"},
            "requires_external": {"type": "boolean"},
            "total_assets": {"type": "number", "description": "Basis for 20% rule."},
        },
        "required": ["action_type", "amount", "requires_external"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def digital_agent_clause_checker(
    action_type: str,
    amount: float,
    requires_external: bool,
    total_assets: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Check whether an action should proceed or escalate.

    Args:
        action_type: Label describing the requested action.
        amount: USD impact of the action.
        requires_external: Whether this action involves an external party.
        total_assets: Total asset base for the 20% rule comparison.

    Returns:
        Envelope confirming authorization status plus reason text.
    """

    try:
        action_lower = action_type.lower()
        authorized = True
        reason = "within charter"

        if total_assets is None and amount > 0:
            raise ValueError("total_assets is required when amount is non-zero")

        if total_assets and amount > total_assets * 0.20:
            authorized = False
            reason = ">20% asset move requires 2FA"

        if "identity" in action_lower or "dox" in action_lower:
            authorized = False
            reason = "Identity exposure is forbidden"

        if requires_external and action_lower not in SAFE_EXTERNAL_ACTIONS:
            authorized = False
            reason = "External communication not pre-cleared"

        data = {"authorized": authorized, "reason": reason}
        if not authorized:
            _log_lesson("digital_agent_clause_checker", f"blocked action: {action_lower}")

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("digital_agent_clause_checker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
