"""Automatically cascade Snowdrop models when rate limits hit."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

CASCADE_CHAIN = ["certification", "default", "draft", "skeptic"]

TOOL_META: dict[str, Any] = {
    "name": "rate_limit_cascade",
    "description": "Downgrades Opus→Sonnet→Haiku→Grok when a model is saturated.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "requested_model": {"type": "string"},
            "rate_limit_state": {
                "type": "object",
                "description": "Remaining invocation counts per model.",
            },
        },
        "required": ["requested_model", "rate_limit_state"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "selected_model": {"type": "string"},
                    "cascade_path": {"type": "array"},
                    "reason": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def rate_limit_cascade(
    requested_model: str,
    rate_limit_state: Mapping[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Return the highest-available model given remaining quotas."""
    try:
        normalized = requested_model.lower()
        chain = _cascade_chain(normalized)
        cascade_path: list[str] = []
        selected = None
        for model in chain:
            remaining = float(rate_limit_state.get(model, 0))
            cascade_path.append(f"{model}:{remaining}")
            if remaining > 0:
                selected = model
                break
        if selected is None:
            raise ValueError("All models exhausted; escalate to Thunder")
        data = {
            "selected_model": selected,
            "cascade_path": cascade_path,
            "reason": f"Requested {requested_model}, fell through chain",
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("rate_limit_cascade", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _cascade_chain(start_model: str) -> list[str]:
    if start_model in CASCADE_CHAIN:
        start_idx = CASCADE_CHAIN.index(start_model)
        return CASCADE_CHAIN[start_idx:]
    return CASCADE_CHAIN


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
