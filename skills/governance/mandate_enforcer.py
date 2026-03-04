"""Prioritize mandated proposals in the sprint plan."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "mandate_enforcer",
    "description": "Injects mandated proposals at top of sprint backlog while respecting capacity.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_sprint": {"type": "array", "items": {"type": "object"}},
            "mandated_proposals": {"type": "array", "items": {"type": "object"}},
            "capacity_hours": {"type": "number", "default": 160},
        },
        "required": ["current_sprint", "mandated_proposals"],
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

_IMMUTABLE_LAYER = {"Layer 1", "Core Ledger"}


def mandate_enforcer(
    current_sprint: list[dict[str, Any]],
    mandated_proposals: list[dict[str, Any]],
    capacity_hours: float = 160,
    **_: Any,
) -> dict[str, Any]:
    """Return sprint backlog with mandated work moved to top."""
    try:
        ordered_sprint = []
        remaining_capacity = capacity_hours
        # add mandated first
        for mandate in mandated_proposals:
            task = {
                "task": mandate.get("title"),
                "proposal_id": mandate.get("proposal_id"),
                "estimated_hours": float(mandate.get("estimated_hours", 0.0)),
                "priority": "mandated",
                "mandated": True,
            }
            if task["task"] in _IMMUTABLE_LAYER:
                continue
            ordered_sprint.append(task)
            remaining_capacity -= task["estimated_hours"]
        # append remaining tasks sorted by priority
        for task in sorted(current_sprint, key=lambda item: item.get("priority", 999)):
            if task.get("task") in _IMMUTABLE_LAYER:
                ordered_sprint.append(task)
                remaining_capacity -= float(task.get("estimated_hours", 0.0))
                continue
            if remaining_capacity - float(task.get("estimated_hours", 0.0)) < 0:
                task = {**task, "bumped": True}
            else:
                remaining_capacity -= float(task.get("estimated_hours", 0.0))
            ordered_sprint.append(task)
        data = {
            "sprint": ordered_sprint,
            "capacity_remaining": round(remaining_capacity, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("mandate_enforcer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
