"""Track weighted occupancy across property types."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "occupancy_rate_tracker",
    "description": "Computes weighted average occupancy and vacancy by property type.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "properties": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "square_feet": {"type": "number"},
                        "occupied_square_feet": {"type": "number"},
                    },
                    "required": ["type", "square_feet", "occupied_square_feet"],
                },
            }
        },
        "required": ["properties"],
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


def occupancy_rate_tracker(properties: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return occupancy stats and vacancy warnings."""
    try:
        total_sf = sum(item.get("square_feet", 0.0) for item in properties)
        total_occ = sum(item.get("occupied_square_feet", 0.0) for item in properties)
        weighted_occupancy = total_occ / total_sf * 100 if total_sf else 0.0
        detail = []
        for item in properties:
            sf = item.get("square_feet", 0.0)
            occ = item.get("occupied_square_feet", 0.0)
            rate = occ / sf * 100 if sf else 0.0
            detail.append(
                {
                    "type": item.get("type", "unknown"),
                    "occupancy_pct": round(rate, 2),
                    "vacancy_pct": round(100 - rate, 2),
                }
            )
        data = {
            "portfolio_occupancy_pct": round(weighted_occupancy, 2),
            "property_breakdown": detail,
            "vacancy_warning": weighted_occupancy < 90,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("occupancy_rate_tracker", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
