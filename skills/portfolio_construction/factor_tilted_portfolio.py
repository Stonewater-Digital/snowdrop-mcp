"""
Executive Summary: Factor-tilted portfolio builder pushing benchmark weights toward desired factor exposures while controlling tracking error.
Inputs: benchmark_weights (list[float]), factor_exposures (dict[str, list[float]]), target_shifts (dict[str, float]), covariance_matrix (list[list[float]])
Outputs: tilted_weights (list[float]), factor_exposure_delta (list[dict]), tracking_error (float), constraint_shadow_cost (float)
MCP Tool Name: factor_tilted_portfolio
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

import numpy as np

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "factor_tilted_portfolio",
    "description": (
        "Implements Barra-style factor tilting by solving a constrained least-squares system to match "
        "target factor shifts while minimizing benchmark deviation."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "benchmark_weights": {
                "type": "array",
                "description": "Benchmark constituent weights summing to unity.",
                "items": {"type": "number"},
            },
            "factor_exposures": {
                "type": "object",
                "description": "Factor exposure matrix keyed by factor name with values per asset.",
                "additionalProperties": {
                    "type": "array",
                    "items": {"type": "number", "description": "Asset exposure"},
                },
            },
            "target_shifts": {
                "type": "object",
                "description": "Desired exposure change for each factor (positive = overweight).",
                "additionalProperties": {"type": "number"},
            },
            "covariance_matrix": {
                "type": "array",
                "description": "Optional covariance matrix for tracking error estimation.",
                "items": {
                    "type": "array",
                    "items": {"type": "number", "description": "Covariance entry"},
                },
            },
            "max_active_weight": {
                "type": "number",
                "description": "Absolute cap on deviation from benchmark for each asset (default 0.05).",
            },
            "regularization": {
                "type": "number",
                "description": "Ridge penalty applied to weight changes (default 1e-4).",
            },
        },
        "required": ["benchmark_weights", "factor_exposures", "target_shifts"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Execution status"},
            "data": {"type": "object", "description": "Post-tilt weights and diagnostics"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def factor_tilted_portfolio(
    benchmark_weights: List[float],
    factor_exposures: Dict[str, List[float]],
    target_shifts: Dict[str, float],
    covariance_matrix: List[List[float]] | None = None,
    max_active_weight: float = 0.05,
    regularization: float = 1e-4,
    **_: Any,
) -> dict[str, Any]:
    try:
        base = np.asarray(benchmark_weights, dtype=float)
        if base.ndim != 1 or base.size == 0:
            raise ValueError("benchmark_weights must be one-dimensional")
        if abs(base.sum() - 1.0) > 1e-4:
            base = base / base.sum()
        factors = sorted(factor_exposures.keys())
        exposure_matrix = np.vstack([factor_exposures[f] for f in factors]).astype(float)
        if exposure_matrix.shape[1] != base.size:
            raise ValueError("Factor exposures must align with benchmark assets")
        desired_shift = np.array([target_shifts.get(f, 0.0) for f in factors], dtype=float)
        baseline = exposure_matrix @ base
        target_exposure = baseline + desired_shift
        # Build augmented system to maintain weight sum = 1
        A = np.vstack([exposure_matrix, np.ones((1, base.size))])
        b = np.concatenate([target_exposure, np.array([1.0])])
        ridge = regularization * np.eye(base.size)
        lhs = A.T @ A + ridge
        rhs = A.T @ b
        solution = np.linalg.solve(lhs, rhs)
        active = np.clip(solution - base, -max_active_weight, max_active_weight)
        tilted = base + active
        tilted = np.clip(tilted, 0.0, None)
        tilted = tilted / tilted.sum()
        factor_after = exposure_matrix @ tilted
        factor_changes = []
        for idx, factor in enumerate(factors):
            factor_changes.append(
                {
                    "factor": factor,
                    "baseline": round(float(baseline[idx]), 6),
                    "target": round(float(target_exposure[idx]), 6),
                    "achieved": round(float(factor_after[idx]), 6),
                }
            )
        tracking_error = None
        if covariance_matrix is not None:
            cov = np.asarray(covariance_matrix, dtype=float)
            if cov.shape[0] != cov.shape[1] or cov.shape[0] != base.size:
                raise ValueError("Covariance matrix mismatch")
            diff = tilted - base
            tracking_error = float(np.sqrt(np.maximum(diff @ cov @ diff, 0.0)))
        shadow_cost = float(np.linalg.norm(active, ord=1))
        data = {
            "tilted_weights": tilted.round(6).tolist(),
            "factor_exposure_delta": factor_changes,
            "tracking_error": None if tracking_error is None else round(tracking_error, 6),
            "constraint_shadow_cost": round(shadow_cost, 6),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, np.linalg.LinAlgError) as e:
        logger.error(f"factor_tilted_portfolio failed: {e}")
        _log_lesson(f"factor_tilted_portfolio: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as fptr:
            fptr.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
