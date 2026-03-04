"""Calculate portfolio variance from weights and a returns matrix.

MCP Tool Name: portfolio_variance_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "portfolio_variance_calculator",
    "description": (
        "Calculates portfolio variance using weights and a matrix of asset returns. "
        "Computes w^T * Cov * w using the sample covariance matrix."
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


def portfolio_variance_calculator(
    weights: list[float], returns_matrix: list[list[float]]
) -> dict[str, Any]:
    """Calculate portfolio variance from weights and returns matrix."""
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

        # Build covariance matrix
        cov = [[0.0] * n_assets for _ in range(n_assets)]
        for i in range(n_assets):
            for j in range(n_assets):
                cov[i][j] = sum(
                    (returns_matrix[i][t] - means[i]) * (returns_matrix[j][t] - means[j])
                    for t in range(n_periods)
                ) / (n_periods - 1)

        # w^T * Cov * w
        variance = 0.0
        for i in range(n_assets):
            for j in range(n_assets):
                variance += weights[i] * weights[j] * cov[i][j]

        return {
            "status": "ok",
            "data": {
                "portfolio_variance": round(variance, 10),
                "covariance_matrix": [[round(cov[i][j], 8) for j in range(n_assets)] for i in range(n_assets)],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
