"""Manage the public agent directory."""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from typing import Any

LOG_PATH = "logs/agent_directory.jsonl"

TOOL_META: dict[str, Any] = {
    "name": "agent_directory_manager",
    "description": "Registers, updates, searches, and deactivates public agent profiles.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["register", "update", "search", "list", "deactivate"],
            },
            "agent_profile": {"type": ["object", "null"], "default": None},
            "search_query": {"type": ["string", "null"], "default": None},
            "filter_capabilities": {
                "type": ["array", "null"],
                "items": {"type": "string"},
                "default": None,
            },
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


def agent_directory_manager(
    operation: str,
    agent_profile: dict[str, Any] | None = None,
    search_query: str | None = None,
    filter_capabilities: list[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Perform the requested directory operation."""
    try:
        directory = _build_directory()
        data: dict[str, Any]
        if operation == "register":
            if not agent_profile:
                raise ValueError("agent_profile required for register")
            agent_id = agent_profile.get("agent_id")
            if not agent_id:
                raise ValueError("agent_id missing")
            directory[agent_id] = {**agent_profile, "active": True}
            _append_log({"action": "register", "profile": directory[agent_id]})
            data = {"profile": directory[agent_id]}
        elif operation == "update":
            if not agent_profile:
                raise ValueError("agent_profile required for update")
            agent_id = agent_profile.get("agent_id")
            if agent_id not in directory:
                raise ValueError("agent not found")
            directory[agent_id].update(agent_profile)
            _append_log({"action": "update", "profile": directory[agent_id]})
            data = {"profile": directory[agent_id]}
        elif operation == "deactivate":
            if not agent_profile or not agent_profile.get("agent_id"):
                raise ValueError("agent_id required for deactivate")
            agent_id = agent_profile["agent_id"]
            if agent_id not in directory:
                raise ValueError("agent not found")
            directory[agent_id]["active"] = False
            _append_log({"action": "deactivate", "agent_id": agent_id})
            data = {"profile": directory[agent_id]}
        elif operation in {"list", "search"}:
            results = [profile for profile in directory.values() if profile.get("active", True)]
            if filter_capabilities:
                needed = set(filter_capabilities)
                results = [
                    profile
                    for profile in results
                    if needed.issubset(set(profile.get("capabilities", [])))
                ]
            if operation == "search" and search_query:
                pattern = re.compile(re.escape(search_query), re.IGNORECASE)
                results = [
                    profile
                    for profile in results
                    if pattern.search(profile.get("display_name", ""))
                    or pattern.search(profile.get("description", ""))
                    or any(pattern.search(cap) for cap in profile.get("capabilities", []))
                ]
            data = {"results": results}
        else:
            raise ValueError("Unsupported operation")

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("agent_directory_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _build_directory() -> dict[str, dict[str, Any]]:
    directory: dict[str, dict[str, Any]] = {}
    if not os.path.exists(LOG_PATH):
        return directory
    with open(LOG_PATH, "r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            action = record.get("action")
            if action in {"register", "update"}:
                profile = record.get("profile", {})
                agent_id = profile.get("agent_id")
                if agent_id:
                    directory[agent_id] = profile
            elif action == "deactivate":
                agent_id = record.get("agent_id")
                if agent_id and agent_id in directory:
                    directory[agent_id]["active"] = False
    return directory


def _append_log(payload: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    payload["logged_at"] = datetime.now(timezone.utc).isoformat()
    with open(LOG_PATH, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
