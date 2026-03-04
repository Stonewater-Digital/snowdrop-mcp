"""
Execuve Summary: Approximates risk parity weights using inverse-vol scaling.
Inputs: returns_matrix (list[list[float]]), asset_names (list[str])
Outputs: risk_parity_weights (dict), risk_contributions (dict), portfolio_vol (float), vs_equal_weight_comparison (dict)
MCP Tool Name: risk_parity_weights
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "risk_parity_weights",
    "description": "Approximates risk-parity allocation via inverse volatility and reports risk contributions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns_matrix": {"type": "array", "description": "List of asset return series."},
            "asset_names": {"type": "array", "description": "Names corresponding to each asset."}
        },
        "required": ["returns_matrix", "asset_names"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def risk_parity_weights(**kwargs: Any) -> dict:
    """Calculates inverse-volatility weights and evaluates contribution to portfolio risk."""
    try:
        returns_matrix = kwargs.get("returns_matrix")
        asset_names = kwargs.get("asset_names")
        if not isinstance(returns_matrix, list) or not isinstance(asset_names, list):
            raise ValueError("returns_matrix and asset_names must be lists")
        if len(returns_matrix) != len(asset_names):
            raise ValueError("asset_names length must match number of assets")
        length = len(returns_matrix[0])
        if any(len(series) != length for series in returns_matrix):
            raise ValueError("all return series must share the same length")

        asset_vols = []
        returns_clean = []
        for series in returns_matrix:
            clean_series = [float(value) for value in series]
            returns_clean.append(clean_series)
            mean_val = sum(clean_series) / len(clean_series)
            variance = sum((value - mean_val) ** 2 for value in clean_series) / (len(clean_series) - 1)
            asset_vols.append(math.sqrt(variance))

        inverse_vols = [1 / vol if vol else 0.0 for vol in asset_vols]
        total_inv = sum(inverse_vols)
        weights = [val / total_inv if total_inv else 0 for val in inverse_vols]

        # Build covariance matrix
        covariance_matrix = []
        for i in range(len(returns_clean)):
            row = []
            mean_i = sum(returns_clean[i]) / length
            for j in range(len(returns_clean)):
                mean_j = sum(returns_clean[j]) / length
                cov = sum((returns_clean[i][k] - mean_i) * (returns_clean[j][k] - mean_j) for k in range(length)) / (length - 1)
                row.append(cov)
            covariance_matrix.append(row)

        marginal_risk = []
        for i in range(len(weights)):
            contribution = sum(covariance_matrix[i][j] * weights[j] for j in range(len(weights)))
            marginal_risk.append(contribution)
        portfolio_variance = sum(weights[i] * marginal_risk[i] for i in range(len(weights)))
        portfolio_vol = math.sqrt(portfolio_variance)
        risk_contributions = {
            name: (weights[idx] * marginal_risk[idx]) / portfolio_variance if portfolio_variance else 0.0
            for idx, name in enumerate(asset_names)
        }
        weight_map = {name: weights[idx] for idx, name in enumerate(asset_names)}

        equal_weight = 1 / len(weights)
        eq_weights = [equal_weight] * len(weights)
        eq_marginal = []
        for i in range(len(eq_weights)):
            eq_marginal.append(sum(covariance_matrix[i][j] * eq_weights[j] for j in range(len(eq_weights))))
        eq_variance = sum(eq_weights[i] * eq_marginal[i] for i in range(len(eq_weights)))
        vs_equal = {
            "equal_weight_vol": math.sqrt(eq_variance),
            "risk_parity_vol": portfolio_vol
        }

        return {
            "status": "success",
            "data": {
                "risk_parity_weights": weight_map,
                "risk_contributions": risk_contributions,
                "portfolio_vol": portfolio_vol,
                "vs_equal_weight_comparison": vs_equal
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"risk_parity_weights failed: {e}")
        _log_lesson(f"risk_parity_weights: {e}")
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
