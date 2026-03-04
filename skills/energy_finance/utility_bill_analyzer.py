"""Analyze utility bill data for patterns and trends.

MCP Tool Name: utility_bill_analyzer
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "utility_bill_analyzer",
    "description": "Analyze a series of monthly utility bills to find average cost per kWh, seasonal patterns, highest/lowest months, and overall trend.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "bills": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "month": {"type": "string", "description": "Month label (e.g. 'Jan 2024')."},
                        "amount": {"type": "number", "description": "Bill amount in USD."},
                        "kwh": {"type": "number", "description": "kWh consumed."},
                    },
                    "required": ["month", "amount", "kwh"],
                },
                "description": "List of monthly bill records.",
            },
        },
        "required": ["bills"],
    },
}


def utility_bill_analyzer(
    bills: list[dict[str, Any]],
) -> dict[str, Any]:
    """Analyze utility bill data."""
    try:
        if not bills:
            return {
                "status": "error",
                "data": {"error": "bills list must not be empty."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Validate and extract
        months = []
        amounts = []
        kwhs = []
        rates = []
        for b in bills:
            if b.get("kwh", 0) <= 0:
                return {
                    "status": "error",
                    "data": {"error": f"kwh must be positive for month '{b.get('month', '?')}'."},
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            months.append(b["month"])
            amounts.append(b["amount"])
            kwhs.append(b["kwh"])
            rates.append(b["amount"] / b["kwh"])

        total_amount = sum(amounts)
        total_kwh = sum(kwhs)
        avg_rate = total_amount / total_kwh if total_kwh > 0 else 0
        avg_monthly_bill = total_amount / len(amounts)
        avg_monthly_kwh = total_kwh / len(kwhs)

        # Highest and lowest
        max_idx = amounts.index(max(amounts))
        min_idx = amounts.index(min(amounts))

        # Trend: simple linear regression on amounts
        n = len(amounts)
        if n >= 2:
            x_mean = (n - 1) / 2
            y_mean = avg_monthly_bill
            numerator = sum((i - x_mean) * (amounts[i] - y_mean) for i in range(n))
            denominator = sum((i - x_mean) ** 2 for i in range(n))
            slope = numerator / denominator if denominator != 0 else 0
            if slope > 1:
                trend = "increasing"
            elif slope < -1:
                trend = "decreasing"
            else:
                trend = "stable"
            monthly_change = slope
        else:
            trend = "insufficient_data"
            monthly_change = 0

        # Per-month detail
        month_details = []
        for i in range(len(bills)):
            month_details.append({
                "month": months[i],
                "amount": round(amounts[i], 2),
                "kwh": round(kwhs[i], 2),
                "rate_per_kwh": round(rates[i], 4),
            })

        return {
            "status": "ok",
            "data": {
                "num_months_analyzed": n,
                "total_cost": round(total_amount, 2),
                "total_kwh": round(total_kwh, 2),
                "avg_cost_per_kwh": round(avg_rate, 4),
                "avg_monthly_bill": round(avg_monthly_bill, 2),
                "avg_monthly_kwh": round(avg_monthly_kwh, 2),
                "highest_month": {
                    "month": months[max_idx],
                    "amount": round(amounts[max_idx], 2),
                    "kwh": round(kwhs[max_idx], 2),
                },
                "lowest_month": {
                    "month": months[min_idx],
                    "amount": round(amounts[min_idx], 2),
                    "kwh": round(kwhs[min_idx], 2),
                },
                "trend": trend,
                "avg_monthly_change": round(monthly_change, 2),
                "month_details": month_details,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
