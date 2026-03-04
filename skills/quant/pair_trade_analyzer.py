"""Analyze statistical arbitrage pair trades."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "pair_trade_analyzer",
    "description": "Computes ratio z-scores, correlation, OLS half-life, and trade signals for price pairs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "series_a": {"type": "array", "items": {"type": "number"}, "description": "Price series for asset A (>= 10 observations)."},
            "series_b": {"type": "array", "items": {"type": "number"}, "description": "Price series for asset B (same length as series_a)."},
            "labels": {"type": "array", "items": {"type": "string"}, "description": "Optional date labels."},
            "entry_z": {"type": "number", "default": 2.0, "description": "Z-score threshold for entry."},
            "exit_z": {"type": "number", "default": 0.5, "description": "Z-score threshold for exit."},
        },
        "required": ["series_a", "series_b"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "correlation": {"type": "number"},
                    "current_z_score": {"type": "number"},
                    "signal": {"type": "string"},
                    "mean_ratio": {"type": "number"},
                    "std_ratio": {"type": "number"},
                    "half_life_periods": {"type": "number"},
                    "ou_mean_reversion_speed": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def pair_trade_analyzer(
    series_a: list[float],
    series_b: list[float],
    labels: list[str] | None = None,
    entry_z: float = 2.0,
    exit_z: float = 0.5,
    **_: Any,
) -> dict[str, Any]:
    """Return z-scores, correlation, OLS-based half-life, and trade recommendations.

    Z-score is based on the price ratio A/B.
    Half-life is estimated via OLS regression:
        delta(ratio_t) = alpha + beta * ratio_{t-1} + epsilon
    Half-life = -ln(2) / beta  (valid when beta < 0, indicating mean reversion).

    Args:
        series_a: Price series for asset A (>= 10 observations).
        series_b: Price series for asset B (same length as series_a).
        labels: Optional date labels.
        entry_z: Z-score threshold for entering a position.
        exit_z: Z-score threshold for exiting a position.

    Returns:
        dict with correlation, current_z_score, signal, mean_ratio,
        std_ratio, half_life_periods, ou_mean_reversion_speed.
    """
    try:
        if len(series_a) != len(series_b):
            raise ValueError("series_a and series_b must be the same length")
        if len(series_a) < 10:
            raise ValueError("Need at least 10 observations for reliable estimates")
        for b in series_b:
            if b == 0:
                raise ValueError("series_b contains zero, cannot compute ratio")

        ratios = [a / b for a, b in zip(series_a, series_b)]
        n = len(ratios)
        mean_ratio = sum(ratios) / n
        variance = sum((r - mean_ratio) ** 2 for r in ratios) / max(n - 1, 1)
        std_ratio = math.sqrt(variance) if variance > 0 else 1e-9

        current_z = (ratios[-1] - mean_ratio) / std_ratio
        correlation = _correlation(series_a, series_b)

        # OU half-life via OLS: regress delta(ratio) on lagged ratio
        # delta_t = alpha + beta * ratio_{t-1}
        lag = ratios[:-1]
        delta = [ratios[i + 1] - ratios[i] for i in range(n - 1)]
        m = len(lag)
        mean_lag = sum(lag) / m
        mean_delta = sum(delta) / m
        cov_ld = sum((lag[i] - mean_lag) * (delta[i] - mean_delta) for i in range(m))
        var_lag = sum((l - mean_lag) ** 2 for l in lag)
        beta = cov_ld / var_lag if var_lag > 0 else 0.0

        if -1.0 < beta < 0.0:
            half_life = -math.log(2) / beta
            ou_speed = -beta
        else:
            half_life = float("inf")
            ou_speed = 0.0

        signal = "neutral"
        if current_z > entry_z:
            signal = "short_a_long_b"
        elif current_z < -entry_z:
            signal = "long_a_short_b"
        elif abs(current_z) < exit_z:
            signal = "close"

        data = {
            "correlation": round(correlation, 3),
            "current_z_score": round(current_z, 2),
            "signal": signal,
            "mean_ratio": round(mean_ratio, 4),
            "std_ratio": round(std_ratio, 4),
            "half_life_periods": round(half_life, 2) if math.isfinite(half_life) else None,
            "ou_mean_reversion_speed": round(ou_speed, 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson(f"pair_trade_analyzer: {exc}")
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _correlation(a: list[float], b: list[float]) -> float:
    """Pearson correlation between two equal-length series."""
    n = len(a)
    mean_a = sum(a) / n
    mean_b = sum(b) / n
    numerator = sum((a[i] - mean_a) * (b[i] - mean_b) for i in range(n))
    denominator = math.sqrt(
        sum((x - mean_a) ** 2 for x in a) * sum((y - mean_b) ** 2 for y in b)
    )
    return numerator / denominator if denominator else 0.0


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
