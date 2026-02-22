"""Measure the velocity of community value creation."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "crowd_value_velocity",
    "description": "Calculates weekly value velocity, acceleration, and forward projections.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "weekly_snapshots": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["weekly_snapshots"],
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


def crowd_value_velocity(weekly_snapshots: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return velocity metrics and projections."""
    try:
        ordered = sorted(weekly_snapshots, key=lambda s: s["week"])
        velocities = [snap.get("value_estimate_usd", 0) for snap in ordered]
        if len(velocities) < 2:
            raise ValueError("At least two snapshots required")
        current_velocity = velocities[-1]
        prior_velocity = velocities[-2]
        acceleration = "accelerating" if current_velocity > prior_velocity else "decelerating" if current_velocity < prior_velocity else "flat"
        trend = [
            {"week": snap["week"], "value": snap.get("value_estimate_usd", 0)}
            for snap in ordered
        ]
        projections = {
            4: current_velocity * 4,
            12: current_velocity * 12,
            26: current_velocity * 26,
        }
        peak_week = max(trend, key=lambda t: t["value"])["week"]
        data = {
            "current_velocity_usd_per_week": round(current_velocity, 2),
            "acceleration": acceleration,
            "projected_value_4w": round(projections[4], 2),
            "projected_value_12w": round(projections[12], 2),
            "projected_value_26w": round(projections[26], 2),
            "peak_velocity_week": peak_week,
            "velocity_trend": trend,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("crowd_value_velocity", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
