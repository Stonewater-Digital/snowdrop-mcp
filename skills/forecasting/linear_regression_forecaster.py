"""Linear regression forecaster with confidence band."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "linear_regression_forecaster",
    "description": "Fits y = mx + b and projects forward values with r-squared diagnostics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "data_points": {"type": "array", "items": {"type": "object"}},
            "forecast_periods": {"type": "integer", "default": 6},
        },
        "required": ["data_points"],
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


def linear_regression_forecaster(
    data_points: list[dict[str, float]],
    forecast_periods: int = 6,
    **_: Any,
) -> dict[str, Any]:
    """Return slope, intercept, r^2, and forecast path."""
    try:
        if len(data_points) < 2:
            raise ValueError("At least two data_points required")
        if forecast_periods <= 0:
            raise ValueError("forecast_periods must be positive")

        xs = [float(point["x"]) for point in data_points]
        ys = [float(point["y"]) for point in data_points]
        mean_x = sum(xs) / len(xs)
        mean_y = sum(ys) / len(ys)
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        denominator = sum((x - mean_x) ** 2 for x in xs)
        if denominator == 0:
            raise ValueError("x values cannot all be identical")
        slope = numerator / denominator
        intercept = mean_y - slope * mean_x
        residuals = [y - (slope * x + intercept) for x, y in zip(xs, ys)]
        ss_res = sum(res ** 2 for res in residuals)
        ss_tot = sum((y - mean_y) ** 2 for y in ys)
        r_squared = 1 - ss_res / ss_tot if ss_tot else 0.0
        std_error = math.sqrt(ss_res / (len(xs) - 2)) if len(xs) > 2 else 0.0

        last_x = max(xs)
        forecast = []
        for i in range(1, forecast_periods + 1):
            future_x = last_x + i
            pred_y = slope * future_x + intercept
            forecast.append(
                {
                    "x": future_x,
                    "y": round(pred_y, 4),
                    "lower": round(pred_y - std_error, 4),
                    "upper": round(pred_y + std_error, 4),
                }
            )

        data = {
            "slope": round(slope, 4),
            "intercept": round(intercept, 4),
            "r_squared": round(r_squared, 4),
            "confidence_band": {"plus_minus": round(std_error, 4)},
            "forecasted_values": forecast,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("linear_regression_forecaster", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
