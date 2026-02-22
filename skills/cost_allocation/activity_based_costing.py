"""Allocate shared costs using activity-based costing."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "activity_based_costing",
    "description": "Distributes cost pools based on activity driver consumption.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cost_pools": {"type": "array", "items": {"type": "object"}},
            "activities": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["cost_pools", "activities"],
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


def activity_based_costing(
    cost_pools: list[dict[str, Any]],
    activities: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Allocate each pool proportionally to driver usage."""
    try:
        if not cost_pools or not activities:
            raise ValueError("cost_pools and activities are required")
        allocation_summary: dict[str, float] = {activity["name"]: 0.0 for activity in activities}
        detailed_rows: list[dict[str, Any]] = []
        total_cost = sum(float(pool.get("total_cost", 0)) for pool in cost_pools)
        total_driver_units = 0.0
        for pool in cost_pools:
            driver = pool.get("driver")
            pool_cost = float(pool.get("total_cost", 0))
            driver_totals = sum(float(act.get("driver_values", {}).get(driver, 0)) for act in activities)
            if driver_totals == 0:
                continue
            total_driver_units += driver_totals
            for activity in activities:
                activity_name = activity["name"]
                driver_value = float(activity.get("driver_values", {}).get(driver, 0))
                share = driver_value / driver_totals
                allocated = pool_cost * share
                allocation_summary[activity_name] += allocated
                detailed_rows.append(
                    {
                        "activity": activity_name,
                        "pool": pool.get("name"),
                        "allocated_cost": round(allocated, 2),
                    }
                )
        overhead_rate = (total_cost / total_driver_units) if total_driver_units else 0.0
        data = {
            "allocated_costs": {k: round(v, 2) for k, v in allocation_summary.items()},
            "cost_per_activity": detailed_rows,
            "overhead_rate": round(overhead_rate, 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("activity_based_costing", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
