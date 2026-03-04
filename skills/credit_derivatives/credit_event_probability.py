"""
Executive Summary: Converts hazard rates into marginal and cumulative default probabilities across a CDS curve.
Inputs: hazard_rates (list[float]), time_grid_years (list[float])
Outputs: status (str), timestamp (str), data (dict)
MCP Tool Name: credit_event_probability
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "credit_event_probability",
    "description": "Transforms piecewise hazard rates into survival, marginal default probabilities, and event odds per tenor.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "hazard_rates": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Piecewise-constant hazard rates (decimal) for each interval."
            },
            "time_grid_years": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Time grid endpoints in years corresponding to each hazard rate."
            }
        },
        "required": ["hazard_rates", "time_grid_years"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["status", "timestamp"]
    }
}


def credit_event_probability(**kwargs: Any) -> dict[str, Any]:
    try:
        hazard_rates = _clean_vector(kwargs["hazard_rates"])
        time_grid = _clean_vector(kwargs["time_grid_years"])
        if len(hazard_rates) != len(time_grid):
            raise ValueError("hazard_rates and time_grid_years must align")

        survival = 1.0
        prev_t = 0.0
        survival_curve = []
        marginal_pd = []
        cumulative_pd = []

        for hazard, t in zip(hazard_rates, time_grid):
            if t <= prev_t:
                raise ValueError("time grid must be strictly increasing")
            delta = t - prev_t
            s_new = survival * math.exp(-hazard * delta)
            marginal = survival - s_new
            survival_curve.append(s_new)
            marginal_pd.append(marginal)
            cumulative_pd.append(1 - s_new)
            survival = s_new
            prev_t = t

        data = {
            "survival_probabilities": survival_curve,
            "marginal_default_probabilities": marginal_pd,
            "cumulative_default_probabilities": cumulative_pd,
            "time_grid_years": time_grid
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error("credit_event_probability failed: %s", e)
        _log_lesson(f"credit_event_probability: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _clean_vector(values: Sequence[Any]) -> list[float]:
    if not values:
        raise ValueError("Input vectors must be non-empty")
    result: list[float] = []
    for value in values:
        result.append(float(value))
    return result


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
