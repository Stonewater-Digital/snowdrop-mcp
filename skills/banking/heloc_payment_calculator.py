"""Calculate HELOC payments during draw and repayment periods.

MCP Tool Name: heloc_payment_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "heloc_payment_calculator",
    "description": "Calculate HELOC payments: interest-only during draw period, principal + interest during repayment period.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "balance": {"type": "number", "description": "HELOC balance (amount drawn)."},
            "rate": {"type": "number", "description": "Annual interest rate as decimal."},
            "draw_period_months": {"type": "integer", "description": "Length of draw period in months."},
            "repay_period_months": {"type": "integer", "description": "Length of repayment period in months."},
        },
        "required": ["balance", "rate", "draw_period_months", "repay_period_months"],
    },
}


def heloc_payment_calculator(
    balance: float, rate: float, draw_period_months: int, repay_period_months: int
) -> dict[str, Any]:
    """Calculate HELOC payments for draw and repayment periods."""
    try:
        if balance <= 0:
            return {
                "status": "error",
                "data": {"error": "balance must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if draw_period_months < 0 or repay_period_months <= 0:
            return {
                "status": "error",
                "data": {"error": "Period lengths must be positive (draw may be 0)."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        monthly_rate = rate / 12

        # Draw period: interest-only
        io_payment = balance * monthly_rate
        draw_total_interest = io_payment * draw_period_months

        # Repayment period: P+I amortization
        if rate == 0:
            pi_payment = balance / repay_period_months
        else:
            pi_payment = balance * monthly_rate * (1 + monthly_rate) ** repay_period_months / (
                (1 + monthly_rate) ** repay_period_months - 1
            )
        repay_total = pi_payment * repay_period_months
        repay_interest = repay_total - balance

        return {
            "status": "ok",
            "data": {
                "balance": balance,
                "annual_rate_pct": round(rate * 100, 4),
                "draw_period_months": draw_period_months,
                "draw_monthly_payment_interest_only": round(io_payment, 2),
                "draw_total_interest": round(draw_total_interest, 2),
                "repay_period_months": repay_period_months,
                "repay_monthly_payment_pi": round(pi_payment, 2),
                "repay_total_paid": round(repay_total, 2),
                "repay_total_interest": round(repay_interest, 2),
                "total_interest_all_periods": round(draw_total_interest + repay_interest, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
