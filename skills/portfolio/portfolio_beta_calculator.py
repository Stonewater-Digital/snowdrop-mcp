"""Calculate portfolio beta relative to the market.

MCP Tool Name: portfolio_beta_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "portfolio_beta_calculator",
    "description": (
        "Calculates portfolio beta as covariance(portfolio, market) / variance(market), "
        "measuring sensitivity to market movements."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio_returns": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of portfolio periodic returns.",
            },
            "market_returns": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of market periodic returns (same length).",
            },
        },
        "required": ["portfolio_returns", "market_returns"],
    },
}


def portfolio_beta_calculator(
    portfolio_returns: list[float], market_returns: list[float]
) -> dict[str, Any]:
    """Calculate portfolio beta."""
    try:
        import statistics

        portfolio_returns = [float(r) for r in portfolio_returns]
        market_returns = [float(r) for r in market_returns]

        if len(portfolio_returns) != len(market_returns):
            raise ValueError("portfolio_returns and market_returns must be the same length.")
        if len(portfolio_returns) < 2:
            raise ValueError("Need at least 2 return periods.")

        n = len(portfolio_returns)
        mean_p = statistics.mean(portfolio_returns)
        mean_m = statistics.mean(market_returns)

        covariance = sum((p - mean_p) * (m - mean_m) for p, m in zip(portfolio_returns, market_returns)) / (n - 1)
        variance_m = sum((m - mean_m) ** 2 for m in market_returns) / (n - 1)

        if variance_m == 0:
            raise ValueError("Market variance is zero; cannot compute beta.")

        beta = covariance / variance_m

        return {
            "status": "ok",
            "data": {
                "beta": round(beta, 6),
                "covariance": round(covariance, 6),
                "market_variance": round(variance_m, 6),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
