"""Analyze rent roll metrics."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "rent_roll_analyzer",
    "description": "Calculates occupancy, income, loss-to-lease, and lease rollover risk.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "units": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["units"],
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


def rent_roll_analyzer(units: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return rent roll KPIs."""
    try:
        occupied = [u for u in units if u.get("status") == "occupied"]
        occupancy_pct = len(occupied) / len(units) * 100 if units else 0.0
        monthly_income = sum(u.get("current_rent", 0.0) for u in occupied)
        market_income = sum(u.get("market_rent", u.get("current_rent", 0.0)) for u in units)
        loss_to_lease = market_income - monthly_income
        sqft_total = sum(u.get("sqft", 0.0) for u in units)
        avg_rent_psf = (monthly_income * 12) / sqft_total if sqft_total else 0.0
        market_rent_psf = (market_income * 12) / sqft_total if sqft_total else 0.0
        now = datetime.now(timezone.utc).date()
        lease_expiry_schedule = []
        for unit in occupied:
            lease_end = unit.get("lease_end")
            if lease_end:
                end_date = datetime.fromisoformat(lease_end).date()
                if end_date - now <= timedelta(days=365):
                    lease_expiry_schedule.append({"unit_id": unit.get("unit_id"), "lease_end": lease_end})
        rollover_risk = "low" if len(lease_expiry_schedule) / max(len(units), 1) < 0.2 else "high"
        data = {
            "occupancy_pct": round(occupancy_pct, 2),
            "monthly_income": round(monthly_income, 2),
            "annual_income": round(monthly_income * 12, 2),
            "loss_to_lease_annual": round(loss_to_lease * 12, 2),
            "avg_rent_psf": round(avg_rent_psf, 2),
            "market_rent_psf": round(market_rent_psf, 2),
            "lease_expiry_schedule": lease_expiry_schedule,
            "rollover_risk": rollover_risk,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("rent_roll_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
