"""
Executive Summary: Equal-risk-contribution allocator solving the Euler risk-budgeting system via Newton projection.
Inputs: covariance_matrix (list[list[float]]), risk_budgets (list[float]), tolerance (float), max_iterations (int)
Outputs: weights (list[float]), risk_contributions (list[dict]), iteration_count (int)
MCP Tool Name: risk_budgeting_allocator
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

import numpy as np

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "risk_budgeting_allocator",
    "description": (
        "Computes equal-risk-contribution weights (a la Maillard, Roncalli, Teiletche 2010) by solving for "
        "the portfolio weights whose marginal contributions match risk budgets."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "covariance_matrix": {
                "type": "array",
                "description": "Covariance matrix of asset returns.",
                "items": {
                    "type": "array",
                    "items": {"type": "number"},
                },
            },
            "risk_budgets": {
                "type": "array",
                "description": "Target share of total risk contributed by each asset (sums to 1).",
                "items": {"type": "number"},
            },
            "tolerance": {
                "type": "number",
                "description": "Stopping tolerance for Euler equation residuals (default 1e-6).",
            },
            "max_iterations": {
                "type": "integer",
                "description": "Maximum Newton steps (default 200).",
            },
        },
        "required": ["covariance_matrix"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Execution status"},
            "data": {"type": "object", "description": "Weights and contribution detail"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def risk_budgeting_allocator(
    covariance_matrix: List[List[float]],
    risk_budgets: List[float] | None = None,
    tolerance: float = 1e-6,
    max_iterations: int = 200,
    **_: Any,
) -> dict[str, Any]:
    try:
        cov = np.asarray(covariance_matrix, dtype=float)
        if cov.shape[0] != cov.shape[1]:
            raise ValueError("Covariance matrix must be square")
        n = cov.shape[0]
        if risk_budgets is None:
            budgets = np.full(n, 1 / n)
        else:
            budgets = np.asarray(risk_budgets, dtype=float)
            if budgets.size != n:
                raise ValueError("risk_budgets must match asset count")
            if (budgets < 0).any():
                raise ValueError("risk_budgets cannot be negative")
            budgets = budgets / budgets.sum()
        weights = np.full(n, 1 / n)
        iteration = 0
        for iteration in range(1, max_iterations + 1):
            marginal = cov @ weights
            risk_contrib = weights * marginal
            total_risk = risk_contrib.sum()
            if total_risk <= 0:
                raise ValueError("Total portfolio variance must be positive")
            target = budgets * total_risk
            residual = risk_contrib - target
            if np.linalg.norm(residual, ord=1) < tolerance:
                break
            gradient = marginal + cov @ weights
            step = 0.5 / np.sqrt(iteration)
            weights = np.maximum(weights - step * residual / gradient, 1e-6)
            weights /= weights.sum()
        risk_details = [
            {
                "asset_index": idx,
                "weight": round(float(weights[idx]), 6),
                "risk_contribution": round(float(risk_contrib[idx] / total_risk), 6),
                "target": round(float(budgets[idx]), 6),
            }
            for idx in range(n)
        ]
        data = {
            "weights": weights.round(6).tolist(),
            "risk_contributions": risk_details,
            "iteration_count": iteration,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"risk_budgeting_allocator failed: {e}")
        _log_lesson(f"risk_budgeting_allocator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as sink:
            sink.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
