"""Routing engine for Watering Hole agent requests with bonding curve pricing."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Sequence

TOOL_META: dict[str, Any] = {
    "name": "watering_hole_order_router",
    "description": (
        "Quotes Watering Hole skill requests via the bonding curve, assigns the correct skill,"
        " and returns billing plus dispatch telemetry."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string", "description": "Snowdrop agent identifier."},
            "requested_skill": {
                "type": "string",
                "description": "Skill name the agent wants to execute.",
            },
            "base_price": {"type": "number"},
            "decay_rate": {"type": "number"},
            "time_elapsed_hours": {"type": "number"},
            "slope": {"type": "number"},
            "delta_units": {"type": "number"},
            "delta_time_hours": {"type": "number"},
            "available_skills": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "category": {"type": "string"},
                        "sla_minutes": {"type": "number"},
                    },
                },
                "description": "Advertised catalog for validation.",
            },
        },
        "required": [
            "agent_id",
            "requested_skill",
            "base_price",
            "decay_rate",
            "time_elapsed_hours",
            "slope",
            "delta_units",
            "delta_time_hours",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string"},
                    "requested_skill": {"type": "string"},
                    "dispatch_reference": {"type": "string"},
                    "quoted_price": {"type": "number"},
                    "billing_breakdown": {"type": "object"},
                    "catalog_match": {"type": "boolean"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def watering_hole_order_router(
    agent_id: str,
    requested_skill: str,
    base_price: float,
    decay_rate: float,
    time_elapsed_hours: float,
    slope: float,
    delta_units: float,
    delta_time_hours: float,
    available_skills: Sequence[dict[str, Any]] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Price and route Watering Hole orders.

    Args:
        agent_id: Requesting agent identifier.
        requested_skill: Tool or service requested.
        base_price: Starting price.
        decay_rate: Cooling constant k in the bonding curve.
        time_elapsed_hours: Time delta since last filled order.
        slope: Demand slope coefficient.
        delta_units: Volume change in the evaluation window.
        delta_time_hours: Window size used for delta_units.
        available_skills: Optional catalog of admissible skills.
        **_: Extra ignored keyword arguments.

    Returns:
        Structured response with billing data and dispatch reference.
    """
    try:
        _validate_positive("base_price", base_price)
        if decay_rate < 0:
            raise ValueError("decay_rate cannot be negative")
        if time_elapsed_hours < 0:
            raise ValueError("time_elapsed_hours cannot be negative")
        _validate_positive("delta_time_hours", delta_time_hours)

        time_component = base_price * math.exp(-decay_rate * time_elapsed_hours)
        demand_velocity = delta_units / delta_time_hours
        demand_component = slope * demand_velocity
        quoted_price = max(time_component + demand_component, 0.0)

        catalog_match = any(
            entry.get("name") == requested_skill for entry in (available_skills or [])
        )
        dispatch_reference = (
            f"{requested_skill}:{agent_id}:{datetime.now(timezone.utc).timestamp():.0f}"
        )
        billing_breakdown = {
            "time_component": round(time_component, 4),
            "demand_component": round(demand_component, 4),
            "demand_velocity": round(demand_velocity, 6),
        }

        data = {
            "agent_id": agent_id,
            "requested_skill": requested_skill,
            "dispatch_reference": dispatch_reference,
            "quoted_price": round(quoted_price, 4),
            "billing_breakdown": billing_breakdown,
            "catalog_match": catalog_match,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("watering_hole_order_router", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _validate_positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
