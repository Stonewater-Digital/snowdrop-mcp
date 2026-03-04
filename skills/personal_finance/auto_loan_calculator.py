"""
Executive Smary: Calculates auto loan payments and total cost of ownership including taxes.
Inputs: vehicle_price (float), down_payment (float), trade_in_value (float), loan_rate (float), loan_term_months (int), sales_tax_rate (float)
Outputs: monthly_payment (float), total_interest (float), total_cost (float), amount_financed (float), tax_amount (float)
MCP Tool Name: auto_loan_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "auto_loan_calculator",
    "description": (
        "Builds a car financing model covering tax, amount financed, monthly payment, "
        "and total interest across the loan term."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "vehicle_price": {
                "type": "number",
                "description": "Agreed purchase price of the vehicle before incentives.",
            },
            "down_payment": {
                "type": "number",
                "description": "Cash down payment applied at signing.",
            },
            "trade_in_value": {
                "type": "number",
                "description": "Value of vehicle traded in, reduces taxable base.",
            },
            "loan_rate": {
                "type": "number",
                "description": "APR for financing as decimal.",
            },
            "loan_term_months": {
                "type": "number",
                "description": "Loan duration in months.",
            },
            "sales_tax_rate": {
                "type": "number",
                "description": "Sales tax applied to purchase price net of trade-in.",
            },
        },
        "required": [
            "vehicle_price",
            "down_payment",
            "trade_in_value",
            "loan_rate",
            "loan_term_months",
            "sales_tax_rate",
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


def auto_loan_calculator(**kwargs: Any) -> dict:
    """Estimate auto loan payment, total interest, and ownership cost."""
    try:
        price = float(kwargs["vehicle_price"])
        down = float(kwargs["down_payment"])
        trade_in = float(kwargs["trade_in_value"])
        rate = float(kwargs["loan_rate"])
        term = int(kwargs["loan_term_months"])
        tax_rate = float(kwargs["sales_tax_rate"])

        if price <= 0 or term <= 0:
            raise ValueError("vehicle_price and loan_term_months must be positive")

        taxable_base = max(price - trade_in, 0.0)
        tax_amount = taxable_base * tax_rate
        amount_financed = max(price - down - trade_in + tax_amount, 0.0)
        monthly_rate = rate / 12
        if amount_financed == 0:
            monthly_payment = 0.0
            total_interest = 0.0
        elif monthly_rate == 0:
            monthly_payment = amount_financed / term
            total_interest = 0.0
        else:
            factor = (1 + monthly_rate) ** term
            monthly_payment = amount_financed * monthly_rate * factor / (factor - 1)
            total_interest = monthly_payment * term - amount_financed

        total_cost = monthly_payment * term + down + trade_in

        return {
            "status": "success",
            "data": {
                "monthly_payment": monthly_payment,
                "total_interest": total_interest,
                "total_cost": total_cost,
                "amount_financed": amount_financed,
                "tax_amount": tax_amount,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"auto_loan_calculator failed: {e}")
        _log_lesson(f"auto_loan_calculator: {e}")
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
