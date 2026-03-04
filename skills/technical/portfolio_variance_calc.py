"""
Executive Summary: Calculate portfolio expected return, variance, standard deviation, Sharpe ratio, and diversification benefit using Modern Portfolio Theory.
Inputs: holdings (list of dicts), correlation_matrix (list of lists of floats)
Outputs: portfolio_return (float), portfolio_std_dev (float), sharpe_ratio (float or null), diversification_benefit (float)
MCP Tool Name: portfolio_variance_calc
"""
import os
import math
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "portfolio_variance_calc",
    "description": "Calculate portfolio expected return, variance, standard deviation, Sharpe ratio, and diversification benefit using Modern Portfolio Theory (MPT).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "holdings": {
                "type": "array",
                "description": "List of holding dicts: asset (str), weight (float, 0-1), expected_return (float, annualized decimal e.g. 0.12 for 12%), std_dev (float, annualized decimal).",
                "items": {
                    "type": "object",
                    "properties": {
                        "asset": {"type": "string"},
                        "weight": {"type": "number"},
                        "expected_return": {"type": "number"},
                        "std_dev": {"type": "number"}
                    },
                    "required": ["asset", "weight", "expected_return", "std_dev"]
                }
            },
            "correlation_matrix": {
                "type": "array",
                "description": "NxN correlation matrix (list of lists of floats in [-1, 1]). Must match number of holdings.",
                "items": {
                    "type": "array",
                    "items": {"type": "number"}
                }
            },
            "risk_free_rate": {
                "type": "number",
                "description": "Annualized risk-free rate (e.g. 0.05 for 5%). If provided, enables Sharpe ratio calculation.",
                "default": None
            }
        },
        "required": ["holdings", "correlation_matrix"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "portfolio_return": {"type": "number"},
            "portfolio_std_dev": {"type": "number"},
            "sharpe_ratio": {"type": ["number", "null"]},
            "diversification_benefit": {"type": "number"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["portfolio_return", "portfolio_std_dev", "sharpe_ratio", "diversification_benefit", "status", "timestamp"]
    }
}


def _validate_correlation_matrix(matrix: list[list[float]], n: int) -> None:
    """Validate that the correlation matrix is NxN, symmetric, and values in [-1, 1].

    Args:
        matrix: The correlation matrix (list of lists).
        n: Expected dimension (number of assets).

    Raises:
        ValueError: If matrix dimensions, symmetry, or value range are invalid.
    """
    if len(matrix) != n:
        raise ValueError(f"correlation_matrix must be {n}x{n}, got {len(matrix)} rows.")

    for i, row in enumerate(matrix):
        if len(row) != n:
            raise ValueError(f"correlation_matrix row {i} has {len(row)} columns, expected {n}.")

        for j, val in enumerate(row):
            if not (-1.0 - 1e-9 <= float(val) <= 1.0 + 1e-9):
                raise ValueError(
                    f"correlation_matrix[{i}][{j}] = {val} is outside [-1, 1]."
                )

    # Check diagonal is 1 (asset correlated with itself)
    for i in range(n):
        if abs(float(matrix[i][i]) - 1.0) > 1e-6:
            raise ValueError(f"correlation_matrix diagonal [{i}][{i}] must be 1.0, got {matrix[i][i]}.")

    # Check approximate symmetry
    for i in range(n):
        for j in range(i + 1, n):
            if abs(float(matrix[i][j]) - float(matrix[j][i])) > 1e-6:
                raise ValueError(
                    f"correlation_matrix is not symmetric: [{i}][{j}]={matrix[i][j]} != [{j}][{i}]={matrix[j][i]}."
                )


def _build_covariance_matrix(
    std_devs: list[float],
    correlation_matrix: list[list[float]],
) -> list[list[float]]:
    """Compute the covariance matrix from standard deviations and correlations.

    cov[i][j] = std_dev[i] * std_dev[j] * correlation[i][j]

    Args:
        std_devs: List of per-asset standard deviations.
        correlation_matrix: NxN correlation matrix.

    Returns:
        NxN covariance matrix as list of lists.
    """
    n = len(std_devs)
    cov = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cov[i][j] = std_devs[i] * std_devs[j] * float(correlation_matrix[i][j])
    return cov


def _portfolio_variance(weights: list[float], cov_matrix: list[list[float]]) -> float:
    """Compute portfolio variance: w^T * Sigma * w.

    Args:
        weights: List of asset weights (must sum to 1).
        cov_matrix: NxN covariance matrix.

    Returns:
        Portfolio variance (scalar).
    """
    n = len(weights)
    variance = 0.0
    for i in range(n):
        for j in range(n):
            variance += weights[i] * weights[j] * cov_matrix[i][j]
    return variance


def portfolio_variance_calc(
    holdings: list[dict],
    correlation_matrix: list[list[float]],
    risk_free_rate: float | None = None,
) -> dict:
    """Calculate Modern Portfolio Theory metrics for a multi-asset portfolio.

    Computes the portfolio expected return (weighted sum of individual returns),
    portfolio variance using the full covariance matrix (sigma_p^2 = w^T Sigma w),
    portfolio standard deviation (sqrt of variance), Sharpe ratio if risk-free
    rate is provided, and diversification benefit (reduction in volatility from
    holding a portfolio vs. a single weighted-average volatility position).

    Args:
        holdings: List of holding dicts with:
            - asset (str): Asset name or ticker.
            - weight (float): Portfolio weight (0-1). All weights must sum to ~1.
            - expected_return (float): Annualized expected return (decimal, e.g. 0.12).
            - std_dev (float): Annualized standard deviation (decimal, e.g. 0.20).
        correlation_matrix: NxN matrix of pairwise correlations. Values in [-1, 1].
            Diagonal must be 1. Must be symmetric.
        risk_free_rate: Optional annualized risk-free rate for Sharpe ratio (decimal).

    Returns:
        A dict with keys:
            - portfolio_return (float): Weighted expected return.
            - portfolio_std_dev (float): Portfolio standard deviation (volatility).
            - sharpe_ratio (float or None): (return - rf) / std_dev, or None if no rf.
            - diversification_benefit (float): Volatility reduction from diversification in bps.
            - status (str): "success" or "error".
            - timestamp (str): ISO 8601 UTC timestamp.
    """
    try:
        if not isinstance(holdings, list) or len(holdings) == 0:
            raise ValueError("holdings must be a non-empty list.")
        if not isinstance(correlation_matrix, list):
            raise TypeError(f"correlation_matrix must be a list, got {type(correlation_matrix).__name__}.")

        n = len(holdings)

        # Validate all holding fields
        assets: list[str] = []
        weights: list[float] = []
        expected_returns: list[float] = []
        std_devs: list[float] = []

        for idx, h in enumerate(holdings):
            for field in ("asset", "weight", "expected_return", "std_dev"):
                if field not in h:
                    raise ValueError(f"Holding at index {idx} missing field '{field}'.")

            w = float(h["weight"])
            er = float(h["expected_return"])
            sd = float(h["std_dev"])

            if not (0.0 <= w <= 1.0):
                raise ValueError(f"Holding '{h['asset']}' weight {w} must be in [0, 1].")
            if sd < 0:
                raise ValueError(f"Holding '{h['asset']}' std_dev {sd} cannot be negative.")

            assets.append(str(h["asset"]))
            weights.append(w)
            expected_returns.append(er)
            std_devs.append(sd)

        # Validate weights sum to approximately 1.0
        weight_sum = sum(weights)
        if abs(weight_sum - 1.0) > 1e-4:
            raise ValueError(
                f"Portfolio weights must sum to 1.0, got {weight_sum:.6f}. "
                "Normalize your weights before calling this function."
            )

        # Validate correlation matrix
        _validate_correlation_matrix(correlation_matrix, n)

        # --- Portfolio Expected Return ---
        # E[Rp] = sum(w_i * E[R_i])
        portfolio_return = sum(w * r for w, r in zip(weights, expected_returns))

        # --- Covariance Matrix ---
        cov_matrix = _build_covariance_matrix(std_devs, correlation_matrix)

        # --- Portfolio Variance and Standard Deviation ---
        port_variance = _portfolio_variance(weights, cov_matrix)

        # Clamp tiny floating point negatives to zero before sqrt
        port_variance = max(port_variance, 0.0)
        portfolio_std_dev = math.sqrt(port_variance)

        # --- Sharpe Ratio ---
        sharpe_ratio: float | None = None
        if risk_free_rate is not None:
            rf = float(risk_free_rate)
            if portfolio_std_dev > 1e-10:
                sharpe_ratio = round((portfolio_return - rf) / portfolio_std_dev, 6)
            else:
                sharpe_ratio = None  # Cannot compute Sharpe with zero volatility

        # --- Diversification Benefit ---
        # Naive undiversified volatility = weighted sum of individual std devs
        # (assumes perfect correlation between all assets)
        weighted_vol_sum = sum(w * sd for w, sd in zip(weights, std_devs))
        diversification_benefit_vol = weighted_vol_sum - portfolio_std_dev
        # Express as basis points of reduction
        diversification_benefit_bps = round(diversification_benefit_vol * 10_000.0, 4)

        # --- Per-asset contribution to portfolio variance ---
        # Marginal contribution = w_i * sum_j(w_j * cov[i][j])
        asset_contributions: list[dict] = []
        for i in range(n):
            marginal_variance = sum(weights[j] * cov_matrix[i][j] for j in range(n))
            contribution = weights[i] * marginal_variance
            pct_of_total = (contribution / port_variance * 100.0) if port_variance > 0 else 0.0
            asset_contributions.append({
                "asset": assets[i],
                "weight": round(weights[i], 6),
                "expected_return": round(expected_returns[i], 6),
                "std_dev": round(std_devs[i], 6),
                "variance_contribution": round(contribution, 8),
                "pct_of_portfolio_variance": round(pct_of_total, 4),
            })

        # Sort by variance contribution descending
        asset_contributions.sort(key=lambda x: x["variance_contribution"], reverse=True)

        return {
            "status": "success",
            "portfolio_return": round(portfolio_return, 8),
            "portfolio_variance": round(port_variance, 8),
            "portfolio_std_dev": round(portfolio_std_dev, 8),
            "sharpe_ratio": sharpe_ratio,
            "risk_free_rate": risk_free_rate,
            "diversification_benefit": diversification_benefit_bps,
            "diversification_benefit_vol": round(diversification_benefit_vol, 8),
            "weighted_undiversified_vol": round(weighted_vol_sum, 8),
            "asset_count": n,
            "asset_contributions": asset_contributions,
            "metrics": {
                "portfolio_return_pct": round(portfolio_return * 100.0, 4),
                "portfolio_std_dev_pct": round(portfolio_std_dev * 100.0, 4),
                "portfolio_variance_pct_sq": round(port_variance * 100.0 ** 2, 6),
                "diversification_reduction_pct": round(
                    (diversification_benefit_vol / weighted_vol_sum * 100.0) if weighted_vol_sum > 0 else 0.0, 4
                ),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"portfolio_variance_calc failed: {e}")
        _log_lesson(f"portfolio_variance_calc: {e}")
        return {
            "status": "error",
            "error": str(e),
            "portfolio_return": 0.0,
            "portfolio_std_dev": 0.0,
            "sharpe_ratio": None,
            "diversification_benefit": 0.0,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the lessons log file.

    Args:
        message: The lesson message to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
