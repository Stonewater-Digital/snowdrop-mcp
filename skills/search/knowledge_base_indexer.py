"""Index and query Snowdrop knowledge artifacts."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "knowledge_base_indexer",
    "description": "Builds an inverted index over documents and answers keyword queries.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "documents": {"type": "array", "items": {"type": "object"}},
            "query": {"type": ["string", "null"], "default": None},
        },
        "required": ["documents"],
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


def knowledge_base_indexer(
    documents: list[dict[str, Any]],
    query: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Build an inverted index and optionally answer a query."""
    try:
        if not documents:
            raise ValueError("documents cannot be empty")
        index = _build_index(documents)
        data: dict[str, Any] = {
            "index_size": len(index),
            "documents_indexed": len(documents),
        }
        if query:
            results = _search_index(index, documents, query)
            data["results"] = results
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("knowledge_base_indexer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _build_index(documents: list[dict[str, Any]]) -> dict[str, set[int]]:
    index: dict[str, set[int]] = defaultdict(set)
    for idx, doc in enumerate(documents):
        terms = _tokenize(doc.get("content", ""))
        for term in terms:
            index[term].add(idx)
    return index


def _search_index(
    index: dict[str, set[int]],
    documents: list[dict[str, Any]],
    query: str,
) -> list[dict[str, Any]]:
    terms = _tokenize(query)
    scores: dict[int, int] = defaultdict(int)
    for term in terms:
        for doc_idx in index.get(term, set()):
            scores[doc_idx] += 1
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    results = []
    for doc_idx, score in ranked:
        doc = documents[doc_idx]
        results.append(
            {
                "path": doc.get("path"),
                "doc_type": doc.get("doc_type"),
                "score": score,
            }
        )
    return results


def _tokenize(text: str) -> list[str]:
    return [token.lower() for token in text.split() if token.strip()]


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
