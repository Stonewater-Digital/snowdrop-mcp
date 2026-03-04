"""Analyze rental rate growth and mark-to-market spreads."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "rental_rate_growth_calculator",
    "description": "Calculates cash and GAAP leasing spreads versus expiring rents.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "expiring_rent_psf": {"type": "number"},
            "new_rent_psf": {"type": "number"},
            "market_rent_psf": {"type": "number"},
            "retained_pct": {"type": "number", "default": 70.0},
        },
        "required": ["expiring_rent_psf", "new_rent_psf", "market_rent_psf"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def rental_rate_growth_calculator(
    expiring_rent_psf: float,
    new_rent_psf: float,
    market_rent_psf: float,
    retained_pct: float = 70.0,
    **_: Any,
) -> dict[str, Any]:
    """Return rent spread metrics."""
    try:
        cash_spread = (new_rent_psf - expiring_rent_psf) / expiring_rent_psf * 100 if expiring_rent_psf else 0.0
        mark_to_market = (market_rent_psf - expiring_rent_psf) / expiring_rent_psf * 100 if expiring_rent_psf else 0.0
        blended_growth = (retained_pct / 100) * cash_spread + (1 - retained_pct / 100) * mark_to_market
        data = {
            "cash_leasing_spread_pct": round(cash_spread, 2),
            "mark_to_market_pct": round(mark_to_market, 2),
            "blended_growth_pct": round(blended_growth, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("rental_rate_growth_calculator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
