"""Calculate the cash conversion cycle from its three components.

MCP Tool Name: cash_conversion_cycle_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "cash_conversion_cycle_calculator",
    "description": (
        "Calculates the cash conversion cycle (DIO + DSO - DPO), measuring the "
        "number of days it takes to convert inventory investments into cash."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "days_inventory": {
                "type": "number",
                "description": "Days inventory outstanding (DIO).",
            },
            "days_receivables": {
                "type": "number",
                "description": "Days sales outstanding (DSO).",
            },
            "days_payables": {
                "type": "number",
                "description": "Days payable outstanding (DPO).",
            },
        },
        "required": ["days_inventory", "days_receivables", "days_payables"],
    },
}


def cash_conversion_cycle_calculator(
    days_inventory: float, days_receivables: float, days_payables: float
) -> dict[str, Any]:
    """Calculate the cash conversion cycle."""
    try:
        days_inventory = float(days_inventory)
        days_receivables = float(days_receivables)
        days_payables = float(days_payables)

        ccc = days_inventory + days_receivables - days_payables

        return {
            "status": "ok",
            "data": {
                "cash_conversion_cycle_days": round(ccc, 2),
                "days_inventory": round(days_inventory, 2),
                "days_receivables": round(days_receivables, 2),
                "days_payables": round(days_payables, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
