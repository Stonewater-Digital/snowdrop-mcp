"""Aggregate model verdicts using Snowdrop weighting."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "jury_verdict_aggregator",
    "description": "Roll up model verdicts with dynamic confidence weighting and escalation logic.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "verdicts": {
                "type": "array",
                "items": {"type": "object"},
                "description": "List of verdict dicts (model, position, confidence, reasoning).",
            },
            "weights": {
                "type": "object",
                "default": {"opus": 3, "sonnet": 2, "grok": 1, "gemini": 1},
                "description": "Custom model vote multipliers.",
            },
        },
        "required": ["verdicts"],
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

_POSITION_SCORE = {"support": 1.0, "oppose": -1.0, "abstain": 0.0}


def jury_verdict_aggregator(
    verdicts: list[dict[str, Any]],
    weights: dict[str, float] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Compute a weighted collective decision and escalation recommendation."""
    try:
        if not verdicts:
            raise ValueError("verdicts cannot be empty")

        model_weights = weights or {"opus": 3, "sonnet": 2, "grok": 1, "gemini": 1}
        weighted_scores = defaultdict(float)
        total_weight = 0.0
        reasoning_fragments: list[str] = []

        for verdict in verdicts:
            model = str(verdict.get("model", ""))
            position = verdict.get("position", "abstain").lower()
            confidence = float(verdict.get("confidence", 0.0))
            reasoning = verdict.get("reasoning")
            if reasoning:
                reasoning_fragments.append(f"{model}: {reasoning}")

            position_score = _POSITION_SCORE.get(position, 0.0)
            model_weight = float(model_weights.get(model, 1.0))
            weight_multiplier = confidence * model_weight
            weighted_scores[position] += position_score * weight_multiplier
            total_weight += abs(weight_multiplier)

        decision = _resolve_decision(weighted_scores)
        margin = _compute_margin(weighted_scores, total_weight)
        escalate_to_opus = margin < 0.10 and decision != "abstain"
        summary = "; ".join(reasoning_fragments[:6])

        data = {
            "decision": decision,
            "confidence": round(max(weighted_scores.get(decision, 0.0), 0.0), 3),
            "margin": round(margin, 3),
            "escalate_to_opus": escalate_to_opus,
            "reasoning_summary": summary,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("jury_verdict_aggregator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _resolve_decision(weighted_scores: dict[str, float]) -> str:
    if not weighted_scores:
        return "abstain"
    ordered = sorted(weighted_scores.items(), key=lambda item: item[1], reverse=True)
    best_position, best_score = ordered[0]
    if best_score == 0:
        return "abstain"
    return best_position


def _compute_margin(weighted_scores: dict[str, float], total_weight: float) -> float:
    if total_weight == 0:
        return 0.0
    sorted_scores = sorted(weighted_scores.values(), reverse=True)
    if not sorted_scores:
        return 0.0
    lead = sorted_scores[0]
    runner_up = sorted_scores[1] if len(sorted_scores) > 1 else 0.0
    return abs(lead - runner_up) / max(total_weight, 1e-6)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
