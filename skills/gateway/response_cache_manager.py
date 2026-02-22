"""Manage cached responses for Snowdrop skills."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "response_cache_manager",
    "description": "Provides get/set/invalidate operations for skill response cache entries.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {"type": "string", "enum": ["get", "set", "invalidate"]},
            "cache_key": {"type": "string"},
            "value": {"type": ["object", "null"]},
            "ttl_seconds": {"type": "integer", "default": 300},
        },
        "required": ["operation", "cache_key"],
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

CACHE_PATH = "logs/response_cache.json"


def response_cache_manager(
    operation: str,
    cache_key: str,
    value: dict[str, Any] | None = None,
    ttl_seconds: int = 300,
    **_: Any,
) -> dict[str, Any]:
    """Perform cache operations with TTL enforcement."""

    try:
        cache = _load_cache()
        now = datetime.now(timezone.utc)
        if operation == "get":
            entry = cache.get(cache_key)
            if not entry:
                data = {"hit": False, "data": None, "age_seconds": None}
            else:
                age = (now - datetime.fromisoformat(entry["stored_at"])).total_seconds()
                if age > entry["ttl_seconds"]:
                    cache.pop(cache_key, None)
                    _save_cache(cache)
                    data = {"hit": False, "data": None, "age_seconds": age}
                else:
                    data = {"hit": True, "data": entry["value"], "age_seconds": round(age, 2)}
        elif operation == "set":
            if value is None:
                raise ValueError("value is required for set operations")
            cache[cache_key] = {
                "value": value,
                "stored_at": now.isoformat(),
                "ttl_seconds": ttl_seconds,
            }
            _save_cache(cache)
            data = {"stored": True}
        else:  # invalidate
            removed = cache.pop(cache_key, None) is not None
            _save_cache(cache)
            data = {"invalidated": removed}

        return {
            "status": "success",
            "data": data,
            "timestamp": now.isoformat(),
        }
    except Exception as exc:
        _log_lesson("response_cache_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _load_cache() -> dict[str, Any]:
    if not os.path.exists(CACHE_PATH):
        return {}
    with open(CACHE_PATH, "r", encoding="utf-8") as handle:
        try:
            return json.load(handle)
        except json.JSONDecodeError:
            return {}


def _save_cache(data: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
