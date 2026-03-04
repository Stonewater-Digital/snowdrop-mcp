"""Evaluate senior and total loan-to-value metrics."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "loan_to_value_calculator",
    "description": "Calculates senior and total LTV ratios with headroom checks.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "collateral_value": {"type": "number"},
            "senior_debt": {"type": "number"},
            "total_debt": {"type": "number"},
            "advance_rate_limit": {"type": "number", "default": 65.0},
        },
        "required": ["collateral_value", "senior_debt", "total_debt"],
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


def loan_to_value_calculator(
    collateral_value: float,
    senior_debt: float,
    total_debt: float,
    advance_rate_limit: float | None = 65.0,
    **_: Any,
) -> dict[str, Any]:
    """Return senior/total LTV ratios and remaining collateral cushion."""
    try:
        collateral = collateral_value if collateral_value else 0.0
        senior_ltv = (senior_debt / collateral) * 100 if collateral else 0.0
        total_ltv = (total_debt / collateral) * 100 if collateral else 0.0
        headroom = (advance_rate_limit - total_ltv) if (advance_rate_limit is not None) else None
        breaching = advance_rate_limit is not None and total_ltv > advance_rate_limit
        data = {
            "senior_ltv_pct": round(senior_ltv, 2),
            "total_ltv_pct": round(total_ltv, 2),
            "collateral_headroom_pct": round(headroom, 2) if headroom is not None else None,
            "advance_rate_limit_pct": advance_rate_limit,
            "breach": breaching,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("loan_to_value_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
