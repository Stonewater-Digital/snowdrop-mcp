"""Calculate accounts receivable turnover ratio and days sales outstanding.

MCP Tool Name: accounts_receivable_turnover_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "accounts_receivable_turnover_calculator",
    "description": (
        "Calculates the accounts receivable turnover ratio and average collection "
        "period (days sales outstanding)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_credit_sales": {
                "type": "number",
                "description": "Total net credit sales for the period.",
            },
            "avg_accounts_receivable": {
                "type": "number",
                "description": "Average accounts receivable balance for the period.",
            },
        },
        "required": ["net_credit_sales", "avg_accounts_receivable"],
    },
}


def accounts_receivable_turnover_calculator(
    net_credit_sales: float, avg_accounts_receivable: float
) -> dict[str, Any]:
    """Calculate AR turnover and days sales outstanding."""
    try:
        net_credit_sales = float(net_credit_sales)
        avg_accounts_receivable = float(avg_accounts_receivable)

        if avg_accounts_receivable == 0:
            raise ValueError("avg_accounts_receivable must not be zero.")

        turnover = net_credit_sales / avg_accounts_receivable
        days_sales_outstanding = 365.0 / turnover if turnover != 0 else float("inf")

        return {
            "status": "ok",
            "data": {
                "turnover_ratio": round(turnover, 4),
                "days_sales_outstanding": round(days_sales_outstanding, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
