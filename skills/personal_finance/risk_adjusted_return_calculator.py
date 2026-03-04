"""
Executive Smary: Computes Sharpe, Sortino, Treynor, drawdown, and annualized performance metrics.
Inputs: returns (list), risk_free_rate (float), benchmark_returns (list)
Outputs: sharpe_ratio (float), sortino_ratio (float), treynor_ratio (float|None), max_drawdown (float), annualized_return (float), annualized_vol (float)
MCP Tool Name: risk_adjusted_return_calculator
"""
import logging
from datetime import datetime, timezone
from math import sqrt
from typing import Any, List, Optional

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "risk_adjusted_return_calculator",
    "description": (
        "Calculates risk-adjusted metrics (Sharpe, Sortino, Treynor) plus annualized "
        "return/volatility and maximum drawdown from a series of periodic returns."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {
                "type": "array",
                "description": "List of periodic returns expressed as decimals (e.g., 0.01).",
                "items": {"type": "number"},
            },
            "risk_free_rate": {
                "type": "number",
                "description": "Periodic risk-free rate matching the return frequency.",
            },
            "benchmark_returns": {
                "type": "array",
                "description": "Optional benchmark return series for Treynor ratio.",
                "items": {"type": "number"},
            },
        },
        "required": ["returns", "risk_free_rate"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
        },
        "required": ["status", "timestamp"],
    },
}


def risk_adjusted_return_calculator(**kwargs: Any) -> dict:
    """Evaluate Sharpe, Sortino, Treynor ratios and drawdown for a return series."""
    try:
        returns_input = kwargs["returns"]
        risk_free = float(kwargs["risk_free_rate"])
        benchmark_returns_input = kwargs.get("benchmark_returns")

        if not isinstance(returns_input, list) or len(returns_input) < 2:
            raise ValueError("returns must be a list with at least two observations")

        returns: List[float] = [float(r) for r in returns_input]
        benchmark_returns: Optional[List[float]] = (
            [float(r) for r in benchmark_returns_input] if benchmark_returns_input else None
        )

        excess_returns = [r - risk_free for r in returns]
        avg_return = sum(returns) / len(returns)
        variance = sum((r - avg_return) ** 2 for r in returns) / (len(returns) - 1)
        vol = sqrt(variance)
        sharpe = (sum(excess_returns) / len(excess_returns)) / vol if vol > 0 else 0.0

        downside = [min(0, r - risk_free) for r in returns]
        downside_variance = sum(d**2 for d in downside) / max(len(downside) - 1, 1)
        downside_dev = sqrt(downside_variance)
        sortino = (
            (sum(excess_returns) / len(excess_returns)) / downside_dev if downside_dev > 0 else 0.0
        )

        treynor: Optional[float] = None
        if benchmark_returns and len(benchmark_returns) == len(returns):
            bench_avg = sum(benchmark_returns) / len(benchmark_returns)
            cov = sum(
                (r - avg_return) * (b - bench_avg) for r, b in zip(returns, benchmark_returns)
            ) / (len(returns) - 1)
            bench_var = sum((b - bench_avg) ** 2 for b in benchmark_returns) / (len(returns) - 1)
            beta = cov / bench_var if bench_var > 0 else None
            if beta and beta != 0:
                treynor = (sum(excess_returns) / len(excess_returns)) / beta

        # Max drawdown
        cumulative = []
        value = 1.0
        max_value = 1.0
        max_drawdown = 0.0
        for r in returns:
            value *= 1 + r
            max_value = max(max_value, value)
            drawdown = (value - max_value) / max_value
            max_drawdown = min(max_drawdown, drawdown)
            cumulative.append(value)

        periods_per_year = 12 if len(returns) >= 12 else len(returns)
        annualized_return = (1 + avg_return) ** periods_per_year - 1
        annualized_vol = vol * sqrt(periods_per_year)

        return {
            "status": "success",
            "data": {
                "sharpe_ratio": sharpe,
                "sortino_ratio": sortino,
                "treynor_ratio": treynor,
                "max_drawdown": max_drawdown,
                "annualized_return": annualized_return,
                "annualized_vol": annualized_vol,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"risk_adjusted_return_calculator failed: {e}")
        _log_lesson(f"risk_adjusted_return_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
