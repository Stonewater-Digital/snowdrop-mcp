"""Analyze debt consolidation: compare current debts vs a single consolidated loan.

MCP Tool Name: debt_consolidation_analyzer
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "debt_consolidation_analyzer",
    "description": "Compare current multiple debts against a single consolidated loan. Calculates monthly savings and total interest savings.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "debts": {
                "type": "array",
                "description": "List of current debts.",
                "items": {
                    "type": "object",
                    "properties": {
                        "balance": {"type": "number", "description": "Outstanding balance."},
                        "rate": {"type": "number", "description": "Annual rate as decimal."},
                        "payment": {"type": "number", "description": "Current monthly payment."},
                    },
                    "required": ["balance", "rate", "payment"],
                },
            },
            "new_rate": {"type": "number", "description": "Consolidated loan annual rate as decimal."},
            "new_term_months": {"type": "integer", "description": "Consolidated loan term in months."},
        },
        "required": ["debts", "new_rate", "new_term_months"],
    },
}


def debt_consolidation_analyzer(
    debts: list[dict[str, Any]], new_rate: float, new_term_months: int
) -> dict[str, Any]:
    """Analyze debt consolidation opportunity."""
    try:
        if not debts:
            return {
                "status": "error",
                "data": {"error": "debts list must not be empty."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if new_term_months <= 0:
            return {
                "status": "error",
                "data": {"error": "new_term_months must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        total_balance = sum(d["balance"] for d in debts)
        current_monthly = sum(d["payment"] for d in debts)

        # Estimate current total interest by simulating payoff
        current_total_interest = 0.0
        for d in debts:
            bal = d["balance"]
            r = d["rate"] / 12
            pmt = d["payment"]
            interest_sum = 0.0
            months = 0
            while bal > 0.01 and months < 600:
                intr = bal * r
                interest_sum += intr
                bal = bal + intr - pmt
                months += 1
            current_total_interest += interest_sum

        # Consolidated loan
        r_new = new_rate / 12
        if new_rate == 0:
            new_pmt = total_balance / new_term_months
        else:
            new_pmt = total_balance * r_new * (1 + r_new) ** new_term_months / (
                (1 + r_new) ** new_term_months - 1
            )
        new_total_paid = new_pmt * new_term_months
        new_total_interest = new_total_paid - total_balance

        monthly_savings = current_monthly - new_pmt
        interest_savings = current_total_interest - new_total_interest

        return {
            "status": "ok",
            "data": {
                "total_balance": round(total_balance, 2),
                "current_monthly_total": round(current_monthly, 2),
                "current_total_interest": round(current_total_interest, 2),
                "consolidated_monthly_payment": round(new_pmt, 2),
                "consolidated_total_interest": round(new_total_interest, 2),
                "monthly_savings": round(monthly_savings, 2),
                "total_interest_savings": round(interest_savings, 2),
                "recommendation": "Consolidate" if interest_savings > 0 else "Keep separate",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
