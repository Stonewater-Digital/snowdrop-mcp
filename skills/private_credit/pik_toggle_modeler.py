"""Model PIK toggle interest accruals."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

COMPOUND_FREQ = {
    "quarterly": 4,
    "semi_annual": 2,
    "annual": 1,
}

TOOL_META: dict[str, Any] = {
    "name": "pik_toggle_modeler",
    "description": "Builds period schedules for cash and PIK interest accruals.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "principal": {"type": "number"},
            "cash_coupon_pct": {"type": "number"},
            "pik_coupon_pct": {"type": "number"},
            "toggle_type": {"type": "string", "enum": ["mandatory_pik", "optional_toggle", "partial_pik"]},
            "pik_periods": {"type": "integer"},
            "total_periods": {"type": "integer"},
            "compounding": {"type": "string", "enum": ["quarterly", "semi_annual", "annual"], "default": "quarterly"},
        },
        "required": ["principal", "cash_coupon_pct", "pik_coupon_pct", "toggle_type", "pik_periods", "total_periods"],
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


def pik_toggle_modeler(
    principal: float,
    cash_coupon_pct: float,
    pik_coupon_pct: float,
    toggle_type: str,
    pik_periods: int,
    total_periods: int,
    compounding: str = "quarterly",
    **_: Any,
) -> dict[str, Any]:
    """Return schedule with ending principal, cash interest, and PIK accruals."""
    try:
        freq = COMPOUND_FREQ.get(compounding, 4)
        principal_balance = principal
        schedule = []
        total_cash = 0.0
        total_pik = 0.0
        for period in range(1, total_periods + 1):
            is_pik = period <= pik_periods or toggle_type == "mandatory_pik"
            cash_rate = cash_coupon_pct / 100 / freq
            pik_rate = pik_coupon_pct / 100 / freq
            cash_interest = 0.0 if is_pik else principal_balance * cash_rate
            pik_interest = principal_balance * pik_rate if is_pik or toggle_type == "partial_pik" else 0.0
            principal_balance += pik_interest
            total_cash += cash_interest
            total_pik += pik_interest
            schedule.append(
                {
                    "period": period,
                    "cash_interest": round(cash_interest, 2),
                    "pik_interest": round(pik_interest, 2),
                    "ending_principal": round(principal_balance, 2),
                }
            )
        effective_yield = (total_cash + total_pik) / (principal * total_periods / freq) if total_periods else 0.0
        ltv_drift = principal_balance / principal - 1
        data = {
            "ending_principal": round(principal_balance, 2),
            "total_cash_interest": round(total_cash, 2),
            "total_pik_accrued": round(total_pik, 2),
            "effective_yield": round(effective_yield, 4),
            "principal_growth_pct": round(ltv_drift * 100, 2),
            "period_schedule": schedule,
            "ltv_drift_warning": ltv_drift > 0.25,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("pik_toggle_modeler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
