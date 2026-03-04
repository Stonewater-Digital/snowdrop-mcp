"""Calculate forex profit or loss for a closed trade.

MCP Tool Name: fx_profit_loss_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "fx_profit_loss_calculator",
    "description": "Calculate profit/loss for a forex trade given entry price, exit price, lot size, and direction (long/short). Computes P&L in pips and currency.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "entry_price": {
                "type": "number",
                "description": "Trade entry price.",
            },
            "exit_price": {
                "type": "number",
                "description": "Trade exit price.",
            },
            "lot_size": {
                "type": "number",
                "description": "Position size in units of base currency.",
                "default": 100000,
            },
            "direction": {
                "type": "string",
                "description": "Trade direction: 'long' or 'short'.",
                "enum": ["long", "short"],
                "default": "long",
            },
        },
        "required": ["entry_price", "exit_price"],
    },
}


def fx_profit_loss_calculator(
    entry_price: float,
    exit_price: float,
    lot_size: float = 100000,
    direction: str = "long",
) -> dict[str, Any]:
    """Calculate forex profit/loss."""
    try:
        direction = direction.lower().strip()
        if direction not in ("long", "short"):
            return {
                "status": "error",
                "data": {"error": "direction must be 'long' or 'short'."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if entry_price <= 0 or exit_price <= 0:
            return {
                "status": "error",
                "data": {"error": "Prices must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Determine pip size based on price magnitude
        is_jpy = entry_price > 10  # Heuristic for JPY pairs
        pip_size = 0.01 if is_jpy else 0.0001
        pip_multiplier = 100 if is_jpy else 10000

        raw_diff = exit_price - entry_price
        if direction == "short":
            raw_diff = -raw_diff

        pips = raw_diff * pip_multiplier
        pnl = raw_diff * lot_size * pip_size / pip_size  # simplified: raw_diff * lot_size for standard
        # Actually: P&L = (exit - entry) * lot_size for long; (entry - exit) * lot_size for short
        # But we need it in quote currency terms
        pnl = raw_diff * lot_size * pip_size  # in quote currency per pip movement
        # Correct formula: pnl = pips * pip_value_per_pip
        # pip_value = pip_size * lot_size
        pip_value = pip_size * lot_size
        pnl = pips * pip_value

        return {
            "status": "ok",
            "data": {
                "entry_price": entry_price,
                "exit_price": exit_price,
                "direction": direction,
                "lot_size": lot_size,
                "pip_size": pip_size,
                "pips": round(pips, 1),
                "pip_value": round(pip_value, 4),
                "profit_loss": round(pnl, 2),
                "result": "profit" if pnl > 0 else "loss" if pnl < 0 else "breakeven",
                "return_on_position_pct": round(pnl / (entry_price * lot_size) * 100, 4) if entry_price * lot_size > 0 else 0,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
