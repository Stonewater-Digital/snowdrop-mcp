"""Risk-adjusted performance ratios for Snowdrop portfolios."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "sharpe_ratio_calculator",
    "description": "Calculates Sharpe, Sortino, and ancillary performance stats.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {
                "type": "array",
                "items": {"type": "number"},
            },
            "risk_free_rate_annual": {"type": "number", "default": 0.05},
        },
        "required": ["returns"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "sharpe_ratio": {"type": "number"},
                    "sortino_ratio": {"type": "number"},
                    "annualized_return": {"type": "number"},
                    "annualized_volatility": {"type": "number"},
                    "max_loss_streak": {"type": "integer"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def sharpe_ratio_calculator(
    returns: list[float],
    risk_free_rate_annual: float = 0.05,
    **_: Any,
) -> dict[str, Any]:
    """Compute risk-adjusted metrics."""

    try:
        if len(returns) < 2:
            raise ValueError("returns must contain at least two observations")

        daily_returns = [float(r) for r in returns]
        mean_daily = sum(daily_returns) / len(daily_returns)
        variance = sum((r - mean_daily) ** 2 for r in daily_returns) / (len(daily_returns) - 1)
        std_daily = math.sqrt(max(variance, 0))
        daily_rf = (1 + risk_free_rate_annual) ** (1 / 252) - 1

        sharpe = 0.0 if std_daily == 0 else (mean_daily - daily_rf) / std_daily * math.sqrt(252)

        downside = [min(0.0, r - daily_rf) for r in daily_returns]
        downside_variance = sum(d ** 2 for d in downside) / len(downside)
        downside_std = math.sqrt(max(downside_variance, 0))
        sortino = (
            0.0
            if downside_std == 0
            else (mean_daily - daily_rf) / downside_std * math.sqrt(252)
        )

        ann_return = (1 + mean_daily) ** 252 - 1
        ann_vol = std_daily * math.sqrt(252)
        loss_streak = _max_loss_streak(daily_returns)

        data = {
            "sharpe_ratio": round(sharpe, 4),
            "sortino_ratio": round(sortino, 4),
            "annualized_return": round(ann_return, 4),
            "annualized_volatility": round(ann_vol, 4),
            "max_loss_streak": loss_streak,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("sharpe_ratio_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _max_loss_streak(returns: list[float]) -> int:
    streak = 0
    max_streak = 0
    for value in returns:
        if value < 0:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0
    return max_streak


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
