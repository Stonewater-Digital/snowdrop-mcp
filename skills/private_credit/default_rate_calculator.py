"""Compute cohort default rates across periods."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence

TOOL_META: dict[str, Any] = {
    "name": "default_rate_calculator",
    "description": "Calculates period and trailing default rates from cohort data.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "defaults_by_period": {"type": "array", "items": {"type": "number"}},
            "outstandings_by_period": {"type": "array", "items": {"type": "number"}},
            "lookback_periods": {"type": "integer", "default": 4},
        },
        "required": ["defaults_by_period", "outstandings_by_period"],
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


def default_rate_calculator(
    defaults_by_period: Sequence[float],
    outstandings_by_period: Sequence[float],
    lookback_periods: int = 4,
    **_: Any,
) -> dict[str, Any]:
    """Return default rates and trailing averages."""
    try:
        if len(defaults_by_period) != len(outstandings_by_period):
            raise ValueError("defaults_by_period and outstandings_by_period must be same length")
        period_rates = []
        for defaults, outstanding in zip(defaults_by_period, outstandings_by_period):
            rate = defaults / outstanding if outstanding else 0.0
            period_rates.append(round(rate * 100, 2))
        trailing = period_rates[-lookback_periods:] if lookback_periods else period_rates
        trailing_avg = sum(trailing) / len(trailing) if trailing else 0.0
        cumulative_defaults = sum(defaults_by_period)
        cumulative_outstanding = sum(outstandings_by_period)
        cumulative_rate = cumulative_defaults / cumulative_outstanding * 100 if cumulative_outstanding else 0.0
        data = {
            "period_default_rates_pct": period_rates,
            "trailing_avg_default_rate_pct": round(trailing_avg, 2),
            "cumulative_default_rate_pct": round(cumulative_rate, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("default_rate_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
