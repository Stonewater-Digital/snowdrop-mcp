"""Analyze futures roll economics."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "futures_roll_analyzer",
    "description": "Evaluates roll cost, carry, and recommendation for futures positions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "front_price": {"type": "number"},
            "back_price": {"type": "number"},
            "days_to_expiry": {"type": "integer"},
            "position_size": {"type": "number"},
            "contract_value": {"type": "number"},
        },
        "required": [
            "front_price",
            "back_price",
            "days_to_expiry",
            "position_size",
            "contract_value",
        ],
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


def futures_roll_analyzer(
    front_price: float,
    back_price: float,
    days_to_expiry: int,
    position_size: float,
    contract_value: float,
    **_: Any,
) -> dict[str, Any]:
    """Return roll cost, carry, and recommendation."""
    try:
        days_to_expiry = max(days_to_expiry, 1)
        roll_cost = (back_price - front_price) * position_size
        annualized_roll_cost_pct = ((back_price / front_price) - 1) * (365 / days_to_expiry)
        carry_pct = (contract_value + roll_cost) / contract_value - 1 if contract_value else 0.0
        recommendation = "roll_later"
        if annualized_roll_cost_pct < -0.02:
            recommendation = "roll_now"
        elif annualized_roll_cost_pct > 0.02:
            recommendation = "hold"
        data = {
            "roll_cost": round(roll_cost, 2),
            "annualized_roll_cost_pct": round(annualized_roll_cost_pct * 100, 2),
            "carry_pct": round(carry_pct * 100, 2),
            "roll_recommendation": recommendation,
        }
        return {"status": "ok", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        try:
            with open("logs/lessons.md", "a") as _f:
                _f.write(f"- [{datetime.now(timezone.utc).isoformat()}] futures_roll_analyzer: {exc}\n")
        except OSError:
            pass
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
