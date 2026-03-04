"""Track delayed draw term loan utilization and costs."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "delayed_draw_term_loan_tracker",
    "description": "Calculates drawn/undrawn balances, fees, and blended costs for DDTLs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_commitment": {"type": "number"},
            "draws": {"type": "array", "items": {"type": "object"}},
            "commitment_fee_bps": {"type": "integer"},
            "drawn_spread_bps": {"type": "integer"},
            "draw_period_end": {"type": "string"},
            "availability_conditions": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["total_commitment", "draws", "commitment_fee_bps", "drawn_spread_bps", "draw_period_end"],
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


def delayed_draw_term_loan_tracker(
    total_commitment: float,
    draws: list[dict[str, Any]],
    commitment_fee_bps: int,
    drawn_spread_bps: int,
    draw_period_end: str,
    availability_conditions: list[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return DDTL utilization stats."""
    try:
        drawn = sum(float(draw.get("amount", 0.0)) for draw in draws)
        undrawn = max(total_commitment - drawn, 0.0)
        utilization_pct = drawn / total_commitment * 100 if total_commitment else 0.0
        annual_commitment_fee = undrawn * (commitment_fee_bps / 10000)
        annual_drawn_interest = drawn * (drawn_spread_bps / 10000)
        blended_cost = (annual_commitment_fee + annual_drawn_interest) / max(drawn, 1)
        period_end = datetime.fromisoformat(draw_period_end)
        days_remaining = (period_end - datetime.now(timezone.utc)).days
        data = {
            "drawn": round(drawn, 2),
            "undrawn": round(undrawn, 2),
            "utilization_pct": round(utilization_pct, 2),
            "annual_commitment_fee": round(annual_commitment_fee, 2),
            "annual_drawn_interest": round(annual_drawn_interest, 2),
            "blended_cost": round(blended_cost, 4),
            "draw_period_remaining_days": max(days_remaining, 0),
            "draws_history": draws,
            "availability_conditions": availability_conditions or [],
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("delayed_draw_term_loan_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
