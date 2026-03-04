"""
Execuve Summary: Runs a Monte Carlo simulation to estimate VaR.
Inputs: mean_return (float), volatility (float), num_simulations (int), confidence_level (float), horizon_days (int)
Outputs: var_amount (float), var_pct (float), expected_shortfall (float), percentile_table (dict)
MCP Tool Name: value_at_risk_montecarlo
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

_LCG_STATE = 987654321
TRADING_DAYS = 252

TOOL_META = {
    "name": "value_at_risk_montecarlo",
    "description": "Simulates returns via a Gaussian process to estimate VaR and expected shortfall.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "mean_return": {"type": "number", "description": "Expected daily return (decimal)."},
            "volatility": {"type": "number", "description": "Daily volatility (standard deviation)."},
            "num_simulations": {"type": "integer", "description": "Number of Monte Carlo paths."},
            "confidence_level": {"type": "number", "description": "Confidence level between 0 and 1."},
            "horizon_days": {"type": "integer", "description": "Holding period in days."}
        },
        "required": ["mean_return", "volatility", "num_simulations", "confidence_level", "horizon_days"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def value_at_risk_montecarlo(**kwargs: Any) -> dict:
    """Runs Box-Muller generated scenarios to compute VaR and ES."""
    try:
        mean_return = kwargs.get("mean_return")
        volatility = kwargs.get("volatility")
        num_simulations = kwargs.get("num_simulations")
        confidence = kwargs.get("confidence_level")
        horizon = kwargs.get("horizon_days")

        for label, value in (("mean_return", mean_return), ("volatility", volatility), ("confidence_level", confidence)):
            if not isinstance(value, (int, float)):
                raise ValueError(f"{label} must be numeric")
        if not isinstance(num_simulations, int) or num_simulations <= 0:
            raise ValueError("num_simulations must be positive integer")
        if not isinstance(horizon, int) or horizon <= 0:
            raise ValueError("horizon_days must be positive integer")
        if not 0.5 < confidence < 0.999:
            raise ValueError("confidence_level must be between 0.5 and 0.999")

        path_returns = []
        drift = mean_return * horizon
        vol_term = volatility * math.sqrt(horizon)
        for _ in range(num_simulations):
            draw = _std_normal()
            simulated = drift + vol_term * draw
            path_returns.append(simulated)

        path_returns.sort()
        index = max(0, int((1 - confidence) * num_simulations) - 1)
        var_pct = -path_returns[index]
        tail = path_returns[: index + 1]
        expected_shortfall = -sum(tail) / len(tail)
        percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
        percentile_table = {}
        for pct in percentiles:
            pos = int((pct / 100) * (num_simulations - 1))
            percentile_table[str(pct)] = path_returns[pos]

        return {
            "status": "success",
            "data": {
                "var_amount": var_pct,
                "var_pct": var_pct,
                "expected_shortfall": expected_shortfall,
                "percentile_table": percentile_table
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"value_at_risk_montecarlo failed: {e}")
        _log_lesson(f"value_at_risk_montecarlo: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _std_normal() -> float:
    u1 = max(_uniform(), 1e-12)
    u2 = _uniform()
    return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)


def _uniform() -> float:
    global _LCG_STATE
    _LCG_STATE = (1664525 * _LCG_STATE + 1013904223) % (2 ** 32)
    return _LCG_STATE / (2 ** 32)


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
