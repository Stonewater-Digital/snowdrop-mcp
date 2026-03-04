"""Analyze monthly cash flow from income and expense items.

MCP Tool Name: monthly_cash_flow_analyzer
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "monthly_cash_flow_analyzer",
    "description": "Analyzes monthly cash flow by comparing total income to total expenses and calculating net cash flow.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "income_items": {
                "type": "array",
                "description": "List of income sources with name and amount.",
                "items": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string"},
                        "amount": {"type": "number"},
                    },
                    "required": ["source", "amount"],
                },
            },
            "expense_items": {
                "type": "array",
                "description": "List of expense categories with name and amount.",
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
        "required": ["income_items", "expense_items"],
    },
}


def monthly_cash_flow_analyzer(
    income_items: list[dict[str, Any]], expense_items: list[dict[str, Any]]
) -> dict[str, Any]:
    """Analyzes monthly cash flow from income and expense items."""
    try:
        total_income = sum(i["amount"] for i in income_items)
        total_expenses = sum(e["amount"] for e in expense_items)
        net_cash_flow = round(total_income - total_expenses, 2)

        income_breakdown = sorted(
            [{"source": i["source"], "amount": round(i["amount"], 2)} for i in income_items],
            key=lambda x: x["amount"],
            reverse=True,
        )

        expense_breakdown = []
        for e in expense_items:
            pct = round((e["amount"] / total_income) * 100, 2) if total_income > 0 else 0
            expense_breakdown.append({
                "category": e["category"],
                "amount": round(e["amount"], 2),
                "percentage_of_income": pct,
            })
        expense_breakdown.sort(key=lambda x: x["amount"], reverse=True)

        if net_cash_flow > 0:
            status_msg = "positive"
            advice = f"You have ${net_cash_flow:.2f}/month surplus. Direct this toward savings, investments, or debt repayment."
        elif net_cash_flow < 0:
            status_msg = "negative"
            advice = f"You are spending ${abs(net_cash_flow):.2f}/month more than you earn. Review expenses for reductions or find additional income."
        else:
            status_msg = "break-even"
            advice = "Income exactly matches expenses. No room for savings. Look for ways to increase income or reduce spending."

        return {
            "status": "ok",
            "data": {
                "total_income": round(total_income, 2),
                "total_expenses": round(total_expenses, 2),
                "net_cash_flow": net_cash_flow,
                "cash_flow_status": status_msg,
                "expense_to_income_ratio": round((total_expenses / total_income) * 100, 2) if total_income > 0 else None,
                "income_breakdown": income_breakdown,
                "expense_breakdown": expense_breakdown,
                "advice": advice,
                "annual_projection": {
                    "annual_income": round(total_income * 12, 2),
                    "annual_expenses": round(total_expenses * 12, 2),
                    "annual_net": round(net_cash_flow * 12, 2),
                },
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
