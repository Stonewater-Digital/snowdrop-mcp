"""Prepare Telnyx SMS alerts for Thunder."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "telnyx_alert",
    "description": "Drafts Telnyx SMS payloads to notify Thunder of high-priority events.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "priority": {
                "type": "string",
                "enum": ["info", "warning", "critical"],
            },
        },
        "required": ["message", "priority"],
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


def telnyx_alert(message: str, priority: str, **_: Any) -> dict[str, Any]:
    """Return a pending Telnyx API payload.

    Args:
        message: Body of the SMS alert.
        priority: Alert priority (info, warning, or critical).

    Returns:
        Envelope with the prepared Telnyx request and submission status.
    """

    try:
        api_key = os.getenv("TELNYX_API_KEY")
        thunder_phone = os.getenv("THUNDER_PHONE")
        sender_number = os.getenv("TELNYX_FROM_NUMBER", "pending_assignment")
        if not api_key:
            raise ValueError("TELNYX_API_KEY missing; see .env.template")
        if not thunder_phone:
            raise ValueError("THUNDER_PHONE missing; see .env.template")

        payload = {
            "url": "https://api.telnyx.com/v2/messages",
            "headers": {"Authorization": "Bearer ***redacted***"},
            "body": {
                "from": sender_number,
                "to": thunder_phone,
                "text": f"[{priority.upper()}] {message}",
            },
        }

        submission_status = "pending_thunder_approval"
        if priority == "critical":
            submission_status = "awaiting_manual_override"

        return {
            "status": "success",
            "data": {"prepared_request": payload, "submission_status": submission_status},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("telnyx_alert", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
