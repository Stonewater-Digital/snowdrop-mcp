"""Detect mean-reversion strength for a price series."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Sequence

TOOL_META: dict[str, Any] = {
    "name": "mean_reversion_detector",
    "description": "Estimates Ornstein-Uhlenbeck half-life and current deviation z-score via OLS regression.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "price_series": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Time-ordered price series (at least 10 observations recommended).",
            },
        },
        "required": ["price_series"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "z_score": {"type": "number"},
                    "ou_beta": {"type": "number"},
                    "half_life_periods": {"type": ["number", "null"]},
                    "long_run_mean": {"type": "number"},
                    "signal": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def mean_reversion_detector(price_series: Sequence[float], **_: Any) -> dict[str, Any]:
    """Return OU half-life, long-run mean, and standardized deviation.

    Estimates the OU mean-reversion parameter via OLS:
        delta(P_t) = alpha + beta * P_{t-1} + epsilon
    where beta < 0 implies mean reversion.
    Half-life = -ln(2) / beta.
    Long-run mean = -alpha / beta (the equilibrium level).

    Args:
        price_series: Time-ordered price series (>= 5 observations).

    Returns:
        dict with z_score (deviation from historical mean), ou_beta,
        half_life_periods, long_run_mean, signal.
    """
    try:
        if len(price_series) < 5:
            raise ValueError("price_series must have at least 5 observations")

        values = [float(p) for p in price_series]
        n = len(values)

        # Historical mean and std for z-score
        hist_mean = sum(values) / n
        variance = sum((v - hist_mean) ** 2 for v in values) / max(n - 1, 1)
        std_dev = math.sqrt(variance) if variance > 0 else 0.0
        current_z = (values[-1] - hist_mean) / std_dev if std_dev else 0.0

        # OLS: regress delta(P) on alpha + beta * lag(P)
        lag = values[:-1]
        delta = [values[i + 1] - values[i] for i in range(n - 1)]
        m = len(lag)

        mean_lag = sum(lag) / m
        mean_delta = sum(delta) / m

        cov_ld = sum((lag[i] - mean_lag) * (delta[i] - mean_delta) for i in range(m))
        var_lag = sum((l - mean_lag) ** 2 for l in lag)

        if var_lag == 0:
            raise ValueError("Insufficient variation in price_series to estimate OU parameters")

        beta = cov_ld / var_lag
        alpha = mean_delta - beta * mean_lag

        # Long-run mean (equilibrium): E[P] = -alpha/beta
        long_run_mean = -alpha / beta if beta != 0 else hist_mean

        if -1.0 < beta < 0.0:
            half_life = -math.log(2) / beta
        else:
            half_life = float("inf")

        signal = "revert" if abs(current_z) > 1 and beta < 0 else "drift"

        data = {
            "z_score": round(current_z, 2),
            "ou_beta": round(beta, 4),
            "half_life_periods": round(half_life, 2) if math.isfinite(half_life) else None,
            "long_run_mean": round(long_run_mean, 4),
            "signal": signal,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson(f"mean_reversion_detector: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
