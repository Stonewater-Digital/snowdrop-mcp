"""
Executive Summary: Robust covariance estimator combining Ledoit-Wolf shrinkage with a Minimum Covariance Determinant proxy.
Inputs: return_series (list[list[float]]), subset_fraction (float)
Outputs: ledroit_wolf_cov (list[list[float]]), mcd_cov (list[list[float]]), shrinkage_intensity (float)
MCP Tool Name: robust_covariance_estimator
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

import numpy as np

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "robust_covariance_estimator",
    "description": (
        "Produces Ledoit-Wolf shrunk covariance and a Minimum Covariance Determinant (MCD) estimate to stabilize "
        "mean-variance inputs against outliers and regime shifts."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "return_series": {
                "type": "array",
                "description": "Matrix of historical returns (rows=observations, columns=assets).",
                "items": {
                    "type": "array",
                    "items": {"type": "number"},
                },
            },
            "subset_fraction": {
                "type": "number",
                "description": "Fraction of observations used for the MCD subset (default 0.75).",
            },
        },
        "required": ["return_series"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Execution status"},
            "data": {"type": "object", "description": "Robust covariance outputs"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _ledoit_wolf(x: np.ndarray) -> tuple[np.ndarray, float]:
    t, n = x.shape
    mean = x.mean(axis=0, keepdims=True)
    xm = x - mean
    sample = (xm.T @ xm) / (t - 1)
    target = np.diag(np.diag(sample))
    phi_matrix = (xm**2).T @ (xm**2) / t - sample**2
    phi = phi_matrix.sum()
    gamma = np.linalg.norm(sample - target, ord="fro") ** 2
    shrinkage = max(0.0, min(1.0, phi / gamma / t)) if gamma > 0 else 1.0
    shrunk = shrinkage * target + (1 - shrinkage) * sample
    return shrunk, shrinkage


def _mcd_covariance(x: np.ndarray, subset_fraction: float) -> np.ndarray:
    subset_fraction = min(max(subset_fraction, 0.5), 0.9)
    center = np.median(x, axis=0)
    distances = np.linalg.norm(x - center, axis=1)
    subset_size = max(int(len(x) * subset_fraction), x.shape[1] + 1)
    subset_idx = np.argsort(distances)[:subset_size]
    subset = x[subset_idx]
    if subset.shape[0] <= subset.shape[1]:
        raise ValueError("Not enough observations for MCD subset")
    return np.cov(subset.T)


def robust_covariance_estimator(
    return_series: List[List[float]],
    subset_fraction: float = 0.75,
    **_: Any,
) -> dict[str, Any]:
    try:
        matrix = np.asarray(return_series, dtype=float)
        if matrix.ndim != 2 or matrix.shape[0] <= matrix.shape[1]:
            raise ValueError("return_series must have more observations than assets")
        shrunk, shrinkage = _ledoit_wolf(matrix)
        mcd = _mcd_covariance(matrix, subset_fraction)
        data = {
            "ledoit_wolf_cov": shrunk.round(8).tolist(),
            "mcd_cov": mcd.round(8).tolist(),
            "shrinkage_intensity": round(float(shrinkage), 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, np.linalg.LinAlgError) as e:
        logger.error(f"robust_covariance_estimator failed: {e}")
        _log_lesson(f"robust_covariance_estimator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as fh:
            fh.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
