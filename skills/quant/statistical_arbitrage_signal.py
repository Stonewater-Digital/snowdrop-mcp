"""Create stat-arb entry signals from two price series."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Sequence

TOOL_META: dict[str, Any] = {
    "name": "statistical_arbitrage_signal",
    "description": "Computes OLS hedge ratio, spread z-score, and entry/exit guidance for a pair.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "series_x": {"type": "array", "items": {"type": "number"}, "description": "Price series for asset X (>= 10 observations)."},
            "series_y": {"type": "array", "items": {"type": "number"}, "description": "Price series for asset Y (same length as series_x)."},
            "entry_z": {"type": "number", "default": 2.0, "description": "Z-score threshold for trade entry."},
            "exit_z": {"type": "number", "default": 0.5, "description": "Z-score threshold for trade exit."},
        },
        "required": ["series_x", "series_y"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "hedge_ratio": {"type": "number"},
                    "spread_z_score": {"type": "number"},
                    "spread_mean": {"type": "number"},
                    "spread_std": {"type": "number"},
                    "signal": {"type": "string"},
                    "entry_threshold": {"type": "number"},
                    "exit_threshold": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def statistical_arbitrage_signal(
    series_x: Sequence[float],
    series_y: Sequence[float],
    entry_z: float = 2.0,
    exit_z: float = 0.5,
    **_: Any,
) -> dict[str, Any]:
    """Compute hedge ratio and spread z-score for a stat-arb pair.

    Hedge ratio beta = cov(X, Y) / var(Y), so that:
        spread_t = X_t - beta * Y_t
    is the regression residual of X on Y.

    Signal logic:
        z > +entry_z  -> enter_short_x (spread too wide, X expensive vs Y)
        z < -entry_z  -> enter_long_x  (spread too narrow, X cheap vs Y)
        |z| <= exit_z -> close position

    Args:
        series_x: Price series for asset X (>= 10 observations).
        series_y: Price series for asset Y (same length as series_x).
        entry_z: Entry threshold.
        exit_z: Exit threshold.

    Returns:
        dict with hedge_ratio, spread_z_score, spread_mean, spread_std,
        signal, entry_threshold, exit_threshold.
    """
    try:
        if len(series_x) != len(series_y):
            raise ValueError("series_x and series_y must be the same length")
        if len(series_x) < 10:
            raise ValueError("Need at least 10 observations for reliable estimates")
        if entry_z <= exit_z:
            raise ValueError("entry_z must be greater than exit_z")

        x_vals = [float(v) for v in series_x]
        y_vals = [float(v) for v in series_y]
        n = len(x_vals)

        mean_x = sum(x_vals) / n
        mean_y = sum(y_vals) / n

        # OLS regression of X on Y: beta = cov(X,Y) / var(Y)
        cov_xy = sum((x_vals[i] - mean_x) * (y_vals[i] - mean_y) for i in range(n))
        var_y = sum((y - mean_y) ** 2 for y in y_vals)

        if var_y == 0:
            raise ValueError("series_y has zero variance; cannot compute hedge ratio")

        beta = cov_xy / var_y

        # Spread = X - beta * Y
        spread = [x_vals[i] - beta * y_vals[i] for i in range(n)]
        spread_mean = sum(spread) / n
        variance = sum((s - spread_mean) ** 2 for s in spread) / max(n - 1, 1)
        std_dev = math.sqrt(variance) if variance > 0 else 0.0

        if std_dev == 0:
            raise ValueError("Spread has zero variance; cannot compute z-score")

        latest = spread[-1]
        z_score = (latest - spread_mean) / std_dev

        if abs(z_score) >= entry_z:
            signal = "enter_long_x" if z_score < 0 else "enter_short_x"
        elif abs(z_score) <= exit_z:
            signal = "close"
        else:
            signal = "hold"

        data = {
            "hedge_ratio": round(beta, 4),
            "spread_z_score": round(z_score, 2),
            "spread_mean": round(spread_mean, 4),
            "spread_std": round(std_dev, 4),
            "signal": signal,
            "entry_threshold": entry_z,
            "exit_threshold": exit_z,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson(f"statistical_arbitrage_signal: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
