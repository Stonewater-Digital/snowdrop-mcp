"""Calculate the information ratio comparing active return to tracking error.

MCP Tool Name: information_ratio_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "information_ratio_calculator",
    "description": (
        "Calculates the information ratio, measuring a portfolio manager's ability "
        "to generate excess returns relative to a benchmark per unit of tracking error."
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


def information_ratio_calculator(
    portfolio_returns: list[float], benchmark_returns: list[float]
) -> dict[str, Any]:
    """Calculate the information ratio."""
    try:
        import statistics

        portfolio_returns = [float(r) for r in portfolio_returns]
        benchmark_returns = [float(r) for r in benchmark_returns]

        if len(portfolio_returns) != len(benchmark_returns):
            raise ValueError("portfolio_returns and benchmark_returns must be the same length.")
        if len(portfolio_returns) < 2:
            raise ValueError("Need at least 2 return periods.")

        active_returns = [p - b for p, b in zip(portfolio_returns, benchmark_returns)]
        mean_active = statistics.mean(active_returns)
        std_active = statistics.stdev(active_returns)

        if std_active == 0:
            raise ValueError("Tracking error is zero; cannot compute information ratio.")

        ir = mean_active / std_active

        return {
            "status": "ok",
            "data": {
                "information_ratio": round(ir, 6),
                "mean_active_return": round(mean_active, 6),
                "tracking_error": round(std_active, 6),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
