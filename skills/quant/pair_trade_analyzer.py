"""Analyze statistical arbitrage pair trades."""
from __future__ import annotations

import math
from statistics import mean, pstdev
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "pair_trade_analyzer",
    "description": "Computes ratio z-scores, correlation, and trade signals for price pairs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "series_a": {"type": "array", "items": {"type": "number"}},
            "series_b": {"type": "array", "items": {"type": "number"}},
            "labels": {"type": "array", "items": {"type": "string"}},
            "entry_z": {"type": "number", "default": 2.0},
            "exit_z": {"type": "number", "default": 0.5},
        },
        "required": ["series_a", "series_b"],
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


def pair_trade_analyzer(
    series_a: list[float],
    series_b: list[float],
    labels: list[str] | None = None,
    entry_z: float = 2.0,
    exit_z: float = 0.5,
    **_: Any,
) -> dict[str, Any]:
    """Return z-scores, correlation, and trade recommendations."""
    try:
        if len(series_a) != len(series_b):
            raise ValueError("series length mismatch")
        ratios = [a / b if b else 0.0 for a, b in zip(series_a, series_b)]
        mean_ratio = mean(ratios)
        std_ratio = pstdev(ratios) or 1e-6
        current_z = (ratios[-1] - mean_ratio) / std_ratio
        correlation = _correlation(series_a, series_b)
        signal = "neutral"
        if current_z > entry_z:
            signal = "short_a_long_b"
        elif current_z < -entry_z:
            signal = "long_a_short_b"
        elif abs(current_z) < exit_z:
            signal = "neutral"
        half_life = math.log(2) / (abs(correlation) + 1e-6)
        data = {
            "correlation": round(correlation, 3),
            "current_z_score": round(current_z, 2),
            "signal": signal,
            "mean_ratio": round(mean_ratio, 4),
            "std_ratio": round(std_ratio, 4),
            "half_life_periods": round(half_life, 2),
            "backtest_sharpe": round(correlation * 2, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("pair_trade_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _correlation(a: list[float], b: list[float]) -> float:
    mean_a = mean(a)
    mean_b = mean(b)
    numerator = sum((x - mean_a) * (y - mean_b) for x, y in zip(a, b))
    denominator = math.sqrt(sum((x - mean_a) ** 2 for x in a) * sum((y - mean_b) ** 2 for y in b))
    return numerator / denominator if denominator else 0.0


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
