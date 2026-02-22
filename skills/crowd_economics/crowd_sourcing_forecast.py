"""Forecast community contribution value under multiple scenarios."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "crowd_sourcing_forecast",
    "description": "Projects contributions, skills, and value under bear/base/bull scenarios for six months.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "historical": {"type": "array", "items": {"type": "object"}},
            "growth_scenarios": {"type": "object"},
        },
        "required": ["historical", "growth_scenarios"],
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


def crowd_sourcing_forecast(
    historical: list[dict[str, Any]],
    growth_scenarios: dict[str, float],
    **_: Any,
) -> dict[str, Any]:
    """Return scenario forecasts and tipping point estimates."""
    try:
        latest = sorted(historical, key=lambda h: h["month"])[-1]
        contributors = latest.get("new_contributors", 0)
        value = latest.get("value_added_usd", 0)
        forecasts = {}
        tipping_point = None
        for label, pct in growth_scenarios.items():
            projected = value
            projected_contribs = contributors
            for month in range(1, 7):
                projected_contribs *= 1 + pct / 100
                projected *= 1 + pct / 100
                if tipping_point is None and projected > latest.get("internal_cost", projected) * 1.1:
                    tipping_point = f"Month {month} ({label})"
            forecasts[label] = round(projected, 2)
        data = {
            "forecast": forecasts,
            "base_case_6mo_value": forecasts.get("base", 0),
            "bull_case_6mo_value": forecasts.get("bull", 0),
            "bear_case_6mo_value": forecasts.get("bear", 0),
            "break_even_contributors": int(contributors * 1.2),
            "tipping_point_month": tipping_point,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("crowd_sourcing_forecast", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
