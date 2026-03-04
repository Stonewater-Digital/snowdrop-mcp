"""Determine multi-sig routing for high-value actions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "multi_sig_workflow",
    "description": "Classifies an action into auto, 2FA, or multi-sig approval paths.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {"type": "object"},
            "approval_rules": {"type": "object"},
        },
        "required": ["action"],
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


def multi_sig_workflow(
    action: dict[str, Any],
    approval_rules: dict[str, Any] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Route an action through the appropriate approval level."""
    try:
        if not isinstance(action, dict):
            raise ValueError("action must be a dict")
        approval_rules = approval_rules or {}
        if not isinstance(approval_rules, dict):
            raise ValueError("approval_rules must be a dict when provided")

        amount = float(action.get("amount", 0.0))
        threshold_2fa = float(approval_rules.get("threshold_usd_2fa", 5000))
        threshold_multi = float(approval_rules.get("threshold_usd_multi", 20000))
        required_approvers = int(approval_rules.get("required_approvers", 2))

        if amount < threshold_2fa:
            status = "auto_approved"
            approval_level = "standard"
            approvers_needed = 0
            execution = "auto"
        elif amount < threshold_multi:
            status = "pending_2fa"
            approval_level = "two_factor"
            approvers_needed = 1
            execution = "pending_thunder_approval"
        else:
            status = "pending_multi_sig"
            approval_level = "multi_sig"
            approvers_needed = max(required_approvers, 2)
            execution = "pending_thunder_approval"

        data = {
            "action": action,
            "approval_level": approval_level,
            "approvers_needed": approvers_needed,
            "status": status,
            "execution": execution,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("multi_sig_workflow", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
