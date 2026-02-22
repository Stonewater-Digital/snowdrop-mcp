"""Plan compute scale timelines from usage trends."""
from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "compute_capacity_planner",
    "description": "Projects when capacity will be breached and recommends actions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "usage_history": {"type": "array", "items": {"type": "object"}},
            "capacity_limit": {"type": "number"},
            "growth_rate_pct": {"type": ["number", "null"], "default": None},
        },
        "required": ["usage_history", "capacity_limit"],
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


def compute_capacity_planner(
    usage_history: list[dict[str, Any]],
    capacity_limit: int,
    growth_rate_pct: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Estimate the date capacity will be exceeded and plan mitigations."""
    try:
        if not usage_history:
            raise ValueError("usage_history cannot be empty")
        if capacity_limit <= 0:
            raise ValueError("capacity_limit must be positive")
        ordered = sorted(usage_history, key=lambda item: item["date"])
        latest = ordered[-1]
        current_requests = float(latest.get("requests", 0))
        current_util = min(current_requests / capacity_limit * 100, 200.0)
        growth_rate = growth_rate_pct
        if growth_rate is None and len(ordered) > 1:
            first = ordered[0]
            first_requests = max(float(first.get("requests", 0)), 1.0)
            days = max((_parse_date(latest["date"]) - _parse_date(first["date"])).days, 1)
            growth_rate = ((current_requests / first_requests) ** (1 / days) - 1) * 100
        if growth_rate is None:
            growth_rate = 0.0

        projected_date = _project_capacity_date(
            current_requests,
            capacity_limit,
            growth_rate,
            _parse_date(latest["date"]),
        )
        recommended_action = _recommend_action(current_util, projected_date)
        cost_at_capacity = _cost_projection(latest, capacity_limit, current_requests)
        data = {
            "current_utilization_pct": round(current_util, 2),
            "projected_capacity_date": projected_date.isoformat() if projected_date else None,
            "recommended_action": recommended_action,
            "cost_at_capacity": round(cost_at_capacity, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("compute_capacity_planner", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _project_capacity_date(
    current_requests: float,
    capacity_limit: int,
    growth_rate_pct: float,
    last_date: datetime,
) -> datetime | None:
    if growth_rate_pct <= 0 or current_requests <= 0:
        return None
    if current_requests >= capacity_limit:
        return last_date
    ratio = capacity_limit / current_requests
    if ratio <= 1:
        return last_date
    growth_daily = 1 + growth_rate_pct / 100
    if growth_daily <= 1:
        return None
    periods = math.log(ratio, growth_daily)
    days = max(periods, 0)
    return last_date + timedelta(days=days)


def _recommend_action(util_pct: float, projected_date: datetime | None) -> str:
    if util_pct >= 95:
        return "Scale up immediately"
    if projected_date and projected_date <= datetime.now(timezone.utc) + timedelta(days=7):
        return "Prepare emergency capacity"
    if util_pct >= 80:
        return "Plan scale event"
    return "Monitor"


def _cost_projection(latest: dict[str, Any], capacity_limit: int, current_requests: float) -> float:
    current_cost = float(latest.get("cost", 0))
    if current_requests == 0:
        return current_cost
    cost_per_request = current_cost / current_requests
    return cost_per_request * capacity_limit


def _parse_date(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
