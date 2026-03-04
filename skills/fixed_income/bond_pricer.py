"""Price a plain-vanilla coupon bond."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "bond_pricer",
    "description": "Computes clean/dirty price, duration, convexity, and current yield.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "face_value": {"type": "number"},
            "coupon_rate": {"type": "number"},
            "yield_to_maturity": {"type": "number"},
            "years_to_maturity": {"type": "integer"},
            "payments_per_year": {"type": "integer", "default": 2},
        },
        "required": [
            "face_value",
            "coupon_rate",
            "yield_to_maturity",
            "years_to_maturity",
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


def bond_pricer(
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years_to_maturity: int,
    payments_per_year: int = 2,
    **_: Any,
) -> dict[str, Any]:
    """Discount coupon cash flows to determine bond analytics."""
    try:
        if face_value <= 0 or coupon_rate < 0 or yield_to_maturity < 0:
            raise ValueError("Inputs must be non-negative and face_value positive")
        if years_to_maturity <= 0 or payments_per_year <= 0:
            raise ValueError("years_to_maturity and payments_per_year must be positive")

        periods = years_to_maturity * payments_per_year
        coupon = face_value * coupon_rate / payments_per_year
        period_rate = yield_to_maturity / payments_per_year
        price = 0.0
        duration_numer = 0.0
        convexity_numer = 0.0
        for period in range(1, periods + 1):
            cash_flow = coupon if period < periods else coupon + face_value
            discount_factor = (1 + period_rate) ** period
            pv = cash_flow / discount_factor
            price += pv
            duration_numer += period * pv
            convexity_numer += period * (period + 1) * pv
        macaulay_duration = duration_numer / (price * payments_per_year)
        convexity = convexity_numer / (price * (payments_per_year ** 2))
        accrued_interest = coupon / 2  # assumes pricing halfway through coupon period
        dirty_price = price + accrued_interest
        current_yield = (coupon * payments_per_year) / price if price else 0
        data = {
            "clean_price": round(price, 4),
            "accrued_interest": round(accrued_interest, 4),
            "dirty_price": round(dirty_price, 4),
            "duration": round(macaulay_duration, 4),
            "convexity": round(convexity, 4),
            "current_yield": round(current_yield * 100, 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("bond_pricer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
