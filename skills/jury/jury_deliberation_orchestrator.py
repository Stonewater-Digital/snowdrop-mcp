"""Coordinate Snowdrop's multi-model jury deliberations."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "jury_deliberation_orchestrator",
    "description": "Structures prompts and verdicts for the Sonnet/Grok/Gemini debate loop.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "thesis": {
                "type": "object",
                "description": "Structured thesis payload (summary, confidence, risks, etc.).",
            },
            "models": {
                "type": "array",
                "items": {"type": "string"},
                "default": ["sonnet", "grok", "gemini"],
                "description": "Ordered model roster to involve in deliberation.",
            },
        },
        "required": ["thesis"],
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

_ROLE_MAP: dict[str, str] = {
    "sonnet": "Builder",
    "grok": "Skeptic",
    "gemini": "Secretary",
}


_DEF_ROLE_INSTRUCTIONS: dict[str, str] = {
    "Builder": (
        "Synthesize the thesis, emphasize execution pathways, and note enabling assumptions."
    ),
    "Skeptic": "Interrogate downside scenarios, exploit adversarial evidence, and quantify tail risk.",
    "Secretary": "Capture deliberation structure, highlight decisions/risks, and enforce clarity.",
}


def jury_deliberation_orchestrator(
    thesis: dict[str, Any],
    models: list[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Simulate a prompt-crafting and verdict rollup for the Snowdrop jury."""
    try:
        roster = models or ["sonnet", "grok", "gemini"]
        if not roster:
            raise ValueError("At least one model must be specified")

        base_confidence = float(thesis.get("confidence", 0.5))
        base_confidence = max(0.0, min(1.0, base_confidence))
        subject = thesis.get("summary") or thesis.get("title") or "the thesis"
        risk_summary = thesis.get("risks") or thesis.get("threats", [])

        structured_prompts: dict[str, dict[str, Any]] = {}
        verdicts: list[dict[str, Any]] = []

        for model in roster:
            role = _ROLE_MAP.get(model.lower(), "Advisor")
            instructions = _DEF_ROLE_INSTRUCTIONS.get(
                role,
                "Deliver a concise evaluation with clear bulletproofing of your argument.",
            )
            perspective_shift = {
                "Builder": 0.15,
                "Skeptic": -0.2,
                "Secretary": 0.0,
                "Advisor": 0.05,
            }.get(role, 0.0)
            modeled_conf = max(0.0, min(1.0, base_confidence + perspective_shift))
            position = _position_from_confidence(modeled_conf)
            reasoning = _build_reasoning(role, subject, risk_summary, thesis)

            structured_prompts[model] = {
                "role": role,
                "instructions": instructions,
                "context": thesis,
            }
            verdicts.append(
                {
                    "model": model,
                    "role": role,
                    "position": position,
                    "confidence": round(modeled_conf, 3),
                    "reasoning": reasoning,
                }
            )

        majority_position, majority_confidence = _aggregate_positions(verdicts)
        deliberation_record = {
            "structured_prompts": structured_prompts,
            "verdicts": verdicts,
            "majority_position": majority_position,
            "majority_confidence": majority_confidence,
            "consensus_strength": _consensus_label(majority_confidence),
            "thesis": thesis,
        }
        return {
            "status": "success",
            "data": deliberation_record,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("jury_deliberation_orchestrator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _position_from_confidence(confidence: float) -> str:
    if confidence >= 0.6:
        return "support"
    if confidence <= 0.4:
        return "oppose"
    return "abstain"


def _build_reasoning(
    role: str,
    subject: str,
    risks: Any,
    thesis: dict[str, Any],
) -> str:
    focus = {
        "Builder": "delivery levers and upside catalysts",
        "Skeptic": "risk cliffs and failure modes",
        "Secretary": "decision clarity and owner assignments",
        "Advisor": "balanced perspective",
    }.get(role, "holistic view")
    risk_text = ", ".join(risks) if isinstance(risks, list) else str(risks or "no major risks noted")
    return (
        f"As the {role}, focus on {focus} for {subject}. Key risks: {risk_text}."
        f" Thesis inputs: {thesis.get('summary') or thesis.get('rationale', 'unspecified')}"
    )


def _aggregate_positions(verdicts: list[dict[str, Any]]) -> tuple[str, float]:
    if not verdicts:
        return "abstain", 0.0
    tally = Counter()
    total_conf = 0.0
    for entry in verdicts:
        position = entry.get("position", "abstain")
        confidence = float(entry.get("confidence", 0.0))
        tally[position] += confidence
        total_conf += confidence
    majority_position, confidence_sum = tally.most_common(1)[0]
    if total_conf == 0:
        return majority_position, 0.0
    return majority_position, round(confidence_sum / total_conf, 3)


def _consensus_label(majority_confidence: float) -> str:
    if majority_confidence >= 0.7:
        return "strong"
    if majority_confidence >= 0.45:
        return "mixed"
    return "weak"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
