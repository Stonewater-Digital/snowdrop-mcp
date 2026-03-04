"""
Executive Smary: Estimates HELOC borrowing capacity and payment phases.
Inputs: home_value (float), mortgage_balance (float), ltv_limit (float), draw_amount (float), rate (float), draw_period_years (float), repayment_period_years (float)
Outputs: available_equity (float), max_credit_line (float), draw_period_payment (float), repayment_period_payment (float), total_interest (float)
MCP Tool Name: heloc_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "heloc_calculator",
    "description": (
        "Calculates HELOC borrowing power, interest-only draw payments, amortized "
        "repayment amounts, and total interest based on rate and term parameters."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "home_value": {
                "type": "number",
                "description": "Current market value of the property securing the HELOC.",
            },
            "mortgage_balance": {
                "type": "number",
                "description": "Outstanding first mortgage principal.",
            },
            "ltv_limit": {
                "type": "number",
                "description": "Maximum combined loan-to-value allowed (e.g., 0.85).",
            },
            "draw_amount": {
                "type": "number",
                "description": "Amount planned to draw from the HELOC immediately.",
            },
            "rate": {
                "type": "number",
                "description": "Annual interest rate as decimal, assume constant.",
            },
            "draw_period_years": {
                "type": "number",
                "description": "Years of interest-only payments during the draw.",
            },
            "repayment_period_years": {
                "type": "number",
                "description": "Years for amortized repayment after draw ends.",
            },
        },
        "required": [
            "home_value",
            "mortgage_balance",
            "ltv_limit",
            "draw_amount",
            "rate",
            "draw_period_years",
            "repayment_period_years",
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


def heloc_calculator(**kwargs: Any) -> dict:
    """Compute HELOC borrowing capacity, phase payments, and interest costs."""
    try:
        home_value = float(kwargs["home_value"])
        mortgage_balance = float(kwargs["mortgage_balance"])
        ltv_limit = float(kwargs["ltv_limit"])
        draw_amount = float(kwargs["draw_amount"])
        rate = float(kwargs["rate"])
        draw_period_years = float(kwargs["draw_period_years"])
        repayment_period_years = float(kwargs["repayment_period_years"])

        if home_value <= 0 or ltv_limit <= 0 or draw_amount < 0:
            raise ValueError("home_value, ltv_limit must be positive and draw_amount non-negative")

        available_equity = max(home_value * ltv_limit - mortgage_balance, 0.0)
        max_credit_line = available_equity
        if draw_amount > max_credit_line:
            raise ValueError("draw_amount exceeds maximum allowable credit line")

        monthly_rate = rate / 12
        draw_period_payment = draw_amount * monthly_rate
        draw_months = int(draw_period_years * 12)
        repayment_months = int(repayment_period_years * 12)
        if repayment_months <= 0:
            raise ValueError("repayment_period_years must be positive")
        if monthly_rate == 0:
            repayment_payment = draw_amount / repayment_months
            amort_interest = 0.0
        else:
            factor = (1 + monthly_rate) ** repayment_months
            repayment_payment = draw_amount * monthly_rate * factor / (factor - 1)
            amort_interest = repayment_payment * repayment_months - draw_amount

        total_interest = draw_period_payment * draw_months + amort_interest

        return {
            "status": "success",
            "data": {
                "available_equity": available_equity,
                "max_credit_line": max_credit_line,
                "draw_period_payment": draw_period_payment,
                "repayment_period_payment": repayment_payment,
                "total_interest": total_interest,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"heloc_calculator failed: {e}")
        _log_lesson(f"heloc_calculator: {e}")
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
