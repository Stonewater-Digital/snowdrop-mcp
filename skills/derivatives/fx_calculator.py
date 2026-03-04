"""FX forward calculator."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "fx_calculator",
    "description": "Computes FX forward rates via covered interest parity and related metrics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot_rate": {"type": "number", "description": "Spot FX rate (domestic per foreign unit, e.g. USD/EUR). Must be > 0."},
            "domestic_rate_pct": {"type": "number", "description": "Domestic interest rate as a percentage (simple, actual/360)."},
            "foreign_rate_pct": {"type": "number", "description": "Foreign interest rate as a percentage (simple, actual/360)."},
            "days_to_maturity": {"type": "integer", "description": "Number of days to forward delivery (must be >= 1)."},
            "notional_domestic": {"type": "number", "description": "Domestic currency notional amount."},
        },
        "required": [
            "spot_rate",
            "domestic_rate_pct",
            "foreign_rate_pct",
            "days_to_maturity",
            "notional_domestic",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "forward_rate": {"type": "number"},
                    "forward_points": {"type": "number"},
                    "swap_points_annualized_pct": {"type": "number"},
                    "notional_foreign": {"type": "number"},
                    "uip_implied_appreciation_pct": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def fx_calculator(
    spot_rate: float,
    domestic_rate_pct: float,
    foreign_rate_pct: float,
    days_to_maturity: int,
    notional_domestic: float,
    **_: Any,
) -> dict[str, Any]:
    """Return FX forward rate, swap points, and notional conversion.

    Uses covered interest parity (CIP):
        F = S * (1 + r_d * T) / (1 + r_f * T)
    where T = days / 360.

    Args:
        spot_rate: Spot rate (domestic per foreign). Must be > 0.
        domestic_rate_pct: Domestic simple interest rate as a percentage.
        foreign_rate_pct: Foreign simple interest rate as a percentage.
        days_to_maturity: Days to forward delivery. Must be >= 1.
        notional_domestic: Domestic currency amount.

    Returns:
        dict with forward_rate, forward_points, swap_points_annualized_pct,
        notional_foreign, uip_implied_appreciation_pct.
    """
    try:
        if spot_rate <= 0:
            raise ValueError("spot_rate must be positive")
        if days_to_maturity < 1:
            raise ValueError("days_to_maturity must be at least 1")
        if notional_domestic <= 0:
            raise ValueError("notional_domestic must be positive")

        year_fraction = days_to_maturity / 360.0
        rd = domestic_rate_pct / 100.0
        rf = foreign_rate_pct / 100.0

        denom = 1 + rf * year_fraction
        if denom == 0:
            raise ValueError("Foreign rate produces zero denominator")

        forward_rate = spot_rate * (1 + rd * year_fraction) / denom
        forward_points = forward_rate - spot_rate
        swap_points_annualized_pct = (forward_points / spot_rate) / year_fraction * 100
        notional_foreign = notional_domestic / forward_rate
        # UIP: expected appreciation = interest rate differential (simplified)
        uip = (rd - rf) * year_fraction * 100

        data = {
            "forward_rate": round(forward_rate, 6),
            "forward_points": round(forward_points, 6),
            "swap_points_annualized_pct": round(swap_points_annualized_pct, 4),
            "notional_foreign": round(notional_foreign, 2),
            "uip_implied_appreciation_pct": round(uip, 4),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson(f"fx_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
