"""Route swarm messages between Snowdrop agents."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "swarm_message_router",
    "description": "Validates sender/recipient roles and produces routing envelopes.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "sender": {"type": "string"},
            "recipient": {"type": "string"},
            "message_type": {"type": "string", "enum": ["task", "verdict", "challenge", "report"]},
            "payload": {"type": "object"},
        },
        "required": ["sender", "recipient", "message_type", "payload"],
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

_ROLES = {"cfo", "builder", "skeptic", "secretary"}


def swarm_message_router(
    sender: str,
    recipient: str,
    message_type: str,
    payload: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Return routing confirmation for swarm communications."""
    try:
        sender_role = sender.lower()
        recipient_role = recipient.lower()
        if sender_role not in _ROLES:
            raise ValueError("sender role not recognized")
        if recipient_role not in _ROLES and recipient_role != "broadcast":
            raise ValueError("recipient role not recognized")
        routing_id = str(uuid.uuid4())
        envelope = {
            "routing_id": routing_id,
            "sender": sender_role,
            "recipient": recipient_role,
            "message_type": message_type,
            "payload": payload,
            "delivered_at": datetime.now(timezone.utc).isoformat(),
        }
        return {
            "status": "success",
            "data": envelope,
            "timestamp": envelope["delivered_at"],
        }
    except Exception as exc:
        _log_lesson("swarm_message_router", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
