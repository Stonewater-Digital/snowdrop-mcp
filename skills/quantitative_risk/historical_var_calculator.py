"""
Executive Summary: Historical simulation VaR with backtesting diagnostics under Basel traffic-light regime.
Inputs: historical_returns (list[list[float]]), confidence_level (float), horizon_days (int), portfolio_weights (list[float]), weighting_scheme (str)
Outputs: value_at_risk (float), expected_shortfall (float), violations (int), backtest_p_value (float)
MCP Tool Name: historical_var_calculator
"""
import logging
from datetime import datetime, timezone
from math import comb, sqrt
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "historical_var_calculator",
    "description": "Historical simulation VaR/ES with Kupiec backtest p-value using equal or exponential age weights.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "historical_returns": {
                "type": "array",
                "description": "Matrix of historical asset returns, each row is one observation with decimals.",
                "items": {
                    "type": "array",
                    "items": {"type": "number", "description": "Return for an asset"},
                    "description": "Observation row",
                },
            },
            "confidence_level": {
                "type": "number",
                "description": "Confidence level such as 0.99 for 99% VaR.",
            },
            "horizon_days": {
                "type": "integer",
                "description": "Forecast horizon in days for square-root-of-time scaling.",
            },
            "portfolio_weights": {
                "type": "array",
                "description": "Portfolio weights corresponding to assets in the historical matrix.",
                "items": {"type": "number"},
            },
            "weighting_scheme": {
                "type": "string",
                "description": "equal for standard Basel HS VaR or age for exponentially weighted (lambda=0.97).",
                "enum": ["equal", "age"],
                "default": "equal",
            },
        },
        "required": [
            "historical_returns",
            "confidence_level",
            "horizon_days",
            "portfolio_weights",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status value"},
            "data": {"type": "object", "description": "VaR output"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _weighted_quantile(values: List[float], weights: List[float], quantile: float) -> float:
    pairs = sorted(zip(values, weights), key=lambda item: item[0])
    cumulative = 0.0
    total_weight = sum(weights)
    if total_weight <= 0:
        raise ValueError("weights must sum positive")
    threshold = quantile * total_weight
    for value, weight in pairs:
        cumulative += weight
        if cumulative >= threshold:
            return value
    return pairs[-1][0]


def _expected_shortfall(values: List[float], weights: List[float], cutoff: float) -> float:
    tail_losses = [loss for loss in values if loss >= cutoff]
    tail_weights = [weights[idx] for idx, loss in enumerate(values) if loss >= cutoff]
    if not tail_losses:
        return cutoff
    total_weight = sum(tail_weights)
    return sum(loss * w for loss, w in zip(tail_losses, tail_weights)) / total_weight


def historical_var_calculator(
    historical_returns: List[List[float]],
    confidence_level: float,
    horizon_days: int,
    portfolio_weights: List[float],
    weighting_scheme: str = "equal",
    **_: Any,
) -> dict[str, Any]:
    try:
        if not 0 < confidence_level < 1:
            raise ValueError("confidence_level must be between 0 and 1")
        if horizon_days <= 0:
            raise ValueError("horizon_days must be positive")
        if not historical_returns:
            raise ValueError("historical_returns required")
        num_assets = len(portfolio_weights)
        if num_assets == 0:
            raise ValueError("portfolio_weights required")
        for row in historical_returns:
            if len(row) != num_assets:
                raise ValueError("each historical row must match number of weights")

        # Build portfolio loss series
        losses = []
        for row in historical_returns:
            port_return = sum(weight * asset_return for weight, asset_return in zip(portfolio_weights, row))
            losses.append(-port_return)

        n = len(losses)
        if weighting_scheme == "age":
            decay = 0.97
            weights = [decay ** (n - idx - 1) for idx in range(n)]
        else:
            weights = [1.0 for _ in range(n)]
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]
        quantile = _weighted_quantile(losses, normalized_weights, confidence_level)
        es = _expected_shortfall(losses, normalized_weights, quantile)

        scaled_var = quantile * sqrt(horizon_days)
        scaled_es = es * sqrt(horizon_days)

        expected_violations = n * (1 - confidence_level)
        actual_violations = sum(1 for loss in losses if loss > quantile)

        # Kupiec test p-value
        prob = 1 - confidence_level
        p_value = 0.0
        for k in range(actual_violations, n + 1):
            p_value += comb(n, k) * (prob ** k) * ((1 - prob) ** (n - k))

        data = {
            "value_at_risk": round(scaled_var, 6),
            "expected_shortfall": round(scaled_es, 6),
            "one_day_var": round(quantile, 6),
            "violations": actual_violations,
            "expected_violations": round(expected_violations, 2),
            "kupiec_p_value": round(min(p_value, 1.0), 6),
            "weighting_scheme": weighting_scheme,
            "horizon_days": horizon_days,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"historical_var_calculator failed: {e}")
        _log_lesson(f"historical_var_calculator: {e}")
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
