"""Generate knowledge base articles from resolved tickets."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "knowledge_base_article_generator",
    "description": "Summarizes frequent ticket resolutions into KB articles to reduce load.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "resolved_tickets": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["resolved_tickets"],
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


def knowledge_base_article_generator(
    resolved_tickets: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Group high-frequency issues into KB articles."""
    try:
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for ticket in resolved_tickets:
            key = ticket.get("subject", "general")
            grouped[key].append(ticket)
        articles: list[dict[str, Any]] = []
        for subject, tickets in grouped.items():
            freq = sum(ticket.get("frequency", 1) for ticket in tickets)
            if freq <= 3:
                continue
            first = tickets[0]
            article = {
                "title": subject,
                "problem": first.get("description", ""),
                "solution": first.get("resolution", ""),
                "category": first.get("category", "general"),
                "tags": list({first.get("category", "general"), "kb"}),
                "source_tickets": len(tickets),
            }
            articles.append(article)
        data = {"articles": articles}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("knowledge_base_article_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
