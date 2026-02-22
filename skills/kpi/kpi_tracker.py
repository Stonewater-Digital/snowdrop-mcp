"""Track KPI attainment versus targets."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "kpi_tracker",
    "description": "Calculates KPI progress, highlights off-track metrics, and summarizes health.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "kpis": {"type": "array", "items": {"type": "object"}},
            "period": {"type": "string"},
        },
        "required": ["kpis", "period"],
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


def kpi_tracker(kpis: list[dict[str, Any]], period: str, **_: Any) -> dict[str, Any]:
    """Return KPI tracking summary."""
    try:
        evaluated = []
        off_track: list[dict[str, Any]] = []
        on_track_count = 0

        for kpi in kpis:
            target = float(kpi.get("target_value", 0.0))
            current = float(kpi.get("current_value", 0.0))
            direction = kpi.get("direction", "higher_better")
            if target == 0:
                achievement = 0.0
            elif direction == "lower_better":
                achievement = min(target / current, 1.2) if current else 1.2
            else:
                achievement = min(current / target, 1.2)
            status = "on_track" if achievement >= 0.9 else "off_track"
            entry = {
                "name": kpi.get("name"),
                "category": kpi.get("category"),
                "current_value": current,
                "target_value": target,
                "unit": kpi.get("unit"),
                "direction": direction,
                "achievement_pct": round(achievement * 100, 2),
                "status": status,
            }
            evaluated.append(entry)
            if status == "on_track":
                on_track_count += 1
            else:
                off_track.append(entry)

        off_track_count = len(off_track)
        health_ratio = on_track_count / len(kpis) if kpis else 0.0
        if health_ratio >= 0.75:
            health = "healthy"
        elif health_ratio >= 0.5:
            health = "watch"
        else:
            health = "at_risk"
        top_concern = off_track[0]["name"] if off_track else None
        data = {
            "period": period,
            "kpis": evaluated,
            "on_track_count": on_track_count,
            "off_track_count": off_track_count,
            "overall_health": health,
            "top_concern": top_concern,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("kpi_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
