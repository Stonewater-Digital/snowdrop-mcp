"""Consensus protocol for multi-agent decisions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "consensus_protocol",
    "description": "Evaluates votes for quorum and flags potential Byzantine behavior.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "votes": {"type": "array", "items": {"type": "object"}},
            "quorum_threshold": {"type": "number", "default": 0.67},
            "min_voters": {"type": "integer", "default": 3},
        },
        "required": ["votes"],
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


def consensus_protocol(
    votes: list[dict[str, Any]],
    quorum_threshold: float = 0.67,
    min_voters: int = 3,
    **_: Any,
) -> dict[str, Any]:
    """Return consensus decision and dissent list."""
    try:
        if len(votes) < min_voters:
            raise ValueError("Not enough votes for consensus")
        decision_counts: dict[str, float] = {}
        dissenting_agents: list[str] = []
        total_weight = 0.0
        for vote in votes:
            decision = vote.get("decision")
            confidence = float(vote.get("confidence", 0.0))
            total_weight += confidence
            decision_counts[decision] = decision_counts.get(decision, 0.0) + confidence
            reasoning = vote.get("reasoning", "")
            if reasoning and decision and decision.lower() not in reasoning.lower():
                dissenting_agents.append(vote.get("agent_role", "unknown"))
        if not decision_counts:
            raise ValueError("No valid votes recorded")
        best_decision = max(decision_counts, key=decision_counts.get)
        best_share = decision_counts[best_decision] / total_weight if total_weight else 0.0
        consensus_reached = best_share >= quorum_threshold
        data = {
            "consensus_reached": consensus_reached,
            "decision": best_decision if consensus_reached else "undecided",
            "confidence": round(best_share, 3),
            "dissenting_agents": dissenting_agents,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("consensus_protocol", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
