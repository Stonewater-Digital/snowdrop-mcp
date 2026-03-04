"""Monitor Snowdrop data source freshness."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "data_freshness_monitor",
    "description": "Checks data sources against allowed staleness windows.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "sources": {
                "type": "array",
                "items": {"type": "object"},
            }
        },
        "required": ["sources"],
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


def data_freshness_monitor(sources: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return freshness score and stale sources list."""

    try:
        now = datetime.now(timezone.utc)
        stale_sources: list[dict[str, Any]] = []
        for source in sources:
            last_updated = source.get("last_updated")
            max_age = int(source.get("max_age_minutes", 0))
            if not last_updated or max_age <= 0:
                raise ValueError("Each source requires last_updated ISO string and max_age_minutes")
            updated_at = datetime.fromisoformat(last_updated)
            age_minutes = (now - updated_at).total_seconds() / 60
            source["age_minutes"] = round(age_minutes, 2)
            if age_minutes > max_age:
                source["status"] = "stale"
                source["minutes_overdue"] = round(age_minutes - max_age, 2)
                stale_sources.append(source)
            else:
                source["status"] = "fresh"

        total_sources = len(sources)
        stale_count = len(stale_sources)
        freshness_score = 100 if total_sources == 0 else max(0, 100 - (stale_count / total_sources) * 100)
        data = {
            "all_fresh": stale_count == 0,
            "stale_sources": stale_sources,
            "freshness_score": round(freshness_score, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": now.isoformat(),
        }
    except Exception as exc:
        _log_lesson("data_freshness_monitor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
