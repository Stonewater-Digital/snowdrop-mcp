"""Calculate trades needed to rebalance a portfolio to target weights.

MCP Tool Name: portfolio_rebalance_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "portfolio_rebalance_calculator",
    "description": (
        "Calculates the trades needed to rebalance a portfolio from current values "
        "to target weights, showing buy/sell amounts per asset."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_values": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of current dollar values per asset.",
            },
            "target_weights": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of target weights (should sum to 1).",
            },
        },
        "required": ["current_values", "target_weights"],
    },
}


def portfolio_rebalance_calculator(
    current_values: list[float], target_weights: list[float]
) -> dict[str, Any]:
    """Calculate rebalancing trades."""
    try:
        current_values = [float(v) for v in current_values]
        target_weights = [float(w) for w in target_weights]

        if len(current_values) != len(target_weights):
            raise ValueError("current_values and target_weights must have the same length.")
        if len(current_values) == 0:
            raise ValueError("Must have at least one asset.")

        total = sum(current_values)
        if total == 0:
            raise ValueError("Total portfolio value must not be zero.")

        trades = []
        for i in range(len(current_values)):
            target_value = total * target_weights[i]
            trade = target_value - current_values[i]
            current_weight = current_values[i] / total
            trades.append({
                "asset": i + 1,
                "current_value": round(current_values[i], 2),
                "current_weight": round(current_weight, 6),
                "target_weight": round(target_weights[i], 6),
                "target_value": round(target_value, 2),
                "trade_amount": round(trade, 2),
                "action": "buy" if trade > 0.005 else ("sell" if trade < -0.005 else "hold"),
            })

        return {
            "status": "ok",
            "data": {
                "total_portfolio_value": round(total, 2),
                "trades": trades,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
