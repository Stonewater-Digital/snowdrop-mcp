"""
Executive Summary: Monte Carlo VaR using correlated normal shocks and Basel square-root-of-time scaling.
Inputs: expected_returns (list[float]), covariance_matrix (list[list[float]]), num_simulations (int), horizon_days (int), confidence_level (float)
Outputs: value_at_risk (float), expected_shortfall (float), percentile_losses (dict), worst_case_loss (float)
MCP Tool Name: monte_carlo_var
"""
import logging
import random
from datetime import datetime, timezone
from math import sqrt
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "monte_carlo_var",
    "description": "Monte Carlo VaR/ES with Cholesky-based correlated shocks consistent with Basel 99% methodologies.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "expected_returns": {
                "type": "array",
                "description": "Expected daily returns per asset expressed in decimals.",
                "items": {"type": "number"},
            },
            "covariance_matrix": {
                "type": "array",
                "description": "Positive semi-definite covariance matrix aligned with expected_returns order.",
                "items": {
                    "type": "array",
                    "items": {"type": "number", "description": "Covariance entry"},
                    "description": "Matrix row",
                },
            },
            "num_simulations": {
                "type": "integer",
                "description": "Number of Monte Carlo draws for the loss distribution.",
            },
            "horizon_days": {
                "type": "integer",
                "description": "Holding period for scaling simulated returns.",
            },
            "confidence_level": {
                "type": "number",
                "description": "Confidence level for VaR, e.g., 0.99.",
            },
        },
        "required": [
            "expected_returns",
            "covariance_matrix",
            "num_simulations",
            "horizon_days",
            "confidence_level",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "VaR details"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _cholesky(matrix: List[List[float]]) -> List[List[float]]:
    n = len(matrix)
    lower = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            sum_val = matrix[i][j]
            for k in range(j):
                sum_val -= lower[i][k] * lower[j][k]
            if i == j:
                if sum_val <= 0:
                    raise ValueError("covariance_matrix must be positive definite")
                lower[i][j] = sqrt(sum_val)
            else:
                lower[i][j] = sum_val / lower[j][j]
    return lower


def monte_carlo_var(
    expected_returns: List[float],
    covariance_matrix: List[List[float]],
    num_simulations: int,
    horizon_days: int,
    confidence_level: float,
    **_: Any,
) -> dict[str, Any]:
    try:
        if not 0 < confidence_level < 1:
            raise ValueError("confidence_level must be between 0 and 1")
        if horizon_days <= 0:
            raise ValueError("horizon_days must be positive")
        if num_simulations <= 0:
            raise ValueError("num_simulations must be positive")
        num_assets = len(expected_returns)
        if num_assets == 0:
            raise ValueError("expected_returns required")
        if len(covariance_matrix) != num_assets:
            raise ValueError("covariance_matrix must match expected_returns length")
        for row in covariance_matrix:
            if len(row) != num_assets:
                raise ValueError("covariance_matrix must be square")

        chol = _cholesky(covariance_matrix)
        sqrt_horizon = sqrt(horizon_days)

        simulated_losses = []
        for _ in range(num_simulations):
            z = [random.gauss(0, 1) for _ in range(num_assets)]
            correlated = []
            for i in range(num_assets):
                value = 0.0
                for k in range(i + 1):
                    value += chol[i][k] * z[k]
                correlated.append(value)
            scenario_return = sum(
                (mu * horizon_days) + correlated[i] * sqrt_horizon for i, mu in enumerate(expected_returns)
            )
            simulated_losses.append(-scenario_return)

        simulated_losses.sort()
        index = max(int(confidence_level * num_simulations) - 1, 0)
        var_value = simulated_losses[index]
        tail_losses = simulated_losses[index:]
        es = sum(tail_losses) / len(tail_losses) if tail_losses else var_value

        percentiles = {}
        for p in (0.95, 0.975, 0.99):
            idx = max(int(p * num_simulations) - 1, 0)
            percentiles[str(int(p * 100))] = simulated_losses[idx]

        data = {
            "value_at_risk": round(var_value, 6),
            "expected_shortfall": round(es, 6),
            "simulation_percentiles": percentiles,
            "worst_case_loss": round(simulated_losses[-1], 6),
            "num_simulations": num_simulations,
            "confidence_level": confidence_level,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"monte_carlo_var failed: {e}")
        _log_lesson(f"monte_carlo_var: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as handle:
            handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
