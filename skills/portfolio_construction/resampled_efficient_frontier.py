"""
Executive Summary: Michaud resampled efficient frontier blending bootstrap portfolios for more stable allocations.
Inputs: expected_returns (list[float]), covariance_matrix (list[list[float]]), sample_runs (int), frontier_points (int)
Outputs: resampled_weights (list[float]), efficient_frontier (list[dict]), dispersion_metrics (dict)
MCP Tool Name: resampled_efficient_frontier
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

import numpy as np

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "resampled_efficient_frontier",
    "description": (
        "Applies Michaud resampling by bootstrapping mean-variance inputs and averaging allocations "
        "to produce confidence bands for the efficient frontier."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "expected_returns": {
                "type": "array",
                "description": "Vector of expected returns (decimal) for each asset.",
                "items": {"type": "number"},
            },
            "covariance_matrix": {
                "type": "array",
                "description": "Positive-definite covariance matrix corresponding to expected returns.",
                "items": {
                    "type": "array",
                    "items": {"type": "number", "description": "Covariance entry"},
                },
            },
            "sample_runs": {
                "type": "integer",
                "description": "Number of bootstrap draws for resampling (default 250).",
            },
            "frontier_points": {
                "type": "integer",
                "description": "Granularity of frontier target returns (default 10).",
            },
            "confidence_level": {
                "type": "number",
                "description": "Confidence level for dispersion bands (default 0.9).",
            },
        },
        "required": ["expected_returns", "covariance_matrix"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Execution status"},
            "data": {"type": "object", "description": "Frontier statistics"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _mv_weights(mu: np.ndarray, cov: np.ndarray, target: float) -> np.ndarray:
    inv_cov = np.linalg.pinv(cov)
    ones = np.ones_like(mu)
    A = ones @ inv_cov @ ones
    B = ones @ inv_cov @ mu
    C = mu @ inv_cov @ mu
    denom = A * C - B**2
    if denom == 0:
        return ones / ones.size
    lambda1 = (C - B * target) / denom
    lambda2 = (A * target - B) / denom
    weights = inv_cov @ (lambda1 * ones + lambda2 * mu)
    weights = np.maximum(weights, 0.0)
    if weights.sum() == 0:
        return ones / ones.size
    return weights / weights.sum()


def resampled_efficient_frontier(
    expected_returns: List[float],
    covariance_matrix: List[List[float]],
    sample_runs: int = 250,
    frontier_points: int = 10,
    confidence_level: float = 0.9,
    **_: Any,
) -> dict[str, Any]:
    try:
        mu = np.asarray(expected_returns, dtype=float)
        cov = np.asarray(covariance_matrix, dtype=float)
        if cov.shape[0] != cov.shape[1] or cov.shape[0] != mu.size:
            raise ValueError("Dimension mismatch between returns and covariance")
        if sample_runs <= 0 or frontier_points < 2:
            raise ValueError("sample_runs and frontier_points must be positive")
        if not 0.5 < confidence_level < 1:
            raise ValueError("confidence_level must lie within (0.5, 1)")
        base_vol = np.sqrt(np.clip(np.diag(cov), 1e-9, None)).mean()
        targets = np.linspace(mu.min(), mu.max(), frontier_points)
        bootstrap_weights = np.zeros((sample_runs, frontier_points, mu.size))
        bootstrap_vars = np.zeros((sample_runs, frontier_points))
        rng = np.random.default_rng(42)
        for i in range(sample_runs):
            simulated = rng.multivariate_normal(mu, cov)
            sampled_mu = simulated
            sampled_cov = cov + np.eye(mu.size) * 1e-8
            for j, target in enumerate(targets):
                weights = _mv_weights(sampled_mu, sampled_cov, target)
                bootstrap_weights[i, j] = weights
                bootstrap_vars[i, j] = weights @ cov @ weights
        avg_weights = bootstrap_weights.mean(axis=0)
        lower = np.quantile(bootstrap_weights, (1 - confidence_level) / 2, axis=0)
        upper = np.quantile(bootstrap_weights, 1 - (1 - confidence_level) / 2, axis=0)
        efficient_frontier = []
        for idx, target in enumerate(targets):
            weights = avg_weights[idx]
            variance = float(weights @ cov @ weights)
            efficient_frontier.append(
                {
                    "target_return": round(float(target), 6),
                    "volatility": round(float(np.sqrt(max(variance, 0))), 6),
                    "weight_band": {
                        "lower": lower[idx].round(6).tolist(),
                        "upper": upper[idx].round(6).tolist(),
                    },
                }
            )
        dispersion = {
            "average_variance": float(bootstrap_vars.mean()),
            "variance_confidence_band": [
                float(np.quantile(bootstrap_vars, (1 - confidence_level) / 2)),
                float(np.quantile(bootstrap_vars, 1 - (1 - confidence_level) / 2)),
            ],
        }
        data = {
            "resampled_weights": avg_weights[-1].round(6).tolist(),
            "efficient_frontier": efficient_frontier,
            "dispersion_metrics": dispersion,
            "base_volatility": round(float(base_vol), 6),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, np.linalg.LinAlgError) as e:
        logger.error(f"resampled_efficient_frontier failed: {e}")
        _log_lesson(f"resampled_efficient_frontier: {e}")
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
