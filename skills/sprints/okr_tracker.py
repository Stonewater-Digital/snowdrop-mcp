"""Track Objectives and Key Results progress."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "okr_tracker",
    "description": "Calculates OKR progress, color codes, and highlights at-risk objectives.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "okrs": {"type": "array", "items": {"type": "object"}},
            "quarter": {"type": "string", "description": "Quarter label (e.g., Q2-2026)."},
        },
        "required": ["okrs"],
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


def okr_tracker(okrs: list[dict[str, Any]], quarter: str | None = None, **_: Any) -> dict[str, Any]:
    """Return OKR scoring summary."""
    try:
        objectives_summary = []
        at_risk = []
        on_track = []
        objective_scores: list[float] = []

        for okr in okrs:
            key_results = okr.get("key_results", []) or []
            kr_entries = []
            kr_scores: list[float] = []
            for kr in key_results:
                target = float(kr.get("target", 0.0))
                current = float(kr.get("current", 0.0))
                if target <= 0:
                    progress = 0.0
                else:
                    progress = min(current / target, 1.2)
                color = _color(progress)
                entry = {
                    "description": kr.get("description"),
                    "target": target,
                    "current": current,
                    "progress_pct": round(progress * 100, 2),
                    "color": color,
                    "unit": kr.get("unit"),
                }
                kr_entries.append(entry)
                kr_scores.append(progress)
            objective_score = sum(kr_scores) / len(kr_scores) if kr_scores else 0.0
            objective_scores.append(objective_score)
            objective_entry = {
                "objective": okr.get("objective"),
                "score_pct": round(objective_score * 100, 2),
                "color": _color(objective_score),
                "key_results": kr_entries,
            }
            objectives_summary.append(objective_entry)
            if objective_score < 0.4:
                at_risk.append(objective_entry)
            elif objective_score >= 0.7:
                on_track.append(objective_entry)

        overall_score = sum(objective_scores) / len(objective_scores) if objective_scores else 0.0
        data = {
            "quarter": quarter,
            "objectives": objectives_summary,
            "overall_score": round(overall_score * 100, 2),
            "at_risk": at_risk,
            "on_track": on_track,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("okr_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _color(progress: float) -> str:
    if progress >= 0.7:
        return "green"
    if progress >= 0.4:
        return "yellow"
    return "red"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
