"""Build a zero-based budget from income and categorized expenses.

MCP Tool Name: zero_based_budget_builder
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "zero_based_budget_builder",
    "description": "Builds a zero-based budget: every dollar of income is assigned to a category. Shows remaining unallocated funds.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "monthly_income": {
                "type": "number",
                "description": "Total monthly income in dollars.",
            },
            "expenses": {
                "type": "array",
                "description": "List of expense categories with amounts.",
                "items": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string"},
                        "amount": {"type": "number"},
                    },
                    "required": ["category", "amount"],
                },
            },
        },
        "required": ["monthly_income", "expenses"],
    },
}


def zero_based_budget_builder(
    monthly_income: float, expenses: list[dict[str, Any]]
) -> dict[str, Any]:
    """Builds a zero-based budget from income and categorized expenses."""
    try:
        if monthly_income <= 0:
            return {
                "status": "error",
                "data": {"error": "Monthly income must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        total_expenses = sum(e["amount"] for e in expenses)
        remaining = round(monthly_income - total_expenses, 2)

        breakdown = []
        for e in expenses:
            pct = round((e["amount"] / monthly_income) * 100, 2) if monthly_income else 0
            breakdown.append({
                "category": e["category"],
                "amount": round(e["amount"], 2),
                "percentage_of_income": pct,
            })

        breakdown.sort(key=lambda x: x["amount"], reverse=True)

        status_msg = "balanced"
        if remaining > 0:
            status_msg = "under-allocated"
        elif remaining < 0:
            status_msg = "over-allocated"

        return {
            "status": "ok",
            "data": {
                "monthly_income": monthly_income,
                "total_expenses": round(total_expenses, 2),
                "remaining_unallocated": remaining,
                "budget_status": status_msg,
                "expense_breakdown": breakdown,
                "num_categories": len(expenses),
                "note": "In a zero-based budget, remaining should be $0. Every dollar has a job."
                if remaining != 0
                else "Perfect zero-based budget. Every dollar is allocated.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
