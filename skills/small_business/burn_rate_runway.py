"""
Executive Smary: Calculates startup burn rate, runway, and zero-cash date with revenue growth.
Inputs: monthly_revenue (float), monthly_expenses (float), cash_on_hand (float), revenue_growth_rate (float)
Outputs: gross_burn (float), net_burn (float), runway_months (float), runway_with_growth (float), zero_cash_date (str)
MCP Tool Name: burn_rate_runway
"""
import calendar
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")


def _add_months(dt: datetime, months: int) -> datetime:
    year = dt.year + (dt.month - 1 + months) // 12
    month = (dt.month - 1 + months) % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return datetime(year, month, day, tzinfo=timezone.utc)


TOOL_META = {
    "name": "burn_rate_runway",
    "description": (
        "Computes gross and net burn rates, cash runway, and projected zero-cash date "
        "accounting for compounding revenue growth."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "monthly_revenue": {
                "type": "number",
                "description": "Current recurring revenue per month.",
            },
            "monthly_expenses": {
                "type": "number",
                "description": "Operating expenses per month.",
            },
            "cash_on_hand": {
                "type": "number",
                "description": "Cash reserves available.",
            },
            "revenue_growth_rate": {
                "type": "number",
                "description": "Expected monthly revenue growth rate as decimal.",
            },
        },
        "required": ["monthly_revenue", "monthly_expenses", "cash_on_hand", "revenue_growth_rate"],
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


def burn_rate_runway(**kwargs: Any) -> dict:
    """Model burn rate and projected runway with growth in revenue."""
    try:
        monthly_revenue = float(kwargs["monthly_revenue"])
        monthly_expenses = float(kwargs["monthly_expenses"])
        cash_on_hand = float(kwargs["cash_on_hand"])
        revenue_growth_rate = float(kwargs["revenue_growth_rate"])

        if monthly_expenses < 0 or cash_on_hand < 0:
            raise ValueError("expenses and cash must be non-negative")

        gross_burn = monthly_expenses
        net_burn = monthly_expenses - monthly_revenue
        runway_months = cash_on_hand / net_burn if net_burn > 0 else float("inf")

        # Growth-adjusted runway simulation
        cash = cash_on_hand
        months = 0
        revenue = monthly_revenue
        while cash > 0 and months < 120:
            net = monthly_expenses - revenue
            if net <= 0:
                runway_with_growth = float("inf")
                zero_date = None
                break
            cash -= net
            revenue *= (1 + revenue_growth_rate)
            months += 1
        else:
            runway_with_growth = months
            zero_date = _add_months(datetime.now(timezone.utc), months)

        if cash <= 0:
            zero_date = _add_months(datetime.now(timezone.utc), months)

        return {
            "status": "success",
            "data": {
                "gross_burn": gross_burn,
                "net_burn": net_burn,
                "runway_months": runway_months,
                "runway_with_growth": runway_with_growth,
                "zero_cash_date": zero_date.isoformat() if zero_date else "never",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"burn_rate_runway failed: {e}")
        _log_lesson(f"burn_rate_runway: {e}")
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
