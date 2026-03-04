"""Calculate risk-reward ratio for a trade.

MCP Tool Name: risk_reward_ratio_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "risk_reward_ratio_calculator",
    "description": "Calculate risk-reward ratio from entry price, stop-loss, and take-profit levels. Also computes breakeven win rate.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "entry_price": {
                "type": "number",
                "description": "Trade entry price.",
            },
            "stop_loss": {
                "type": "number",
                "description": "Stop-loss price level.",
            },
            "take_profit": {
                "type": "number",
                "description": "Take-profit price level.",
            },
        },
        "required": ["entry_price", "stop_loss", "take_profit"],
    },
}


def risk_reward_ratio_calculator(
    entry_price: float,
    stop_loss: float,
    take_profit: float,
) -> dict[str, Any]:
    """Calculate risk-reward ratio."""
    try:
        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit - entry_price)

        if risk == 0:
            return {
                "status": "error",
                "data": {"error": "Risk is zero (entry_price equals stop_loss)."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        rr_ratio = reward / risk
        # Breakeven win rate: win_rate = 1 / (1 + R:R)
        breakeven_win_rate = 1 / (1 + rr_ratio) * 100 if rr_ratio > 0 else 100.0

        # Determine direction
        if take_profit > entry_price and stop_loss < entry_price:
            direction = "long"
        elif take_profit < entry_price and stop_loss > entry_price:
            direction = "short"
        else:
            direction = "invalid_setup"

        if rr_ratio >= 3:
            assessment = "Excellent risk-reward ratio."
        elif rr_ratio >= 2:
            assessment = "Good risk-reward ratio."
        elif rr_ratio >= 1:
            assessment = "Acceptable — reward matches or exceeds risk."
        else:
            assessment = "Poor — risk exceeds reward. Consider adjusting levels."

        return {
            "status": "ok",
            "data": {
                "entry_price": entry_price,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "direction": direction,
                "risk": round(risk, 6),
                "reward": round(reward, 6),
                "risk_reward_ratio": round(rr_ratio, 3),
                "breakeven_win_rate_pct": round(breakeven_win_rate, 2),
                "assessment": assessment,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
