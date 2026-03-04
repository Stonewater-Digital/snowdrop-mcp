"""Generate momentum signal for commodity prices."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Sequence

TOOL_META: dict[str, Any] = {
    "name": "commodity_momentum_signal",
    "description": (
        "Builds a time-series momentum signal using short and long lookback returns "
        "with volatility-adjusted scoring. Standard approach: 12-1 momentum skips "
        "the most recent month to avoid short-term reversal contamination."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "price_series": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Price series ordered from oldest to newest (must be > 0). At least lookback_long + 2 points.",
                "minItems": 4,
            },
            "lookback_short": {
                "type": "integer",
                "default": 12,
                "description": "Short lookback window in periods for momentum computation. Default 12.",
            },
            "lookback_long": {
                "type": "integer",
                "default": 36,
                "description": "Long lookback window for trend context. Default 36.",
            },
            "skip_recent": {
                "type": "integer",
                "default": 1,
                "description": "Periods to skip from end (reversal avoidance). Default 1 (12-1 style).",
            },
        },
        "required": ["price_series"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "short_return_pct": {"type": "number"},
            "long_return_pct": {"type": "number"},
            "realized_vol_pct": {"type": "number"},
            "momentum_score": {"type": "number"},
            "signal": {"type": "string"},
            "timestamp": {"type": "string"},
        },
    },
}


def commodity_momentum_signal(
    price_series: Sequence[float],
    lookback_short: int = 12,
    lookback_long: int = 36,
    skip_recent: int = 1,
    **_: Any,
) -> dict[str, Any]:
    """Return momentum score and directional signal.

    Args:
        price_series: Ordered price series from oldest to newest (all > 0).
        lookback_short: Short return lookback in periods (default 12).
        lookback_long: Long trend context lookback in periods (default 36).
        skip_recent: Periods to skip from most recent end to avoid reversal
            (default 1, implementing 12-1 momentum convention).

    Returns:
        dict with status, short_return_pct, long_return_pct, realized_vol_pct,
        momentum_score (return / vol), and directional signal.

    12-1 momentum:
        reference_price = price_series[-(1 + skip_recent)]  # skip most recent
        short_return = reference_price / price_series[-(lookback_short + skip_recent)] - 1
        long_return  = reference_price / price_series[-(lookback_long + skip_recent)] - 1

    Volatility: realized vol from period returns over short lookback window.
    Momentum score: short_return / realized_vol (Sharpe-like ratio).
    """
    try:
        prices = [float(p) for p in price_series]
        if any(p <= 0 for p in prices):
            raise ValueError("All prices must be positive")
        required_len = lookback_long + skip_recent + 1
        if len(prices) < required_len:
            raise ValueError(
                f"price_series needs at least {required_len} points "
                f"(lookback_long={lookback_long} + skip_recent={skip_recent} + 1)"
            )
        if lookback_short >= lookback_long:
            raise ValueError("lookback_short must be less than lookback_long")
        if skip_recent < 0:
            raise ValueError("skip_recent must be >= 0")

        # Reference index (skip most recent to avoid reversal)
        ref_idx = -(1 + skip_recent)
        short_start_idx = -(lookback_short + skip_recent + 1)
        long_start_idx = -(lookback_long + skip_recent + 1)

        ref_price = prices[ref_idx]
        short_return = ref_price / prices[short_start_idx] - 1.0
        long_return = ref_price / prices[long_start_idx] - 1.0

        # Realized volatility from period returns over short lookback
        short_window = prices[short_start_idx: ref_idx if ref_idx != -1 else len(prices)]
        period_returns = [
            short_window[i] / short_window[i - 1] - 1.0
            for i in range(1, len(short_window))
        ]
        if period_returns:
            mean_r = sum(period_returns) / len(period_returns)
            variance = sum((r - mean_r) ** 2 for r in period_returns) / max(len(period_returns) - 1, 1)
            realized_vol = math.sqrt(variance)
        else:
            realized_vol = 1e-9

        # Volatility-adjusted momentum score
        score = short_return / max(realized_vol, 1e-9)

        if score > 0.5:
            signal = "long"
        elif score < -0.5:
            signal = "short"
        else:
            signal = "flat"

        return {
            "status": "success",
            "short_return_pct": round(short_return * 100.0, 3),
            "long_return_pct": round(long_return * 100.0, 3),
            "realized_vol_pct": round(realized_vol * 100.0, 3),
            "momentum_score": round(score, 3),
            "signal": signal,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("commodity_momentum_signal", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
