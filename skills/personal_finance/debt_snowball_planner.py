"""
Executive Smary: Builds a debt snowball payoff plan attacking smallest balances first.
Inputs: debts (list), extra_payment (float)
Outputs: payoff_order (list), total_months (int), total_interest_paid (float), month_by_month_schedule (list), debt_free_date (str)
MCP Tool Name: debt_snowball_planner
"""
import calendar
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")


def _add_months(dt: datetime, months: int) -> datetime:
    year = dt.year + (dt.month - 1 + months) // 12
    month = (dt.month - 1 + months) % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return datetime(year, month, day, tzinfo=timezone.utc)


TOOL_META = {
    "name": "debt_snowball_planner",
    "description": (
        "Simulates a debt snowball strategy by ordering balances from smallest to largest, "
        "applying extra cash to the current focus account, and outputting the payoff timeline."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "debts": {
                "type": "array",
                "description": "List of debts with name, balance, rate, and min_payment.",
                "items": {"type": "object"},
            },
            "extra_payment": {
                "type": "number",
                "description": "Additional dollars applied to the current snowball focus.",
            },
        },
        "required": ["debts", "extra_payment"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
        },
        "required": ["status", "timestamp"],
    },
}


def debt_snowball_planner(**kwargs: Any) -> dict:
    """Simulate debt snowball elimination schedule and payoff order."""
    try:
        debts_input = kwargs["debts"]
        extra_payment = float(kwargs["extra_payment"])

        if not isinstance(debts_input, list) or not debts_input:
            raise ValueError("debts must be a non-empty list")
        if extra_payment < 0:
            raise ValueError("extra_payment must be non-negative")

        debts = [
            {
                "name": str(item["name"]),
                "balance": float(item["balance"]),
                "rate": float(item.get("rate", 0.0)),
                "min_payment": float(item["min_payment"]),
            }
            for item in debts_input
        ]

        for debt in debts:
            if debt["balance"] <= 0 or debt["min_payment"] <= 0:
                raise ValueError("balances and min payments must be positive")

        debts.sort(key=lambda x: x["balance"])
        payoff_order: List[str] = []
        schedule = []
        month = 0
        total_interest = 0.0
        while debts:
            month += 1
            payments = []
            focus = debts[0]
            extra_available = extra_payment
            for debt in list(debts):
                monthly_rate = debt["rate"] / 12
                interest = debt["balance"] * monthly_rate
                payment = debt["min_payment"]
                if debt is focus:
                    payment += extra_available
                principal = payment - interest
                if principal <= 0:
                    raise ValueError("Payment does not cover accrued interest for snowball plan")
                debt["balance"] -= principal
                total_interest += interest
                payments.append(
                    {
                        "debt": debt["name"],
                        "interest": interest,
                        "principal": principal,
                        "remaining_balance": max(debt["balance"], 0.0),
                    }
                )
                if debt["balance"] <= 0:
                    payoff_order.append(debt["name"])
                    debts.remove(debt)
            schedule.append({"month": month, "payments": payments})
            if month > 600:
                raise ValueError("Snowball plan exceeds 50 years; check inputs")

        debt_free_date = _add_months(datetime.now(timezone.utc), month).isoformat()

        return {
            "status": "success",
            "data": {
                "payoff_order": payoff_order,
                "total_months": month,
                "total_interest_paid": total_interest,
                "month_by_month_schedule": schedule,
                "debt_free_date": debt_free_date,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"debt_snowball_planner failed: {e}")
        _log_lesson(f"debt_snowball_planner: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
