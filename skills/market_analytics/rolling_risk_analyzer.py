"""
Execuve Summary: Computes rolling Sharpe, drawdown, and beta metrics to detect regime shifts.
Inputs: returns (list[float]), window_size (int), benchmark_returns (list[float]|None)
Outputs: rolling_sharpe (list[float]), rolling_max_dd (list[float]), rolling_beta (list[float]|None), regime_changes_detected (list[int])
MCP Tool Name: rolling_risk_analyzer
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "rolling_risk_analyzer",
    "description": "Computes rolling Sharpe, max drawdown, beta (optional), and detects volatility regime shifts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {"type": "array", "description": "Return series."},
            "window_size": {"type": "integer", "description": "Rolling window length."},
            "benchmark_returns": {"type": "array", "description": "Optional benchmark returns for beta."}
        },
        "required": ["returns", "window_size"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def rolling_risk_analyzer(**kwargs: Any) -> dict:
    """Generates rolling risk metrics and flags volatility regime changes."""
    try:
        returns = kwargs.get("returns")
        window_size = kwargs.get("window_size")
        benchmark = kwargs.get("benchmark_returns")
        if not isinstance(returns, list) or len(returns) < window_size:
            raise ValueError("returns must be at least as long as window_size")
        if not isinstance(window_size, int) or window_size <= 1:
            raise ValueError("window_size must be integer > 1")
        if benchmark is not None and (not isinstance(benchmark, list) or len(benchmark) != len(returns)):
            raise ValueError("benchmark_returns must match returns length if provided")

        rolling_sharpe = []
        rolling_max_dd = []
        rolling_beta = [] if benchmark is not None else None
        regime_changes = []
        prev_vol = None
        for idx in range(window_size, len(returns) + 1):
            window = [float(r) for r in returns[idx - window_size: idx]]
            mean_return = sum(window) / window_size
            variance = sum((r - mean_return) ** 2 for r in window) / (window_size - 1)
            std_dev = math.sqrt(variance)
            sharpe = mean_return / std_dev if std_dev else math.inf
            rolling_sharpe.append(sharpe)

            peak = window[0]
            max_dd = 0.0
            for price in window:
                peak = max(peak, price)
                drawdown = price / peak - 1
                max_dd = min(max_dd, drawdown)
            rolling_max_dd.append(max_dd)

            if benchmark is not None:
                bench_window = [float(r) for r in benchmark[idx - window_size: idx]]
                mean_bench = sum(bench_window) / window_size
                cov = sum((a - mean_return) * (b - mean_bench) for a, b in zip(window, bench_window)) / (window_size - 1)
                var_bench = sum((b - mean_bench) ** 2 for b in bench_window) / (window_size - 1)
                beta = cov / var_bench if var_bench else 0.0
                rolling_beta.append(beta)

            if prev_vol is not None and std_dev != 0:
                change = abs(std_dev - prev_vol) / prev_vol
                if change > 0.3:
                    regime_changes.append(idx - 1)
            prev_vol = std_dev if std_dev else prev_vol

        data = {
            "rolling_sharpe": rolling_sharpe,
            "rolling_max_dd": rolling_max_dd,
            "rolling_beta": rolling_beta,
            "regime_changes_detected": regime_changes
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"rolling_risk_analyzer failed: {e}")
        _log_lesson(f"rolling_risk_analyzer: {e}")
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
