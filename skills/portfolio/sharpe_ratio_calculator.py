"""Calculate the Sharpe ratio from a series of returns and a risk-free rate.

MCP Tool Name: sharpe_ratio_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "sharpe_ratio_calculator",
    "description": (
        "Calculates the Sharpe ratio, measuring risk-adjusted return by comparing "
        "excess return over the risk-free rate to portfolio volatility."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of periodic returns (e.g. daily or monthly as decimals).",
            },
            "risk_free_rate": {
                "type": "number",
                "description": "Risk-free rate per period (default 0.02 annualized).",
            },
        },
        "required": ["returns"],
    },
}


def sharpe_ratio_calculator(
    returns: list[float], risk_free_rate: float = 0.02
) -> dict[str, Any]:
    """Calculate the Sharpe ratio."""
    try:
        import statistics

        returns = [float(r) for r in returns]
        risk_free_rate = float(risk_free_rate)

        if len(returns) < 2:
            raise ValueError("returns must contain at least 2 values.")

        mean_return = statistics.mean(returns)
        std_return = statistics.stdev(returns)

        if std_return == 0:
            raise ValueError("Standard deviation of returns is zero; cannot compute Sharpe ratio.")

        sharpe = (mean_return - risk_free_rate) / std_return

        return {
            "status": "ok",
            "data": {
                "sharpe_ratio": round(sharpe, 6),
                "mean_return": round(mean_return, 6),
                "std_return": round(std_return, 6),
                "risk_free_rate": risk_free_rate,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
