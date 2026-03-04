"""Generate cross-over momentum signals."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence

TOOL_META: dict[str, Any] = {
    "name": "momentum_signal_generator",
    "description": "Calculates short vs long lookback momentum and standardized signal strength.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "price_series": {"type": "array", "items": {"type": "number"}},
            "short_window": {"type": "integer", "default": 20},
            "long_window": {"type": "integer", "default": 60},
        },
        "required": ["price_series"],
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


def momentum_signal_generator(
    price_series: Sequence[float],
    short_window: int = 20,
    long_window: int = 60,
    **_: Any,
) -> dict[str, Any]:
    """Return moving-average momentum and z-score."""
    try:
        prices = [float(p) for p in price_series]
        if len(prices) < max(short_window, long_window) + 1:
            raise ValueError("price_series too short for requested windows")
        returns = [(prices[i] / prices[i - 1]) - 1 for i in range(1, len(prices))]
        short_avg = sum(returns[-short_window:]) / short_window
        long_avg = sum(returns[-long_window:]) / long_window
        momentum = short_avg - long_avg
        volatility = (sum((r - long_avg) ** 2 for r in returns[-long_window:]) / long_window) ** 0.5
        z_score = momentum / volatility if volatility else 0.0
        data = {
            "short_momentum_pct": round(short_avg * 100, 2),
            "long_momentum_pct": round(long_avg * 100, 2),
            "spread_pct": round(momentum * 100, 2),
            "z_score": round(z_score, 2),
            "signal": "long" if momentum > 0 else "short" if momentum < 0 else "flat",
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        _log_lesson(f"momentum_signal_generator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
