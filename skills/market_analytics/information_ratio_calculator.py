"""
Execuve Summary: Calculates the Information Ratio relative to a benchmark.
Inputs: portfolio_returns (list[float]), benchmark_returns (list[float])
Outputs: information_ratio (float), active_return (float), tracking_error (float), hit_rate (float)
MCP Tool Name: information_ratio_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TRADING_DAYS = 252

TOOL_META = {
    "name": "information_ratio_calculator",
    "description": "Computes Information Ratio, tracking error, active return, and hit rate.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio_returns": {"type": "array", "description": "Portfolio returns (decimal)."},
            "benchmark_returns": {"type": "array", "description": "Benchmark returns aligned with portfolio."}
        },
        "required": ["portfolio_returns", "benchmark_returns"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["status", "timestamp"]
    }
}


def information_ratio_calculator(**kwargs: Any) -> dict:
    """Computes active return divided by tracking error along with hit rate."""
    try:
        portfolio = kwargs.get("portfolio_returns")
        benchmark = kwargs.get("benchmark_returns")
        if not isinstance(portfolio, list) or not isinstance(benchmark, list):
            raise ValueError("portfolio_returns and benchmark_returns must be lists")
        if len(portfolio) != len(benchmark) or len(portfolio) < 2:
            raise ValueError("series must align and contain at least two items")

        active_returns = []
        wins = 0
        for p, b in zip(portfolio, benchmark):
            if not isinstance(p, (int, float)) or not isinstance(b, (int, float)):
                raise TypeError("returns must be numeric")
            diff = float(p) - float(b)
            active_returns.append(diff)
            if diff > 0:
                wins += 1
        active_return = sum(active_returns) / len(active_returns)
        variance = sum((diff - active_return) ** 2 for diff in active_returns) / (len(active_returns) - 1)
        tracking_error = math.sqrt(variance)
        if tracking_error == 0:
            raise ZeroDivisionError("tracking error is zero; Information Ratio undefined")
        information_ratio = (active_return * TRADING_DAYS) / (tracking_error * math.sqrt(TRADING_DAYS))
        hit_rate = wins / len(active_returns)

        return {
            "status": "success",
            "data": {
                "information_ratio": information_ratio,
                "active_return": active_return * TRADING_DAYS,
                "tracking_error": tracking_error * math.sqrt(TRADING_DAYS),
                "hit_rate": hit_rate
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"information_ratio_calculator failed: {e}")
        _log_lesson(f"information_ratio_calculator: {e}")
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
