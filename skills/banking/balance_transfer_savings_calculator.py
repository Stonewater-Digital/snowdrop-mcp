"""Calculate savings from a credit card balance transfer.

MCP Tool Name: balance_transfer_savings_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "balance_transfer_savings_calculator",
    "description": "Calculate savings from transferring a credit card balance to a promotional APR. Accounts for transfer fee and compares interest saved.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "balance": {"type": "number", "description": "Current balance to transfer."},
            "current_apr": {"type": "number", "description": "Current card APR as decimal."},
            "transfer_apr": {"type": "number", "description": "Promotional APR as decimal (often 0)."},
            "transfer_fee_pct": {"type": "number", "description": "Balance transfer fee as decimal (e.g., 0.03 for 3%)."},
            "promo_months": {"type": "integer", "description": "Number of months at promotional rate."},
        },
        "required": ["balance", "current_apr", "transfer_apr", "transfer_fee_pct", "promo_months"],
    },
}


def balance_transfer_savings_calculator(
    balance: float,
    current_apr: float,
    transfer_apr: float,
    transfer_fee_pct: float,
    promo_months: int,
) -> dict[str, Any]:
    """Calculate balance transfer savings."""
    try:
        if balance <= 0:
            return {
                "status": "error",
                "data": {"error": "balance must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if promo_months <= 0:
            return {
                "status": "error",
                "data": {"error": "promo_months must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        transfer_fee = balance * transfer_fee_pct

        # Simple interest comparison over promo period
        current_interest = balance * (current_apr / 12) * promo_months
        transfer_interest = balance * (transfer_apr / 12) * promo_months

        interest_saved = current_interest - transfer_interest
        net_savings = interest_saved - transfer_fee

        return {
            "status": "ok",
            "data": {
                "balance": balance,
                "current_apr_pct": round(current_apr * 100, 4),
                "transfer_apr_pct": round(transfer_apr * 100, 4),
                "transfer_fee": round(transfer_fee, 2),
                "promo_months": promo_months,
                "current_interest_cost": round(current_interest, 2),
                "transfer_interest_cost": round(transfer_interest, 2),
                "interest_saved": round(interest_saved, 2),
                "net_savings": round(net_savings, 2),
                "recommendation": "Transfer" if net_savings > 0 else "Stay",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
