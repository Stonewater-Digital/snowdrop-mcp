"""Analyze sentiment and themes from feedback."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any

POSITIVE_WORDS = {"love", "great", "awesome", "fast", "thanks"}
NEGATIVE_WORDS = {"bug", "slow", "hate", "angry", "broken", "frustrated"}
STOPWORDS = {"the", "and", "with", "for", "that", "this", "to", "it", "a", "an"}

TOOL_META: dict[str, Any] = {
    "name": "feedback_sentiment_analyzer",
    "description": "Computes sentiment trends and common themes from feedback entries.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "feedback_entries": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["feedback_entries"],
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


def feedback_sentiment_analyzer(feedback_entries: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return sentiment stats, praised/criticized skills, and themes."""
    try:
        sentiment_scores = []
        theme_counter: Counter[str] = Counter()
        praise: Counter[str] = Counter()
        criticism: Counter[str] = Counter()
        for entry in feedback_entries:
            message = str(entry.get("message", ""))
            tokens = [word.strip(".,!?\n").lower() for word in message.split()]
            score = sum(1 for token in tokens if token in POSITIVE_WORDS) - sum(
                1 for token in tokens if token in NEGATIVE_WORDS
            )
            rating = entry.get("rating")
            if rating:
                score += (int(rating) - 3)
            sentiment_scores.append(score)
            skill = entry.get("skill_name", "global")
            if score > 0:
                praise[skill] += 1
            elif score < 0:
                criticism[skill] += 1
            for token in tokens:
                if token and token not in STOPWORDS:
                    theme_counter[token] += 1
        average_score = (sum(sentiment_scores) / len(sentiment_scores)) if sentiment_scores else 0.0
        trend = "improving" if average_score > 0 else "declining" if average_score < 0 else "neutral"
        top_themes = [word for word, _ in theme_counter.most_common(5)]
        data = {
            "overall_score": round(average_score, 2),
            "sentiment_trend": trend,
            "top_themes": top_themes,
            "most_praised_skills": [skill for skill, _ in praise.most_common(3)],
            "most_criticized_skills": [skill for skill, _ in criticism.most_common(3)],
            "actionable_items": _action_items(top_themes, criticism),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("feedback_sentiment_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _action_items(themes: list[str], criticism: Counter[str]) -> list[str]:
    items = []
    if themes:
        items.append(f"Investigate theme: {themes[0]}")
    if criticism:
        skill, _ = criticism.most_common(1)[0]
        items.append(f"Run retro on {skill}")
    return items


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
