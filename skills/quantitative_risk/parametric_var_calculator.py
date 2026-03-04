"""
Executive Summary: Parametric value-at-risk using Basel variance-covariance methodology for linear portfolios.
Inputs: portfolio_weights (list[float]), covariance_matrix (list[list[float]]), confidence_level (float), horizon_days (int)
Outputs: value_at_risk (float), component_var (list[dict]), marginal_var (list[dict]), incremental_var (list[dict])
MCP Tool Name: parametric_var_calculator
"""
import logging
from datetime import datetime, timezone
from statistics import NormalDist
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "parametric_var_calculator",
    "description": "Basel variance-covariance VaR with component, marginal, and incremental attribution over a user horizon.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio_weights": {
                "type": "array",
                "description": "Asset weights or dollar sensitivities; assumed to sum to portfolio exposure.",
                "items": {"type": "number"},
            },
            "covariance_matrix": {
                "type": "array",
                "description": "Square covariance matrix of asset returns expressed in decimal terms.",
                "items": {
                    "type": "array",
                    "items": {"type": "number", "description": "Covariance entry"},
                    "description": "Row of the covariance matrix",
                },
            },
            "confidence_level": {
                "type": "number",
                "description": "Confidence level for VaR, e.g., 0.99 for Basel 99th percentile.",
            },
            "horizon_days": {
                "type": "integer",
                "description": "Liquidation horizon in trading days; VaR scales with sqrt of this horizon.",
            },
        },
        "required": ["portfolio_weights", "covariance_matrix", "confidence_level", "horizon_days"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status indicator"},
            "data": {"type": "object", "description": "VaR metrics and breakdown"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _validate_inputs(weights: List[float], cov: List[List[float]]) -> None:
    if not weights:
        raise ValueError("portfolio_weights must not be empty")
    if len(cov) != len(weights):
        raise ValueError("covariance_matrix dimension mismatch")
    for row in cov:
        if len(row) != len(weights):
            raise ValueError("covariance_matrix must be square")


def _portfolio_variance(weights: List[float], cov: List[List[float]]) -> float:
    exposures = [float(w) for w in weights]
    cov_times_w = []
    for i, row in enumerate(cov):
        value = 0.0
        for j, entry in enumerate(row):
            value += float(entry) * exposures[j]
        cov_times_w.append(value)
    variance = 0.0
    for i, exposure in enumerate(exposures):
        variance += exposure * cov_times_w[i]
    return variance, cov_times_w


def parametric_var_calculator(
    portfolio_weights: List[float],
    covariance_matrix: List[List[float]],
    confidence_level: float,
    horizon_days: int,
    **_: Any,
) -> dict[str, Any]:
    try:
        _validate_inputs(portfolio_weights, covariance_matrix)
        if not 0 < confidence_level < 1:
            raise ValueError("confidence_level must be between 0 and 1")
        if horizon_days <= 0:
            raise ValueError("horizon_days must be positive")

        variance, cov_times_w = _portfolio_variance(portfolio_weights, covariance_matrix)
        if variance <= 0:
            raise ValueError("portfolio variance must be positive")

        sigma = variance ** 0.5
        scaling = (horizon_days) ** 0.5
        z_score = abs(NormalDist().inv_cdf(confidence_level))
        base_var = z_score * sigma
        value_at_risk = base_var * scaling

        component_var = []
        marginal_var = []
        incremental_var = []
        total_contribution = 0.0
        for idx, weight in enumerate(portfolio_weights):
            marginal = cov_times_w[idx] / sigma if sigma else 0.0
            component_value = weight * marginal
            total_contribution += component_value
            component_var.append(
                {
                    "asset_index": idx,
                    "component_share": round(component_value / variance if variance else 0.0, 6),
                    "component_var": round(component_value * z_score * scaling, 6),
                }
            )
            marginal_var.append({"asset_index": idx, "marginal_var": round(marginal * z_score * scaling, 6)})

            reduced_weights = list(portfolio_weights)
            reduced_weights[idx] = 0.0
            reduced_var, _ = _portfolio_variance(reduced_weights, covariance_matrix)
            reduced_sigma = reduced_var ** 0.5
            reduced_value_at_risk = z_score * reduced_sigma * scaling
            incremental_var.append(
                {
                    "asset_index": idx,
                    "incremental_var": round(value_at_risk - reduced_value_at_risk, 6),
                }
            )

        concentration_ratio = total_contribution / variance if variance else 0.0

        data = {
            "value_at_risk": round(value_at_risk, 6),
            "volatility": round(sigma, 6),
            "z_score": round(z_score, 5),
            "horizon_days": horizon_days,
            "component_var": component_var,
            "marginal_var": marginal_var,
            "incremental_var": incremental_var,
            "concentration_ratio": round(concentration_ratio, 6),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"parametric_var_calculator failed: {e}")
        _log_lesson(f"parametric_var_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as handle:
            handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
