"""Calculate the Pearson correlation coefficient between two series.

MCP Tool Name: correlation_calculator
"""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "correlation_calculator",
    "description": (
        "Calculates the Pearson correlation coefficient between two data series, "
        "measuring the linear relationship between them."
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


def correlation_calculator(
    series_a: list[float], series_b: list[float]
) -> dict[str, Any]:
    """Calculate Pearson correlation coefficient."""
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
        std_a = statistics.stdev(series_a)
        std_b = statistics.stdev(series_b)

        if std_a == 0 or std_b == 0:
            raise ValueError("Standard deviation of one or both series is zero.")

        correlation = cov / (std_a * std_b)

        return {
            "status": "ok",
            "data": {
                "correlation": round(correlation, 6),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
