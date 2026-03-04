"""Calculate Jensen's alpha measuring risk-adjusted excess return.

MCP Tool Name: jensen_alpha_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "jensen_alpha_calculator",
    "description": (
        "Calculates Jensen's alpha, the excess return of a portfolio over the "
        "expected return predicted by the CAPM."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio_return": {
                "type": "number",
                "description": "Actual portfolio return (decimal).",
            },
            "risk_free_rate": {
                "type": "number",
                "description": "Risk-free rate (decimal).",
            },
            "beta": {
                "type": "number",
                "description": "Portfolio beta.",
            },
            "market_return": {
                "type": "number",
                "description": "Market return (decimal).",
            },
        },
        "required": ["portfolio_return", "risk_free_rate", "beta", "market_return"],
    },
}


def jensen_alpha_calculator(
    portfolio_return: float, risk_free_rate: float, beta: float, market_return: float
) -> dict[str, Any]:
    """Calculate Jensen's alpha."""
    try:
        portfolio_return = float(portfolio_return)
        risk_free_rate = float(risk_free_rate)
        beta = float(beta)
        market_return = float(market_return)

        expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
        alpha = portfolio_return - expected_return

        return {
            "status": "ok",
            "data": {
                "jensen_alpha": round(alpha, 6),
                "expected_return": round(expected_return, 6),
                "actual_return": round(portfolio_return, 6),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
