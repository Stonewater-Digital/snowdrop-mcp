"""Estimate returns for mezzanine tranches."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "mezzanine_return_calculator",
    "description": "Calculates blended cash, PIK, and equity kicker returns for mezzanine debt.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "principal": {"type": "number"},
            "cash_coupon_pct": {"type": "number"},
            "pik_coupon_pct": {"type": "number"},
            "term_years": {"type": "number"},
            "equity_kicker_pct": {"type": "number"},
            "equity_value_at_exit": {"type": "number"},
        },
        "required": [
            "principal",
            "cash_coupon_pct",
            "pik_coupon_pct",
            "term_years",
            "equity_kicker_pct",
            "equity_value_at_exit",
        ],
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


def mezzanine_return_calculator(
    principal: float,
    cash_coupon_pct: float,
    pik_coupon_pct: float,
    term_years: float,
    equity_kicker_pct: float,
    equity_value_at_exit: float,
    **_: Any,
) -> dict[str, Any]:
    """Return simple IRR style estimate for mezzanine capital."""
    try:
        cash_interest = principal * (cash_coupon_pct / 100) * term_years
        pik_accrual = principal * (pik_coupon_pct / 100) * term_years
        equity_uplift = equity_value_at_exit * (equity_kicker_pct / 100)
        total_value = principal + cash_interest + pik_accrual + equity_uplift
        irr_estimate = (total_value / principal) ** (1 / term_years) - 1 if term_years else 0.0
        data = {
            "cash_interest": round(cash_interest, 2),
            "pik_accrual": round(pik_accrual, 2),
            "equity_kicker_value": round(equity_uplift, 2),
            "total_value": round(total_value, 2),
            "irr_estimate_pct": round(irr_estimate * 100, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("mezzanine_return_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
