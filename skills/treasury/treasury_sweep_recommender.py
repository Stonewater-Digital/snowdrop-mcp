"""Recommend treasury cash sweeps while deferring execution."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

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
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("treasury_sweep_recommender", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _destination_for_amount(amount: float) -> str:
    if amount <= 0:
        return "money_market"
    if amount < 250_000:
        return "money_market"
    if amount < 2_000_000:
        return "t_bills"
    return "staking"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
