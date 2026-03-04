"""Compare Snowdrop portfolio path against benchmark."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "benchmark_comparator",
    "description": "Calculates alpha, beta, tracking error, and rolling alpha versus benchmark.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio_values": {"type": "array", "items": {"type": "number"}},
            "benchmark_values": {"type": "array", "items": {"type": "number"}},
            "period_label": {"type": "string"},
        },
        "required": ["portfolio_values", "benchmark_values", "period_label"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def benchmark_comparator(
    portfolio_values: list[float],
    benchmark_values: list[float],
    period_label: str,
    **_: Any,
) -> dict[str, Any]:
    """Return performance comparison diagnostics."""

    try:
        if len(portfolio_values) < 2 or len(benchmark_values) < 2:
            raise ValueError("Provide at least two observations for both series")
        min_length = min(len(portfolio_values), len(benchmark_values))
        portfolio_values = portfolio_values[:min_length]
        benchmark_values = benchmark_values[:min_length]
        port_returns = _series_returns(portfolio_values)
        bench_returns = _series_returns(benchmark_values)
        diff_returns = [p - b for p, b in zip(port_returns, bench_returns)]

        avg_diff = sum(diff_returns) / len(diff_returns)
        tracking_error = math.sqrt(sum((dr - avg_diff) ** 2 for dr in diff_returns) / len(diff_returns))
        tracking_error_annual = tracking_error * math.sqrt(252)
        covariance = _covariance(port_returns, bench_returns)
        bench_variance = _variance(bench_returns)
        beta = 0.0 if bench_variance == 0 else covariance / bench_variance
        alpha = avg_diff * 252
        info_ratio = 0.0 if tracking_error_annual == 0 else alpha / tracking_error_annual

        cumulative_port = portfolio_values[-1] / portfolio_values[0] - 1
        cumulative_bench = benchmark_values[-1] / benchmark_values[0] - 1
        cumulative_outperformance = cumulative_port - cumulative_bench
        rolling_alpha = _rolling_alpha(diff_returns)
        data = {
            "period": period_label,
            "alpha_annual": round(alpha, 4),
            "beta": round(beta, 4),
            "tracking_error_annual": round(tracking_error_annual, 4),
            "information_ratio": round(info_ratio, 4),
            "cumulative_outperformance": round(cumulative_outperformance, 4),
            "rolling_alpha_30d": rolling_alpha,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("benchmark_comparator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _series_returns(values: list[float]) -> list[float]:
    returns: list[float] = []
    for previous, current in zip(values, values[1:]):
        if previous == 0:
            raise ValueError("Series cannot contain zero values")
        returns.append((current - previous) / previous)
    return returns


def _covariance(a: list[float], b: list[float]) -> float:
    mean_a = sum(a) / len(a)
    mean_b = sum(b) / len(b)
    return sum((x - mean_a) * (y - mean_b) for x, y in zip(a, b)) / len(a)


def _variance(series: list[float]) -> float:
    mean = sum(series) / len(series)
    return sum((value - mean) ** 2 for value in series) / len(series)


def _rolling_alpha(diff_returns: list[float]) -> list[dict[str, Any]]:
    window = 30
    rolling: list[dict[str, Any]] = []
    if len(diff_returns) < window:
        return rolling
    for i in range(window, len(diff_returns) + 1):
        sample = diff_returns[i - window : i]
        annualized = sum(sample) / len(sample) * 252
        rolling.append({"ending_index": i, "alpha_annual": round(annualized, 4)})
    return rolling


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
