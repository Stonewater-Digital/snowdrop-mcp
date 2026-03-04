"""Compute impermanent loss for LP positions."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "impermanent_loss_calculator",
    "description": "Evaluates current LP value vs hold value and required fees to break even.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "initial_price_ratio": {"type": "number"},
            "current_price_ratio": {"type": "number"},
            "initial_deposit_value": {"type": "number"},
        },
        "required": ["initial_price_ratio", "current_price_ratio", "initial_deposit_value"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def impermanent_loss_calculator(
    initial_price_ratio: float,
    current_price_ratio: float,
    initial_deposit_value: float,
    **_: Any,
) -> dict[str, Any]:
    """Return IL percentage, USD impact, and fee hurdle."""
    try:
        if initial_price_ratio <= 0 or current_price_ratio <= 0:
            raise ValueError("price ratios must be positive")
        hold_value = initial_deposit_value * (current_price_ratio / initial_price_ratio) ** 0.5
        price_ratio = current_price_ratio / initial_price_ratio
        il_pct = 2 * math.sqrt(price_ratio) / (1 + price_ratio) - 1
        lp_value = initial_deposit_value * (1 + il_pct)
        il_usd = hold_value - lp_value
        break_even_fee_apy = abs(il_pct) * 365
        data = {
            "il_pct": round(il_pct * 100, 4),
            "il_usd": round(il_usd, 2),
            "hold_value": round(hold_value, 2),
            "lp_value": round(lp_value, 2),
            "break_even_fee_apy": round(break_even_fee_apy * 100, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("impermanent_loss_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
