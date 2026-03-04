"""Track USDG staking yield using continuous compounding."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ton_usdg_yield_tracker",
    "description": "Calculates accrued USDG yield for TON staking ladders.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "principal": {"type": "number"},
            "apy_pct": {"type": "number"},
            "days_staked": {"type": "integer"},
        },
        "required": ["principal", "apy_pct", "days_staked"],
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


def ton_usdg_yield_tracker(principal: float, apy_pct: float, days_staked: int, **_: Any) -> dict[str, Any]:
    """Return the accrued yield and projected annualized return.

    Args:
        principal: USDG principal staked.
        apy_pct: Advertised annual percentage yield in percent.
        days_staked: Number of days that have elapsed.

    Returns:
        Envelope describing earned yield, projected annual yield, and effective rate.
    """

    try:
        if principal <= 0:
            raise ValueError("principal must be positive")
        if apy_pct < 0:
            raise ValueError("apy_pct cannot be negative")
        if days_staked < 0:
            raise ValueError("days_staked cannot be negative")

        r = apy_pct / 100
        t_years = days_staked / 365
        growth = math.exp(r * t_years)
        yield_earned = principal * (growth - 1)
        projected_annual = principal * (math.exp(r) - 1)
        effective_rate_pct = (yield_earned / principal * 100) if principal else 0

        data = {
            "principal": round(principal, 4),
            "apy_pct": apy_pct,
            "days_staked": days_staked,
            "yield_earned": round(yield_earned, 4),
            "projected_annual_yield": round(projected_annual, 4),
            "effective_rate_pct": round(effective_rate_pct, 4),
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("ton_usdg_yield_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
