"""Analyze futures term structure for commodities."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "futures_curve_analyzer",
    "description": "Classifies contango/backwardation, computes roll yield, and signals carry trades.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot_price": {"type": "number"},
            "futures": {"type": "array", "items": {"type": "object"}},
            "storage_cost_monthly": {"type": ["number", "null"], "default": None},
            "convenience_yield_est": {"type": ["number", "null"], "default": None},
        },
        "required": ["spot_price", "futures"],
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


def futures_curve_analyzer(
    spot_price: float,
    futures: list[dict[str, Any]],
    storage_cost_monthly: float | None = None,
    convenience_yield_est: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return structure classification, roll yield, and carry signal."""
    try:
        if spot_price <= 0 or not futures:
            raise ValueError("Spot and futures prices required")
        ordered = sorted(futures, key=lambda f: f.get("expiry_month"))
        basis = [
            {
                "tenor": fut.get("expiry_month"),
                "basis": fut.get("price", 0) - spot_price,
            }
            for fut in ordered
        ]
        first = ordered[0]["price"]
        last = ordered[-1]["price"]
        if first > spot_price and last > first:
            structure = "contango"
        elif first < spot_price and last < first:
            structure = "backwardation"
        else:
            structure = "mixed"
        annualized_roll = (spot_price / first - 1) * 12 if first else 0
        cost_of_carry = (storage_cost_monthly or 0) * 12 - (convenience_yield_est or 0)
        carry_signal = "short_front_long_deferred" if structure == "contango" else "long_front_short_deferred"
        data = {
            "structure": structure,
            "annualized_roll_yield": round(annualized_roll * 100, 2),
            "basis_by_tenor": basis,
            "carry_trade_signal": carry_signal,
            "cost_of_carry_implied": round(cost_of_carry, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("futures_curve_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
