"""Moving average crossover signal generator."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "moving_average_crossover",
    "description": "Calculates SMA/EMA crossovers and emits trading posture signals.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {
                "type": "array",
                "items": {"type": "number"},
            },
            "short_window": {"type": "integer", "default": 20},
            "long_window": {"type": "integer", "default": 50},
            "use_ema": {"type": "boolean", "default": True},
        },
        "required": ["prices"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "short_ma": {"type": "number"},
                    "long_ma": {"type": "number"},
                    "signal": {"type": "string"},
                    "history": {"type": "array", "items": {"type": "object"}},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def moving_average_crossover(
    prices: list[float],
    short_window: int = 20,
    long_window: int = 50,
    use_ema: bool = True,
    **_: Any,
) -> dict[str, Any]:
    """Compute moving averages and signal state."""

    try:
        if len(prices) < max(short_window, long_window):
            raise ValueError("Not enough price points for the requested windows")
        if short_window >= long_window:
            raise ValueError("short_window should be smaller than long_window")

        if use_ema:
            short_series = _ema_series(prices, short_window)
            long_series = _ema_series(prices, long_window)
        else:
            short_series = _sma_series(prices, short_window)
            long_series = _sma_series(prices, long_window)

        current_short = short_series[-1]
        current_long = long_series[-1]
        signal = "neutral"
        if current_short > current_long:
            signal = "bullish_cross"
        elif current_short < current_long:
            signal = "bearish_cross"

        history = _crossover_history(short_series, long_series)
        return {
            "status": "success",
            "data": {
                "short_ma": round(current_short, 6),
                "long_ma": round(current_long, 6),
                "signal": signal,
                "history": history,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("moving_average_crossover", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _ema_series(prices: list[float], window: int) -> list[float]:
    alpha = 2 / (window + 1)
    ema_values: list[float] = []
    ema = sum(prices[:window]) / window
    for idx, price in enumerate(prices):
        if idx < window:
            ema = sum(prices[: idx + 1]) / (idx + 1)
        else:
            ema = ema + alpha * (price - ema)
        ema_values.append(ema)
    return ema_values


def _sma_series(prices: list[float], window: int) -> list[float]:
    smas: list[float] = []
    cumulative = 0.0
    for idx, price in enumerate(prices):
        cumulative += price
        if idx >= window:
            cumulative -= prices[idx - window]
        count = min(idx + 1, window)
        smas.append(cumulative / count)
    return smas


def _crossover_history(short_series: list[float], long_series: list[float]) -> list[dict[str, Any]]:
    history: list[dict[str, Any]] = []
    prev_diff = None
    for idx, (short_val, long_val) in enumerate(zip(short_series, long_series)):
        diff = short_val - long_val
        if prev_diff is None:
            prev_diff = diff
            continue
        if diff == 0:
            prev_diff = diff
            continue
        if prev_diff <= 0 < diff:
            history.append({"index": idx, "signal": "bullish_cross"})
        elif prev_diff >= 0 > diff:
            history.append({"index": idx, "signal": "bearish_cross"})
        prev_diff = diff
    return history


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
