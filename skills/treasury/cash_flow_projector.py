"""Project short-term cash flows for Snowdrop Treasury."""
from __future__ import annotations

from datetime import datetime, timezone
from calendar import month_name
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "cash_flow_projector",
    "description": "Computes monthly cash flow projections with cumulative balances and risk flags.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "recurring_revenue": {"type": "array", "items": {"type": "object"}},
            "recurring_expenses": {"type": "array", "items": {"type": "object"}},
            "one_time_items": {"type": "array", "items": {"type": "object"}},
            "months_forward": {"type": "integer", "default": 6},
        },
        "required": ["recurring_revenue", "recurring_expenses", "one_time_items"],
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


def cash_flow_projector(
    recurring_revenue: list[dict[str, Any]],
    recurring_expenses: list[dict[str, Any]],
    one_time_items: list[dict[str, Any]],
    months_forward: int = 6,
    **_: Any,
) -> dict[str, Any]:
    """Forecast monthly cash movement and highlight first negative balance."""
    try:
        if months_forward <= 0:
            raise ValueError("months_forward must be positive")

        monthly_rev = sum(float(item.get("monthly_amount", 0.0)) for item in recurring_revenue)
        monthly_exp = sum(float(item.get("monthly_amount", 0.0)) for item in recurring_expenses)
        start = datetime.now(timezone.utc)
        schedule = []
        cumulative_balance = 0.0
        first_negative_label = None

        one_time_map: dict[int, float] = {}
        for item in one_time_items:
            month_idx = int(item.get("month", 1))
            amount = float(item.get("amount", 0.0))
            one_time_map[month_idx] = one_time_map.get(month_idx, 0.0) + amount

        for idx in range(1, months_forward + 1):
            ot_amount = one_time_map.get(idx, 0.0)
            net_cash_flow = monthly_rev - monthly_exp + ot_amount
            cumulative_balance += net_cash_flow
            label_month = (start.month + idx - 1 - 1) % 12 + 1
            label_year = start.year + (start.month + idx - 2) // 12
            label = f"{month_name[label_month]} {label_year}"
            schedule.append(
                {
                    "month_index": idx,
                    "label": label,
                    "recurring_revenue": round(monthly_rev, 2),
                    "recurring_expenses": round(monthly_exp, 2),
                    "one_time_items": round(ot_amount, 2),
                    "net_cash_flow": round(net_cash_flow, 2),
                    "cumulative_balance": round(cumulative_balance, 2),
                }
            )
            if cumulative_balance < 0 and first_negative_label is None:
                first_negative_label = label

        data = {
            "monthly_projection": schedule,
            "first_negative_month": first_negative_label,
            "ending_balance": round(cumulative_balance, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("cash_flow_projector", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
