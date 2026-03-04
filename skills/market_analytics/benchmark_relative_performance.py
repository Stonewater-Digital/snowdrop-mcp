"""
Execuve Summary: Provides a comprehensive asset-versus-benchmark comparison.
Inputs: asset_returns (list[float]), benchmark_returns (list[float]), risk_free_rate (float)
Outputs: alpha (float), beta (float), r_squared (float), tracking_error (float), information_ratio (float), up_capture (float), down_capture (float), batting_average (float), active_return (float)
MCP Tool Name: benchmark_relative_performance
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TRADING_DAYS = 252

TOOL_META = {
    "name": "benchmark_relative_performance",
    "description": "Calculates performance statistics versus a benchmark including capture ratios and tracking error.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "asset_returns": {"type": "array", "description": "Portfolio returns."},
            "benchmark_returns": {"type": "array", "description": "Benchmark returns."},
            "risk_free_rate": {"type": "number", "description": "Annual risk-free rate."}
        },
        "required": ["asset_returns", "benchmark_returns", "risk_free_rate"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def benchmark_relative_performance(**kwargs: Any) -> dict:
    """Calculates relative statistics between asset and benchmark."""
    try:
        asset = kwargs.get("asset_returns")
        benchmark = kwargs.get("benchmark_returns")
        risk_free = kwargs.get("risk_free_rate")
        if not isinstance(asset, list) or not isinstance(benchmark, list) or len(asset) != len(benchmark):
            raise ValueError("asset_returns and benchmark_returns must be equal-length lists")
        if not isinstance(risk_free, (int, float)):
            raise ValueError("risk_free_rate must be numeric")
        if len(asset) < 2:
            raise ValueError("series must contain at least two observations")

        asset_clean = [float(r) for r in asset]
        bench_clean = [float(r) for r in benchmark]
        mean_asset = sum(asset_clean) / len(asset_clean)
        mean_bench = sum(bench_clean) / len(bench_clean)
        cov = sum((a - mean_asset) * (b - mean_bench) for a, b in zip(asset_clean, bench_clean)) / (len(asset_clean) - 1)
        var_bench = sum((b - mean_bench) ** 2 for b in bench_clean) / (len(bench_clean) - 1)
        beta = cov / var_bench if var_bench else 0
        alpha = (mean_asset - (risk_free / TRADING_DAYS)) - beta * (mean_bench - risk_free / TRADING_DAYS)
        variance_asset = sum((a - mean_asset) ** 2 for a in asset_clean) / (len(asset_clean) - 1)
        correlation = cov / math.sqrt(var_bench * variance_asset) if variance_asset and var_bench else 0
        r_squared = correlation ** 2

        active_returns = [a - b for a, b in zip(asset_clean, bench_clean)]
        mean_active = sum(active_returns) / len(active_returns)
        tracking_error = math.sqrt(sum((r - mean_active) ** 2 for r in active_returns) / (len(active_returns) - 1))
        information_ratio = (mean_active * TRADING_DAYS) / (tracking_error * math.sqrt(TRADING_DAYS)) if tracking_error else math.inf

        up_periods = [(a, b) for a, b in zip(asset_clean, bench_clean) if b > 0]
        down_periods = [(a, b) for a, b in zip(asset_clean, bench_clean) if b < 0]
        up_capture = (sum(a for a, _ in up_periods) / sum(b for _, b in up_periods)) if up_periods and sum(b for _, b in up_periods) != 0 else math.inf
        down_capture = (sum(a for a, _ in down_periods) / sum(b for _, b in down_periods)) if down_periods and sum(b for _, b in down_periods) != 0 else math.inf
        batting_average = sum(1 for a, b in zip(asset_clean, bench_clean) if a > b) / len(asset_clean)

        return {
            "status": "success",
            "data": {
                "alpha": alpha * TRADING_DAYS,
                "beta": beta,
                "r_squared": r_squared,
                "tracking_error": tracking_error * math.sqrt(TRADING_DAYS),
                "information_ratio": information_ratio,
                "up_capture": up_capture,
                "down_capture": down_capture,
                "batting_average": batting_average,
                "active_return": mean_active * TRADING_DAYS
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"benchmark_relative_performance failed: {e}")
        _log_lesson(f"benchmark_relative_performance: {e}")
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
