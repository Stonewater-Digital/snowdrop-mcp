"""Dynamic bonding curve pricing for The Watering Hole."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "bonding_curve_pricer",
    "description": (
        "Calculates Watering Hole bonding curve prices using time decay, demand velocity, and"
        " snap-back protections."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "base_price": {
                "type": "number",
                "description": "Starting price before decay and demand adjustments (USD).",
            },
            "decay_rate": {
                "type": "number",
                "description": "Exponential decay constant k for time-based cooling.",
            },
            "time_elapsed_hours": {
                "type": "number",
                "description": "Hours since the last pricing event (t).",
            },
            "slope": {
                "type": "number",
                "description": "Demand slope m that translates unit velocity to price delta.",
            },
            "delta_units": {
                "type": "number",
                "description": "Change in filled units since the last evaluation (Δn).",
            },
            "delta_time_hours": {
                "type": "number",
                "description": "Time window in hours for the demand change (Δt).",
            },
            "last_clearing_price": {
                "type": "number",
                "description": "Most recent executed price for snap-back comparisons.",
            },
            "snap_back_threshold_pct": {
                "type": "number",
                "description": (
                    "Maximum allowed deviation (e.g. 0.25 = 25%) from the last clearing price before"
                    " enforcing snap-back caps."
                ),
                "default": 0.25,
            },
        },
        "required": [
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
                    "price": {"type": "number"},
                    "time_component": {"type": "number"},
                    "demand_component": {"type": "number"},
                    "demand_velocity": {"type": "number"},
                    "snap_back_applied": {"type": "boolean"},
                },
            },
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}


def bonding_curve_pricer(
    base_price: float,
    decay_rate: float,
    time_elapsed_hours: float,
    slope: float,
    delta_units: float,
    delta_time_hours: float,
    last_clearing_price: float | None = None,
    snap_back_threshold_pct: float = 0.25,
    **_: Any,
) -> dict[str, Any]:
    """Compute the Watering Hole bonding curve price.

    Args:
        base_price: Starting reference price.
        decay_rate: Exponential cooling constant k.
        time_elapsed_hours: Hours since the last quote.
        slope: Multiplier converting unit velocity to price.
        delta_units: Change in filled units over the evaluation window.
        delta_time_hours: Hours in the measurement window.
        last_clearing_price: Last executed trade price for snap-back control.
        snap_back_threshold_pct: Maximum allowed deviation before capping swings.
        **_: Absorbs unused keyword arguments for MCP compatibility.

    Returns:
        Price components and snap-back diagnostics in the standard skill envelope.
    """
    try:
        if base_price <= 0:
            raise ValueError("base_price must be positive")
        if decay_rate < 0:
            raise ValueError("decay_rate cannot be negative")
        if time_elapsed_hours < 0:
            raise ValueError("time_elapsed_hours cannot be negative")
        if delta_time_hours <= 0:
            raise ValueError("delta_time_hours must be positive")
        if snap_back_threshold_pct < 0:
            raise ValueError("snap_back_threshold_pct cannot be negative")

        time_component = base_price * math.exp(-decay_rate * time_elapsed_hours)
        demand_velocity = delta_units / delta_time_hours
        demand_component = slope * demand_velocity
        quoted_price = time_component + demand_component

        snap_back_applied = False
        if last_clearing_price is not None:
            allowed_move = abs(last_clearing_price) * snap_back_threshold_pct
            deviation = quoted_price - last_clearing_price
            if abs(deviation) > allowed_move:
                quoted_price = last_clearing_price + (
                    allowed_move if deviation > 0 else -allowed_move
                )
                snap_back_applied = True

        result = {
            "price": round(quoted_price, 4),
            "time_component": round(time_component, 4),
            "demand_component": round(demand_component, 4),
            "demand_velocity": round(demand_velocity, 6),
            "snap_back_applied": snap_back_applied,
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("bonding_curve_pricer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
