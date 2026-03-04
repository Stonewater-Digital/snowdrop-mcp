"""Bond duration and convexity calculator."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "bond_duration_calculator",
    "description": "Computes Macaulay duration, modified duration, and convexity for a coupon bond.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "face_value": {"type": "number", "description": "Par/face value of the bond."},
            "coupon_rate_pct": {"type": "number", "description": "Annual coupon rate as a percentage."},
            "years_to_maturity": {"type": "number", "description": "Years until bond matures (must be > 0)."},
            "yield_to_maturity_pct": {"type": "number", "description": "Annual YTM as a percentage."},
            "payments_per_year": {"type": "integer", "default": 2, "description": "Coupon payment frequency (2 = semi-annual)."},
        },
        "required": [
            "face_value",
            "coupon_rate_pct",
            "years_to_maturity",
            "yield_to_maturity_pct",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "price": {"type": "number"},
                    "macaulay_duration": {"type": "number"},
                    "modified_duration": {"type": "number"},
                    "convexity": {"type": "number"},
                    "dv01": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def bond_duration_calculator(
    face_value: float,
    coupon_rate_pct: float,
    years_to_maturity: float,
    yield_to_maturity_pct: float,
    payments_per_year: int = 2,
    **_: Any,
) -> dict[str, Any]:
    """Compute Macaulay duration, modified duration, convexity, and DV01.

    Args:
        face_value: Par value of the bond.
        coupon_rate_pct: Annual coupon rate as a percentage (e.g. 5.0 for 5%).
        years_to_maturity: Time to maturity in years (must be > 0).
        yield_to_maturity_pct: Annual yield to maturity as a percentage.
        payments_per_year: Number of coupon payments per year (default 2 for semi-annual).

    Returns:
        dict with status, data (price, macaulay_duration, modified_duration,
        convexity, dv01), and timestamp.
    """
    try:
        if face_value <= 0:
            raise ValueError("face_value must be positive")
        if years_to_maturity <= 0:
            raise ValueError("years_to_maturity must be positive")
        if payments_per_year <= 0:
            raise ValueError("payments_per_year must be a positive integer")

        periods = int(round(years_to_maturity * payments_per_year))
        if periods <= 0:
            raise ValueError("years_to_maturity too small for given payments_per_year")

        coupon_rate = coupon_rate_pct / 100.0
        ytm = yield_to_maturity_pct / 100.0
        period_rate = ytm / payments_per_year
        coupon_payment = face_value * coupon_rate / payments_per_year

        price = 0.0
        weighted_time = 0.0   # sum of t * PV(CF_t)  [in periods]
        convexity_sum = 0.0   # sum of t*(t+1) * PV(CF_t)

        for t in range(1, periods + 1):
            cf = coupon_payment + (face_value if t == periods else 0.0)
            pv = cf / (1 + period_rate) ** t
            price += pv
            weighted_time += t * pv
            convexity_sum += t * (t + 1) * pv

        if price == 0.0:
            raise ValueError("Bond price computed as zero — check inputs")

        # Macaulay duration in years
        macaulay = (weighted_time / price) / payments_per_year
        # Modified duration
        modified = macaulay / (1 + period_rate)
        # Convexity (in years^2)
        convexity = convexity_sum / (price * (payments_per_year ** 2) * (1 + period_rate) ** 2)
        # DV01: dollar change per 1 bp move in yield
        dv01 = modified * price / 10000.0

        data = {
            "price": round(price, 4),
            "macaulay_duration": round(macaulay, 4),
            "modified_duration": round(modified, 4),
            "convexity": round(convexity, 4),
            "dv01": round(dv01, 6),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson(f"bond_duration_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
