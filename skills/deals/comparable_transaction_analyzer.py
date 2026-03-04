"""Analyze comparable transactions for valuation guidance."""
from __future__ import annotations

from datetime import datetime, timezone
from statistics import mean
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "comparable_transaction_analyzer",
    "description": "Derives valuation ranges from comps using EV/Revenue and EV/EBITDA multiples.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "target": {"type": "object"},
            "comparables": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["target", "comparables"],
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


def comparable_transaction_analyzer(
    target: dict[str, Any],
    comparables: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return comparable multiples and implied valuation bands."""
    try:
        if not comparables:
            raise ValueError("comparables cannot be empty")

        comps_enriched = []
        rev_multiples: list[float] = []
        ebitda_multiples: list[float] = []

        for comp in comparables:
            revenue = float(comp.get("revenue", 0.0))
            ebitda = float(comp.get("ebitda", 0.0))
            ev = float(comp.get("enterprise_value", 0.0))
            rev_mult = ev / revenue if revenue else 0
            ebitda_mult = ev / ebitda if ebitda else 0
            comps_enriched.append(
                {
                    "name": comp.get("name"),
                    "ev_revenue": round(rev_mult, 2),
                    "ev_ebitda": round(ebitda_mult, 2),
                    "sector": comp.get("sector"),
                }
            )
            if rev_mult:
                rev_multiples.append(rev_mult)
            if ebitda_mult:
                ebitda_multiples.append(ebitda_mult)

        median_rev = _median(rev_multiples)
        median_ebitda = _median(ebitda_multiples)
        mean_rev = mean(rev_multiples) if rev_multiples else 0.0
        mean_ebitda = mean(ebitda_multiples) if ebitda_multiples else 0.0

        target_revenue = float(target.get("revenue", 0.0))
        target_ebitda = float(target.get("ebitda", 0.0))
        implied_low = median_rev * target_revenue * 0.8
        implied_high = median_rev * target_revenue * 1.2
        implied_ebitda = median_ebitda * target_ebitda if target_ebitda else 0

        revenue_percentile = _percentile_rank(
            [float(comp.get("revenue", 0.0)) for comp in comparables], target_revenue
        )

        data = {
            "comparables": comps_enriched,
            "multiple_summary": {
                "median_ev_revenue": round(median_rev, 2),
                "median_ev_ebitda": round(median_ebitda, 2),
                "mean_ev_revenue": round(mean_rev, 2),
                "mean_ev_ebitda": round(mean_ebitda, 2),
            },
            "implied_target_valuation": {
                "revenue_low": round(implied_low, 2),
                "revenue_high": round(implied_high, 2),
                "ebitda_point": round(implied_ebitda, 2),
            },
            "target_percentile": {
                "revenue_percentile": round(revenue_percentile, 3),
            },
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("comparable_transaction_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _median(values: list[float]) -> float:
    if not values:
        return 0.0
    values_sorted = sorted(values)
    mid = len(values_sorted) // 2
    if len(values_sorted) % 2 == 0:
        return (values_sorted[mid - 1] + values_sorted[mid]) / 2
    return values_sorted[mid]


def _percentile_rank(universe: list[float], target_value: float) -> float:
    if not universe:
        return 0.0
    count = sum(1 for value in universe if value <= target_value)
    return count / len(universe)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
