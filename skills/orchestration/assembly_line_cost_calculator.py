"""Quantify savings from the Haiku→Sonnet→Opus Assembly Line."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

PRICING = {
    "haiku": {"input": 1.0, "output": 5.0, "weight": 0.4},
    "sonnet": {"input": 3.0, "output": 15.0, "weight": 0.35},
    "opus": {"input": 15.0, "output": 75.0, "weight": 0.25},
}

TOOL_META: dict[str, Any] = {
    "name": "assembly_line_cost_calculator",
    "description": "Compares Assembly Line run-rate against a pure-Opus baseline.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "task_count": {"type": "integer"},
            "avg_tokens_per_task": {"type": "integer"},
        },
        "required": ["task_count", "avg_tokens_per_task"],
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


def assembly_line_cost_calculator(
    task_count: int,
    avg_tokens_per_task: int,
    **_: Any,
) -> dict[str, Any]:
    """Return Assembly Line savings vs. pure Opus.

    Args:
        task_count: Number of tasks moving through the Assembly Line.
        avg_tokens_per_task: Average token count per task spanning the pipeline.

    Returns:
        Envelope contrasting Assembly Line cost with the pure Opus baseline.
    """

    try:
        if task_count <= 0 or avg_tokens_per_task <= 0:
            raise ValueError("task_count and avg_tokens_per_task must be positive")

        total_tokens = task_count * avg_tokens_per_task
        tokens_mt = total_tokens / 1_000_000

        baseline_cost = tokens_mt * (PRICING["opus"]["input"] + PRICING["opus"]["output"])
        pipeline_cost = sum(
            tokens_mt
            * model_data["weight"]
            * (model_data["input"] + model_data["output"])
            for model_data in PRICING.values()
        )

        savings = baseline_cost - pipeline_cost
        savings_pct = savings / baseline_cost * 100 if baseline_cost else 0

        data = {
            "tasks": task_count,
            "avg_tokens_per_task": avg_tokens_per_task,
            "baseline_opus_cost": round(baseline_cost, 4),
            "assembly_line_cost": round(pipeline_cost, 4),
            "savings_usd": round(savings, 4),
            "savings_pct": round(savings_pct, 2),
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("assembly_line_cost_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
