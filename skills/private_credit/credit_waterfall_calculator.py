"""Distribute cash through a credit waterfall."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "credit_waterfall_calculator",
    "description": "Allocates cash to fees, senior, mezzanine, and equity tranches.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cash_available": {"type": "number"},
            "fee_amount": {"type": "number"},
            "senior_outstanding": {"type": "number"},
            "mezz_outstanding": {"type": "number"},
            "equity_share_pct": {"type": "number", "default": 100.0},
        },
        "required": ["cash_available", "fee_amount", "senior_outstanding", "mezz_outstanding"],
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


def credit_waterfall_calculator(
    cash_available: float,
    fee_amount: float,
    senior_outstanding: float,
    mezz_outstanding: float,
    equity_share_pct: float = 100.0,
    **_: Any,
) -> dict[str, Any]:
    """Return waterfall allocation amounts."""
    try:
        remaining = cash_available
        fees_paid = min(fee_amount, remaining)
        remaining -= fees_paid
        senior_paid = min(senior_outstanding, remaining)
        remaining -= senior_paid
        mezz_paid = min(mezz_outstanding, remaining)
        remaining -= mezz_paid
        equity_paid = remaining * (equity_share_pct / 100)
        reserve = remaining - equity_paid
        data = {
            "fees_paid": round(fees_paid, 2),
            "senior_paid": round(senior_paid, 2),
            "mezz_paid": round(mezz_paid, 2),
            "equity_paid": round(equity_paid, 2),
            "cash_reserve": round(reserve, 2),
            "senior_recovery_pct": round(senior_paid / senior_outstanding * 100, 2) if senior_outstanding else 0.0,
            "mezz_recovery_pct": round(mezz_paid / mezz_outstanding * 100, 2) if mezz_outstanding else 0.0,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("credit_waterfall_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
