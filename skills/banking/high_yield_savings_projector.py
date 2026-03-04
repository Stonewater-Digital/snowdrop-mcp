"""Project high-yield savings account growth with monthly deposits.

MCP Tool Name: high_yield_savings_projector
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "high_yield_savings_projector",
    "description": "Project high-yield savings growth with an initial deposit and recurring monthly deposits, compounded monthly. Returns final balance and total interest earned.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "initial_deposit": {"type": "number", "description": "Initial deposit amount."},
            "monthly_deposit": {"type": "number", "description": "Recurring monthly deposit amount."},
            "apy": {"type": "number", "description": "Annual Percentage Yield as decimal."},
            "months": {"type": "integer", "description": "Number of months to project."},
        },
        "required": ["initial_deposit", "monthly_deposit", "apy", "months"],
    },
}


def high_yield_savings_projector(
    initial_deposit: float, monthly_deposit: float, apy: float, months: int
) -> dict[str, Any]:
    """Project savings growth with monthly compounding and deposits."""
    try:
        if months <= 0:
            return {
                "status": "error",
                "data": {"error": "months must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        monthly_rate = (1 + apy) ** (1 / 12) - 1
        balance = initial_deposit
        total_deposits = initial_deposit

        for _ in range(months):
            balance = balance * (1 + monthly_rate) + monthly_deposit
            total_deposits += monthly_deposit

        total_interest = balance - total_deposits

        return {
            "status": "ok",
            "data": {
                "initial_deposit": initial_deposit,
                "monthly_deposit": monthly_deposit,
                "apy_pct": round(apy * 100, 4),
                "months": months,
                "final_balance": round(balance, 2),
                "total_deposits": round(total_deposits, 2),
                "total_interest_earned": round(total_interest, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
