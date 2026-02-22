"""Quantify portfolio fee drag."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "fee_drag_analyzer",
    "description": "Summarizes fees and calculates annualized drag versus AUM.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "fees": {
                "type": "array",
                "items": {"type": "object"},
            },
            "avg_aum": {"type": "number"},
            "period_days": {"type": "integer"},
        },
        "required": ["fees", "avg_aum", "period_days"],
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


def fee_drag_analyzer(
    fees: list[dict[str, Any]],
    avg_aum: float,
    period_days: int,
    **_: Any,
) -> dict[str, Any]:
    """Return fee totals, breakdown, and drag alerts."""

    try:
        if avg_aum <= 0:
            raise ValueError("avg_aum must be positive")
        if period_days <= 0:
            raise ValueError("period_days must be positive")
        total = 0.0
        breakdown: dict[str, float] = defaultdict(float)
        for fee in fees:
            amount = float(fee.get("amount", 0))
            total += amount
            breakdown[fee.get("type", "other")]+= amount
        annualized_pct = (total / avg_aum) * (365 / period_days) * 100
        projected_drag = round(annualized_pct, 4)
        flag = projected_drag > 2
        data = {
            "total_fees": round(total, 2),
            "annualized_fee_pct": round(annualized_pct, 4),
            "fee_breakdown_by_type": {k: round(v, 2) for k, v in breakdown.items()},
            "projected_annual_drag_pct": projected_drag,
            "drag_alert": flag,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("fee_drag_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
