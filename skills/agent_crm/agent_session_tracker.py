"""Track agent session metrics and churn risk."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "agent_session_tracker",
    "description": "Aggregates per-agent usage, spend, and churn risk from session logs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "sessions": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["sessions"],
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


def agent_session_tracker(sessions: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return analytics for each agent id."""
    try:
        if not sessions:
            raise ValueError("sessions cannot be empty")

        aggregates: dict[str, dict[str, Any]] = defaultdict(
            lambda: {
                "total_spend": 0.0,
                "session_count": 0,
                "skills": defaultdict(int),
                "last_active": None,
                "total_duration_ms": 0.0,
            }
        )

        now = datetime.now(timezone.utc)
        for session in sessions:
            agent_id = session.get("agent_id")
            if not agent_id:
                continue
            cost = float(session.get("cost", 0.0))
            duration = float(session.get("duration_ms", 0.0))
            skill = session.get("skill_used", "unknown")
            timestamp_raw = session.get("timestamp")
            timestamp = _parse_datetime(timestamp_raw)

            aggregates[agent_id]["total_spend"] += cost
            aggregates[agent_id]["session_count"] += 1
            aggregates[agent_id]["skills"][skill] += 1
            aggregates[agent_id]["total_duration_ms"] += duration
            if not aggregates[agent_id]["last_active"] or timestamp > aggregates[agent_id]["last_active"]:
                aggregates[agent_id]["last_active"] = timestamp

        analytics = []
        for agent_id, stats in aggregates.items():
            session_count = stats["session_count"] or 1
            last_active = stats["last_active"] or now
            days_since_active = (now - last_active).days
            analytics.append(
                {
                    "agent_id": agent_id,
                    "total_spend": round(stats["total_spend"], 2),
                    "avg_session_cost": round(stats["total_spend"] / session_count, 2),
                    "skills_used_frequency": dict(stats["skills"]),
                    "last_active": last_active.isoformat(),
                    "churn_risk": _churn_risk(days_since_active, session_count),
                }
            )

        return {
            "status": "success",
            "data": {"agents": analytics},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("agent_session_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return datetime.fromisoformat(str(value)).replace(tzinfo=timezone.utc)


def _churn_risk(days_since_active: int, session_count: int) -> str:
    if days_since_active > 45 or session_count < 2:
        return "high"
    if days_since_active > 21:
        return "medium"
    return "low"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
