"""Calculate annualized tracking error between portfolio and benchmark returns.

MCP Tool Name: tracking_error_calculator
"""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "tracking_error_calculator",
    "description": (
        "Calculates the annualized tracking error (standard deviation of active "
        "returns) between a portfolio and its benchmark."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio_returns": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of portfolio periodic returns.",
            },
            "benchmark_returns": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of benchmark periodic returns (same length).",
            },
        },
        "required": ["portfolio_returns", "benchmark_returns"],
    },
}


def tracking_error_calculator(
    portfolio_returns: list[float], benchmark_returns: list[float]
) -> dict[str, Any]:
    """Calculate annualized tracking error."""
    try:
        import statistics

        portfolio_returns = [float(r) for r in portfolio_returns]
        benchmark_returns = [float(r) for r in benchmark_returns]

        if len(portfolio_returns) != len(benchmark_returns):
            raise ValueError("portfolio_returns and benchmark_returns must be the same length.")
        if len(portfolio_returns) < 2:
            raise ValueError("Need at least 2 return periods.")

        active_returns = [p - b for p, b in zip(portfolio_returns, benchmark_returns)]
        te_periodic = statistics.stdev(active_returns)
        te_annualized = te_periodic * math.sqrt(252)

        return {
            "status": "ok",
            "data": {
                "tracking_error_periodic": round(te_periodic, 6),
                "tracking_error_annualized": round(te_annualized, 6),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
