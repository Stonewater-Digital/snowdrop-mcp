"""Monte Carlo simulator for portfolio outcomes."""
from __future__ import annotations

import math
import random
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "monte_carlo_simulator",
    "description": "Runs geometric Brownian motion simulations to generate percentile outcomes.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "initial_value": {"type": "number"},
            "expected_annual_return": {"type": "number"},
            "annual_volatility": {"type": "number"},
            "years": {"type": "integer"},
            "num_simulations": {"type": "integer", "default": 1000},
        },
        "required": [
            "initial_value",
            "expected_annual_return",
            "annual_volatility",
            "years",
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


def monte_carlo_simulator(
    initial_value: float,
    expected_annual_return: float,
    annual_volatility: float,
    years: int,
    num_simulations: int = 1000,
    **_: Any,
) -> dict[str, Any]:
    """Return percentile table, probability of loss, and median ending value."""
    try:
        if initial_value <= 0 or annual_volatility < 0 or years <= 0 or num_simulations <= 0:
            raise ValueError("Inputs must be positive")

        rng = random.Random(42)
        final_values: list[float] = []
        dt = 1.0
        drift = expected_annual_return - 0.5 * annual_volatility**2
        for _ in range(num_simulations):
            value = initial_value
            for _ in range(years):
                shock = rng.gauss(0, 1)
                value *= math.exp(drift * dt + annual_volatility * math.sqrt(dt) * shock)
            final_values.append(value)

        final_values.sort()
        percentiles = {
            "p5": round(_percentile(final_values, 0.05), 2),
            "p25": round(_percentile(final_values, 0.25), 2),
            "p50": round(_percentile(final_values, 0.50), 2),
            "p75": round(_percentile(final_values, 0.75), 2),
            "p95": round(_percentile(final_values, 0.95), 2),
        }
        probability_of_loss = sum(value < initial_value for value in final_values) / len(final_values)
        data = {
            "percentiles": percentiles,
            "probability_of_loss": round(probability_of_loss, 3),
            "median_final_value": percentiles["p50"],
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("monte_carlo_simulator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _percentile(values: list[float], percentile: float) -> float:
    index = int(percentile * (len(values) - 1))
    return values[index]


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
