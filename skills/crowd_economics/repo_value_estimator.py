"""Estimate repo replacement cost in tokens and USD."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

PRICING = {
    "opus": 15,
    "sonnet": 3,
    "haiku": 0.6,
}

TOOL_META: dict[str, Any] = {
    "name": "repo_value_estimator",
    "description": "Estimates tokens and dollars needed to rebuild the repo from scratch.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skills": {"type": "array", "items": {"type": "object"}},
            "model_pricing": {"type": "object"},
            "iterations_per_skill": {"type": "number", "default": 1.5},
            "actual_cost_paid": {"type": "number"},
        },
        "required": ["skills"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def repo_value_estimator(
    skills: list[dict[str, Any]],
    model_pricing: dict[str, float] | None = None,
    iterations_per_skill: float = 1.5,
    actual_cost_paid: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return total LOC, tokens, and cost estimates."""
    try:
        price_table = model_pricing or {"input_per_mtok": 3.0, "output_per_mtok": 9.0}
        total_loc = sum(skill.get("lines_of_code", 0) for skill in skills)
        tokens_output = int(total_loc * 4 * iterations_per_skill)
        tokens_input = tokens_output // 2
        replacement_tokens = tokens_output + tokens_input
        replacement_cost_usd = replacement_tokens / 1000 * (price_table.get("input_per_mtok", 3.0) + price_table.get("output_per_mtok", 9.0)) / 2
        cost_at_models = {
            model: replacement_tokens / 1000 * rate
            for model, rate in PRICING.items()
        }
        savings_pct = None
        if actual_cost_paid is not None:
            savings_pct = (1 - actual_cost_paid / replacement_cost_usd) * 100 if replacement_cost_usd else None
        data = {
            "total_skills": len(skills),
            "total_loc": total_loc,
            "replacement_tokens": replacement_tokens,
            "replacement_cost_usd": round(replacement_cost_usd, 2),
            "cost_at_opus": round(cost_at_models["opus"], 2),
            "cost_at_sonnet": round(cost_at_models["sonnet"], 2),
            "cost_at_haiku": round(cost_at_models["haiku"], 2),
            "actual_cost_paid": actual_cost_paid,
            "savings_pct": round(savings_pct, 2) if savings_pct is not None else None,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("repo_value_estimator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
