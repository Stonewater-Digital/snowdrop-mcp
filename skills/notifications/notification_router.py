"""Route Snowdrop notifications to appropriate channels."""
from __future__ import annotations

from typing import Any

from skills.utils import SkillTelemetryEmitter, get_iso_timestamp, log_lesson

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

    context = context or {}
    normalized_priority = (priority or "").lower()
    emitter = SkillTelemetryEmitter(
        "notification_router",
        {"priority": normalized_priority, "has_context": bool(context)},
    )
    try:
        plan = _build_plan(normalized_priority)
        plan.update({"message": message, "context": context})
        emitter.record(
            "ok",
            {
                "priority": normalized_priority,
                "thunder_ping": plan.get("thunder_ping", False),
                "channels": plan.get("channels"),
            },
        )
        return {
            "status": "success",
            "data": {"routing_plan": plan},
            "timestamp": get_iso_timestamp(),
        }
    except Exception as exc:
        log_lesson(f"notification_router: {exc}")
        emitter.record("error", {"error": str(exc)})
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
        }


def _build_plan(priority: str) -> dict[str, Any]:
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
