"""Fair fixed rate estimator for vanilla interest rate swaps."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "swap_rate_calculator",
    "description": "Computes par swap rate, fixed leg PV, float leg PV, and NPV.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "notional": {"type": "number"},
            "fixed_payment_dates": {"type": "array", "items": {"type": "number"}},
            "float_payment_dates": {"type": "array", "items": {"type": "number"}},
            "discount_factors": {"type": "array", "items": {"type": "number"}},
        },
        "required": [
            "notional",
            "fixed_payment_dates",
            "float_payment_dates",
            "discount_factors",
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


def swap_rate_calculator(
    notional: float,
    fixed_payment_dates: list[float],
    float_payment_dates: list[float],
    discount_factors: list[float],
    **_: Any,
) -> dict[str, Any]:
    """Return par fixed rate, PV of legs, and swap NPV."""
    try:
        if not fixed_payment_dates or not discount_factors:
            raise ValueError("payment dates and discount factors required")
        if len(discount_factors) < len(fixed_payment_dates):
            raise ValueError("discount factors must cover fixed leg dates")
        accruals = []
        prev = 0.0
        for t in fixed_payment_dates:
            accruals.append(max(t - prev, 0.0))
            prev = t
        annuity = sum(acc * discount_factors[idx] for idx, acc in enumerate(accruals))
        df_float_end = discount_factors[len(float_payment_dates) - 1]
        float_leg_pv = notional * (1 - df_float_end)
        fair_rate = float_leg_pv / (notional * annuity) if annuity else 0.0
        fixed_leg_pv = notional * fair_rate * annuity
        swap_npv = float_leg_pv - fixed_leg_pv
        data = {
            "fair_fixed_rate_pct": round(fair_rate * 100, 6),
            "fixed_leg_pv": round(fixed_leg_pv, 2),
            "float_leg_pv": round(float_leg_pv, 2),
            "swap_npv": round(swap_npv, 2),
        }
        return {"status": "ok", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        try:
            with open("logs/lessons.md", "a") as _f:
                _f.write(f"- [{datetime.now(timezone.utc).isoformat()}] swap_rate_calculator: {exc}\n")
        except OSError:
            pass
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
