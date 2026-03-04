"""
Execuve Summary: Calculates the Treynor ratio using beta-adjusted returns.
Inputs: returns (list[float]), benchmark_returns (list[float]), risk_free_rate (float)
Outputs: treynor_ratio (float), beta (float), alpha (float), systematic_risk_pct (float)
MCP Tool Name: treynor_ratio_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TRADING_DAYS = 252

TOOL_META = {
    "name": "treynor_ratio_calculator",
    "description": "Computes Treynor ratio, beta, Jensen's alpha, and systematic risk contribution.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {"type": "array", "description": "Portfolio returns (decimal)."},
            "benchmark_returns": {"type": "array", "description": "Benchmark returns aligned with portfolio."},
            "risk_free_rate": {"type": "number", "description": "Annual risk-free rate."}
        },
        "required": ["returns", "benchmark_returns", "risk_free_rate"]
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


def treynor_ratio_calculator(**kwargs: Any) -> dict:
    """Evaluates risk-adjusted performance by dividing excess return by beta."""
    try:
        returns = kwargs.get("returns")
        benchmark_returns = kwargs.get("benchmark_returns")
        risk_free_rate = kwargs.get("risk_free_rate")
        if not isinstance(returns, list) or not isinstance(benchmark_returns, list):
            raise ValueError("returns and benchmark_returns must be lists")
        if len(returns) != len(benchmark_returns) or len(returns) < 2:
            raise ValueError("series must align and contain at least two points")
        if not isinstance(risk_free_rate, (int, float)):
            raise ValueError("risk_free_rate must be numeric")

        port = [float(r) for r in returns]
        bench = [float(r) for r in benchmark_returns]
        rf_daily = risk_free_rate / TRADING_DAYS
        mean_port = sum(port) / len(port)
        mean_bench = sum(bench) / len(bench)
        covariance = sum((p - mean_port) * (b - mean_bench) for p, b in zip(port, bench)) / (len(port) - 1)
        variance_bench = sum((b - mean_bench) ** 2 for b in bench) / (len(bench) - 1)
        if variance_bench == 0:
            raise ZeroDivisionError("benchmark variance is zero; beta undefined")
        beta = covariance / variance_bench
        if beta == 0:
            raise ZeroDivisionError("beta is zero; Treynor undefined")

        excess_return = mean_port - rf_daily
        treynor_ratio = (excess_return * TRADING_DAYS) / beta
        alpha = (mean_port - rf_daily) - beta * (mean_bench - rf_daily)
        variance_port = sum((p - mean_port) ** 2 for p in port) / (len(port) - 1)
        systematic = beta ** 2 * variance_bench
        systematic_risk_pct = systematic / variance_port if variance_port else math.inf

        return {
            "status": "success",
            "data": {
                "treynor_ratio": treynor_ratio,
                "beta": beta,
                "alpha": alpha * TRADING_DAYS,
                "systematic_risk_pct": systematic_risk_pct
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"treynor_ratio_calculator failed: {e}")
        _log_lesson(f"treynor_ratio_calculator: {e}")
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
