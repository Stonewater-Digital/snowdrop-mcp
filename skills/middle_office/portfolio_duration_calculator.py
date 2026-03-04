"""Calculate portfolio dollar duration and DV01."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "portfolio_duration_calculator",
    "description": "Calculates aggregate dollar duration and DV01 for fixed income books.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "face_value": {"type": "number"},
                        "coupon_pct": {"type": "number"},
                        "years_to_maturity": {"type": "number"},
                        "yield_pct": {"type": "number"},
                    },
                    "required": ["face_value", "coupon_pct", "years_to_maturity", "yield_pct"],
                },
            }
        },
        "required": ["positions"],
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


def _calculate_position_metrics(position: dict[str, Any]) -> dict[str, float]:
    face_value = float(position.get("face_value", 0.0))
    coupon_rate = float(position.get("coupon_pct", 0.0)) / 100.0
    years = float(position.get("years_to_maturity", 0.0))
    yield_rate = float(position.get("yield_pct", 0.0)) / 100.0
    if years <= 0 or face_value <= 0:
        return {"dollar_duration": 0.0, "dv01": 0.0, "modified_duration": 0.0}

    macaulay_duration = years  # simple straight-line approximation
    modified_duration = macaulay_duration / (1 + yield_rate) if yield_rate > -1 else macaulay_duration
    price_approx = face_value * (1 + coupon_rate * years)
    dollar_duration = modified_duration * price_approx / 100.0
    dv01 = dollar_duration / 100.0
    return {
        "dollar_duration": round(dollar_duration, 6),
        "dv01": round(dv01, 6),
        "modified_duration": round(modified_duration, 6),
    }


def portfolio_duration_calculator(positions: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Compute aggregate dollar duration and DV01 across all positions."""
    try:
        breakdown: list[dict[str, Any]] = []
        total_dollar_duration = 0.0
        total_dv01 = 0.0
        for idx, position in enumerate(positions or []):
            metrics = _calculate_position_metrics(position)
            total_dollar_duration += metrics["dollar_duration"]
            total_dv01 += metrics["dv01"]
            breakdown.append(
                {
                    "position_index": idx,
                    "face_value": float(position.get("face_value", 0.0)),
                    "modified_duration": metrics["modified_duration"],
                    "dollar_duration": metrics["dollar_duration"],
                    "dv01": metrics["dv01"],
                }
            )
        data = {
            "total_dollar_duration": round(total_dollar_duration, 6),
            "total_dv01": round(total_dv01, 6),
            "position_breakdown": breakdown,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        return {"status": "ok", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        try:
            with open("logs/lessons.md", "a") as _f:
                _f.write(f"- [{datetime.now(timezone.utc).isoformat()}] portfolio_duration_calculator: {exc}\n")
        except OSError:
            pass
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
