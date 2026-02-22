"""Estimate constant-product DEX swap outputs."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "token_swap_estimator",
    "description": "Estimates CFMM swap execution with slippage buffer for Thunder review.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "input_token": {"type": "string"},
            "output_token": {"type": "string"},
            "input_amount": {"type": "number"},
            "reserves": {"type": "object"},
            "fee_pct": {"type": "number", "default": 0.3},
        },
        "required": ["input_token", "output_token", "input_amount", "reserves"],
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


def token_swap_estimator(
    input_token: str,
    output_token: str,
    input_amount: float,
    reserves: dict[str, float],
    fee_pct: float = 0.3,
    **_: Any,
) -> dict[str, Any]:
    """Return swap estimates under constant-product assumptions."""

    try:
        if input_amount <= 0:
            raise ValueError("input_amount must be positive")
        reserve_in = float(reserves.get("reserve_in", 0))
        reserve_out = float(reserves.get("reserve_out", 0))
        if reserve_in <= 0 or reserve_out <= 0:
            raise ValueError("reserves must include positive reserve_in and reserve_out")

        fee_fraction = fee_pct / 100
        amount_in_after_fee = input_amount * (1 - fee_fraction)
        numerator = amount_in_after_fee * reserve_out
        denominator = reserve_in + amount_in_after_fee
        output_amount = numerator / denominator
        price_impact = (input_amount / (reserve_in + input_amount)) * 100
        effective_price = input_amount / max(output_amount, 1e-12)
        fee_paid = input_amount - amount_in_after_fee
        minimum_received = output_amount * 0.99
        data = {
            "input_token": input_token,
            "output_token": output_token,
            "output_amount": round(output_amount, 8),
            "price_impact_pct": round(price_impact, 4),
            "effective_price": round(effective_price, 8),
            "fee_paid": round(fee_paid, 8),
            "minimum_received": round(minimum_received, 8),
            "execution": "pending_thunder_approval",
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("token_swap_estimator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
