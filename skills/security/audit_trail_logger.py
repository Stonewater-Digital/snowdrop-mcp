"""Append-only audit trail with hash chaining."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "audit_trail_logger",
    "description": "Writes immutable audit entries to logs/audit_trail.jsonl.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {"type": "string"},
            "actor": {"type": "string"},
            "details": {"type": "object"},
            "previous_hash": {"type": "string"},
        },
        "required": ["action", "actor", "details", "previous_hash"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "entry": {"type": "object"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def audit_trail_logger(
    action: str,
    actor: str,
    details: dict[str, Any],
    previous_hash: str,
    **_: Any,
) -> dict[str, Any]:
    """Write a hashed audit entry."""

    try:
        timestamp = datetime.now(timezone.utc).isoformat()
        serialized = json.dumps(details, sort_keys=True)
        payload = f"{previous_hash}{timestamp}{serialized}".encode("utf-8")
        entry_hash = sha256(payload).hexdigest()
        entry = {
            "action": action,
            "actor": actor,
            "details": details,
            "timestamp": timestamp,
            "previous_hash": previous_hash,
            "hash": entry_hash,
        }
        os.makedirs("logs", exist_ok=True)
        with open("logs/audit_trail.jsonl", "a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry) + "\n")
        return {
            "status": "success",
            "data": {"entry": entry},
            "timestamp": timestamp,
        }
    except Exception as exc:
        _log_lesson("audit_trail_logger", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
