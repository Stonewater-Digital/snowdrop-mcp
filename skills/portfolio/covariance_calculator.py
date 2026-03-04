"""Calculate the sample covariance between two series.

MCP Tool Name: covariance_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "covariance_calculator",
    "description": (
        "Calculates the sample covariance between two data series, measuring "
        "how they vary together."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "series_a": {
                "type": "array",
                "items": {"type": "number"},
                "description": "First data series.",
            },
            "series_b": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Second data series (same length as series_a).",
            },
        },
        "required": ["series_a", "series_b"],
    },
}


def covariance_calculator(
    series_a: list[float], series_b: list[float]
) -> dict[str, Any]:
    """Calculate sample covariance."""
    try:
        import statistics

        series_a = [float(x) for x in series_a]
        series_b = [float(x) for x in series_b]

        if len(series_a) != len(series_b):
            raise ValueError("series_a and series_b must have the same length.")
        if len(series_a) < 2:
            raise ValueError("Need at least 2 data points.")

        n = len(series_a)
        mean_a = statistics.mean(series_a)
        mean_b = statistics.mean(series_b)

        cov = sum((a - mean_a) * (b - mean_b) for a, b in zip(series_a, series_b)) / (n - 1)

        return {
            "status": "ok",
            "data": {
                "covariance": round(cov, 8),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
