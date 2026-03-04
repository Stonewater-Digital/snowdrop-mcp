"""Analyze competitive landscape for agent services."""
from __future__ import annotations

from datetime import datetime, timezone
from statistics import median
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "competitive_landscape_tracker",
    "description": "Compares competitor offerings, pricing, and feature coverage.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "competitors": {
                "type": "array",
                "items": {"type": "object"},
            },
            "snowdrop_services": {
                "type": "array",
                "items": {"type": "string"},
            },
            "snowdrop_pricing": {"type": "object"},
        },
        "required": ["competitors", "snowdrop_services", "snowdrop_pricing"],
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


def competitive_landscape_tracker(
    competitors: list[dict[str, Any]],
    snowdrop_services: list[str],
    snowdrop_pricing: dict[str, float],
    **_: Any,
) -> dict[str, Any]:
    """Summarize competitor overlap, price rank, and differentiation."""
    try:
        if not competitors:
            raise ValueError("Provide at least one competitor entry")
        snowdrop_set = set(snowdrop_services)
        our_avg_price = _average_price(snowdrop_pricing)

        competitor_summaries = []
        competitor_avgs = []
        feature_gaps: set[str] = set()
        unique_advantages: set[str] = set(snowdrop_set)

        for competitor in competitors:
            name = str(competitor.get("name", "unknown"))
            services = set(competitor.get("services", []))
            overlap = (len(services & snowdrop_set) / len(snowdrop_set)) if snowdrop_set else 0
            pricing = competitor.get("pricing", {}) or {}
            avg_price = _average_price(pricing)
            competitor_avgs.append(avg_price)
            feature_gaps.update(services - snowdrop_set)
            unique_advantages &= snowdrop_set - services

            price_delta = avg_price - our_avg_price
            competitor_summaries.append(
                {
                    "name": name,
                    "overlap_pct": round(overlap * 100, 2),
                    "relative_price_delta": round(price_delta, 4),
                    "feature_gaps": list(services - snowdrop_set),
                    "last_updated": competitor.get("last_updated"),
                }
            )

        cheaper_count = sum(1 for avg in competitor_avgs if avg < our_avg_price)
        price_rank = cheaper_count + 1
        market_position = _market_position(our_avg_price, competitor_avgs)

        recommended_actions = []
        for gap in sorted(feature_gaps)[:3]:
            recommended_actions.append(f"Evaluate building {gap} capability")
        if price_rank > 2:
            recommended_actions.append("Develop premium narrative to justify pricing")
        elif price_rank == 1:
            recommended_actions.append("Consider modest price increase to capture margin")

        data = {
            "market_position": market_position,
            "price_rank": price_rank,
            "feature_gaps": sorted(feature_gaps),
            "unique_advantages": sorted(unique_advantages),
            "recommended_actions": recommended_actions,
            "competitor_summaries": competitor_summaries,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("competitive_landscape_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _average_price(pricing: dict[str, float]) -> float:
    if not pricing:
        return 0.0
    values = [float(value) for value in pricing.values()]
    return sum(values) / len(values)


def _market_position(our_avg: float, competitor_avgs: list[float]) -> str:
    if not competitor_avgs:
        return "unknown"
    med = median(competitor_avgs)
    if our_avg < med * 0.9:
        return "cost_leader"
    if our_avg > med * 1.1:
        return "premium"
    return "parity"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
