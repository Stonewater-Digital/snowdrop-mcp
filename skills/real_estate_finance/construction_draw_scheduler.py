"""Schedule construction loan draws."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "construction_draw_scheduler",
    "description": "Generates draw schedules, interest carry, and LTC compliance checks.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_budget": {"type": "number"},
            "loan_amount": {"type": "number"},
            "ltc_ratio": {"type": "number"},
            "phases": {"type": "array", "items": {"type": "object"}},
            "interest_rate": {"type": "number"},
            "interest_reserve_months": {"type": "integer", "default": 6},
        },
        "required": ["total_budget", "loan_amount", "ltc_ratio", "phases", "interest_rate"],
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


def construction_draw_scheduler(
    total_budget: float,
    loan_amount: float,
    ltc_ratio: float,
    phases: list[dict[str, Any]],
    interest_rate: float,
    interest_reserve_months: int = 6,
    **_: Any,
) -> dict[str, Any]:
    """Return draw schedule and interest reserve requirements."""
    try:
        cumulative_draw = 0.0
        draw_schedule = []
        total_interest = 0.0
        peak_balance = 0.0
        for phase in phases:
            budget = total_budget * (phase.get("budget_pct", 0.0) / 100)
            draw = min(budget, loan_amount - cumulative_draw)
            cumulative_draw += draw
            months = phase.get("duration_months", 1)
            interest = draw * interest_rate * (months / 12)
            total_interest += interest
            peak_balance = max(peak_balance, cumulative_draw)
            draw_schedule.append(
                {
                    "phase_name": phase.get("phase_name"),
                    "draw_amount": round(draw, 2),
                    "start_month": phase.get("start_month"),
                    "duration_months": months,
                    "ltc_compliant": (cumulative_draw / total_budget) <= (ltc_ratio / 100),
                }
            )
        interest_reserve_required = interest_rate * peak_balance * (interest_reserve_months / 12)
        data = {
            "draw_schedule": draw_schedule,
            "total_draws": round(cumulative_draw, 2),
            "interest_reserve_required": round(interest_reserve_required, 2),
            "total_interest_during_construction": round(total_interest, 2),
            "peak_loan_balance": round(peak_balance, 2),
            "completion_month": max((phase.get("start_month", 0) + phase.get("duration_months", 0)) for phase in phases),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("construction_draw_scheduler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
