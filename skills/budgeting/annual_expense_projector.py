"""Project monthly expenses to annual totals.

MCP Tool Name: annual_expense_projector
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "annual_expense_projector",
    "description": "Projects monthly expenses to annual totals with category breakdown.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "monthly_expenses": {
                "type": "array",
                "description": "List of monthly expense categories with amounts.",
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
        "required": ["monthly_expenses"],
    },
}


def annual_expense_projector(monthly_expenses: list[dict[str, Any]]) -> dict[str, Any]:
    """Projects monthly expenses to annual totals."""
    try:
        if not monthly_expenses:
            return {
                "status": "error",
                "data": {"error": "At least one expense category is required."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        total_monthly = sum(e["amount"] for e in monthly_expenses)
        total_annual = round(total_monthly * 12, 2)

        projections = []
        for e in monthly_expenses:
            annual = round(e["amount"] * 12, 2)
            pct = round((annual / total_annual) * 100, 2) if total_annual > 0 else 0
            projections.append({
                "category": e["category"],
                "monthly": round(e["amount"], 2),
                "annual": annual,
                "percentage_of_total": pct,
            })

        projections.sort(key=lambda x: x["annual"], reverse=True)

        return {
            "status": "ok",
            "data": {
                "total_monthly": round(total_monthly, 2),
                "total_annual": total_annual,
                "daily_average": round(total_annual / 365, 2),
                "num_categories": len(projections),
                "projections": projections,
                "top_3_expenses": [p["category"] for p in projections[:3]],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
