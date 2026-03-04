"""
Executive Summary: Tracking-error minimizer aligning factor exposures to mandates using quadratic Lagrange multipliers.
Inputs: benchmark_weights (list[float]), covariance_matrix (list[list[float]]), factor_loadings (dict[str, list[float]]), target_factor_exposure (dict[str, float])
Outputs: optimized_weights (list[float]), achieved_factor_exposures (list[dict]), tracking_error_pct (float)
MCP Tool Name: tracking_error_optimizer
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

import numpy as np

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "tracking_error_optimizer",
    "description": (
        "Minimizes ex-ante tracking error relative to the benchmark while enforcing factor exposure targets via "
        "Lagrangian solution of the quadratic optimization problem."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "benchmark_weights": {
                "type": "array",
                "description": "Benchmark weights summing to 1.",
                "items": {"type": "number"},
            },
            "covariance_matrix": {
                "type": "array",
                "description": "Return covariance matrix used for tracking error calculations.",
                "items": {
                    "type": "array",
                    "items": {"type": "number"},
                },
            },
            "factor_loadings": {
                "type": "object",
                "description": "Matrix of factor loadings keyed by factor name.",
                "additionalProperties": {
                    "type": "array",
                    "items": {"type": "number"},
                },
            },
            "target_factor_exposure": {
                "type": "object",
                "description": "Desired total factor exposure for each factor after optimization.",
                "additionalProperties": {"type": "number"},
            },
        },
        "required": ["benchmark_weights", "covariance_matrix", "factor_loadings", "target_factor_exposure"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Execution status"},
            "data": {"type": "object", "description": "Optimized portfolio metrics"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def tracking_error_optimizer(
    benchmark_weights: List[float],
    covariance_matrix: List[List[float]],
    factor_loadings: Dict[str, List[float]],
    target_factor_exposure: Dict[str, float],
    **_: Any,
) -> dict[str, Any]:
    try:
        bench = np.asarray(benchmark_weights, dtype=float)
        cov = np.asarray(covariance_matrix, dtype=float)
        if cov.shape[0] != cov.shape[1] or cov.shape[0] != bench.size:
            raise ValueError("Covariance matrix dimension mismatch")
        factors = sorted(factor_loadings.keys())
        loadings = np.vstack([factor_loadings[f] for f in factors]).astype(float)
        if loadings.shape[1] != bench.size:
            raise ValueError("Factor loadings must match benchmark assets")
        inv_cov = np.linalg.pinv(cov)
        current_exposure = loadings @ bench
        target = np.array([target_factor_exposure.get(f, current_exposure[idx]) for idx, f in enumerate(factors)])
        delta = target - current_exposure
        if np.allclose(delta, 0):
            optimized = bench
        else:
            middle = loadings @ inv_cov @ loadings.T
            adjustment_lambda = np.linalg.solve(middle + np.eye(middle.shape[0]) * 1e-8, delta)
            active = inv_cov @ loadings.T @ adjustment_lambda
            optimized = bench + active
            optimized = np.maximum(optimized, 0.0)
            optimized /= optimized.sum()
        diff = optimized - bench
        tracking_var = float(diff @ cov @ diff)
        factor_output = []
        achieved = loadings @ optimized
        for idx, factor in enumerate(factors):
            factor_output.append(
                {
                    "factor": factor,
                    "target": round(float(target[idx]), 6),
                    "achieved": round(float(achieved[idx]), 6),
                    "baseline": round(float(current_exposure[idx]), 6),
                }
            )
        data = {
            "optimized_weights": optimized.round(6).tolist(),
            "tracking_error_pct": round(float(np.sqrt(max(tracking_var, 0))) * 100, 4),
            "achieved_factor_exposures": factor_output,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, np.linalg.LinAlgError) as e:
        logger.error(f"tracking_error_optimizer failed: {e}")
        _log_lesson(f"tracking_error_optimizer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as fp:
            fp.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
