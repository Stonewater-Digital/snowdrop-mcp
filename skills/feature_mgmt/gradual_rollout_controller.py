"""Deterministic gradual rollout controller."""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "gradual_rollout_controller",
    "description": "Decides if an agent is part of a canary rollout using deterministic hashing.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skill_name": {"type": "string"},
            "rollout_pct": {"type": "number"},
            "agent_id": {"type": "string"},
            "population_size": {
                "type": "integer",
                "description": "Optional population estimate for reporting.",
            },
        },
        "required": ["skill_name", "rollout_pct", "agent_id"],
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


def gradual_rollout_controller(
    skill_name: str,
    rollout_pct: float,
    agent_id: str,
    population_size: int | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Determine rollout inclusion for a specific agent."""
    try:
        if not 0 <= rollout_pct <= 100:
            raise ValueError("rollout_pct must be between 0 and 100")
        population = population_size or 1000

        hash_input = f"{skill_name}:{agent_id}".encode("utf-8")
        digest = hashlib.sha256(hash_input).hexdigest()
        bucket = int(digest[:8], 16) % 100
        included = bucket < rollout_pct
        estimated_agents = int(population * (rollout_pct / 100))

        data = {
            "agent_included": included,
            "bucket": bucket,
            "current_rollout_pct": rollout_pct,
            "agents_in_rollout_estimate": estimated_agents,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("gradual_rollout_controller", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
