"""Calculate all-in yields for unitranche facilities."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "unitranche_yield_calculator",
    "description": "Calculates unitranche cash yield plus amortized OID and fees.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "coupon_pct": {"type": "number"},
            "oid_pct": {"type": "number"},
            "origination_fee_pct": {"type": "number"},
            "tenor_years": {"type": "number"},
            "payment_frequency": {"type": "integer", "default": 4},
        },
        "required": ["coupon_pct", "oid_pct", "origination_fee_pct", "tenor_years"],
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


def unitranche_yield_calculator(
    coupon_pct: float,
    oid_pct: float,
    origination_fee_pct: float,
    tenor_years: float,
    payment_frequency: int = 4,
    **_: Any,
) -> dict[str, Any]:
    """Return all-in yield with amortized upfront charges."""
    try:
        coupon_rate = coupon_pct / 100
        amortized_oid = (oid_pct / 100) / tenor_years if tenor_years else 0.0
        amortized_fee = (origination_fee_pct / 100) / tenor_years if tenor_years else 0.0
        effective_yield = coupon_rate + amortized_oid + amortized_fee
        periodic_rate = coupon_rate / payment_frequency if payment_frequency else coupon_rate
        data = {
            "cash_coupon_pct": round(coupon_rate * 100, 2),
            "amortized_oid_pct": round(amortized_oid * 100, 2),
            "amortized_fee_pct": round(amortized_fee * 100, 2),
            "all_in_yield_pct": round(effective_yield * 100, 2),
            "periodic_coupon_rate_pct": round(periodic_rate * 100, 3),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("unitranche_yield_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
