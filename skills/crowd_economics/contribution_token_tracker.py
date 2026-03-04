"""Track internal vs community token spend."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "contribution_token_tracker",
    "description": "Aggregates token usage by contributor type to measure leverage.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "contributions": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["contributions"],
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


TOKEN_RATE_USD = {"input": 3 / 1000, "output": 15 / 1000}


def contribution_token_tracker(contributions: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return token leverage metrics."""
    try:
        internal = community = 0
        trend = "flat"
        for entry in contributions:
            tokens = entry.get("estimated_tokens_input", 0) + entry.get("estimated_tokens_output", 0)
            if entry.get("contributor_type") == "community":
                community += tokens
            else:
                internal += tokens
        leverage_ratio = (community / internal) if internal else float("inf") if community else 0.0
        community_pct = community / (community + internal) * 100 if (community + internal) else 0.0
        cost_equivalent = {
            "internal_usd": internal * TOKEN_RATE_USD["input"],
            "community_usd": community * TOKEN_RATE_USD["input"],
        }
        data = {
            "internal_tokens": internal,
            "community_tokens": community,
            "leverage_ratio": round(leverage_ratio, 2) if leverage_ratio != float("inf") else float("inf"),
            "community_pct": round(community_pct, 2),
            "cost_equivalent_usd": cost_equivalent,
            "trend": trend,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("contribution_token_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
