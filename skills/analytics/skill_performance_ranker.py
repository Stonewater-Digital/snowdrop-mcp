"""Rank skills by operational performance."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "skill_performance_ranker",
    "description": "Combines reliability, latency, popularity, and satisfaction into a composite score.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skill_metrics": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["skill_metrics"],
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


def skill_performance_ranker(skill_metrics: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return ranking data structures for skill health."""
    try:
        rankings = []
        for metric in skill_metrics:
            score = _composite_score(metric)
            entry = {
                "skill_name": metric.get("skill_name"),
                "score": round(score, 2),
                "avg_latency_ms": metric.get("avg_latency_ms"),
                "error_rate_pct": metric.get("error_rate_pct"),
                "calls_count": metric.get("calls_count"),
                "avg_rating": metric.get("avg_rating"),
            }
            rankings.append(entry)

        rankings.sort(key=lambda item: item["score"], reverse=True)
        needs_attention = [entry for entry in rankings if entry["score"] < 50]
        top_performers = rankings[:3]
        degraded = [entry for entry in rankings if (entry.get("error_rate_pct") or 0) > 5]
        data = {
            "rankings": rankings,
            "needs_attention": needs_attention,
            "top_performers": top_performers,
            "degraded": degraded,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("skill_performance_ranker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _composite_score(metric: dict[str, Any]) -> float:
    reliability = 1 - float(metric.get("error_rate_pct", 0.0)) / 100
    reliability_score = max(reliability, 0) * 40
    latency = float(metric.get("avg_latency_ms", 1000))
    latency_score = max(0.0, 1 - (latency / 2000)) * 30
    popularity = math.log(max(float(metric.get("calls_count", 1)), 1), 10)
    popularity_score = min(popularity / 4, 1) * 15
    rating = float(metric.get("avg_rating", 4) or 0)
    satisfaction_score = min(rating / 5, 1) * 15
    return reliability_score + latency_score + popularity_score + satisfaction_score


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
