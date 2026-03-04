"""Greedy context window packing for Snowdrop."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "context_window_optimizer",
    "description": "Packs content sections into the available context window using priority heuristics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "content_sections": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Sections with name, content, priority (1-5) and estimated_tokens.",
            },
            "max_tokens": {"type": "integer"},
        },
        "required": ["content_sections", "max_tokens"],
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


def context_window_optimizer(
    content_sections: list[dict[str, Any]],
    max_tokens: int,
    **_: Any,
) -> dict[str, Any]:
    """Select highest-priority sections without crossing the token ceiling."""
    try:
        if max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        if not content_sections:
            raise ValueError("content_sections cannot be empty")

        normalized_sections = []
        for section in content_sections:
            tokens = int(section.get("estimated_tokens", 0))
            if tokens <= 0:
                continue
            priority = int(section.get("priority", 3))
            normalized_sections.append(
                {
                    "name": section.get("name", "section"),
                    "content": section.get("content"),
                    "priority": max(1, min(5, priority)),
                    "estimated_tokens": tokens,
                }
            )

        prioritized = sorted(
            normalized_sections,
            key=lambda sec: (sec["priority"], sec["estimated_tokens"]),
        )

        selected: list[dict[str, Any]] = []
        dropped: list[dict[str, Any]] = []
        tokens_used = 0
        for section in prioritized:
            if tokens_used + section["estimated_tokens"] <= max_tokens:
                selected.append(section)
                tokens_used += section["estimated_tokens"]
            else:
                dropped.append(
                    {
                        "name": section["name"],
                        "reason": "insufficient remaining tokens",
                        "estimated_tokens": section["estimated_tokens"],
                    }
                )

        data = {
            "selected_sections": selected,
            "total_tokens_used": tokens_used,
            "remaining_tokens": max(0, max_tokens - tokens_used),
            "dropped_sections": dropped,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("context_window_optimizer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
