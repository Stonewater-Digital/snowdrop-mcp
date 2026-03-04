"""Calculate optimal forex position size based on risk parameters.

MCP Tool Name: position_size_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "position_size_calculator",
    "description": "Calculate optimal position size given account balance, risk percentage, stop-loss distance in pips, and pip value.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "account_balance": {
                "type": "number",
                "description": "Account balance in account currency.",
            },
            "risk_pct": {
                "type": "number",
                "description": "Risk per trade as a decimal (e.g. 0.02 for 2%).",
                "default": 0.02,
            },
            "stop_loss_pips": {
                "type": "integer",
                "description": "Stop-loss distance in pips.",
                "default": 50,
            },
            "pip_value": {
                "type": "number",
                "description": "Value of one pip per standard lot in account currency.",
                "default": 10.0,
            },
        },
        "required": ["account_balance"],
    },
}


def position_size_calculator(
    account_balance: float,
    risk_pct: float = 0.02,
    stop_loss_pips: int = 50,
    pip_value: float = 10.0,
) -> dict[str, Any]:
    """Calculate optimal position size."""
    try:
        if account_balance <= 0:
            return {
                "status": "error",
                "data": {"error": "account_balance must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if stop_loss_pips <= 0:
            return {
                "status": "error",
                "data": {"error": "stop_loss_pips must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if pip_value <= 0:
            return {
                "status": "error",
                "data": {"error": "pip_value must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        risk_amount = account_balance * risk_pct
        # lots = risk_amount / (stop_loss_pips * pip_value_per_lot)
        lots = risk_amount / (stop_loss_pips * pip_value)
        units = lots * 100000
        mini_lots = lots * 10
        micro_lots = lots * 100

        return {
            "status": "ok",
            "data": {
                "account_balance": round(account_balance, 2),
                "risk_pct": round(risk_pct * 100, 2),
                "risk_amount": round(risk_amount, 2),
                "stop_loss_pips": stop_loss_pips,
                "pip_value_per_lot": pip_value,
                "standard_lots": round(lots, 4),
                "mini_lots": round(mini_lots, 4),
                "micro_lots": round(micro_lots, 4),
                "units": round(units, 0),
                "max_loss_if_stopped": round(risk_amount, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
