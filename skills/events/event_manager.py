"""Create and manage Watering Hole community events."""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any

LOG_PATH = "logs/events.jsonl"

TOOL_META: dict[str, Any] = {
    "name": "event_manager",
    "description": "Handles creation, updates, registrations, and cancellations for events.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["create", "update", "list", "register", "cancel"],
            },
            "event": {"type": ["object", "null"], "default": None},
            "agent_id": {"type": ["string", "null"], "default": None},
        },
        "required": ["operation"],
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


def event_manager(
    operation: str,
    event: dict[str, Any] | None = None,
    agent_id: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Process the requested event workflow action."""
    try:
        events = _hydrate_events()
        data: dict[str, Any]
        if operation == "create":
            if not event:
                raise ValueError("event payload required for create")
            event_id = str(uuid.uuid4())
            record = {
                **event,
                "event_id": event_id,
                "status": "scheduled",
                "participants": [],
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            events[event_id] = record
            _append_log({"action": "create", "event": record})
            data = {"event": record, "registered_count": 0, "spots_remaining": _spots_remaining(record)}
        elif operation == "update":
            if not event or "event_id" not in event:
                raise ValueError("event_id required for update")
            event_id = event["event_id"]
            if event_id not in events:
                raise ValueError("event not found")
            events[event_id].update(event)
            _append_log({"action": "update", "event": events[event_id]})
            data = {"event": events[event_id], "registered_count": len(events[event_id]["participants"])}
        elif operation == "list":
            data = {"events": list(events.values())}
        elif operation == "register":
            if not agent_id or not event or "event_id" not in event:
                raise ValueError("agent_id and event_id required for register")
            event_id = event["event_id"]
            if event_id not in events:
                raise ValueError("event not found")
            target = events[event_id]
            if target.get("status") == "cancelled":
                raise ValueError("event cancelled")
            if agent_id in target["participants"]:
                raise ValueError("agent already registered")
            if target.get("max_participants") and len(target["participants"]) >= target["max_participants"]:
                raise ValueError("event full")
            target["participants"].append(agent_id)
            _append_log({"action": "register", "event_id": event_id, "agent_id": agent_id})
            data = {
                "event": target,
                "registered_count": len(target["participants"]),
                "spots_remaining": _spots_remaining(target),
            }
        elif operation == "cancel":
            if not event or "event_id" not in event:
                raise ValueError("event_id required for cancel")
            event_id = event["event_id"]
            if event_id not in events:
                raise ValueError("event not found")
            events[event_id]["status"] = "cancelled"
            _append_log({"action": "cancel", "event_id": event_id})
            data = {"event": events[event_id]}
        else:
            raise ValueError("Unsupported operation")

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("event_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _spots_remaining(event: dict[str, Any]) -> int | None:
    max_participants = event.get("max_participants")
    if not max_participants:
        return None
    return max_participants - len(event.get("participants", []))


def _hydrate_events() -> dict[str, dict[str, Any]]:
    events: dict[str, dict[str, Any]] = {}
    if not os.path.exists(LOG_PATH):
        return events
    with open(LOG_PATH, "r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            action = payload.get("action")
            if action in {"create", "update"}:
                event_record = payload.get("event", {})
                events[event_record.get("event_id")] = event_record
            elif action == "register":
                event_id = payload.get("event_id")
                if event_id in events:
                    events[event_id].setdefault("participants", []).append(payload.get("agent_id"))
            elif action == "cancel":
                event_id = payload.get("event_id")
                if event_id in events:
                    events[event_id]["status"] = "cancelled"
    return events


def _append_log(entry: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    entry["logged_at"] = datetime.now(timezone.utc).isoformat()
    with open(LOG_PATH, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
