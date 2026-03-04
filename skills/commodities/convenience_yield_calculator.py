"""Infer convenience yield from futures and carry inputs."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "convenience_yield_calculator",
    "description": (
        "Solves for implied convenience yield using the continuous cost-of-carry relation: "
        "F = S * exp((r + u - y) * T), rearranged as y = r + u - ln(F/S) / T."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot_price": {
                "type": "number",
                "description": "Current spot price of the commodity (must be > 0).",
            },
            "futures_price": {
                "type": "number",
                "description": "Futures price for the given maturity (must be > 0).",
            },
            "risk_free_rate_pct": {
                "type": "number",
                "description": "Annual continuous risk-free rate as % (e.g. 5.0 = 5%).",
            },
            "storage_cost_pct": {
                "type": "number",
                "default": 0.0,
                "description": "Annual storage cost as % of spot (e.g. 2.0 = 2%). Defaults to 0.",
            },
            "time_to_maturity_years": {
                "type": "number",
                "description": "Time to futures maturity in years (must be > 0).",
            },
        },
        "required": [
            "spot_price",
            "futures_price",
            "risk_free_rate_pct",
            "time_to_maturity_years",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "implied_convenience_yield_pct": {"type": "number"},
            "cost_of_carry_pct": {"type": "number"},
            "theoretical_forward": {"type": "number"},
            "forward_premium_pct": {"type": "number"},
            "timestamp": {"type": "string"},
        },
    },
}


def convenience_yield_calculator(
    spot_price: float,
    futures_price: float,
    risk_free_rate_pct: float,
    storage_cost_pct: float = 0.0,
    time_to_maturity_years: float = 1.0,
    **_: Any,
) -> dict[str, Any]:
    """Return implied convenience yield from cost-of-carry relation.

    Args:
        spot_price: Current commodity spot price (must be > 0).
        futures_price: Observed futures price (must be > 0).
        risk_free_rate_pct: Annual continuous risk-free rate as percent.
        storage_cost_pct: Annual storage cost as percent of spot value. Defaults to 0.
        time_to_maturity_years: Time to futures maturity in years (must be > 0).

    Returns:
        dict with status, implied_convenience_yield_pct, cost_of_carry_pct,
        theoretical_forward (at zero convenience yield), and forward_premium_pct.

    Formula (continuous compounding):
        F = S * exp((r + u - y) * T)
        => y = r + u - ln(F / S) / T

    where r = risk-free rate, u = storage cost rate, y = convenience yield,
    T = time to maturity in years.

    The theoretical_forward is what the futures price would be if convenience
    yield were zero: F_theoretical = S * exp((r + u) * T).
    """
    try:
        if spot_price <= 0:
            raise ValueError("spot_price must be positive")
        if futures_price <= 0:
            raise ValueError("futures_price must be positive")
        if time_to_maturity_years <= 0:
            raise ValueError("time_to_maturity_years must be positive")

        r = risk_free_rate_pct / 100.0
        u = storage_cost_pct / 100.0
        t = time_to_maturity_years

        # Implied convenience yield: y = (r + u) - ln(F/S) / T
        ln_ratio = math.log(futures_price / spot_price)
        implied_y = (r + u) - ln_ratio / t

        # Theoretical forward with zero convenience yield
        theoretical_fwd = spot_price * math.exp((r + u) * t)

        # Forward premium vs spot
        forward_premium = (futures_price / spot_price - 1) * 100

        return {
            "status": "success",
            "implied_convenience_yield_pct": round(implied_y * 100, 4),
            "cost_of_carry_pct": round((r + u) * 100, 4),
            "theoretical_forward": round(theoretical_fwd, 4),
            "forward_premium_pct": round(forward_premium, 4),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("convenience_yield_calculator", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
