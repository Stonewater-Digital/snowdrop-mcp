"""
Executive Summary: Conditional value-at-risk optimizer implementing Rockafellar-Uryasev tail minimization under return targets.
Inputs: scenario_returns (list[list[float]]), confidence_level (float), target_return (float), min_weight (float), max_weight (float)
Outputs: optimal_weights (list[float]), expected_return (float), conditional_var (float), value_at_risk (float)
MCP Tool Name: mean_cvar_optimizer
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

import numpy as np

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "mean_cvar_optimizer",
    "description": (
        "Minimizes portfolio conditional VaR via Rockafellar-Uryasev subgradient descent "
        "with simplex projection and optional target return constraint."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "scenario_returns": {
                "type": "array",
                "description": "Matrix of scenario returns (rows=scenarios, cols=assets) in decimals.",
                "items": {
                    "type": "array",
                    "items": {"type": "number", "description": "Asset return in scenario"},
                },
            },
            "confidence_level": {
                "type": "number",
                "description": "Tail confidence (e.g., 0.95) used for VaR / CVaR calculation.",
            },
            "target_return": {
                "type": "number",
                "description": "Optional minimum expected return target; penalty enforced if breached.",
            },
            "min_weight": {
                "type": "number",
                "description": "Lower bound for each asset weight (default 0).",
            },
            "max_weight": {
                "type": "number",
                "description": "Upper bound per asset (default 1).",
            },
            "learning_rate": {
                "type": "number",
                "description": "Gradient step size for CVaR minimization (default 0.05).",
            },
            "iterations": {
                "type": "integer",
                "description": "Number of gradient iterations (default 250).",
            },
        },
        "required": ["scenario_returns", "confidence_level"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Execution status"},
            "data": {"type": "object", "description": "Optimal weights and diagnostics"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _project_simplex(weights: np.ndarray, min_weight: float, max_weight: float) -> np.ndarray:
    clipped = np.clip(weights, min_weight, max_weight)
    total = clipped.sum()
    if total == 0:
        return np.full_like(clipped, 1 / clipped.size)
    return clipped / total


def mean_cvar_optimizer(
    scenario_returns: List[List[float]],
    confidence_level: float,
    target_return: float | None = None,
    min_weight: float = 0.0,
    max_weight: float = 1.0,
    learning_rate: float = 0.05,
    iterations: int = 250,
    **_: Any,
) -> dict[str, Any]:
    try:
        matrix = np.asarray(scenario_returns, dtype=float)
        if matrix.ndim != 2 or matrix.shape[0] < 10 or matrix.shape[1] < 2:
            raise ValueError("scenario_returns must be (scenarios x assets) with sufficient size")
        if not 0.8 <= confidence_level < 1:
            raise ValueError("confidence_level must be within [0.8, 1)")
        if min_weight < 0 or max_weight <= 0 or min_weight >= max_weight:
            raise ValueError("Invalid weight bounds")
        if learning_rate <= 0 or iterations <= 0:
            raise ValueError("learning_rate and iterations must be positive")

        n_assets = matrix.shape[1]
        weights = np.full(n_assets, 1 / n_assets)
        tail_alpha = 1 - confidence_level
        history = []
        for step in range(iterations):
            portfolio_returns = matrix @ weights
            losses = -portfolio_returns
            var_threshold = float(np.quantile(losses, confidence_level))
            tail_mask = losses >= var_threshold - 1e-12
            tail_losses = losses[tail_mask]
            if tail_losses.size == 0:
                cvar = var_threshold
                gradient = np.zeros(n_assets)
            else:
                tail_matrix = matrix[tail_mask]
                cvar = float(var_threshold + tail_losses.mean() - var_threshold)
                gradient = -tail_matrix.mean(axis=0) / (tail_alpha if tail_alpha > 0 else 1e-6)
            expected_return = float(portfolio_returns.mean())
            penalty = 0.0
            if target_return is not None and expected_return < target_return:
                penalty = (target_return - expected_return)
                gradient -= penalty * matrix.mean(axis=0)
            weights = _project_simplex(weights - learning_rate * gradient, min_weight, max_weight)
            history.append(
                {
                    "iteration": step,
                    "expected_return": round(expected_return, 6),
                    "value_at_risk": round(var_threshold, 6),
                    "conditional_var": round(float(tail_losses.mean()) if tail_losses.size else round(var_threshold, 6), 6),
                }
            )

        final_returns = matrix @ weights
        losses = -final_returns
        var_threshold = float(np.quantile(losses, confidence_level))
        tail_mask = losses >= var_threshold - 1e-12
        tail_losses = losses[tail_mask]
        cvar = float(var_threshold if tail_losses.size == 0 else tail_losses.mean())

        data = {
            "optimal_weights": weights.round(6).tolist(),
            "expected_return": round(float(final_returns.mean()), 6),
            "value_at_risk": round(var_threshold, 6),
            "conditional_var": round(cvar, 6),
            "iterations": iterations,
            "convergence": history[-10:],
            "tail_sample_size": int(tail_losses.size),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"mean_cvar_optimizer failed: {e}")
        _log_lesson(f"mean_cvar_optimizer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
