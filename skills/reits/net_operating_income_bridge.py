"""Bridge NOI change by drivers."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "net_operating_income_bridge",
    "description": "Builds an NOI bridge showing contributions from volume, rate, occupancy, and opex.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prior_noi": {"type": "number"},
            "volume_change": {"type": "number"},
            "rate_change": {"type": "number"},
            "occupancy_change": {"type": "number"},
            "expense_change": {"type": "number"},
        },
        "required": ["prior_noi", "volume_change", "rate_change", "occupancy_change", "expense_change"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def net_operating_income_bridge(
    prior_noi: float,
    volume_change: float,
    rate_change: float,
    occupancy_change: float,
    expense_change: float,
    **_: Any,
) -> dict[str, Any]:
    """Return NOI bridge summary."""
    try:
        drivers = {
            "volume": volume_change,
            "rate": rate_change,
            "occupancy": occupancy_change,
            "expenses": expense_change,
        }
        current_noi = prior_noi + sum(drivers.values())
        data = {
            "drivers": {key: round(value, 2) for key, value in drivers.items()},
            "prior_noi": round(prior_noi, 2),
            "current_noi": round(current_noi, 2),
            "growth_pct": round((current_noi - prior_noi) / prior_noi * 100, 2) if prior_noi else 0.0,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("net_operating_income_bridge", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
