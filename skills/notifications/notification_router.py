"""Route Snowdrop notifications to appropriate channels."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "notification_router",
    "description": "Maps alert priority to Telegram/SMS/freeze workflows.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "priority": {
                "type": "string",
                "enum": ["info", "warning", "critical", "emergency"],
            },
            "context": {"type": "object"},
        },
        "required": ["message", "priority"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "routing_plan": {"type": "object"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def notification_router(
    message: str,
    priority: str,
    context: dict[str, Any] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return the routing plan for an alert."""

    try:
        context = context or {}
        plan = _build_plan(priority)
        plan.update({"message": message, "context": context})
        return {
            "status": "success",
            "data": {"routing_plan": plan},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("notification_router", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _build_plan(priority: str) -> dict[str, Any]:
    priority = priority.lower()
    if priority not in {"info", "warning", "critical", "emergency"}:
        raise ValueError("Unsupported priority level")
    base_plan: dict[str, Any] = {
        "priority": priority,
        "channels": ["telegram"],
        "log": priority in {"warning", "critical", "emergency"},
        "sms": priority in {"critical", "emergency"},
        "freeze_recommended": priority == "emergency",
    }
    if priority == "critical":
        base_plan["thunder_ping"] = True
    if priority == "emergency":
        base_plan["thunder_ping"] = True
        base_plan["thunder_signal_status"] = "pending_thunder_approval"
    return base_plan


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
