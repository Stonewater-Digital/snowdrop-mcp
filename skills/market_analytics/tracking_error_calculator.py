"""
Execuve Summary: Calculates ex-post tracking error versus a benchmark.
Inputs: portfolio_returns (list[float]), benchmark_returns (list[float])
Outputs: tracking_error_annualized (float), active_return (float), active_share_approx (float), return_attribution (dict)
MCP Tool Name: tracking_error_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TRADING_DAYS = 252

TOOL_META = {
    "name": "tracking_error_calculator",
    "description": "Computes tracking error, active return, and a rough active-share proxy from return differences.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio_returns": {"type": "array", "description": "Portfolio returns (decimal)."},
            "benchmark_returns": {"type": "array", "description": "Benchmark returns (decimal)."}
        },
        "required": ["portfolio_returns", "benchmark_returns"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def tracking_error_calculator(**kwargs: Any) -> dict:
    """Derives tracking error statistics from portfolio vs benchmark returns."""
    try:
        portfolio = kwargs.get("portfolio_returns")
        benchmark = kwargs.get("benchmark_returns")
        if not isinstance(portfolio, list) or not isinstance(benchmark, list):
            raise ValueError("portfolio_returns and benchmark_returns must be lists")
        if len(portfolio) != len(benchmark) or len(portfolio) < 2:
            raise ValueError("series must align and be >=2 in length")

        active = []
        for p, b in zip(portfolio, benchmark):
            if not isinstance(p, (int, float)) or not isinstance(b, (int, float)):
                raise TypeError("returns must be numeric")
            active.append(float(p) - float(b))
        mean_active = sum(active) / len(active)
        variance = sum((value - mean_active) ** 2 for value in active) / (len(active) - 1)
        tracking_error = math.sqrt(variance)
        tracking_error_annualized = tracking_error * math.sqrt(TRADING_DAYS)
        active_return = mean_active * TRADING_DAYS
        active_share_approx = sum(abs(value) for value in active) / len(active)
        positive = sum(max(value, 0) for value in active)
        negative = sum(min(value, 0) for value in active)
        attribution = {"positive_active": positive, "negative_active": negative}

        return {
            "status": "success",
            "data": {
                "tracking_error_annualized": tracking_error_annualized,
                "active_return": active_return,
                "active_share_approx": active_share_approx,
                "return_attribution": attribution
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"tracking_error_calculator failed: {e}")
        _log_lesson(f"tracking_error_calculator: {e}")
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
