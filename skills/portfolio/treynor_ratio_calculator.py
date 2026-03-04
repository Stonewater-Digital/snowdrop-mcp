"""Calculate the Treynor ratio measuring return per unit of systematic risk.

MCP Tool Name: treynor_ratio_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "treynor_ratio_calculator",
    "description": (
        "Calculates the Treynor ratio, measuring excess return per unit of "
        "systematic risk (beta)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio_return": {
                "type": "number",
                "description": "Portfolio return for the period (decimal).",
            },
            "risk_free_rate": {
                "type": "number",
                "description": "Risk-free rate for the period (decimal).",
            },
            "beta": {
                "type": "number",
                "description": "Portfolio beta relative to the market.",
            },
        },
        "required": ["portfolio_return", "risk_free_rate", "beta"],
    },
}


def treynor_ratio_calculator(
    portfolio_return: float, risk_free_rate: float, beta: float
) -> dict[str, Any]:
    """Calculate the Treynor ratio."""
    try:
        portfolio_return = float(portfolio_return)
        risk_free_rate = float(risk_free_rate)
        beta = float(beta)

        if beta == 0:
            raise ValueError("beta must not be zero.")

        treynor = (portfolio_return - risk_free_rate) / beta

        return {
            "status": "ok",
            "data": {
                "treynor_ratio": round(treynor, 6),
                "excess_return": round(portfolio_return - risk_free_rate, 6),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
