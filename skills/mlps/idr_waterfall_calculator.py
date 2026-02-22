"""Calculate MLP IDR waterfalls."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "idr_waterfall_calculator",
    "description": "Allocates distributable cash through IDR tiers for MLPs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_distributable_cash": {"type": "number"},
            "lp_units": {"type": "integer"},
            "gp_units": {"type": "integer"},
            "idr_tiers": {"type": "array", "items": {"type": "object"}},
            "minimum_quarterly_distribution": {"type": "number"},
        },
        "required": ["total_distributable_cash", "lp_units", "gp_units", "idr_tiers", "minimum_quarterly_distribution"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def idr_waterfall_calculator(
    total_distributable_cash: float,
    lp_units: int,
    gp_units: int,
    idr_tiers: list[dict[str, Any]],
    minimum_quarterly_distribution: float,
    **_: Any,
) -> dict[str, Any]:
    """Return IDR allocations per tier."""
    try:
        remaining = total_distributable_cash
        tier_breakdown = []
        current_tier = None
        cash_per_unit = remaining / lp_units if lp_units else 0.0
        for tier in sorted(idr_tiers, key=lambda t: t.get("threshold_per_unit", 0.0)):
            threshold = tier.get("threshold_per_unit", 0.0)
            lp_split = tier.get("lp_split_pct", 0.0) / 100
            gp_split = tier.get("gp_split_pct", 0.0) / 100
            allocatable = max(0.0, min(remaining, (threshold - minimum_quarterly_distribution) * lp_units)) if threshold else remaining
            lp_amount = allocatable * lp_split
            gp_amount = allocatable * gp_split
            remaining -= allocatable
            tier_breakdown.append({"tier": threshold, "lp_amount": round(lp_amount, 2), "gp_amount": round(gp_amount, 2)})
            if remaining <= 0:
                current_tier = tier
                break
        lp_total = sum(t["lp_amount"] for t in tier_breakdown)
        gp_total = total_distributable_cash - lp_total
        gp_idr = gp_total
        gp_take = gp_total / total_distributable_cash * 100 if total_distributable_cash else 0.0
        data = {
            "lp_total": round(lp_total, 2),
            "gp_total": round(gp_total, 2),
            "gp_idr_amount": round(gp_idr, 2),
            "gp_effective_take_pct": round(gp_take, 2),
            "current_tier": current_tier,
            "dpu": round(total_distributable_cash / lp_units, 3) if lp_units else 0.0,
            "tier_breakdown": tier_breakdown,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("idr_waterfall_calculator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
