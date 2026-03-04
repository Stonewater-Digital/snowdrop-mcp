"""Calculate the Sortino ratio using downside deviation only.

MCP Tool Name: sortino_ratio_calculator
"""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "sortino_ratio_calculator",
    "description": (
        "Calculates the Sortino ratio, a variation of the Sharpe ratio that only "
        "penalizes downside volatility rather than total volatility."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of periodic returns as decimals.",
            },
            "risk_free_rate": {
                "type": "number",
                "description": "Risk-free rate per period (default 0.02).",
            },
        },
        "required": ["returns"],
    },
}


def sortino_ratio_calculator(
    returns: list[float], risk_free_rate: float = 0.02
) -> dict[str, Any]:
    """Calculate the Sortino ratio."""
    try:
        import statistics

        returns = [float(r) for r in returns]
        risk_free_rate = float(risk_free_rate)

        if len(returns) < 2:
            raise ValueError("returns must contain at least 2 values.")

        mean_return = statistics.mean(returns)
        downside_diffs = [min(r - risk_free_rate, 0) ** 2 for r in returns]
        downside_dev = math.sqrt(statistics.mean(downside_diffs))

        if downside_dev == 0:
            raise ValueError("Downside deviation is zero; cannot compute Sortino ratio.")

        sortino = (mean_return - risk_free_rate) / downside_dev

        return {
            "status": "ok",
            "data": {
                "sortino_ratio": round(sortino, 6),
                "mean_return": round(mean_return, 6),
                "downside_deviation": round(downside_dev, 6),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
