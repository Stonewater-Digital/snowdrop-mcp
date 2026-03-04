"""Estimate credit spread using coupon, price, and benchmark yield."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "credit_spread_calculator",
    "description": "Computes approximate yield and spread from coupon, price, and benchmark rates.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "coupon_pct": {"type": "number"},
            "price_pct_of_par": {"type": "number"},
            "maturity_years": {"type": "number"},
            "benchmark_yield_pct": {"type": "number"},
        },
        "required": ["coupon_pct", "price_pct_of_par", "maturity_years", "benchmark_yield_pct"],
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


def credit_spread_calculator(
    coupon_pct: float,
    price_pct_of_par: float,
    maturity_years: float,
    benchmark_yield_pct: float,
    **_: Any,
) -> dict[str, Any]:
    """Return approximate OAS/Z-spread metrics."""
    try:
        price = price_pct_of_par
        coupon = coupon_pct
        avg_price = (100 + price) / 2
        ytm = ((coupon + (100 - price) / maturity_years) / avg_price) if maturity_years else 0.0
        spread = ytm - (benchmark_yield_pct / 100)
        data = {
            "approx_yield_pct": round(ytm * 100, 2),
            "spread_bps": round(spread * 10000, 1),
            "discount_margin_pct": round(spread * 100, 3),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("credit_spread_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
