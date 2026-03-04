"""
Executive Summary: Black-Litterman optimizer blending CAPM equilibrium returns with investor views for stable allocations.
Inputs: market_weights (list[float]), covariance_matrix (list[list[float]]), views (list[dict]), risk_aversion (float), tau (float)
Outputs: posterior_returns (list[float]), posterior_covariance (list[list[float]]), optimal_weights (list[float]), view_marginals (list[dict])
MCP Tool Name: black_litterman_optimizer
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

import numpy as np

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "black_litterman_optimizer",
    "description": (
        "Computes Black-Litterman posterior returns and optimal weights using CAPM equilibrium "
        "implied returns blended with confidence-weighted views per He and Litterman (1999)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "market_weights": {
                "type": "array",
                "description": "Market capitalization weights representing the equilibrium portfolio.",
                "items": {"type": "number"},
            },
            "covariance_matrix": {
                "type": "array",
                "description": "Positive-definite covariance matrix of asset returns (decimal).",
                "items": {
                    "type": "array",
                    "description": "Row of the covariance matrix",
                    "items": {"type": "number", "description": "Covariance entry"},
                },
            },
            "views": {
                "type": "array",
                "description": (
                    "List of views, each with assets dict (asset->exposure), view_return, and confidence (0-1)."
                ),
                "items": {
                    "type": "object",
                    "properties": {
                        "assets": {
                            "type": "object",
                            "description": "Mapping of asset names or indices to exposure weights in the view.",
                            "additionalProperties": {"type": "number"},
                        },
                        "view_return": {
                            "type": "number",
                            "description": "Expected return (decimal) for the view portfolio.",
                        },
                        "confidence": {
                            "type": "number",
                            "description": "Confidence level between 0 and 1 controlling Omega (higher = tighter).",
                        },
                    },
                    "required": ["assets", "view_return", "confidence"],
                },
            },
            "risk_aversion": {
                "type": "number",
                "description": "Risk aversion (lambda) typically estimated from market Sharpe (default 3).",
            },
            "tau": {
                "type": "number",
                "description": "Scalar scaling prior uncertainty; standard BL uses small value like 0.05.",
            },
            "asset_labels": {
                "type": "array",
                "description": "Optional labels for assets; defaults to indices.",
                "items": {"type": "string"},
            },
        },
        "required": ["market_weights", "covariance_matrix", "views"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Execution status"},
            "data": {"type": "object", "description": "Posterior statistics and allocations"},
            "timestamp": {"type": "string", "description": "UTC ISO timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _build_view_matrix(
    views: List[Dict[str, Any]],
    labels: List[str],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n_assets = len(labels)
    if n_assets == 0:
        raise ValueError("Asset universe cannot be empty")
    p_rows = []
    q_vals = []
    omega_diag = []
    for view in views:
        confidence = float(view.get("confidence", 0.5))
        if not 0 < confidence <= 1:
            raise ValueError("confidence must be within 0-1")
        row = np.zeros(n_assets)
        assets = view.get("assets", {})
        if not assets:
            raise ValueError("Each view must specify asset exposures")
        for key, exposure in assets.items():
            if isinstance(key, int):
                idx = key
            else:
                if key not in labels:
                    raise ValueError(f"Unknown asset label {key}")
                idx = labels.index(key)
            row[idx] = float(exposure)
        p_rows.append(row)
        q_vals.append(float(view["view_return"]))
        omega_diag.append((1 - confidence) + 1e-6)
    return np.array(p_rows), np.array(q_vals), np.diag(omega_diag)


def black_litterman_optimizer(
    market_weights: List[float],
    covariance_matrix: List[List[float]],
    views: List[Dict[str, Any]],
    risk_aversion: float = 3.0,
    tau: float = 0.05,
    asset_labels: List[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    try:
        weights = np.asarray(market_weights, dtype=float)
        cov = np.asarray(covariance_matrix, dtype=float)
        if cov.shape[0] != cov.shape[1] or cov.shape[0] != weights.size:
            raise ValueError("Covariance matrix must be square and match weight length")
        if np.linalg.det(cov) <= 0:
            cov += np.eye(cov.shape[0]) * 1e-9
        labels = asset_labels or [f"asset_{i}" for i in range(weights.size)]
        if len(labels) != weights.size:
            raise ValueError("asset_labels must match number of assets")
        tau = float(tau)
        if tau <= 0:
            raise ValueError("tau must be positive")
        risk_aversion = float(risk_aversion)
        if risk_aversion <= 0:
            raise ValueError("risk_aversion must be positive")

        implied_pi = risk_aversion * cov @ weights
        if not views:
            posterior_mean = implied_pi
            posterior_cov = cov
        else:
            p, q, omega_diag = _build_view_matrix(views, labels)
            p_tau = p @ (tau * cov)
            omega = np.diag(np.diag(p_tau @ p.T))
            scaling = np.maximum(np.diag(omega), 1e-9) / np.diag(omega_diag)
            omega = np.diag(scaling)
            middle = np.linalg.inv(tau * cov) + p.T @ np.linalg.inv(omega) @ p
            rhs = np.linalg.inv(tau * cov) @ implied_pi + p.T @ np.linalg.inv(omega) @ q
            posterior_mean = np.linalg.solve(middle, rhs)
            posterior_cov = cov + np.linalg.inv(middle)

        inv_cov = np.linalg.pinv(cov)
        optimal = inv_cov @ posterior_mean / risk_aversion
        optimal = np.maximum(optimal, 0.0)
        if optimal.sum() == 0:
            optimal = np.ones_like(optimal) / optimal.size
        else:
            optimal = optimal / optimal.sum()

        view_marginals = []
        for idx, view in enumerate(views or []):
            p_vec = np.zeros(weights.size)
            for key, exposure in view.get("assets", {}).items():
                asset_idx = key if isinstance(key, int) else labels.index(key)
                p_vec[asset_idx] = float(exposure)
            marginal = float(p_vec @ posterior_mean)
            view_marginals.append(
                {
                    "view_index": idx,
                    "implied_return": round(marginal, 6),
                    "original_target": float(view["view_return"]),
                    "confidence": float(view.get("confidence", 0.5)),
                }
            )

        data = {
            "posterior_returns": posterior_mean.round(8).tolist(),
            "posterior_covariance": posterior_cov.round(8).tolist(),
            "optimal_weights": optimal.round(6).tolist(),
            "equilibrium_returns": implied_pi.round(6).tolist(),
            "view_marginals": view_marginals,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError, np.linalg.LinAlgError) as e:
        logger.error(f"black_litterman_optimizer failed: {e}")
        _log_lesson(f"black_litterman_optimizer: {e}")
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
