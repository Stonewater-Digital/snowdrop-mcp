"""Track OpenRouter usage and annotate ROI."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

PRICING = {
    "haiku": {"input": 1.0, "output": 5.0},
    "sonnet": {"input": 3.0, "output": 15.0},
    "opus": {"input": 15.0, "output": 75.0},
}

TOOL_META: dict[str, Any] = {
    "name": "openrouter_cost_logger",
    "description": "Calculates OpenRouter call costs using the internal pricing table.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "model": {"type": "string", "description": "Model slug (haiku/sonnet/opus)."},
            "input_tokens": {"type": "integer"},
            "output_tokens": {"type": "integer"},
            "purpose": {"type": "string"},
        },
        "required": ["model", "input_tokens", "output_tokens", "purpose"],
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


def openrouter_cost_logger(
    model: str,
    input_tokens: int,
    output_tokens: int,
    purpose: str,
    **_: Any,
) -> dict[str, Any]:
    """Compute the USD cost of an OpenRouter call.

    Args:
        model: Model slug (haiku, sonnet, or opus).
        input_tokens: Number of prompt tokens consumed.
        output_tokens: Number of completion tokens produced.
        purpose: Explanation of the workload.

    Returns:
        Envelope containing cost breakdown and ROI annotation.
    """

    try:
        normalized_model = model.lower()
        if normalized_model not in PRICING:
            raise ValueError(f"Unknown OpenRouter model '{model}'")

        rates = PRICING[normalized_model]
        input_cost = input_tokens / 1_000_000 * rates["input"]
        output_cost = output_tokens / 1_000_000 * rates["output"]
        total_cost = round(input_cost + output_cost, 6)

        roi_annotation = _annotate_roi(normalized_model, purpose, total_cost)

        data = {
            "model": normalized_model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_breakdown": {
                "input_usd": round(input_cost, 6),
                "output_usd": round(output_cost, 6),
                "total_usd": total_cost,
            },
            "purpose": purpose,
            "roi_annotation": roi_annotation,
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("openrouter_cost_logger", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _annotate_roi(model: str, purpose: str, cost: float) -> str:
    if model == "haiku":
        return f"${cost:.4f} exploratory spend — cheapest Ralph scout for {purpose}."
    if model == "sonnet":
        return f"${cost:.4f} builder spend unlocking production grade output for {purpose}."
    return f"${cost:.4f} Opus certification to derisk {purpose}."


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
