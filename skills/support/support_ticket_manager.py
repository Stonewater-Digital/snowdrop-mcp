"""Manage support tickets for Watering Hole agents."""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

LOG_PATH = "logs/support_tickets.jsonl"
SLA_MAP = {
    "urgent": 1,
    "high": 4,
    "medium": 24,
    "low": 72,
}

TOOL_META: dict[str, Any] = {
    "name": "support_ticket_manager",
    "description": "Creates, updates, closes, and lists support tickets with SLA tracking.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["create", "update", "close", "list", "get"],
            },
            "ticket": {"type": ["object", "null"], "default": None},
            "ticket_id": {"type": ["string", "null"], "default": None},
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


def support_ticket_manager(
    operation: str,
    ticket: dict[str, Any] | None = None,
    ticket_id: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Execute ticket workflow."""
    try:
        tickets = _hydrate_tickets()
        data: dict[str, Any]
        if operation == "create":
            if not ticket:
                raise ValueError("ticket payload required")
            new_id = str(uuid.uuid4())
            priority = ticket.get("priority", "medium")
            deadline = _sla_deadline(priority)
            record = {
                **ticket,
                "ticket_id": new_id,
                "status": "open",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "sla_deadline": deadline.isoformat(),
            }
            tickets[new_id] = record
            _append_log({"action": "create", "ticket": record})
            data = {
                "ticket": record,
                "sla_deadline": record["sla_deadline"],
                "position_in_queue": len([t for t in tickets.values() if t["status"] == "open"]),
            }
        elif operation == "update":
            if not ticket or "ticket_id" not in ticket:
                raise ValueError("ticket_id required for update")
            tid = ticket["ticket_id"]
            if tid not in tickets:
                raise ValueError("ticket not found")
            tickets[tid].update(ticket)
            _append_log({"action": "update", "ticket": tickets[tid]})
            data = {"ticket": tickets[tid], "sla_deadline": tickets[tid]["sla_deadline"], "position_in_queue": _queue_position(tickets, tid)}
        elif operation == "close":
            tid = ticket_id or (ticket or {}).get("ticket_id")
            if not tid or tid not in tickets:
                raise ValueError("ticket_id missing or not found")
            tickets[tid]["status"] = "closed"
            tickets[tid]["closed_at"] = datetime.now(timezone.utc).isoformat()
            _append_log({"action": "close", "ticket_id": tid})
            data = {"ticket": tickets[tid], "sla_deadline": tickets[tid]["sla_deadline"], "position_in_queue": _queue_position(tickets, tid)}
        elif operation == "list":
            data = {"tickets": list(tickets.values())}
        elif operation == "get":
            tid = ticket_id or (ticket or {}).get("ticket_id")
            if not tid or tid not in tickets:
                raise ValueError("ticket not found")
            data = {"ticket": tickets[tid], "sla_deadline": tickets[tid]["sla_deadline"], "position_in_queue": _queue_position(tickets, tid)}
        else:
            raise ValueError("Unsupported operation")

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("support_ticket_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _sla_deadline(priority: str) -> datetime:
    hours = SLA_MAP.get(priority, 24)
    return datetime.now(timezone.utc) + timedelta(hours=hours)


def _queue_position(tickets: dict[str, dict[str, Any]], ticket_id: str) -> int:
    open_tickets = [tid for tid, payload in tickets.items() if payload["status"] == "open"]
    return sorted(open_tickets).index(ticket_id) + 1 if ticket_id in open_tickets else 0


def _hydrate_tickets() -> dict[str, dict[str, Any]]:
    tickets: dict[str, dict[str, Any]] = {}
    if not os.path.exists(LOG_PATH):
        return tickets
    with open(LOG_PATH, "r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            action = payload.get("action")
            if action == "create":
                ticket = payload.get("ticket", {})
                tickets[ticket.get("ticket_id")] = ticket
            elif action == "update":
                ticket = payload.get("ticket", {})
                tickets[ticket.get("ticket_id")] = ticket
            elif action == "close":
                tid = payload.get("ticket_id")
                if tid in tickets:
                    tickets[tid]["status"] = "closed"
    return tickets


def _append_log(entry: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    entry["logged_at"] = datetime.now(timezone.utc).isoformat()
    with open(LOG_PATH, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
