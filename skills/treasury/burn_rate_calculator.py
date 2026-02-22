"""Calculate net burn dynamics and runway guidance."""
from __future__ import annotations

from datetime import datetime, timezone
from statistics import mean
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "burn_rate_calculator",
    "description": "Calculates gross/net burn, runway, and trend classification from recent data.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "monthly_expenses": {"type": "array", "items": {"type": "number"}},
            "monthly_revenue": {"type": "array", "items": {"type": "number"}},
            "current_cash": {"type": "number"},
        },
        "required": ["monthly_expenses", "monthly_revenue", "current_cash"],
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


def burn_rate_calculator(
    monthly_expenses: list[float],
    monthly_revenue: list[float],
    current_cash: float,
    **_: Any,
) -> dict[str, Any]:
    """Return burn metrics and qualitative trend."""
    try:
        if not monthly_expenses:
            raise ValueError("monthly_expenses required")
        if not monthly_revenue:
            raise ValueError("monthly_revenue required")
        if current_cash < 0:
            raise ValueError("current_cash cannot be negative")

        gross_burn = mean(monthly_expenses)
        net_burn = gross_burn - mean(monthly_revenue)
        net_burn = round(net_burn, 2)
        runway_months = float("inf") if net_burn <= 0 else round(current_cash / net_burn, 1)
        break_even_revenue = round(gross_burn, 2)
        trend = _trend_direction(monthly_expenses)

        data = {
            "gross_burn_rate": round(gross_burn, 2),
            "net_burn_rate": net_burn,
            "runway_months": runway_months,
            "break_even_monthly_revenue": break_even_revenue,
            "trend": trend,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("burn_rate_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _trend_direction(series: list[float]) -> str:
    if len(series) < 3:
        return "insufficient_data"
    recent = series[-3:]
    deltas = [recent[i + 1] - recent[i] for i in range(len(recent) - 1)]
    avg_delta = sum(deltas) / len(deltas)
    if avg_delta > 0:
        return "accelerating"
    if avg_delta < 0:
        return "decelerating"
    return "stable"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
