"""Plan Snowdrop development sprints with dependency awareness."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "sprint_planner",
    "description": "Selects backlog tasks for the sprint based on priority, capacity, and dependencies.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "backlog": {
                "type": "array",
                "items": {"type": "object"},
            },
            "team_capacity_points": {"type": "integer"},
            "sprint_duration_days": {"type": "integer", "default": 14},
        },
        "required": ["backlog", "team_capacity_points"],
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


def sprint_planner(
    backlog: list[dict[str, Any]],
    team_capacity_points: int,
    sprint_duration_days: int = 14,
    **_: Any,
) -> dict[str, Any]:
    """Return a sprint forecast using available capacity."""
    try:
        if team_capacity_points <= 0:
            raise ValueError("team_capacity_points must be positive")
        sorted_backlog = sorted(
            backlog,
            key=lambda item: (int(item.get("priority", 9999)), -int(item.get("story_points", 0))),
        )
        selected: list[dict[str, Any]] = []
        deferred: list[dict[str, Any]] = []
        risk_items: list[dict[str, Any]] = []
        used_points = 0
        completed_ids: set[str] = set()

        for task in sorted_backlog:
            story_points = int(task.get("story_points", 0))
            dependencies = task.get("dependencies", []) or []
            task_id = str(task.get("task_id", task.get("title", "unknown")))
            deps_met = all(dep in completed_ids for dep in dependencies)
            if dependencies and not deps_met:
                risk_items.append(
                    {
                        "task_id": task_id,
                        "blocking_dependencies": dependencies,
                    }
                )
                deferred.append(task)
                continue
            if used_points + story_points <= team_capacity_points:
                selected.append(task)
                used_points += story_points
                completed_ids.add(task_id)
            else:
                deferred.append(task)

        capacity_used_pct = used_points / team_capacity_points if team_capacity_points else 0.0
        data = {
            "sprint_tasks": selected,
            "total_points": used_points,
            "capacity_used_pct": round(capacity_used_pct * 100, 2),
            "deferred": deferred,
            "risk_items": risk_items,
            "sprint_duration_days": sprint_duration_days,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("sprint_planner", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
