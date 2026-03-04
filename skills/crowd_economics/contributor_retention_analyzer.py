"""Analyze contributor retention and churn."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "contributor_retention_analyzer",
    "description": "Tracks contributor repeat rates, retention curves, and churn metrics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "contributions": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["contributions"],
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


def contributor_retention_analyzer(contributions: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return contributor retention insights."""
    try:
        if not contributions:
            raise ValueError("contributions required")
        contrib_map: dict[str, list[datetime]] = defaultdict(list)
        for entry in contributions:
            dt = datetime.fromisoformat(entry.get("date").replace("Z", "+00:00"))
            contrib_map[entry.get("contributor_id")].append(dt)
        total_contributors = len(contrib_map)
        repeaters = sum(1 for dates in contrib_map.values() if len(dates) > 1)
        repeat_rate = repeaters / max(total_contributors, 1) * 100
        retention_curve = {
            "1m": _retention(contrib_map, 30),
            "3m": _retention(contrib_map, 90),
            "6m": _retention(contrib_map, 180),
        }
        monthly_actives = _monthly_actives(contributions)
        power_contributors = [cid for cid, dates in contrib_map.items() if len(dates) >= 5]
        half_life = _half_life(contrib_map)
        data = {
            "total_contributors": total_contributors,
            "repeat_rate_pct": round(repeat_rate, 2),
            "retention_curve": retention_curve,
            "monthly_active_contributors": monthly_actives,
            "power_contributors": power_contributors,
            "contributor_half_life_months": half_life,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("contributor_retention_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _retention(contrib_map: dict[str, list[datetime]], days: int) -> float:
    cutoff = days
    retained = 0
    for dates in contrib_map.values():
        dates_sorted = sorted(dates)
        if (dates_sorted[-1] - dates_sorted[0]).days >= cutoff:
            retained += 1
    return round(retained / max(len(contrib_map), 1) * 100, 2)


def _monthly_actives(contributions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    monthly = defaultdict(set)
    for entry in contributions:
        dt = datetime.fromisoformat(entry.get("date").replace("Z", "+00:00"))
        key = dt.strftime("%Y-%m")
        monthly[key].add(entry.get("contributor_id"))
    return [{"month": month, "active_contributors": len(ids)} for month, ids in sorted(monthly.items())]


def _half_life(contrib_map: dict[str, list[datetime]]) -> float:
    durations = [(max(dates) - min(dates)).days for dates in contrib_map.values()]
    if not durations:
        return 0.0
    durations.sort()
    mid = len(durations) // 2
    return durations[mid] / 30


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
