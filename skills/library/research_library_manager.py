"""Manage the community research library."""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from typing import Any

LOG_PATH = "logs/research_library.jsonl"

TOOL_META: dict[str, Any] = {
    "name": "research_library_manager",
    "description": "Publishes and queries Goodwill research papers for the community.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["publish", "search", "list", "get"],
            },
            "paper": {"type": ["object", "null"], "default": None},
            "search_query": {"type": ["string", "null"], "default": None},
        },
        "required": ["operation"],
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


def research_library_manager(
    operation: str,
    paper: dict[str, Any] | None = None,
    search_query: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Execute research library operations."""
    try:
        papers = _load_papers()
        data: dict[str, Any]
        if operation == "publish":
            if not paper:
                raise ValueError("paper payload required")
            paper_id = f"paper_{len(papers) + 1}"
            record = {
                **paper,
                "paper_id": paper_id,
                "published_at": datetime.now(timezone.utc).isoformat(),
                "downloads": paper.get("downloads", 0),
            }
            _append_log(record)
            papers.append(record)
            data = {"paper": record}
        elif operation == "list":
            data = {"papers": papers, "total_papers": len(papers)}
        elif operation == "get":
            if not paper or "paper_id" not in paper:
                raise ValueError("paper_id required")
            match = next((p for p in papers if p["paper_id"] == paper["paper_id"]), None)
            if not match:
                raise ValueError("paper not found")
            data = {"paper": match, "downloads": match.get("downloads", 0)}
        elif operation == "search":
            if not search_query:
                raise ValueError("search_query required")
            pattern = re.compile(re.escape(search_query), re.IGNORECASE)
            results = [
                p for p in papers if pattern.search(p.get("title", "")) or pattern.search(p.get("content_md", ""))
            ]
            data = {"results": results, "total_papers": len(results), "downloads": sum(p.get("downloads", 0) for p in results)}
        else:
            raise ValueError("Unsupported operation")
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("research_library_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _load_papers() -> list[dict[str, Any]]:
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _append_log(record: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
