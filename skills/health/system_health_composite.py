"""Compute a composite view of subsystem health."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "system_health_composite",
    "description": "Rolls subsystem telemetry into a weighted score and recommendations.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "subsystems": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["subsystems"],
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


STATUS_SCORES = {
    "healthy": 100,
    "degraded": 50,
    "down": 0,
}


def system_health_composite(
    subsystems: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Produce a composite health score and recommendations."""
    try:
        if not subsystems:
            raise ValueError("subsystems cannot be empty")
        total_weight = sum(float(sub.get("weight", 1.0)) for sub in subsystems)
        if total_weight == 0:
            raise ValueError("Sum of weights cannot be zero")
        score_sum = 0.0
        down_systems = []
        status_breakdown = []
        actions: list[str] = []
        for subsystem in subsystems:
            status = subsystem.get("status", "healthy").lower()
            weight = float(subsystem.get("weight", 1.0))
            contribution = STATUS_SCORES.get(status, 0)
            score_sum += contribution * weight
            status_breakdown.append(
                {
                    "name": subsystem.get("name"),
                    "status": status,
                    "weight": weight,
                }
            )
            if status == "down":
                down_systems.append(subsystem.get("name"))
                actions.append(f"Recover {subsystem.get('name')} immediately")
            elif status == "degraded":
                actions.append(f"Stabilize {subsystem.get('name')} within 1h")
        composite = score_sum / total_weight
        sla_at_risk = composite < 90 or bool(down_systems)
        if not actions:
            actions.append("Maintain normal operations")
        data = {
            "composite_score": round(composite, 2),
            "status_breakdown": status_breakdown,
            "down_systems": down_systems,
            "recommended_actions": actions,
            "sla_at_risk": sla_at_risk,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("system_health_composite", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
