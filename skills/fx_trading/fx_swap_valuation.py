"""Value FX swaps via domestic vs foreign leg PV."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "fx_swap_valuation",
    "description": "Values currency basis swaps using discounted cash flows.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "notional_domestic": {"type": "number"},
            "notional_foreign": {"type": "number"},
            "domestic_fixed_rate": {"type": "number"},
            "foreign_fixed_rate": {"type": "number"},
            "spot_at_inception": {"type": "number"},
            "current_spot": {"type": "number"},
            "remaining_years": {"type": "number"},
            "domestic_discount_rate": {"type": "number"},
            "foreign_discount_rate": {"type": "number"},
        },
        "required": [
            "notional_domestic",
            "notional_foreign",
            "domestic_fixed_rate",
            "foreign_fixed_rate",
            "spot_at_inception",
            "current_spot",
            "remaining_years",
            "domestic_discount_rate",
            "foreign_discount_rate",
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


def fx_swap_valuation(
    notional_domestic: float,
    notional_foreign: float,
    domestic_fixed_rate: float,
    foreign_fixed_rate: float,
    spot_at_inception: float,
    current_spot: float,
    remaining_years: float,
    domestic_discount_rate: float,
    foreign_discount_rate: float,
    **_: Any,
) -> dict[str, Any]:
    """Return MTM for an FX swap."""
    try:
        domestic_leg_pv = notional_domestic * (1 + domestic_fixed_rate * remaining_years) / (1 + domestic_discount_rate * remaining_years)
        foreign_leg_pv = notional_foreign * (1 + foreign_fixed_rate * remaining_years) / (1 + foreign_discount_rate * remaining_years)
        foreign_leg_domestic = foreign_leg_pv * current_spot
        mtm_value = domestic_leg_pv - foreign_leg_domestic
        fx_component = (current_spot - spot_at_inception) * notional_foreign
        rate_component = mtm_value - fx_component
        dv01 = notional_domestic * remaining_years * 0.0001
        data = {
            "mtm_value": round(mtm_value, 2),
            "domestic_leg_pv": round(domestic_leg_pv, 2),
            "foreign_leg_pv_in_domestic": round(foreign_leg_domestic, 2),
            "fx_component": round(fx_component, 2),
            "rate_component": round(rate_component, 2),
            "dv01": round(dv01, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("fx_swap_valuation", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
