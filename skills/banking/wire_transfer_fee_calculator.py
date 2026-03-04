"""Calculate wire transfer total cost and fee percentage.

MCP Tool Name: wire_transfer_fee_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "wire_transfer_fee_calculator",
    "description": "Calculate total cost of a wire transfer including fees, and express the fee as a percentage of the transfer amount.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "amount": {
                "type": "number",
                "description": "Transfer amount in dollars.",
            },
            "domestic": {
                "type": "boolean",
                "description": "True for domestic wire, False for international (default True).",
                "default": True,
            },
            "bank_fee": {
                "type": "number",
                "description": "Bank wire fee in dollars (default 25.0).",
                "default": 25.0,
            },
        },
        "required": ["amount"],
    },
}


def wire_transfer_fee_calculator(
    amount: float, domestic: bool = True, bank_fee: float = 25.0
) -> dict[str, Any]:
    """Calculate wire transfer total cost and fee percentage."""
    try:
        if amount <= 0:
            return {
                "status": "error",
                "data": {"error": "amount must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # International wires typically cost more
        effective_fee = bank_fee if domestic else bank_fee * 2
        total_cost = amount + effective_fee
        fee_pct = (effective_fee / amount) * 100

        return {
            "status": "ok",
            "data": {
                "amount": amount,
                "domestic": domestic,
                "bank_fee": round(effective_fee, 2),
                "total_cost": round(total_cost, 2),
                "fee_pct": round(fee_pct, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
