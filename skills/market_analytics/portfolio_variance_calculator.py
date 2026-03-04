"""
Execuve Summary: Calculates portfolio variance and decomposes risk contributions.
Inputs: weights (list[float]), returns_matrix (list[list[float]])
Outputs: portfolio_variance (float), portfolio_vol (float), covariance_matrix (list[list[float]]), risk_contribution_per_asset (list[float]), marginal_risk_per_asset (list[float]), diversification_ratio (float)
MCP Tool Name: portfolio_variance_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "portfolio_variance_calculator",
    "description": "Computes covariance matrix, portfolio variance/volatility, and risk contributions from asset weights.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "weights": {"type": "array", "description": "Portfolio weights (sum to 1)."},
            "returns_matrix": {"type": "array", "description": "List of return series for each asset."}
        },
        "required": ["weights", "returns_matrix"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def portfolio_variance_calculator(**kwargs: Any) -> dict:
    """Calculates portfolio variance, volatility, and risk attribution."""
    try:
        weights = kwargs.get("weights")
        returns_matrix = kwargs.get("returns_matrix")
        if not isinstance(weights, list) or not isinstance(returns_matrix, list):
            raise ValueError("weights and returns_matrix must be lists")
        if len(weights) != len(returns_matrix):
            raise ValueError("weights length must equal number of assets")
        if any(not isinstance(series, list) or len(series) < 2 for series in returns_matrix):
            raise ValueError("each asset return series must contain at least two observations")

        weights_clean = [float(w) for w in weights]
        length = len(returns_matrix[0])
        for series in returns_matrix:
            if len(series) != length:
                raise ValueError("all return series must be equal length")
        returns_clean = [[float(val) for val in series] for series in returns_matrix]

        asset_means = [sum(series) / length for series in returns_clean]
        covariance_matrix = []
        for i in range(len(returns_clean)):
            row = []
            for j in range(len(returns_clean)):
                cov = sum(
                    (returns_clean[i][k] - asset_means[i]) * (returns_clean[j][k] - asset_means[j])
                    for k in range(length)
                ) / (length - 1)
                row.append(cov)
            covariance_matrix.append(row)

        # Portfolio variance = w^T * Cov * w
        marginal_risk = []
        for i in range(len(weights_clean)):
            contribution = sum(covariance_matrix[i][j] * weights_clean[j] for j in range(len(weights_clean)))
            marginal_risk.append(contribution)
        portfolio_variance = sum(weights_clean[i] * marginal_risk[i] for i in range(len(weights_clean)))
        portfolio_vol = math.sqrt(portfolio_variance)
        if portfolio_vol == 0:
            raise ZeroDivisionError("portfolio volatility is zero")

        risk_contribution = [weights_clean[i] * marginal_risk[i] / portfolio_variance for i in range(len(weights_clean))]
        asset_vols = [math.sqrt(covariance_matrix[i][i]) for i in range(len(weights_clean))]
        diversification_ratio = (sum(weights_clean[i] * asset_vols[i] for i in range(len(weights_clean))) / portfolio_vol)

        return {
            "status": "success",
            "data": {
                "portfolio_variance": portfolio_variance,
                "portfolio_vol": portfolio_vol,
                "covariance_matrix": covariance_matrix,
                "risk_contribution_per_asset": risk_contribution,
                "marginal_risk_per_asset": marginal_risk,
                "diversification_ratio": diversification_ratio
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"portfolio_variance_calculator failed: {e}")
        _log_lesson(f"portfolio_variance_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
