"""Compare total cost of leasing vs buying a vehicle.

MCP Tool Name: auto_lease_vs_buy_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "auto_lease_vs_buy_calculator",
    "description": "Compare total cost of leasing versus buying a vehicle. Accounts for loan payments, down payment, lease payments, and residual value.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "purchase_price": {"type": "number", "description": "Vehicle purchase price."},
            "down_payment": {"type": "number", "description": "Down payment for purchase."},
            "loan_rate": {"type": "number", "description": "Annual loan rate as decimal."},
            "loan_months": {"type": "integer", "description": "Loan term in months."},
            "lease_monthly": {"type": "number", "description": "Monthly lease payment."},
            "lease_months": {"type": "integer", "description": "Lease term in months."},
            "residual_value": {"type": "number", "description": "Estimated vehicle value at end of lease/loan term."},
        },
        "required": [
            "purchase_price", "down_payment", "loan_rate", "loan_months",
            "lease_monthly", "lease_months", "residual_value",
        ],
    },
}


def auto_lease_vs_buy_calculator(
    purchase_price: float,
    down_payment: float,
    loan_rate: float,
    loan_months: int,
    lease_monthly: float,
    lease_months: int,
    residual_value: float,
) -> dict[str, Any]:
    """Compare lease vs buy total cost for a vehicle."""
    try:
        # Buy: loan payment calculation
        loan_amount = purchase_price - down_payment
        if loan_rate == 0:
            monthly_loan = loan_amount / loan_months if loan_months > 0 else 0
        else:
            r = loan_rate / 12
            monthly_loan = loan_amount * r * (1 + r) ** loan_months / ((1 + r) ** loan_months - 1)

        buy_total_payments = down_payment + monthly_loan * loan_months
        # Net cost of buying = total payments - residual value (you own the car)
        buy_net_cost = buy_total_payments - residual_value

        # Lease: total payments
        lease_total = lease_monthly * lease_months

        cheaper = "buy" if buy_net_cost < lease_total else "lease"
        savings = abs(buy_net_cost - lease_total)

        return {
            "status": "ok",
            "data": {
                "buy": {
                    "purchase_price": purchase_price,
                    "down_payment": down_payment,
                    "loan_amount": round(loan_amount, 2),
                    "monthly_payment": round(monthly_loan, 2),
                    "total_payments": round(buy_total_payments, 2),
                    "residual_value": residual_value,
                    "net_cost": round(buy_net_cost, 2),
                },
                "lease": {
                    "monthly_payment": lease_monthly,
                    "lease_months": lease_months,
                    "total_cost": round(lease_total, 2),
                },
                "cheaper_option": cheaper,
                "savings": round(savings, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
