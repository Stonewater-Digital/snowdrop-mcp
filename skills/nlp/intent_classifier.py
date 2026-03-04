"""Classify Thunder's utterances into Snowdrop intent buckets."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "intent_classifier",
    "description": "Heuristically classifies operator text into MCP skill intents",
    "inputSchema": {
        "type": "object",
        "properties": {
            "user_input": {"type": "string"},
            "available_categories": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["user_input", "available_categories"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "intent": {"type": "string"},
                    "confidence": {"type": "number"},
                    "matched_keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "suggested_skills": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}

INTENT_KEYWORDS: dict[str, tuple[str, ...]] = {
    "balance_query": ("how much", "balance", "holdings", "cash"),
    "payment": ("send", "transfer", "wire", "pay"),
    "reconciliation": ("audit", "reconcile", "match", "variance"),
    "scenario_modeling": ("what if", "simulate", "stress", "model"),
    "intel_request": ("status", "update", "report"),
}


def intent_classifier(
    user_input: str,
    available_categories: list[str],
    **_: Any,
) -> dict[str, Any]:
    """Return the intent classification with keyword provenance."""

    try:
        if not user_input.strip():
            raise ValueError("user_input cannot be empty")
        normalized_categories = [cat.lower() for cat in available_categories]
        text = user_input.lower()
        matches: list[str] = []
        matched_keywords: list[str] = []
        for intent, keywords in INTENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    matches.append(intent)
                    matched_keywords.append(keyword)
                    break

        selected = _select_intent(matches, normalized_categories)
        confidence = 0.2 + 0.2 * len(matched_keywords)
        confidence = min(confidence, 0.95 if selected else 0.4)
        suggested = [intent for intent in matches if intent in normalized_categories]
        if not suggested and normalized_categories:
            suggested.append(normalized_categories[0])
        data = {
            "intent": selected or (suggested[0] if suggested else "unknown"),
            "confidence": round(confidence, 3),
            "matched_keywords": matched_keywords,
            "suggested_skills": suggested,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("intent_classifier", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _select_intent(matches: list[str], available: list[str]) -> str | None:
    for match in matches:
        if match in available:
            return match
    return matches[0] if matches else (available[0] if available else None)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
