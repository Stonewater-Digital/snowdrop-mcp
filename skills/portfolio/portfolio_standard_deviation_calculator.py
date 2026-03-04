"""Calculate portfolio standard deviation from weights and a returns matrix.

MCP Tool Name: portfolio_standard_deviation_calculator
"""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "portfolio_standard_deviation_calculator",
    "description": (
        "Calculates portfolio standard deviation (volatility) from weights and a "
        "matrix of asset returns as sqrt(w^T * Cov * w)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "weights": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of portfolio weights (should sum to 1).",
            },
            "returns_matrix": {
                "type": "array",
                "items": {"type": "array", "items": {"type": "number"}},
                "description": "List of lists; each inner list is the return series for one asset.",
            },
        },
        "required": ["weights", "returns_matrix"],
    },
}


def portfolio_standard_deviation_calculator(
    weights: list[float], returns_matrix: list[list[float]]
) -> dict[str, Any]:
    """Calculate portfolio standard deviation."""
    try:
        import statistics

        weights = [float(w) for w in weights]
        returns_matrix = [[float(r) for r in series] for series in returns_matrix]

        n_assets = len(weights)
        if n_assets != len(returns_matrix):
            raise ValueError("Number of weights must match number of asset return series.")
        if n_assets == 0:
            raise ValueError("Must have at least one asset.")

        n_periods = len(returns_matrix[0])
        for series in returns_matrix:
            if len(series) != n_periods:
                raise ValueError("All return series must have the same length.")
        if n_periods < 2:
            raise ValueError("Need at least 2 return periods.")

        means = [statistics.mean(series) for series in returns_matrix]

        cov = [[0.0] * n_assets for _ in range(n_assets)]
        for i in range(n_assets):
            for j in range(n_assets):
                cov[i][j] = sum(
                    (returns_matrix[i][t] - means[i]) * (returns_matrix[j][t] - means[j])
                    for t in range(n_periods)
                ) / (n_periods - 1)

        variance = 0.0
        for i in range(n_assets):
            for j in range(n_assets):
                variance += weights[i] * weights[j] * cov[i][j]

        std_dev = math.sqrt(max(variance, 0.0))

        return {
            "status": "ok",
            "data": {
                "portfolio_standard_deviation": round(std_dev, 10),
                "portfolio_variance": round(variance, 10),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
