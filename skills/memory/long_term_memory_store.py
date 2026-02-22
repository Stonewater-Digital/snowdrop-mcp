"""Persistent semantic memory store for Snowdrop."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "long_term_memory_store",
    "description": "Append-only JSONL memory store with taggable search and CRUD operations.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["read", "write", "search", "delete"],
            },
            "key": {"type": "string"},
            "value": {"type": ["object", "array", "string", "number", "boolean", "null"]},
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Semantic tags for retrieval",
            },
        },
        "required": ["operation", "key"],
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

_MEMORY_FILE = "logs/memory_store.jsonl"


def long_term_memory_store(
    operation: str,
    key: str,
    value: Any | None = None,
    tags: list[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """CRUD interface for Snowdrop's long-term memory JSONL file."""
    try:
        op = operation.lower()
        if op not in {"read", "write", "search", "delete"}:
            raise ValueError("operation must be one of read/write/search/delete")
        if not key:
            raise ValueError("key cannot be empty")

        os.makedirs(os.path.dirname(_MEMORY_FILE), exist_ok=True)
        entries = _load_entries()

        if op == "write":
            record = {
                "key": key,
                "value": value,
                "tags": tags or [],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            with open(_MEMORY_FILE, "a", encoding="utf-8") as handle:
                handle.write(json.dumps(record) + "\n")
            data = {"result": "written", "record": record}
        elif op == "read":
            matches = [entry for entry in entries if entry.get("key") == key]
            data = {"matches": matches}
        elif op == "search":
            tag_set = set((tags or []))
            if not tag_set:
                raise ValueError("tags are required for search")
            filtered = [
                entry
                for entry in entries
                if tag_set.intersection(entry.get("tags", []))
            ]
            data = {"matches": filtered}
        else:  # delete
            remaining = [entry for entry in entries if entry.get("key") != key]
            removed = len(entries) - len(remaining)
            with open(_MEMORY_FILE, "w", encoding="utf-8") as handle:
                for entry in remaining:
                    handle.write(json.dumps(entry) + "\n")
            data = {"removed": removed}

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("long_term_memory_store", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _load_entries() -> list[dict[str, Any]]:
    if not os.path.exists(_MEMORY_FILE):
        return []
    entries: list[dict[str, Any]] = []
    with open(_MEMORY_FILE, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
