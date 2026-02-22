"""Value a plain vanilla interest rate swap."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

PAY_FREQ = {"quarterly": 4, "semi_annual": 2, "annual": 1}

TOOL_META: dict[str, Any] = {
    "name": "interest_rate_swap_valuer",
    "description": "Computes MTM, PV legs, and DV01 for swaps using provided discount curve.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "notional": {"type": "number"},
            "fixed_rate": {"type": "number"},
            "floating_rate_current": {"type": "number"},
            "swap_tenor_remaining_years": {"type": "number"},
            "payment_frequency": {"type": "string", "enum": ["quarterly", "semi_annual", "annual"], "default": "semi_annual"},
            "position": {"type": "string", "enum": ["pay_fixed", "receive_fixed"]},
            "discount_curve": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["notional", "fixed_rate", "floating_rate_current", "swap_tenor_remaining_years", "position", "discount_curve"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def interest_rate_swap_valuer(
    notional: float,
    fixed_rate: float,
    floating_rate_current: float,
    swap_tenor_remaining_years: float,
    position: str,
    discount_curve: list[dict[str, Any]],
    payment_frequency: str = "semi_annual",
    **_: Any,
) -> dict[str, Any]:
    """Return swap MTM."""
    try:
        periods = int(swap_tenor_remaining_years * PAY_FREQ[payment_frequency])
        accrual = 1 / PAY_FREQ[payment_frequency]
        fixed_leg_pv = 0.0
        floating_leg_pv = notional
        for period in range(1, periods + 1):
            discount_rate = _rate_for_tenor(discount_curve, period * accrual)
            df = math.exp(-discount_rate * period * accrual)
            fixed_leg_pv += notional * fixed_rate * accrual * df
            floating_leg_pv += notional * floating_rate_current * accrual * df
        floating_leg_pv = floating_leg_pv - notional
        mtm = floating_leg_pv - fixed_leg_pv if position == "pay_fixed" else fixed_leg_pv - floating_leg_pv
        dv01 = notional * accrual * swap_tenor_remaining_years / 10_000
        data = {
            "mtm_value": round(mtm, 2),
            "fixed_leg_pv": round(fixed_leg_pv, 2),
            "floating_leg_pv": round(floating_leg_pv, 2),
            "dv01": round(dv01, 2),
            "annual_net_payment": round((fixed_rate - floating_rate_current) * notional, 2),
            "in_the_money": mtm > 0,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("interest_rate_swap_valuer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _rate_for_tenor(curve: list[dict[str, Any]], tenor: float) -> float:
    curve_sorted = sorted(curve, key=lambda x: x.get("tenor_years", 0.0))
    for point in curve_sorted:
        if tenor <= point.get("tenor_years", 0.0):
            return point.get("rate", 0.0)
    return curve_sorted[-1].get("rate", 0.0) if curve_sorted else 0.0


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
