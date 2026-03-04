"""
Executive Smary: Discounts future cash flows to present value for sums or annuities.
Inputs: future_value (float|None), payment (float|None), rate (float), periods (int), annuity_type (str)
Outputs: present_value (float), total_payments (float), total_interest (float), discount_factor (float)
MCP Tool Name: present_value_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "present_value_calculator",
    "description": (
        "Computes the present value of a lump sum or annuity, adjusting for payment timing "
        "and reporting aggregate payments and implied interest."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "future_value": {
                "type": "number",
                "description": "Future lump sum value in dollars (optional).",
            },
            "payment": {
                "type": "number",
                "description": "Recurring payment amount for annuities (optional).",
            },
            "rate": {
                "type": "number",
                "description": "Periodic discount rate as decimal.",
            },
            "periods": {
                "type": "number",
                "description": "Number of compounding or payment periods.",
            },
            "annuity_type": {
                "type": "string",
                "description": "Payment timing: ordinary (end) or due (beginning).",
            },
        },
        "required": ["rate", "periods", "annuity_type"],
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


def present_value_calculator(**kwargs: Any) -> dict:
    """Calculate present value and related metrics for a future amount or annuity."""
    try:
        future_value = kwargs.get("future_value")
        payment = kwargs.get("payment")
        rate = float(kwargs["rate"])
        periods = int(kwargs["periods"])
        annuity_type = str(kwargs["annuity_type"]).strip().lower()

        if periods <= 0:
            raise ValueError("periods must be positive")
        if annuity_type not in {"ordinary", "due"}:
            raise ValueError("annuity_type must be ordinary or due")
        if future_value is None and payment is None:
            raise ValueError("either future_value or payment is required")

        fv_value: Optional[float] = float(future_value) if future_value is not None else None
        payment_value: Optional[float] = float(payment) if payment is not None else None

        discount_factor = 1 / (1 + rate) ** periods if rate != 0 else 1.0
        pv = 0.0
        total_payments = 0.0

        if fv_value is not None:
            pv += fv_value * discount_factor
            total_payments += fv_value

        if payment_value is not None:
            if rate == 0:
                factor = periods
            else:
                factor = (1 - (1 + rate) ** (-periods)) / rate
            if annuity_type == "due":
                factor *= (1 + rate)
            pv += payment_value * factor
            total_payments += payment_value * periods

        total_interest = total_payments - pv if total_payments else 0.0

        return {
            "status": "success",
            "data": {
                "present_value": pv,
                "total_payments": total_payments,
                "total_interest": total_interest,
                "discount_factor": discount_factor,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"present_value_calculator failed: {e}")
        _log_lesson(f"present_value_calculator: {e}")
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
