"""Collect agent heartbeats and flag issues."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "agent_heartbeat_collector",
    "description": "Rolls up heartbeat telemetry and surfaces degraded/dead agents.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "heartbeats": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["heartbeats"],
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

_FIVE_MINUTES = 300


def agent_heartbeat_collector(heartbeats: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return swarm health summary."""
    try:
        now = datetime.now(timezone.utc)
        agents = []
        dead_agents: list[str] = []
        action_needed = False
        for beat in heartbeats:
            role = beat.get("agent_role")
            timestamp = datetime.fromisoformat(str(beat.get("timestamp"))).replace(tzinfo=timezone.utc)
            seconds_since = (now - timestamp).total_seconds()
            status = beat.get("status", "alive")
            if seconds_since > _FIVE_MINUTES or status == "dead":
                action_needed = True
                dead_agents.append(role)
            agents.append(
                {
                    "agent_role": role,
                    "status": status,
                    "time_since_last_beat_sec": seconds_since,
                    "last_task": beat.get("last_task"),
                    "error": beat.get("error"),
                }
            )
        swarm_health = "critical" if dead_agents else "stable"
        data = {
            "swarm_health": swarm_health,
            "agents": agents,
            "dead_agents": dead_agents,
            "action_needed": action_needed,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": now.isoformat(),
        }
    except Exception as exc:
        _log_lesson("agent_heartbeat_collector", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
