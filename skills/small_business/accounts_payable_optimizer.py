"""
Executive Smary: Prioritizes invoice payments to capture early-pay discounts within cash constraints.
Inputs: invoices (list), available_cash (float), cost_of_capital (float)
Outputs: optimal_payment_schedule (list), discount_savings (float), annualized_return_on_early_pay (list), cash_impact (float)
MCP Tool Name: accounts_payable_optimizer
"""
import logging
from datetime import datetime, timezone
from typing import Any, List, Dict

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "accounts_payable_optimizer",
    "description": (
        "Evaluates supplier invoices for early payment discounts versus company cost of "
        "capital to recommend an optimal payment schedule."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "invoices": {
                "type": "array",
                "description": "Invoices with id, amount, terms, early_pay_discount, early_pay_days.",
                "items": {"type": "object"},
            },
            "available_cash": {
                "type": "number",
                "description": "Cash available for accelerated payments.",
            },
            "cost_of_capital": {
                "type": "number",
                "description": "Annual cost of capital as decimal.",
            },
        },
        "required": ["invoices", "available_cash", "cost_of_capital"],
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


def accounts_payable_optimizer(**kwargs: Any) -> dict:
    """Select invoices for early payment based on effective annualized return."""
    try:
        invoices_input = kwargs["invoices"]
        available_cash = float(kwargs["available_cash"])
        cost_of_capital = float(kwargs["cost_of_capital"])

        if not isinstance(invoices_input, list):
            raise ValueError("invoices must be a list")

        opportunities: List[Dict[str, Any]] = []
        schedule: List[Dict[str, Any]] = []
        discount_savings = 0.0
        annualized_returns: List[Dict[str, Any]] = []

        for invoice in invoices_input:
            amount = float(invoice["amount"])
            discount = float(invoice.get("early_pay_discount", 0.0))
            terms = float(invoice.get("terms", 30))
            early_days = float(invoice.get("early_pay_days", terms - 10))
            if discount <= 0:
                continue
            saved = amount * discount
            period = terms - early_days
            annual_return = (saved / (amount - saved)) * (365 / period)
            opportunities.append(
                {
                    "id": invoice.get("id", invoice.get("vendor", "invoice")),
                    "amount": amount,
                    "savings": saved,
                    "annualized_return": annual_return,
                }
            )

        opportunities.sort(key=lambda x: x["annualized_return"], reverse=True)
        cash_used = 0.0
        for opp in opportunities:
            if opp["annualized_return"] < cost_of_capital:
                continue
            if cash_used + opp["amount"] > available_cash:
                continue
            cash_used += opp["amount"]
            discount_savings += opp["savings"]
            schedule.append({"invoice": opp["id"], "pay_now": True, "savings": opp["savings"]})
            annualized_returns.append(
                {"invoice": opp["id"], "annualized_return": opp["annualized_return"]}
            )

        cash_impact = cash_used

        return {
            "status": "success",
            "data": {
                "optimal_payment_schedule": schedule,
                "discount_savings": discount_savings,
                "annualized_return_on_early_pay": annualized_returns,
                "cash_impact": cash_impact,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error(f"accounts_payable_optimizer failed: {e}")
        _log_lesson(f"accounts_payable_optimizer: {e}")
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
