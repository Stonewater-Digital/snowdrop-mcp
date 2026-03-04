"""Detect recurring Snowdrop error patterns."""
from __future__ import annotations

import difflib
from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "error_pattern_detector",
    "description": "Clusters similar errors and surfaces bursts for remediation.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "errors": {
                "type": "array",
                "items": {"type": "object"},
            }
        },
        "required": ["errors"],
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


def error_pattern_detector(errors: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return pattern clusters, bursts, and fix ideas."""

    try:
        clusters = _cluster_errors(errors)
        bursts = _detect_bursts(errors)
        recommendations = [f"Review {cluster['skill']} for '{cluster['representative']}'" for cluster in clusters[:3]]
        data = {
            "patterns": clusters,
            "burst_alerts": bursts,
            "recommended_fixes": recommendations,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("error_pattern_detector", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _cluster_errors(errors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    clusters: list[dict[str, Any]] = []
    for error in errors:
        message = error.get("error_message", "")
        skill = error.get("skill_name", "unknown")
        placed = False
        for cluster in clusters:
            similarity = difflib.SequenceMatcher(None, cluster["representative"], message).ratio()
            if similarity >= 0.8:
                cluster["count"] += 1
                cluster.setdefault("skills", set()).add(skill)
                placed = True
                break
        if not placed:
            clusters.append(
                {
                    "representative": message,
                    "count": 1,
                    "skill": skill,
                    "skills": {skill},
                }
            )
    for cluster in clusters:
        cluster["skills"] = list(cluster["skills"])
    clusters.sort(key=lambda item: item["count"], reverse=True)
    return clusters


def _detect_bursts(errors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    bursts: list[dict[str, Any]] = []
    grouped: dict[str, list[datetime]] = {}
    for error in errors:
        message = error.get("error_message", "")
        timestamp = error.get("timestamp")
        if not timestamp:
            continue
        grouped.setdefault(message, []).append(datetime.fromisoformat(timestamp))
    for message, timestamps in grouped.items():
        timestamps.sort()
        for idx in range(len(timestamps)):
            window = [t for t in timestamps if 0 <= (t - timestamps[idx]).total_seconds() <= 3600]
            if len(window) >= 3:
                bursts.append({"error_message": message, "count": len(window), "window_start": timestamps[idx].isoformat()})
                break
    return bursts


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
