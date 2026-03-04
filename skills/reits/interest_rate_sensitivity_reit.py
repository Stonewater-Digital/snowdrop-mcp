"""Estimate REIT debt duration and rate sensitivity."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "interest_rate_sensitivity_reit",
    "description": "Calculates fixed vs floating mix, duration, and DV01 for the debt stack.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "debt_instruments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "enum": ["fixed", "floating"]},
                        "notional": {"type": "number"},
                        "maturity_years": {"type": "number"},
                        "coupon_pct": {"type": "number"},
                    },
                    "required": ["type", "notional", "maturity_years", "coupon_pct"],
                },
            }
        },
        "required": ["debt_instruments"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def interest_rate_sensitivity_reit(debt_instruments: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return sensitivity metrics for the debt stack."""
    try:
        total_notional = sum(item.get("notional", 0.0) for item in debt_instruments)
        if total_notional <= 0:
            raise ValueError("Total notional must be positive")
        weighted_duration = (
            sum(item.get("notional", 0.0) * item.get("maturity_years", 0.0) for item in debt_instruments) / total_notional
        )
        convexity = (
            sum(item.get("notional", 0.0) * (item.get("maturity_years", 0.0) ** 2) for item in debt_instruments)
            / total_notional
        )
        dv01 = weighted_duration * total_notional / 10000
        fixed_notional = sum(item.get("notional", 0.0) for item in debt_instruments if item.get("type") == "fixed")
        floating_notional = total_notional - fixed_notional
        data = {
            "weighted_duration_years": round(weighted_duration, 2),
            "convexity": round(convexity, 2),
            "dv01": round(dv01, 2),
            "fixed_pct": round(fixed_notional / total_notional * 100, 2),
            "floating_pct": round(floating_notional / total_notional * 100, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("interest_rate_sensitivity_reit", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
