"""Recommend treasury cash sweeps while deferring execution."""
from __future__ import annotations

from typing import Any

from skills.utils import SkillTelemetryEmitter, get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "treasury_sweep_recommender",
    "description": "Identifies idle cash available for sweeps and proposes destinations (pending Thunder).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "account_balances": {"type": "object"},
            "operating_buffer_months": {"type": "integer", "default": 3},
            "monthly_burn": {"type": "number"},
        },
        "required": ["account_balances", "monthly_burn"],
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

_YIELD_TABLE = {
    "money_market": 0.037,
    "t_bills": 0.045,
    "staking": 0.12,
}


def treasury_sweep_recommender(
    account_balances: dict[str, float],
    monthly_burn: float,
    operating_buffer_months: int = 3,
    **_: Any,
) -> dict[str, Any]:
    """Return sweep recommendation flagged for Thunder approval."""
    emitter = SkillTelemetryEmitter(
        "treasury_sweep_recommender",
        {"account_count": len(account_balances or {}), "operating_buffer_months": operating_buffer_months},
    )
    try:
        if monthly_burn <= 0:
            raise ValueError("monthly_burn must be positive")
        if operating_buffer_months <= 0:
            raise ValueError("operating_buffer_months must be positive")
        if not account_balances:
            raise ValueError("account_balances cannot be empty")

        total_cash = sum(float(balance) for balance in account_balances.values())
        reserve_required = monthly_burn * operating_buffer_months
        sweepable = max(0.0, total_cash - reserve_required)
        destination = _destination_for_amount(sweepable)
        projected_yield = _YIELD_TABLE.get(destination, 0.0)

        data = {
            "total_cash": round(total_cash, 2),
            "reserve_required": round(reserve_required, 2),
            "sweep_amount": round(sweepable, 2),
            "recommended_destination": destination,
            "projected_annual_yield": projected_yield,
            "execution_status": "pending_thunder_approval",
        }
        emitter.record(
            "ok",
            {
                "sweep_amount": round(sweepable, 2),
                "destination": destination,
                "reserve_multiple": round(total_cash / reserve_required, 2) if reserve_required else None,
            },
        )
        return {
            "status": "success",
            "data": data,
            "timestamp": get_iso_timestamp(),
        }
    except Exception as exc:
        log_lesson(f"treasury_sweep_recommender: {exc}")
        emitter.record("error", {"error": str(exc)})
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
        }


def _destination_for_amount(amount: float) -> str:
    if amount <= 0:
        return "money_market"
    if amount < 250_000:
        return "money_market"
    if amount < 2_000_000:
        return "t_bills"
    return "staking"
