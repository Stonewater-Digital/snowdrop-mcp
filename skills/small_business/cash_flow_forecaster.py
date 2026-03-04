"""
Executive Smary: Projects 12-month cash flow using revenue growth, fixed/variable costs, and one-time expenses.
Inputs: starting_cash (float), monthly_revenue (float), revenue_growth_rate (float), fixed_expenses (list), variable_expense_pct (float), one_time_expenses (list)
Outputs: month_by_month_forecast (list), ending_cash (float), lowest_cash_month (dict), positive_cash_flow_month (int)
MCP Tool Name: cash_flow_forecaster
"""
import logging
from datetime import datetime, timezone
from typing import Any, List, Dict

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "cash_flow_forecaster",
    "description": (
        "Builds a 12-month cash forecast factoring in revenue growth, fixed operating "
        "costs, variable expenses, and scheduled one-time cash outlays."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "starting_cash": {"type": "number", "description": "Beginning cash balance."},
            "monthly_revenue": {"type": "number", "description": "Current monthly revenue run rate."},
            "revenue_growth_rate": {"type": "number", "description": "Expected monthly growth rate as decimal."},
            "fixed_expenses": {
                "type": "array",
                "description": "List of fixed expenses per month.",
                "items": {"type": "number"},
            },
            "variable_expense_pct": {
                "type": "number",
                "description": "Variable expense percentage of revenue.",
            },
            "one_time_expenses": {
                "type": "array",
                "description": "List of {month, amount} one-time cash items.",
                "items": {"type": "object"},
            },
        },
        "required": [
            "starting_cash",
            "monthly_revenue",
            "revenue_growth_rate",
            "fixed_expenses",
            "variable_expense_pct",
            "one_time_expenses",
        ],
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


def cash_flow_forecaster(**kwargs: Any) -> dict:
    """Create a 12-month cash forecast with revenue growth and expense assumptions."""
    try:
        starting_cash = float(kwargs["starting_cash"])
        revenue = float(kwargs["monthly_revenue"])
        growth = float(kwargs["revenue_growth_rate"])
        fixed_expenses = [float(val) for val in kwargs["fixed_expenses"]]
        variable_pct = float(kwargs["variable_expense_pct"])
        one_times = kwargs["one_time_expenses"]

        fixed_total = sum(fixed_expenses)
        one_time_map = {int(item["month"]): float(item["amount"]) for item in one_times}
        cash = starting_cash
        forecast: List[Dict[str, float]] = []
        lowest = {"month": 0, "cash": cash}
        positive_month = None

        for month in range(1, 13):
            revenue *= (1 + growth) if month > 1 else 1 + 0
            variable_expense = revenue * variable_pct
            one_time = one_time_map.get(month, 0.0)
            net = revenue - fixed_total - variable_expense - one_time
            cash += net
            if cash < lowest["cash"]:
                lowest = {"month": month, "cash": cash}
            if positive_month is None and net > 0:
                positive_month = month
            forecast.append(
                {
                    "month": month,
                    "revenue": revenue,
                    "net_cash_flow": net,
                    "ending_cash": cash,
                }
            )

        return {
            "status": "success",
            "data": {
                "month_by_month_forecast": forecast,
                "ending_cash": cash,
                "lowest_cash_month": lowest,
                "positive_cash_flow_month": positive_month,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error(f"cash_flow_forecaster failed: {e}")
        _log_lesson(f"cash_flow_forecaster: {e}")
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
