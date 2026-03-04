"""Distribute Watering Hole gratuity pools using weighted roles."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

ROLE_MULTIPLIERS = {
    "barkeep": 1.0,
    "bouncer": 1.2,
    "maid": 0.5,
    "promoter": 0.8,
}

TOOL_META: dict[str, Any] = {
    "name": "tip_pool_distributor",
    "description": "Splits gratuities by hours worked and role multipliers for Watering Hole staff.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "gratuity_pool": {
                "type": "number",
                "description": "Total USD pool to distribute.",
            },
            "shifts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "role": {"type": "string"},
                        "hours": {"type": "number"},
                    },
                },
                "description": "Hours logged for each team member.",
            },
        },
        "required": ["gratuity_pool", "shifts"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "distributions": {"type": "array"},
                    "pool_remainder": {"type": "number"},
                    "total_weight": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def tip_pool_distributor(gratuity_pool: float, shifts: Iterable[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Allocate gratuity pool using hours × role multipliers.

    Args:
        gratuity_pool: Total USD gratuities available.
        shifts: Iterable of shift dicts containing name, role, and hours.
        **_: Ignored keyword arguments for compatibility.

    Returns:
        Distribution list plus diagnostics.
    """
    try:
        if gratuity_pool < 0:
            raise ValueError("gratuity_pool cannot be negative")

        weighted_hours: list[tuple[str, str, float]] = []
        total_weight = 0.0
        for shift in shifts:
            name = shift.get("name")
            role = (shift.get("role") or "").lower()
            hours = float(shift.get("hours", 0.0))
            if not name:
                raise ValueError("Each shift requires a name")
            if hours < 0:
                raise ValueError(f"hours cannot be negative (name={name})")
            multiplier = ROLE_MULTIPLIERS.get(role, 1.0)
            weight = hours * multiplier
            weighted_hours.append((name, role or "unknown", weight))
            total_weight += weight

        if total_weight == 0:
            raise ValueError("Total weighted hours cannot be zero")

        distributions = []
        running_total = 0.0
        for name, role, weight in weighted_hours:
            share = (weight / total_weight) * gratuity_pool
            running_total += share
            distributions.append({
                "name": name,
                "role": role,
                "weight": round(weight, 4),
                "payout": round(share, 2),
            })

        remainder = round(gratuity_pool - running_total, 2)
        data = {
            "distributions": distributions,
            "pool_remainder": remainder,
            "total_weight": round(total_weight, 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("tip_pool_distributor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
