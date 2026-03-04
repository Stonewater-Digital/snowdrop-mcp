"""Track sprint velocity trendlines."""
from __future__ import annotations

import statistics
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "velocity_tracker",
    "description": "Summarizes velocity averages, trend, and predictability over past sprints.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "sprint_history": {
                "type": "array",
                "items": {"type": "object"},
            }
        },
        "required": ["sprint_history"],
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


def velocity_tracker(sprint_history: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Compute key velocity metrics."""
    try:
        if len(sprint_history) == 0:
            raise ValueError("sprint_history cannot be empty")
        history = sorted(sprint_history, key=lambda item: item.get("end_date", ""))
        last_three = history[-3:]
        velocities = [float(entry.get("completed_points", 0.0)) for entry in last_three]
        avg_velocity = sum(velocities) / len(velocities)

        ratios = [
            (entry.get("completed_points", 0) / entry.get("planned_points", 1))
            if entry.get("planned_points")
            else 0.0
            for entry in last_three
        ]
        if len(ratios) > 1:
            std_dev = statistics.pstdev(ratios)
        else:
            std_dev = 0.0
        predictability = max(0.0, 1 - std_dev)

        trend = _trend_label(velocities)
        recommended_capacity = int(round(avg_velocity * predictability))
        burndown_health = "green" if predictability > 0.8 else "yellow" if predictability > 0.6 else "red"

        data = {
            "avg_velocity": round(avg_velocity, 2),
            "trend": trend,
            "predictability": round(predictability, 3),
            "recommended_next_sprint_capacity": max(recommended_capacity, 1),
            "burndown_health": burndown_health,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("velocity_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _trend_label(values: list[float]) -> str:
    if len(values) < 2:
        return "stable"
    if values[-1] > values[0] * 1.1:
        return "accelerating"
    if values[-1] < values[0] * 0.9:
        return "decelerating"
    return "stable"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
