"""Compare provider costs for a task profile."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "vendor_cost_comparator",
    "description": "Computes daily/monthly spend per provider and ranks by cost-effectiveness.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "task_profile": {"type": "object"},
            "providers": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["task_profile", "providers"],
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


def vendor_cost_comparator(
    task_profile: dict[str, Any],
    providers: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return ranked provider cost table"""
    try:
        avg_in = float(task_profile.get("avg_input_tokens", 0.0))
        avg_out = float(task_profile.get("avg_output_tokens", 0.0))
        daily_calls = int(task_profile.get("daily_calls", 0))
        ranked = []
        for provider in providers:
            input_cost = avg_in / 1_000 * float(provider.get("input_cost_per_mtok", 0.0))
            output_cost = avg_out / 1_000 * float(provider.get("output_cost_per_mtok", 0.0))
            daily_cost = (input_cost + output_cost) * daily_calls
            monthly_cost = daily_cost * 30
            quality = float(provider.get("quality_score", 1.0)) or 1.0
            cost_per_quality = monthly_cost / quality
            ranked.append(
                {
                    "provider": provider.get("name"),
                    "model": provider.get("model"),
                    "daily_cost": round(daily_cost, 2),
                    "monthly_cost": round(monthly_cost, 2),
                    "quality_score": quality,
                    "cost_per_quality": round(cost_per_quality, 2),
                    "context_window": provider.get("context_window"),
                }
            )
        ranked.sort(key=lambda item: item["cost_per_quality"])
        data = {"providers": ranked}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("vendor_cost_comparator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
