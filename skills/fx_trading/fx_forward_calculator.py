"""Compute FX forward rates via covered interest parity."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "fx_forward_calculator",
    "description": "Calculates forward rates, points, and hedging costs for currency hedges.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot_rate": {"type": "number"},
            "domestic_rate": {"type": "number"},
            "foreign_rate": {"type": "number"},
            "tenor_days": {"type": "integer"},
            "notional_base": {"type": "number"},
        },
        "required": ["spot_rate", "domestic_rate", "foreign_rate", "tenor_days", "notional_base"],
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


def fx_forward_calculator(
    spot_rate: float,
    domestic_rate: float,
    foreign_rate: float,
    tenor_days: int,
    notional_base: float,
    **_: Any,
) -> dict[str, Any]:
    """Return forward metrics."""
    try:
        tenor_years = tenor_days / 365
        forward = spot_rate * (1 + domestic_rate * tenor_years) / (1 + foreign_rate * tenor_years)
        forward_points = forward - spot_rate
        forward_premium_pct = forward_points / spot_rate * 100
        annualized = (forward / spot_rate - 1) / tenor_years if tenor_years else 0.0
        hedging_cost = forward_points * notional_base
        data = {
            "forward_rate": round(forward, 6),
            "forward_points": round(forward_points * 10000, 2),
            "forward_premium_pct": round(forward_premium_pct, 4),
            "annualized_premium": round(annualized, 4),
            "hedging_cost_in_base": round(hedging_cost, 2),
            "breakeven_spot_move": round(abs(forward_points), 6),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("fx_forward_calculator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
