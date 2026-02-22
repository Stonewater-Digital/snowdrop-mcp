"""Search across skill metadata using TF-IDF-style weighting."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "skill_search_engine",
    "description": "Ranks skills by textual similarity to a query string.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "skill_catalog": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["query", "skill_catalog"],
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


def skill_search_engine(
    query: str,
    skill_catalog: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Compute weighted term matches against the catalog."""
    try:
        if not query.strip():
            raise ValueError("query cannot be empty")
        if not skill_catalog:
            raise ValueError("skill_catalog cannot be empty")
        query_terms = _tokenize(query)
        query_counter = Counter(query_terms)
        results = []
        for skill in skill_catalog:
            score = _score_skill(skill, query_counter)
            if score > 0:
                results.append({"skill": skill, "score": round(score, 3)})
        results.sort(key=lambda item: item["score"], reverse=True)
        data = {
            "results": results,
            "total_matches": len(results),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("skill_search_engine", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _tokenize(text: str) -> list[str]:
    return [token.lower() for token in text.split() if token.strip()]


def _score_skill(skill: dict[str, Any], query_counter: Counter) -> float:
    name_terms = _tokenize(skill.get("name", ""))
    description_terms = _tokenize(skill.get("description", ""))
    category_terms = _tokenize(skill.get("category", ""))
    input_terms = _tokenize(" ".join(skill.get("input_fields", [])))
    score = 0.0
    for term, freq in query_counter.items():
        score += 3 * freq * name_terms.count(term)
        score += 1 * freq * description_terms.count(term)
        score += 2 * freq * category_terms.count(term)
        score += 1 * freq * input_terms.count(term)
    return score


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
