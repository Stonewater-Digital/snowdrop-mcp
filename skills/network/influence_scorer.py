"""Simplified PageRank influence scoring."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "influence_scorer",
    "description": "Scores agent influence using a simplified PageRank iteration.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "interactions": {
                "type": "array",
                "items": {"type": "object"},
            },
            "damping": {"type": "number", "default": 0.85},
            "iterations": {"type": "integer", "default": 20},
        },
        "required": ["interactions"],
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


def influence_scorer(
    interactions: list[dict[str, Any]],
    damping: float = 0.85,
    iterations: int = 20,
    **_: Any,
) -> dict[str, Any]:
    """Compute influence scores for each agent."""
    try:
        if not isinstance(interactions, list):
            raise ValueError("interactions must be a list")
        if not 0 < damping < 1:
            raise ValueError("damping must be between 0 and 1")
        if iterations <= 0:
            raise ValueError("iterations must be positive")

        nodes = set()
        outgoing: dict[str, list[tuple[str, float]]] = defaultdict(list)
        incoming: dict[str, list[tuple[str, float]]] = defaultdict(list)

        for interaction in interactions:
            if not isinstance(interaction, dict):
                raise ValueError("each interaction must be a dict")
            source = str(interaction.get("from_agent"))
            target = str(interaction.get("to_agent"))
            weight = float(interaction.get("weight", 1.0))
            if not source or not target:
                continue
            nodes.update({source, target})
            outgoing[source].append((target, weight))
            incoming[target].append((source, weight))

        if not nodes:
            return {
                "status": "success",
                "data": {"scores": []},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        n = len(nodes)
        scores = {node: 1 / n for node in nodes}

        for _ in range(iterations):
            new_scores = {node: (1 - damping) / n for node in nodes}
            for node in nodes:
                share = scores[node]
                total_weight = sum(weight for _, weight in outgoing.get(node, []))
                if total_weight == 0:
                    for target in nodes:
                        new_scores[target] += damping * (share / n)
                else:
                    for target, weight in outgoing.get(node, []):
                        new_scores[target] += damping * share * (weight / total_weight)
            scores = new_scores

        max_score = max(scores.values())
        normalized = []
        for node, score in scores.items():
            normalized_score = (score / max_score) * 100 if max_score else 0.0
            tier = _tier_from_score(normalized_score)
            normalized.append(
                {
                    "agent_id": node,
                    "score": round(normalized_score, 2),
                    "tier": tier,
                }
            )

        normalized.sort(key=lambda entry: entry["score"], reverse=True)
        return {
            "status": "success",
            "data": {"scores": normalized},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("influence_scorer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _tier_from_score(score: float) -> str:
    if score >= 66:
        return "whale"
    if score >= 33:
        return "regular"
    return "newcomer"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
