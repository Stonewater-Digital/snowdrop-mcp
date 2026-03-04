"""Estimate model token usage and cost."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "token_estimator",
    "description": "Estimates token counts and costs across Claude/GPT/Gemini families.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "model_family": {
                "type": "string",
                "enum": ["claude", "gpt", "gemini"],
            },
        },
        "required": ["text", "model_family"],
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

PRICING_PER_1K = {
    "gpt": {"input": 0.0005, "output": 0.0015},
    "claude": {"input": 0.0008, "output": 0.0024},
    "gemini": {"input": 0.000275, "output": 0.00055},
}


def token_estimator(text: str, model_family: str, **_: Any) -> dict[str, Any]:
    """Return heuristic token/cost estimate."""

    try:
        if not text:
            raise ValueError("text cannot be empty")
        model_family = model_family.lower()
        if model_family not in PRICING_PER_1K:
            raise ValueError("Unsupported model_family")
        char_count = len(text)
        divisor = 4 if model_family in {"claude", "gpt"} else 3.5
        estimated_tokens = int(char_count / divisor) + 50  # overhead for system prompts
        pricing = PRICING_PER_1K[model_family]
        input_cost = estimated_tokens / 1000 * pricing["input"]
        output_cost = estimated_tokens / 1000 * pricing["output"]
        data = {
            "estimated_tokens": estimated_tokens,
            "estimated_cost_input": round(input_cost, 6),
            "estimated_cost_output": round(output_cost, 6),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("token_estimator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
