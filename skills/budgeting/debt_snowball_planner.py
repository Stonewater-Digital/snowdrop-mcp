"""Plan debt payoff using the snowball method (smallest balance first).

MCP Tool Name: debt_snowball_planner
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "debt_snowball_planner",
    "description": "Plans debt payoff using the snowball method: pay minimums on all debts, apply extra payment to the smallest balance first.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "debts": {
                "type": "array",
                "description": "List of debts with name, balance, minimum payment, and interest rate.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "balance": {"type": "number"},
                        "min_payment": {"type": "number"},
                        "rate": {"type": "number", "description": "Annual interest rate as a percentage (e.g., 18.5)."},
                    },
                    "required": ["name", "balance", "min_payment", "rate"],
                },
            },
            "extra_payment": {
                "type": "number",
                "description": "Additional monthly amount to apply toward debt payoff.",
            },
        },
        "required": ["debts", "extra_payment"],
    },
}


def debt_snowball_planner(
    debts: list[dict[str, Any]], extra_payment: float
) -> dict[str, Any]:
    """Plans debt payoff using the snowball method."""
    try:
        if not debts:
            return {
                "status": "error",
                "data": {"error": "At least one debt is required."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if extra_payment < 0:
            return {
                "status": "error",
                "data": {"error": "Extra payment must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Sort by balance ascending (snowball)
        working = sorted(
            [
                {
                    "name": d["name"],
                    "balance": float(d["balance"]),
                    "min_payment": float(d["min_payment"]),
                    "rate": float(d["rate"]),
                }
                for d in debts
            ],
            key=lambda x: x["balance"],
        )

        total_balance = sum(d["balance"] for d in working)
        total_min_payments = sum(d["min_payment"] for d in working)
        total_interest_paid = 0.0
        month = 0
        max_months = 600  # 50-year cap
        payoff_order = []

        while any(d["balance"] > 0 for d in working) and month < max_months:
            month += 1
            available_extra = extra_payment

            # Apply interest
            for d in working:
                if d["balance"] > 0:
                    monthly_interest = d["balance"] * (d["rate"] / 100 / 12)
                    d["balance"] += monthly_interest
                    total_interest_paid += monthly_interest

            # Pay minimums
            for d in working:
                if d["balance"] > 0:
                    payment = min(d["min_payment"], d["balance"])
                    d["balance"] -= payment
                    d["balance"] = round(d["balance"], 2)

            # Apply extra to smallest balance
            for d in working:
                if d["balance"] > 0 and available_extra > 0:
                    payment = min(available_extra, d["balance"])
                    d["balance"] -= payment
                    d["balance"] = round(d["balance"], 2)
                    available_extra -= payment
                    if d["balance"] <= 0:
                        d["balance"] = 0
                        payoff_order.append({"name": d["name"], "paid_off_month": month})
                        # Freed minimum payment becomes extra for next debt
                        available_extra += d["min_payment"]
                    break  # Only apply extra to the first (smallest) remaining debt

            # Check for newly paid-off debts from minimum payments
            for d in working:
                if d["balance"] <= 0 and d["name"] not in [p["name"] for p in payoff_order]:
                    d["balance"] = 0
                    payoff_order.append({"name": d["name"], "paid_off_month": month})

        return {
            "status": "ok",
            "data": {
                "method": "Debt Snowball (smallest balance first)",
                "total_starting_balance": round(total_balance, 2),
                "total_monthly_payment": round(total_min_payments + extra_payment, 2),
                "extra_monthly_payment": extra_payment,
                "total_months_to_payoff": month,
                "total_years_to_payoff": round(month / 12, 1),
                "total_interest_paid": round(total_interest_paid, 2),
                "total_cost": round(total_balance + total_interest_paid, 2),
                "payoff_order": payoff_order,
                "note": "The snowball method prioritizes psychological wins by paying off smallest balances first. The avalanche method (highest rate first) saves more on interest.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
