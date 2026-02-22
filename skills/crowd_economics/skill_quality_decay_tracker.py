"""Track quality decay across community skills."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "skill_quality_decay_tracker",
    "description": "Measures error rate drift and maintenance burden for community skills over time.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skill_snapshots": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["skill_snapshots"],
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


def skill_quality_decay_tracker(skill_snapshots: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return error rate by age bucket and refresh recommendations."""
    try:
        age_buckets = {"0-30": [], "31-90": [], "91-180": [], "180+": []}
        maintenance_reports = 0
        needs_refresh = []
        now = datetime.now(timezone.utc)
        for snap in skill_snapshots:
            added = datetime.fromisoformat(snap.get("date_added", now.isoformat()).replace("Z", "+00:00"))
            age_days = (now - added).days
            bug_reports = snap.get("bug_reports", 0)
            maintenance_reports += bug_reports
            if snap.get("current_error_rate", 0) > 0.1 or bug_reports > 3:
                needs_refresh.append(snap.get("skill_name"))
            bucket = _bucket(age_days)
            age_buckets[bucket].append(snap.get("current_error_rate", 0))
        avg_error = {
            bucket: round(sum(values) / len(values), 4) if values else 0
            for bucket, values in age_buckets.items()
        }
        decay_detected = avg_error["180+"] > avg_error["0-30"] if age_buckets["0-30"] else False
        maintenance_burden = maintenance_reports / max(len(skill_snapshots), 1)
        half_life = _half_life(age_buckets)
        data = {
            "decay_detected": decay_detected,
            "avg_error_by_age": avg_error,
            "maintenance_burden_per_skill": round(maintenance_burden, 2),
            "needs_refresh": needs_refresh,
            "quality_half_life_days": half_life,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("skill_quality_decay_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _bucket(age_days: int) -> str:
    if age_days <= 30:
        return "0-30"
    if age_days <= 90:
        return "31-90"
    if age_days <= 180:
        return "91-180"
    return "180+"


def _half_life(buckets: dict[str, list[float]]) -> float | None:
    if not buckets["0-30"] or not buckets["180+"]:
        return None
    base = sum(buckets["0-30"]) / len(buckets["0-30"])
    if base == 0:
        return None
    target = base / 2
    for bucket in ["31-90", "91-180", "180+"]:
        if buckets[bucket]:
            avg = sum(buckets[bucket]) / len(buckets[bucket])
            if avg >= target:
                return {"31-90": 60, "91-180": 135, "180+": 210}[bucket]
    return None


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
