"""
Executive Smary: Debt avalanche model targeting highest-rate balances first.
Inputs: debts (list), extra_payment (float)
Outputs: payoff_order (list), total_months (int), total_interest_paid (float), month_by_month_schedule (list), debt_free_date (str), comparison_vs_snowball (dict)
MCP Tool Name: debt_avalanche_planner
"""
import calendar
import logging
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Tuple

logger = logging.getLogger("snowdrop.skills")


def _add_months(dt: datetime, months: int) -> datetime:
    year = dt.year + (dt.month - 1 + months) // 12
    month = (dt.month - 1 + months) % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return datetime(year, month, day, tzinfo=timezone.utc)


TOOL_META = {
    "name": "debt_avalanche_planner",
    "description": (
        "Simulates the debt avalanche payoff strategy (highest interest rate first) and "
        "contrasts it against a classic snowball to highlight savings."
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
                "description": "Additional monthly dollars directed at the focus debt.",
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


def debt_avalanche_planner(**kwargs: Any) -> dict:
    """Run the avalanche plan and compare to snowball to show time and interest savings."""
    try:
        debts_input = kwargs["debts"]
        extra_payment = float(kwargs["extra_payment"])

        if not isinstance(debts_input, list) or not debts_input:
            raise ValueError("debts must be a non-empty list")
        if extra_payment < 0:
            raise ValueError("extra_payment must be non-negative")

        avalanche = _simulate_strategy(debts_input, extra_payment, lambda d: -d["rate"])
        snowball = _simulate_strategy(debts_input, extra_payment, lambda d: d["balance"])

        comparison = {
            "months_saved": snowball["total_months"] - avalanche["total_months"],
            "interest_saved": snowball["total_interest_paid"] - avalanche["total_interest_paid"],
        }

        return {
            "status": "success",
            "data": {
                **avalanche,
                "comparison_vs_snowball": comparison,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"debt_avalanche_planner failed: {e}")
        _log_lesson(f"debt_avalanche_planner: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _simulate_strategy(
    debts_input: List[Dict[str, Any]],
    extra_payment: float,
    sort_key: Callable[[Dict[str, float]], float],
) -> Dict[str, Any]:
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

    payoff_order: List[str] = []
    schedule: List[Dict[str, Any]] = []
    month = 0
    total_interest = 0.0
    while debts:
        debts.sort(key=sort_key)
        focus = debts[0]
        month += 1
        payments = []
        for debt in list(debts):
            monthly_rate = debt["rate"] / 12
            interest = debt["balance"] * monthly_rate
            payment = debt["min_payment"]
            if debt is focus:
                payment += extra_payment
            principal = payment - interest
            if principal <= 0:
                raise ValueError("Payments do not cover interest; increase extra_payment")
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
            raise ValueError("Repayment exceeds 50 years; verify inputs")

    debt_free_date = _add_months(datetime.now(timezone.utc), month).isoformat()
    return {
        "payoff_order": payoff_order,
        "total_months": month,
        "total_interest_paid": total_interest,
        "month_by_month_schedule": schedule,
        "debt_free_date": debt_free_date,
    }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
