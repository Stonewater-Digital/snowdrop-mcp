"""Manage Snowdrop agent notification preferences."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LOG_PATH = Path("logs/notification_prefs.jsonl")

TOOL_META: dict[str, Any] = {
    "name": "notification_preferences_manager",
    "description": "Gets, sets, or resets notification preferences per agent with persistence.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {"type": "string", "enum": ["get", "set", "reset"]},
            "agent_id": {"type": "string"},
            "preferences": {"type": "object"},
        },
        "required": ["operation", "agent_id"],
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


def notification_preferences_manager(
    operation: str,
    agent_id: str,
    preferences: dict[str, Any] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Manage preference records in a JSONL ledger."""
    try:
        records = _load()
        current = records.get(agent_id, _default_preferences(agent_id))
        operation = operation.lower()
        if operation == "get":
            result = current
        elif operation == "set":
            if preferences is None:
                raise ValueError("preferences required for set")
            current.update(preferences)
            _append(agent_id, current)
            result = current
        elif operation == "reset":
            current = _default_preferences(agent_id)
            _append(agent_id, current)
            result = current
        else:
            raise ValueError("Unsupported operation")
        data = {"agent_id": agent_id, "preferences": result}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("notification_preferences_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _load() -> dict[str, dict[str, Any]]:
    if not LOG_PATH.exists():
        return {}
    result: dict[str, dict[str, Any]] = {}
    with LOG_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            result[record["agent_id"]] = record["preferences"]
    return result


def _append(agent_id: str, prefs: dict[str, Any]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"agent_id": agent_id, "preferences": prefs, "timestamp": datetime.now(timezone.utc).isoformat()}
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def _default_preferences(agent_id: str) -> dict[str, Any]:
    return {
        "agent_id": agent_id,
        "channels": ["telegram"],
        "frequency": "realtime",
        "quiet_hours": None,
        "severity_filter": "all",
    }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
