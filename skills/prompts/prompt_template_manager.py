"""Manage Assembly Line prompt templates."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "prompt_template_manager",
    "description": "Provides CRUD operations on config/prompt_templates.json.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["get", "save", "list", "delete"],
            },
            "template_name": {"type": "string"},
            "template": {"type": ["object", "null"]},
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

TEMPLATE_PATH = "config/prompt_templates.json"


def prompt_template_manager(
    operation: str,
    template_name: str | None = None,
    template: dict[str, Any] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Handle template storage operations."""

    try:
        templates = _load_templates()
        if operation == "list":
            data = {"templates": list(templates.keys())}
        elif operation == "get":
            if not template_name:
                raise ValueError("template_name required for get")
            data = {"template": templates.get(template_name)}
        elif operation == "save":
            if not template_name or not template:
                raise ValueError("template_name and template required for save")
            templates[template_name] = template
            _save_templates(templates)
            data = {"saved": True}
        else:  # delete
            if not template_name:
                raise ValueError("template_name required for delete")
            templates.pop(template_name, None)
            _save_templates(templates)
            data = {"deleted": True}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("prompt_template_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _load_templates() -> dict[str, Any]:
    if not os.path.exists(TEMPLATE_PATH):
        return {}
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as handle:
        try:
            return json.load(handle)
        except json.JSONDecodeError:
            return {}


def _save_templates(data: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(TEMPLATE_PATH), exist_ok=True)
    with open(TEMPLATE_PATH, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
