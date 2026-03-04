"""Analyze revenue per skill for Watering Hole."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "revenue_per_skill_analyzer",
    "description": "Aggregates billing records to highlight top-performing skills and concentration",
    "inputSchema": {
        "type": "object",
        "properties": {
            "billing_records": {
                "type": "array",
                "items": {"type": "object"},
            },
            "period": {"type": "string"},
        },
        "required": ["billing_records", "period"],
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


def revenue_per_skill_analyzer(
    billing_records: list[dict[str, Any]],
    period: str,
    **_: Any,
) -> dict[str, Any]:
    """Return revenue metrics grouped by skill."""
    try:
        totals: dict[str, float] = defaultdict(float)
        counts: dict[str, int] = defaultdict(int)
        timestamps: dict[str, list[datetime]] = defaultdict(list)

        for record in billing_records:
            skill = str(record.get("skill_name", "unknown"))
            amount = float(record.get("amount", 0.0))
            totals[skill] += amount
            counts[skill] += 1
            ts_str = record.get("timestamp")
            if ts_str:
                try:
                    timestamps[skill].append(datetime.fromisoformat(ts_str))
                except ValueError:
                    continue

        total_revenue = sum(totals.values())
        top_skills = []
        for skill, revenue in sorted(totals.items(), key=lambda item: item[1], reverse=True):
            count = counts[skill]
            avg = revenue / count if count else 0.0
            trend = _trend_label(timestamps[skill])
            top_skills.append(
                {
                    "skill_name": skill,
                    "revenue": round(revenue, 2),
                    "calls": count,
                    "avg_revenue_per_call": round(avg, 4),
                    "trend": trend,
                }
            )

        concentration_pct = (
            (top_skills[0]["revenue"] / total_revenue * 100) if top_skills and total_revenue else 0.0
        )
        long_tail_count = len([entry for entry in top_skills if entry["revenue"] < (total_revenue * 0.02)])
        data = {
            "period": period,
            "top_skills": top_skills,
            "total_revenue": round(total_revenue, 2),
            "revenue_concentration_pct": round(concentration_pct, 2),
            "long_tail_count": long_tail_count,
            "zero_revenue_skills": [],
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("revenue_per_skill_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _trend_label(events: list[datetime]) -> str:
    if len(events) < 2:
        return "flat"
    events.sort()
    midpoint = len(events) // 2
    first_half = events[:midpoint]
    second_half = events[midpoint:]
    return "rising" if len(second_half) > len(first_half) else "flat"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
