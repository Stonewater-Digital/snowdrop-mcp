"""Calculate profit and effective hourly rate from a side hustle.

MCP Tool Name: side_hustle_profit_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "side_hustle_profit_calculator",
    "description": "Calculate profit, effective hourly rate, and estimated tax liability from a side hustle or gig work.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "revenue": {
                "type": "number",
                "description": "Total revenue earned.",
            },
            "expenses": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "item": {"type": "string"},
                        "amount": {"type": "number"},
                    },
                    "required": ["item", "amount"],
                },
                "description": "List of expense items with name and amount.",
            },
            "hours_worked": {
                "type": "number",
                "description": "Total hours worked on the side hustle.",
            },
        },
        "required": ["revenue", "expenses", "hours_worked"],
    },
}


def side_hustle_profit_calculator(
    revenue: float,
    expenses: list[dict[str, Any]],
    hours_worked: float,
) -> dict[str, Any]:
    """Calculate side hustle profit and effective hourly rate."""
    try:
        if hours_worked <= 0:
            return {
                "status": "error",
                "data": {"error": "Hours worked must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        total_expenses = sum(e.get("amount", 0) for e in expenses)
        net_profit = revenue - total_expenses
        profit_margin = (net_profit / revenue * 100) if revenue > 0 else 0
        effective_hourly = net_profit / hours_worked

        # Estimate self-employment tax (15.3% on 92.35% of net earnings)
        se_taxable = net_profit * 0.9235
        se_tax = se_taxable * 0.153 if net_profit > 0 else 0

        # Estimate income tax (assume 22% marginal bracket for side income)
        income_tax_estimate = max(0, net_profit * 0.22)
        total_tax = se_tax + income_tax_estimate
        after_tax_profit = net_profit - total_tax
        after_tax_hourly = after_tax_profit / hours_worked

        expense_breakdown = sorted(
            [{"item": e.get("item", "Unknown"), "amount": e.get("amount", 0)} for e in expenses],
            key=lambda x: x["amount"],
            reverse=True,
        )

        return {
            "status": "ok",
            "data": {
                "revenue": round(revenue, 2),
                "total_expenses": round(total_expenses, 2),
                "net_profit": round(net_profit, 2),
                "profit_margin_pct": round(profit_margin, 1),
                "hours_worked": hours_worked,
                "effective_hourly_rate": round(effective_hourly, 2),
                "tax_estimates": {
                    "self_employment_tax": round(se_tax, 2),
                    "income_tax_estimate_22pct": round(income_tax_estimate, 2),
                    "total_estimated_tax": round(total_tax, 2),
                },
                "after_tax_profit": round(after_tax_profit, 2),
                "after_tax_hourly_rate": round(after_tax_hourly, 2),
                "expense_breakdown": expense_breakdown,
                "note": "Self-employment tax is 15.3% (12.4% SS + 2.9% Medicare) on 92.35% of net earnings. "
                "Income tax estimate uses 22% marginal rate — adjust for your actual bracket. "
                "If net earnings exceed $400, you must file Schedule SE. "
                "Consider quarterly estimated tax payments to avoid penalties.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
